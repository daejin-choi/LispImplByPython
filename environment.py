import exceptions
import exc
import sys


def analyze_define(form):

  if not isinstance(form, list) or not isinstance(form[0], Symbol):
    raise exceptions.TypeError

  if len(form) != 2:
    raise exc.ArgumentError

  name = str(form[0])
  val = analyze(form[1])

  def eval_define(env, name, val):
    env[name] = val(env)
  return lambda env:eval_define(env, name, val)

def analyze_if(form):

  if len(form) != 3:
    raise exc.ArgumentError

  val_cond = analyze(form[0])
  val_true = analyze(form[1])
  val_false = analyze(form[2])

  return lambda env:val_true(env) if val_cond(env) else val_false(env)

def analyze_let(forms):
  anal_dic = {}
  for form in forms[0]:
    if not isinstance( form, list ):
      raise TypeError

    if len(form) != 2:
      raise exceptions.ArgumentError

    name = str(form[0])
    anal_dic[name] = analyze(form[1])

  args = map( lambda form:analyze(form), forms[1:] )

  def eval_let(env, anal_dic, args):
    eval_dic = {}
    for func_key in anal_dic.keys():
      eval_dic[func_key] = anal_dic[func_key](env)

    sub_env = Environment( eval_dic, env )
    ret_objs = map ( lambda func:func(sub_env), args )

    return ret_objs[-1]

  return lambda env:eval_let(env, anal_dic, args)


def analyze_quote(form):
  return lambda env:form[0]

def analyze_setf(form):
  if len(form) != 2:
    raise exceptions.ArgumentError

  name = str(form[0])
  vals = analyze(form[1])

  return lambda env:env.setf(name, vals(env))

def analyze_lambda(forms):
  args = forms[0]
  body = map( analyze, forms[1:] )
  return lambda env:Lambda(args, body, env)


class Lambda(object):

  def __init__(self, params, body, env):
    self.params = params
    self.body = body
    self.env = env

  def __call__(self, *args):
    env = Environment({}, self.env)
    for i, arg in enumerate(args):
      env[str(self.params[i])] = arg
    ret_val = map( lambda body:body(env), self.body )
    return ret_val[-1]

SPECIAL_FORMS  = {
    'define':analyze_define ,
    'if':analyze_if,
    'quote':analyze_quote,
    'let': analyze_let,
    'lambda':analyze_lambda,
    'setf!':analyze_setf
}

INITIAL_ENV = {
    'eval': lambda code, env: evaluate(env, code),
    'car':lambda x:x[0],
    'cdr':lambda x:x[1:],
    'null?':lambda x:not len(x),
    '+':lambda *args:reduce(lambda x,y:x+y, args),
    '-':lambda *args:reduce(lambda x,y:x-y, args),
    '*':lambda *args:reduce(lambda x,y:x*y, args),
    '/':lambda *args:reduce(lambda x,y:x/y, args),
    '%':lambda x, y:x%y,
    '=':lambda x, y:x==y,
    't':True,
    'f':False,
    'nil':None,
    'display': lambda x:sys.stdout.write(str(x)+ '\n'),
    'apply':apply
}

class Environment(object):


  def __init__(self, dic, parent):
    self.dic = dic
    self.parent = parent

  def __getitem__(self, key):
    try:
      return self.dic[key]
    except KeyError:
      if self.parent:
        return self.parent[key]
      raise

  def __setitem__(self, key, value):
    self.dic[key] = value

  def setf(self, key, value):
    if key in self.dic:
      self.dic[key] = value
    elif self.parent:
      obj = self.parent.setf(key, value)
    else:
      raise KeyError(repr(key))

class Symbol(object):
  def __init__(self, symbol):
    self.symbol = symbol

  def __str__(self):
    return str(self.symbol)

  def __repr__(self):
    return 'Symbol({0!r})'.format(self.symbol)

def evaluate(env, form):
  obj = analyze(form)
  return obj(env)



def analyze(form):

  if isinstance( form, list ):
    if not form:
      raise TypeError('call cannot be an empty list')
    elif isinstance(form[0], (int, float, basestring)):
      raise TypeError('{0} is not callable'.format(form[0]))
    special_obj = SPECIAL_FORMS.get(str(form[0]))
    if special_obj is not None:
      return special_obj(form[1:])

  if isinstance(form, Symbol):
    name = str(form)
    return lambda env:env[name]
  elif isinstance(form, (int, float, basestring)):
    return lambda env:form
  elif isinstance(form, list):
    anal_funcs = map(analyze, form)
    def eval_(env):
      args = []
      for func in anal_funcs:
        args.append(func(env))
      return args[0](*args[1:])
    return eval_
  else:
    raise TypeError('{0!r} cannot be evaluated'.format(lst))


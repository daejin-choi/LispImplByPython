import exceptions
import exc
import sys

def macro_define(env, lst):

  if not isinstance(lst, list) or not isinstance(lst[0], Symbol):
    raise exceptions.TypeError

  if len(lst) != 2:
    raise exc.ArgumentError

  env[str(lst[0])] = evaluate(env, lst[1])

  return env[str(lst[0])]

def macro_if(env, lst):

  if len(lst) != 3:
    raise exc.ArgumentError

  if evaluate(env, lst[0]):
    return evaluate( env, lst[1] )
  else:
    return evaluate( env, lst[2] )

def macro_let(env, forms):
  sub_dic={}
  for form in forms[0]:
    if not isinstance( form, list ):
      raise TypeError

    if len(form) != 2:
      raise exceptions.ArgumentError

    sub_dic[str(form[0])] = evaluate(env, form[1])

  sub_env = Environment(sub_dic, env)
  ret_obj = map( lambda forms:evaluate(sub_env, forms), forms[1:] )

  return ret_obj[len(ret_obj)-1]


SPECIAL_FORMS  = {
    'define':macro_define ,
    'if':macro_if,
    'quote':lambda env, forms: forms[0],
    'let': macro_let
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
    't':True,
    'f':False,
    'nil':None,
    'display': lambda x:sys.stdout.write(str(x)+ '\n')
}

"""
  def __getitem__(self, key):
    ret_obj = self.dic.get(key)

    if ret_obj is None:
      if self.parent is not None:
        ret_obj = self.parent[key]
      else:
        raise exceptions.KeyError

    return ret_obj
"""
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



class Symbol(object):
  def __init__(self, symbol):
    self.symbol = symbol

  def __str__(self):
    return str(self.symbol)

  def __repr__(self):
    return 'Symbol({0!r})'.format(self.symbol)

def evaluate(env, lst):
  """
  Check Special Form
  """
  if isinstance( lst, list ):
    special_obj = SPECIAL_FORMS.get(str(lst[0]))
    if special_obj is not None:
      return special_obj(env, lst[1:])
  if isinstance(lst, list):
    ret_rst = map( lambda lst:evaluate(env, lst), lst )
    return apply(ret_rst[0], ret_rst[1:])
  elif isinstance(lst, Symbol):
    return env[str(lst)]
  elif isinstance(lst, int):
    return int(lst)
  elif isinstance(lst, float):
    return float(lst)
  elif isinstance(lst, basestring):
    return str(lst)
  else:
    raise TypeError('{0!r} cannot be evaluated'.format(lst))


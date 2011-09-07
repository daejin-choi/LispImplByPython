import exceptions
import exc
import sys

def macro_define(env, lst):

  if not isinstance(lst, list) or not isinstance(lst[0], Symbol):
    raise exceiptions.TypeError

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

SPECIAL_FORMS  = {
    'define':macro_define ,
    'if':macro_if,
    'quote':lambda env, forms: forms[0]
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
    'display': sys.stdout.write
}

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
    eval_result = apply(ret_rst[0], ret_rst[1:])
    return eval_result
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


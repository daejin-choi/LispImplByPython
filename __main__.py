import parser
import exc
import environment

if __name__ == '__main__':
  import sys
  code = sys.stdin.read()

  try:
    rst = list(parser.parsing(code))
#    print 'parse result : ', rst
    env = environment.Environment(environment.INITIAL_ENV, None)
    env['env'] = env
    ret_value = map( lambda rst:environment.evaluate(env, rst), rst)
  except exc.SyntaxError as e:
    e.display_error()
  else:
    print 'implement result : ', ret_value

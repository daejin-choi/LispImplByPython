import parser
import exc
import environment

if __name__ == '__main__':
  import sys
  print '> '
  code = sys.stdin.read()
#  for token in list ( lexer.lexing(code) ):
#    print token.type, token.token, token.offset
  try:
    rst = list(parser.parsing(code))
    print 'parse result : ', rst
    env = environment.TABLE_ENV
    ret_value = map( lambda rst:environment.evaluate(env, rst), rst)
  except exc.SyntaxError as e:
    e.display_error()
  else:
    print 'implement result : ', ret_value

import parser
import exc

if __name__ == '__main__':
  import sys
  print '> '
  code = sys.stdin.read()
#  for token in list ( lexer.lexing(code) ):
#    print token.type, token.token, token.offset
  try:
    rst = list(parser.parsing(code))
  except exc.SyntaxError as e:
    e.display_error()
  else:
    print rst

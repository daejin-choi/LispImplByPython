import re
import exc

TOKEN_TYPE_RE = re.compile(r'''
  (?P<open> [({] | \[ ) |
  (?P<close> [)}] | \] ) |
  (?P<number> \d+(?:\.\d+)? ) |
  (?P<string> " [^\"]* " | ' [^\']* ' ) |
  (?P<symbol> [-_A-Za-z+*/%?!<>=][-0-9A-Za-z+*/%?!<>=]* )
''', re.VERBOSE)

class structToken:
  def __init__(self, type, token, code, offset):
    self.type = type
    self.token = token
    self.code = code
    self.offset = offset
  def __iter__(self):
    yield self.type
    yield self.token
    yield self.code
    yield self.offset

def lexing(code) :
  last_index = 0
  for match in TOKEN_TYPE_RE.finditer(code) :
    current_index = match.start()
    if last_index != 0 and code[last_index:current_index].strip() != '' :
      raise exc.LexingError(code, current_index, 'unknown type')
    last_index = match.end()
    for type, token in match.groupdict().iteritems():
      if token is not None :
        yield structToken(type, token, code, current_index)

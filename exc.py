

import exceptions


class SyntaxError(exceptions.SyntaxError):

  def __init__( self, code, offset, message ):
    self.code = code
    self.offset = offset
    self.msg = message

  @property
  def lineno (self):
    return self.code.count('\n', 0, self.offset)

  @property
  def column (self):
    return self.offset - self.code.rfind('\n', 0, self.offset)

  def display_error(self):
    print type(self).__name__ + '\n   Line: ' + str(self.lineno+1) + '\n   Column: ' +str(self.column+1)


class ParsingError(SyntaxError):

  pass


class LexingError(ParsingError):

  pass


class ParenthesisUnopenedError(ParsingError):

  def __init__(self, code, offset, index, message):
    SyntaxError.__init__(self, code, offset, message)
    self.index = index

  @property
  def gotoindex(self):
    return self.index+1


class ParenthesisUnclosedError(ParsingError):

  def __init__(self, code, offset, index, message):
    SyntaxError.__init__(self, code, offset, message)
    self.index = index

  @property
  def gotoindex(self):
    return self.index+1



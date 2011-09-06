
class Symbol(object):
  def __init__(self, symbol):
    self.symbol = symbol

  def __str__(self):
    return str(self.symbol)

  def __repr__(self):
    return 'Symbol({0!r})'.format(self.symbol)

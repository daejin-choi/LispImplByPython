import lexer
import exc
import environment


def parsing(code):
  if isinstance(code, basestring) :
    tokens = list(lexer.lexing(code))
  else :
    tokens = list(code)

  goto = None

  for i, token in enumerate(tokens):
    if goto is not None:
      if i <= goto:
        continue
      goto = None

    type, value, code, offset = token

    if type == 'open':
      local_list = []
      try :
        for element in parsing(tokens[i+1:]) :
            local_list.append(element)
      except exc.ParenthesisUnopenedError as e:
        goto = i + e.gotoindex
      else :
        raise exc.ParenthesisUnclosedError(code, offset, i,
                                           'Parenthesis is not closed')

      yield local_list

    elif type == 'close':
      raise exc.ParenthesisUnopenedError(code, offset, i, 
                                         'Parenthesis is not opened')

    elif type == 'number':
      if '.' in value:
        yield float(value)
      else:
        yield int(value)

    elif type == 'symbol':
      yield environment.Symbol(value)

    elif type == 'string':
      yield eval(value)

    else:
      raise exc.ParsingError(code, offset, 'Unknown type error')

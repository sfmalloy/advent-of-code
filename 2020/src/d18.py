import fileinput

# eval -> int: Evaluates a op b. Only '+' and '*' are supported.
# a: first number
# b: second number
# op: operator (one of '+','*')
def eval(a, b, op):
  if op == '+':
    return a+b
  return a*b

# to_postfix -> list: converts infix expression to postfix.
# exp: infix expression containing ()*+ and 0-9
# prec: precedence dictionary defining which operators have higher precedences
#   for when converting. Needed here because part 1 and 2 have different precedences
#   for + and *.
def to_postfix(exp, prec):
  ops = []
  postfix = []
  token_idx = 0
  while token_idx < len(exp):
    token = exp[token_idx]
    if token == '(':
      ops.insert(0, token)
    elif token in '*+':
      while len(ops) > 0 and ops[0] != '(' and prec[ops[0]] >= prec[token]:
        postfix.append(ops.pop(0))
      ops.insert(0, token)
    elif token == ')':
      while len(ops) > 0 and ops[0] != '(':
        postfix.append(ops.pop(0))
      if ops[0] == '(':
        ops.pop(0)
    else:
      postfix.append(int(token))
    token_idx += 1
  while len(ops) > 0:
    op = ops.pop(0)
    if op != '(':
      postfix.append(op)
  return postfix

# eval_exp -> int: evaluates infix expression
# exp: infix expression (that is converted to postfix)
# prec: operator precedence dictionary
def eval_exp(exp, prec):
  postfix = to_postfix(exp, prec)
  res = []
  while len(postfix) > 0:
    while len(postfix) > 0 and isinstance(postfix[0], int):
      res.insert(0, postfix.pop(0))
    op = postfix.pop(0)
    a = res.pop(0)
    b = res.pop(0)
    res.insert(0, eval(a,b,op))
  return res[0]

# Sum up results of eval_exp calls for both parts 1 and 2.
# Part 1 both * and + have equal precedence.
# Part 2 + has higher precedence over *
s1 = 0
s2 = 0
for exp in fileinput.input():
  exp = list(filter(lambda c: c not in [' ', '\n'], exp))
  s1 += eval_exp(exp, {'+':0, '*':0})
  s2 += eval_exp(exp, {'+':1, '*':0})
print(s1)
print(s2)
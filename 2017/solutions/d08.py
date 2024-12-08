from lib import advent
from io import TextIOWrapper
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class Expression:
    reg: str
    op: str
    val: int


@dataclass
class Instruction:
    mod_expr: Expression
    cond_expr: Expression

    def eval_mod(self, reg: defaultdict[str, int]):
        if self.mod_expr.op == 'inc':
            reg[self.mod_expr.reg] += self.mod_expr.val
        else:
            reg[self.mod_expr.reg] -= self.mod_expr.val
        return reg[self.mod_expr.reg]

    def eval_cond(self, reg: defaultdict[str, int]):
        reg_val = reg[self.cond_expr.reg]
        match self.cond_expr.op:
            case '>': return reg_val > self.cond_expr.val
            case '<': return reg_val < self.cond_expr.val
            case '>=': return reg_val >= self.cond_expr.val
            case '<=': return reg_val <= self.cond_expr.val
            case '!=': return reg_val != self.cond_expr.val
            case '==': return reg_val == self.cond_expr.val


@advent.parser(8)
def parse(file: TextIOWrapper):
    instructions: list[Instruction] = []
    for line in file.readlines():
        mod_reg, mod_op, mod_val, _, cond_reg, cond_op, cond_val = line.split()
        instructions.append(Instruction(
            Expression(mod_reg, mod_op, int(mod_val)),
            Expression(cond_reg, cond_op, int(cond_val))
        ))
    return instructions


@advent.solver(8)
def solve(instructions: list[Instruction]):
    reg: defaultdict[str, int] = defaultdict(int)
    max_val = 0
    for line in instructions:
        if line.eval_cond(reg):
            max_val = max(max_val, line.eval_mod(reg))
    return max(reg.values()), max_val

# Copyright (c) 2009-2010, matthieu.kaczmarek@mines-nancy.org
# Rewritten from udis86 -- Vivek Mohan <vivek@sig9.com>
# All rights reserved.

from operand import P_OSO, P_ASO, P_IMPADDR
from common import DecodeException
from string import Template
from syn_intel import intel_syntax
from syn_att import translate_att

def c_operand_cast(op):
    """Returns operand casts."""

    if op.size in (8, 16, 32, 64, 84):
        return 'uint' + str(op.size) + '_t'
    else:
        raise KeyError('Unknown operand size: %s' % str(op.size))


def c_operand_syntax(op):
    """Generates assembly output for operands."""

    ret = list()

    if op.type is None:
        return ''

    if op.type == 'OP_REG':
        return op.base

    if op.type == 'OP_MEM':
        op_f = False
	ret.append('*(')
	if op.cast is 1:
	    ret.append('(' + c_operand_cast(op) + ')')
        ret.append('(')

        if op.seg:
            ret.extend([op.seg, ':'])

        if op.base is not None:
            ret.append(op.base)
            op_f = True

        if op.index is not None:
            if op_f:
                ret.append('+')

            ret.append(op.index)
            op_f = True

        if op.scale:
            ret.append(str(op.scale))

        if op.offset in [8, 16, 32, 64]:
            if (op.lval < 0):
                ret.extend(['-', hex(-op.lval)])
            else:
                if op_f:
                    if op.lval is 0.0:
                        op.lval = 0
                    ret.extend(['+', hex(op.lval)])
                else:
                    ret.append(hex(op.lval))

        ret.append('))')

    elif op.type == 'OP_IMM':
        ret.append(hex(op.lval))

    elif op.type == 'OP_JIMM':
        ret.append(hex(op.pc + op.lval))

    elif op.type == 'OP_PTR':
        ret.extend(['word ', hex(op.lval.seg), ':', hex(op.lval.off)])

    return ''.join(ret)


def c_syntax(self):
    """Translates to C syntax."""

    c_syntax_str = Template(self.itab_entry.c_syntax)
    op1 = op2 = op3 = ''
    if self.operand:
        op1 = c_operand_syntax(self.operand[0])
        if len(self.operand) > 1:
           op2 = c_operand_syntax(self.operand[1])
           if len(self.operand) > 2:
              op3 = c_operand_syntax(self.operand[2])

    c_syntax_str = c_syntax_str.safe_substitute(op1=op1, op2=op2, op3=op3)

    result = intel_syntax(self).ljust(40, ' ')
    if (c_syntax_str != ""):
	result += "# " + c_syntax_str

    return result

#!/usr/bin/env python
# ------------------------------------------------------------
# ast.py
#
# Setlan Abstract Syntactic Tree
#
# Author:
# Victor De Ponte, 05-38087, <rdbvictor19@gmail.com>
# ------------------------------------------------------------


class Setlan(object):
    SPACE = "    "

    def __init__(self, *args, **kwargs):
        super(Setlan, self).__init__()
        self._position = kwargs.get('position', None)
        self._instruction = kwargs.get('instruction', None)

    def __repr__(self):
        return self.__unicode__()

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        string = self.print_ast(0)
        return string

    def _get_indentation(self, level):
        return level * self.SPACE

    def print_ast(self, level):
        string = "Setlan Program:\n%s" % self._instruction.print_ast(level+1)
        return string


class Printable(Setlan):

    def __unicode__(self):
        return "%s%s: Not Implemented" % (self.SPACE, self.__class__.__name__)


class Instruction(Setlan):

    def __unicode__(self):
        return "%s%s: Not Implemented" % (self.SPACE, self.__class__.__name__)


class Declaration(Setlan):

    def __unicode__(self):
        return "%s%s: Not Implemented" % (self.SPACE, self.__class__.__name__)


class Expression(Printable):
    pass

class String(Printable):

    def __init__(self, value, *args, **kwargs):
        super(String , self).__init__(args,kwargs)
        self._value    = value

    def print_ast(self, level):
        string = "%sString: '%s'" % (
            self._get_indentation(level),
            repr(self._value)
            )
        return string


class Variable(Expression):

    def __init__(self, tkid, *args, **kwargs):
        super(Variable, self).__init__(args,kwargs)
        self._id = tkid

    def print_ast(self, level):
        string = "%sVariable: %s" % (self._get_indentation(level), self._id)
        return string


class Assignment(Instruction):

    def __init__(self, variable, value, *args, **kwargs):
        super(Assignment , self).__init__(args,kwargs)
        self._variable = variable
        self._value    = value

    def print_ast(self, level):
        string = "%sAssignment Instruction:\n%sVariable:\n%s\n%sValue:\n%s" % (
            self._get_indentation(level),
            self._get_indentation(level+1),
            self._variable.print_ast(level+2),
            self._get_indentation(level+1),
            self._value.print_ast(level+2)
            )
        return string



class Block(Instruction):

    def __init__(self, declarations, instructions, *args, **kwargs):
        super(Block, self).__init__(args,kwargs)
        self._declarations = declarations
        self._instructions = instructions

    def print_ast(self, level):
        string = "%sBlock Instruction:\n%sVariable Declarations:" % (
            self._get_indentation(level),
            self._get_indentation(level+1),
            )
        for declaration in self._declarations:
            string += "%s" % declaration.print_ast(level+2)
        string += "\n%sInstructions:" % self._get_indentation(level+1)
        for instruction in self._instructions:
            string += "\n%s" % instruction.print_ast(level+2)
        return string


class VariableDeclaration(Declaration):

    def __init__(self, type_class, variables, *args, **kwargs):
        super(VariableDeclaration, self).__init__(args,kwargs)
        self._type      = type_class
        self._variables = variables

    def print_ast(self, level):
        string = "\n%sVariable Declaration:\n" % self._get_indentation(level+1)
        string += "%sType:\n" % self._get_indentation(level+2)
        string += "%s" % self._type.print_ast(level+3)
        string += "%sVariables:" % self._get_indentation(level+2)
        for variable in self._variables:
            string += "\n%s" % variable.print_ast(level+3)
        return string


class Type(Setlan):

    def __init__(self, *args, **kwargs):
        super(Type, self).__init__()
        self._position = kwargs.get('position', None)

    def __unicode__(self):
        return "%s%s: Not Implemented" % (self.SPACE, self.__class__.__name__)

    def print_ast(self, level):
        string = "%s%s\n" % (
            self._get_indentation(level),
            self
            )
        return string


class IntegerType(Type):

    def __unicode__(self):
        return "Integer"


class BooleanType(Type):

    def __unicode__(self):
        return "Boolean"


class SetType(Type):

    def __unicode__(self):
        return "Set"


class Input(Instruction):

    def __init__(self, variable, *args, **kwargs):
        super(Input, self).__init__(args,kwargs)
        self._variable = variable

    def print_ast(self, level):
        string = "%sScan Instruction:\n%s" % (
            self._get_indentation(level),
            self._variable.print_ast(level+1)
            )
        return string

    
class Output(Instruction):

    def __init__(self, printables, *args, **kwargs):
        super(Output, self).__init__(args,kwargs)
        self._printables = printables
        self._lnsufix = kwargs.get('sufix',None)
        if self._lnsufix is None:
            self._op_name = 'Print'
        else :
            self._op_name = 'PrintLn'
            self._printables.append(String("\n", position=kwargs.get('position', None)))

    def print_ast(self, level):
        string = "%s%s Instruction:\n%sExpressions:" % (
            self._get_indentation(level),
            self._op_name,
            self._get_indentation(level+1)
            )
        for printable in self._printables:
            string += "\n%s" % (
                printable.print_ast(level+2)
                )
        return string

class Conditional(Instruction):

    def __init__(self, condition, instruction, alt_instruction=None, *args, **kwargs):
        super(Conditional, self).__init__(args,kwargs)
        self._condition = condition
        self._instruction = instruction
        self._alt_instruction = alt_instruction

    def print_ast(self, level):
        string = "%sConditional Instruction:\n" % self._get_indentation(level)
        string += "%sCondition:\n" % self._get_indentation(level+1)
        string += "%s\n" % self._condition.print_ast(level+2)
        string += "%sInstruction:\n" % self._get_indentation(level+1)
        string += "%s" % self._instruction.print_ast(level+2)
        if self._alt_instruction is not None:
            string += "\n%sAlternative Instruction:\n" % self._get_indentation(level+1)
            string += "%s" % self._alt_instruction.print_ast(level+2)
        return string


class ForLoop(Instruction):

    def __init__(self, variable, ordering, set_exp, instruction, *args, **kwargs):
        super(ForLoop, self).__init__(args,kwargs)
        self._variable    = variable
        self._ordering    = ordering
        self._set         = set_exp
        self._instruction = instruction

    def print_ast(self, level):
        string = "%sFor Loop Instruction:\n" % self._get_indentation(level)
        string += "%sVariable:\n" % self._get_indentation(level+1)
        string += "%s\n" % self._variable.print_ast(level+2)
        string += "%sOrdering: " % self._get_indentation(level+1)
        if self._ordering:
            string += "Ascendent"
        else :
            string += "Descendent"
        string += "\n%sIterable Set:\n" % self._get_indentation(level+1)
        string += "%s\n" % self._set.print_ast(level+2)
        string += "%sInstruction:\n" % self._get_indentation(level+1)
        string += "%s" % self._instruction.print_ast(level+2)
        return string


class RepeatWhileLoop(Instruction):

    def __init__(self, prev_instruction, condition, instruction, *args, **kwargs):
        super(RepeatWhileLoop, self).__init__(args,kwargs)
        self._prev_instruction = prev_instruction
        self._condition        = condition
        self._instruction      = instruction

    def print_ast(self, level):
        string = "%sRepeate While Loop Instruction:\n" % self._get_indentation(level)
        if self._prev_instruction is not None:
            string += "%sPrevious Instruction:\n" % self._get_indentation(level+1)
            string += "%s\n" % self._prev_instruction.print_ast(level+2)
        string += "%sCondition:\n" % self._get_indentation(level+1)
        string += "%s\n" % self._condition.print_ast(level+2)
        string += "%sInstruction:\n" % self._get_indentation(level+1)
        string += "%s" % self._instruction.print_ast(level+2)
        return string


class BinaryExpression(Expression):

    def __init__(self, left, op, right, *args, **kwargs):
        super(BinaryExpression, self).__init__(args,kwargs)
        self._left = left
        self._function = op
        self._right = right
        self._operation = ""

    def print_ast(self, level):
        string = "%s%s:\n%sLeft Operand:\n%s\n%sRight Operand:\n%s" % (
            self._get_indentation(level),
            self._operation,
            self._get_indentation(level+1),
            self._left.print_ast(level+2),
            self._get_indentation(level+1),
            self._right.print_ast(level+2)
            )
        return string


class UnaryExpression(Expression):

    def __init__(self, op, expression, *args, **kwargs):
        super(UnaryExpression, self).__init__(args,kwargs)
        self._expression = expression
        self._function = op
        self._operation = ""

    def print_ast(self, level):
        string = "%s%s:\n%sOperand:\n%s" % (
            self._get_indentation(level),
            self._operation,
            self._get_indentation(level+1),
            self._expression.print_ast(level+2)
            )
        return string


class Sum(BinaryExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(Sum, self).__init__(left, None, right, args, kwargs)
        self._operation = "Sum"


class Subtraction(BinaryExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(Subtraction, self).__init__(left, None, right, args, kwargs)
        self._operation = "Subtraction"


class Times(BinaryExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(Times, self).__init__(left, None, right, args, kwargs)
        self._operation = "Times"


class Division(BinaryExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(Division, self).__init__(left, None, right, args, kwargs)
        self._operation = "Division"


class Modulus(BinaryExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(Modulus, self).__init__(left, None, right, args, kwargs)
        self._operation = "Modulus"


class Union(BinaryExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(Union, self).__init__(left, None, right, args, kwargs)
        self._operation = "Union"


class Difference(BinaryExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(Difference, self).__init__(left, None, right, args, kwargs)
        self._operation = "Difference"


class Intersection(BinaryExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(Intersection, self).__init__(left, None, right, args, kwargs)
        self._operation = "Intersection"


class SetSum(BinaryExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(SetSum, self).__init__(left, None, right, args, kwargs)
        self._operation = "SetSum"


class SetSubtraction(BinaryExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(SetSubtraction, self).__init__(left, None, right, args, kwargs)
        self._operation = "SetSubtraction"


class SetTimes(BinaryExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(SetTimes, self).__init__(left, None, right, args, kwargs)
        self._operation = "SetTimes"


class SetDivision(BinaryExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(SetDivision, self).__init__(left, None, right, args, kwargs)
        self._operation = "SetDivision"


class SetModulus(BinaryExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(SetModulus, self).__init__(left, None, right, args, kwargs)
        self._operation = "SetModulus"


class GreaterThan(BinaryExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(GreaterThan, self).__init__(left, None, right, args, kwargs)
        self._operation = "GreaterThan"


class GreaterOrEqual(BinaryExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(GreaterOrEqual, self).__init__(left, None, right, args, kwargs)
        self._operation = "GreaterOrEqual"


class LessThan(BinaryExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(LessThan, self).__init__(left, None, right, args, kwargs)
        self._operation = "LessThan"


class LessOrEqual(BinaryExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(LessOrEqual, self).__init__(left, None, right, args, kwargs)
        self._operation = "LessOrEqual"


class Equals(BinaryExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(Equals, self).__init__(left, None, right, args, kwargs)
        self._operation = "Equals"


class NotEquals(BinaryExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(NotEquals, self).__init__(left, None, right, args, kwargs)
        self._operation = "NotEquals"


class And(BinaryExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(And, self).__init__(left, None, right, args, kwargs)
        self._operation = "And"


class Or(BinaryExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(Or, self).__init__(left, None, right, args, kwargs)
        self._operation = "Or"


class IsIn(BinaryExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(IsIn, self).__init__(left, None, right, args, kwargs)
        self._operation = "IsIn"


class Minus(UnaryExpression):

    def __init__(self, expression, *args, **kwargs):
        super(Minus, self).__init__(None, expression, args, kwargs)
        self._operation = "Minus"


class GetMax(UnaryExpression):

    def __init__(self, expression, *args, **kwargs):
        super(GetMax, self).__init__(None, expression, args, kwargs)
        self._operation = "GetMax"


class GetMin(UnaryExpression):

    def __init__(self, expression, *args, **kwargs):
        super(GetMin, self).__init__(None, expression, args, kwargs)
        self._operation = "GetMin"


class GetSize(UnaryExpression):

    def __init__(self, expression, *args, **kwargs):
        super(GetSize, self).__init__(None, expression, args, kwargs)
        self._operation = "GetSize"


class Not(UnaryExpression):

    def __init__(self, expression, *args, **kwargs):
        super(Not, self).__init__(None, expression, args, kwargs)
        self._operation = "Not"


class TrueValue(Expression):

    def __init__(self, *args, **kwargs):
        super(TrueValue, self).__init__(args, kwargs)
        self._value = True

    def print_ast(self, level):
        string = "%sBoolean: True" % self._get_indentation(level)
        return string


class FalseValue(Expression):

    def __init__(self, *args, **kwargs):
        super(FalseValue, self).__init__(args, kwargs)
        self._value = False

    def print_ast(self, level):
        string = "%sBoolean: False" % self._get_indentation(level)
        return string


class Number(Expression):

    def __init__(self, value, *args, **kwargs):
        super(Number, self).__init__(args, kwargs)
        self._value = value

    def print_ast(self, level):
        string = "%sNumber: %s" % (self._get_indentation(level), str(self._value))
        return string


class Set(Expression):

    def __init__(self, elements, *args, **kwargs):
        super(Set, self).__init__(args, kwargs)
        self._value = elements

    def print_ast(self, level):
        string = "%sSet:" % self._get_indentation(level)
        for index, element in enumerate(self._value):
            string += "\n%sElement[%d]:" % (
                self._get_indentation(level+1),
                index
                )
            string += "\n%s" % element.print_ast(level+2)


        return string
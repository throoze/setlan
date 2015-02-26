#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# ast.py
#
# Setlan Abstract Syntactic Tree
#
# Author:
# Victor De Ponte, 05-38087, <rdbvictor19@gmail.com>
# ------------------------------------------------------------
from config import SetlanConfig

from sym_table import SymTable

from exceptions import ( SetlanTypeError, SetlanSyntaxError)

class Setlan(SetlanConfig):

    def __init__(self, instruction, *args, **kwargs):
        super(Setlan, self).__init__(args, kwargs)
        self._position = kwargs.get('position', None)
        self._instruction = instruction

    def __repr__(self):
        return self.__unicode__()

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        string = self.print_ast(0)
        return string

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        """Define a non-equality test"""
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def __hash__(self):
        """Override the default hash behavior (that returns the id or the object)"""
        return hash(tuple(sorted(self.__dict__.items())))

    def print_ast(self, level):
        string = "Setlan Program:\n%s" % self._instruction.print_ast(level+1)
        return string

    def staticChecks(self):
        st = self._check(None)
        while st.getFather() is not None:
            st = st.getFather()
        return st

    def _check(self, symtable):
        check = self._instruction._check(symtable)
        if isinstance(check, SymTable):
            return check
        else:
            return SymTable(father=None) 


class Printable(Setlan):

    def __init__(self, *args, **kwargs):
        super(Printable, self).__init__(args, kwargs)
        self._position = kwargs.get('position', None)

    def print_ast(self, level):
        return "%s%s: Not Implemented" % (self.SPACE, self.__class__.__name__)


class Instruction(Setlan):

    def __init__(self, *args, **kwargs):
        super(Instruction, self).__init__(args, kwargs)
        self._position = kwargs.get('position', None)

    def print_ast(self, level):
        return "%s%s: Not Implemented" % (self.SPACE, self.__class__.__name__)

    def _check(self, symtable):
        print "%s: Check function Not Implemented" % (self.__class__.__name__)


class Declaration(Setlan):

    def print_ast(self, level):
        return "%s%s: Not Implemented" % (self.SPACE, self.__class__.__name__)


class Expression(Printable):

    def __init__(self, *args, **kwargs):
        super(Expression, self).__init__(args, kwargs)
        self._position = kwargs.get('position', None)


class String(Printable):

    def __init__(self, value, *args, **kwargs):
        super(String, self).__init__(args,kwargs)
        self._value = value

    def print_ast(self, level):
        string = "%sString: %s" % (
            self._get_indentation(level),
            str(self._value)
            )
        return string

    def _check(self, symtable):
        return True


class Block(Instruction):

    def __init__(self, declarations, instructions, *args, **kwargs):
        super(Block, self).__init__(args,kwargs)
        self._position = kwargs.get('position', None)
        self._declarations = declarations
        self._instructions = instructions

    def print_ast(self, level):
        string = "%sBlock Instruction:" % self._get_indentation(level)
        if self._declarations is not None and self._declarations:
            string += "\n%sVariable Declarations:" % self._get_indentation(level+1)
            for declaration in self._declarations:
                string += "%s" % declaration.print_ast(level+2)
        if self._instructions is not None and self._instructions:
            string += "\n%sInstructions:" % self._get_indentation(level+1)
            for instruction in self._instructions:
                string += "\n%s" % instruction.print_ast(level+2)
        return string

    def _check(self, symtable):
        if self._declarations is not None and self._declarations:
            new_symtable = SymTable(father=symtable)
            for declaration in self._declarations:
                declaration._check(new_symtable)
        else:
            new_symtable = symtable
        if self._instructions is not None and self._instructions:
            for instruction in self._instructions:
                instruction._check(new_symtable)
        if symtable is None:
            return new_symtable
        else:
            return True


class VariableDeclaration(Declaration):

    def __init__(self, type_class, variables, *args, **kwargs):
        super(VariableDeclaration, self).__init__(args,kwargs)
        self._position = kwargs.get('position', None)
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

    def _check(self, symtable):
        if self._variables is not None and self._variables:
            for variable in self._variables:
                symtable.insert(variable.getName(), self._type)
        else:
            error  = "In line %d, column %d, " % self._position
            error += "there must be at least one variable declared."
            raise SetlanSyntaxError(error)
        return True


class Variable(Expression):

    def __init__(self, tkid, *args, **kwargs):
        super(Variable, self).__init__(args,kwargs)
        self._position = kwargs.get('position', None)
        self._id = tkid

    def print_ast(self, level):
        string = "%sVariable: %s" % (self._get_indentation(level), self._id)
        return string

    def getName(self):
        return self._id

    def _check(self, symtable):
        var_info = symtable.lookup(self.getName(),self._position)
        return var_info.getType()


class Type(Setlan):

    def __init__(self, *args, **kwargs):
        super(Type, self).__init__(args, kwargs)
        self._position = kwargs.get('position', None)
        self._default = None

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return True
        return False

    def __ne__(self, other):
        """Define a non-equality test"""
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return True

    def __hash__(self):
        """
        Override the default hash behavior (that returns the id or the object)
        """
        dictionary = {
            "class" : self.__class__,
            "default" : self._default
        }
        return hash(tuple(sorted(dictionary.items())))

    def __str__(self):
        return self.__unicode__()

    def getPosition(self):
        return self._position

    def getDefault(self):
        return self._default

    def canBeAssigned(self, value):
        return False

    def __unicode__(self):
        return "%s%s: Not Implemented" % (self.SPACE, self.__class__.__name__)

    def print_ast(self, level):
        string = "%s%s\n" % (
            self._get_indentation(level),
            self
            )
        return string

    def canBeAssigned(self, type_class):
        return self == type_class

    def isInt(self):
        return isinstance(self, IntegerType)

    def isBool(self):
        return isinstance(self, BooleanType)

    def isSet(self):
        return isinstance(self, SetType)


class IntegerType(Type):

    def __init__(self, *args, **kwargs):
        super(IntegerType, self).__init__(args, kwargs)
        self._position = kwargs.get('position', None)
        self._default = 0

    def __unicode__(self):
        return "Integer"


class BooleanType(Type):

    def __init__(self, *args, **kwargs):
        super(BooleanType, self).__init__(args, kwargs)
        self._position = kwargs.get('position', None)
        self._default = False

    def __unicode__(self):
        return "Boolean"


class SetType(Type):

    def __init__(self, *args, **kwargs):
        super(SetType, self).__init__(args, kwargs)
        self._position = kwargs.get('position', None)
        self._default = set([])

    def __unicode__(self):
        return "Set"


class Assignment(Instruction):

    def __init__(self, variable, value, *args, **kwargs):
        super(Assignment , self).__init__(args,kwargs)
        self._position = kwargs.get('position', None)
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

    def _check(self, symtable):
        var_info = symtable.lookup(self._variable.getName(), self._position)
        val_type_class = self._value._check(symtable)
        if not var_info.canAssign(val_type_class):
            error  = "In line %d, column %d, " % self._position
            error += "cannot assign a %s value to a %s variable." % (
                val_type_class,
                var_info.getType()
                )
            raise SetlanTypeError(error)
        return True


class Input(Instruction):

    def __init__(self, variable, *args, **kwargs):
        super(Input, self).__init__(args,kwargs)
        self._position = kwargs.get('position', None)
        self._variable = variable

    def print_ast(self, level):
        string = "%sScan Instruction:\n%s" % (
            self._get_indentation(level),
            self._variable.print_ast(level+1)
            )
        return string

    def _check(self, symtable):
        self._variable._check(symtable)
        return True


    
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

    def _check(self, symtable):
        if self._printables is not None and self._printables:
            for printable in self._printables:
                printable._check(symtable)
        return True



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

    def _check(self, symtable):
        condition_type = self._condition._check(symtable)
        instruction_check = self._instruction._check(symtable)
        if self._alt_instruction is not None:
            alt_instruction_check = self._alt_instruction._check(symtable)
        else:
            alt_instruction_check = True
        if not condition_type.isBool():
            error  = "In line %d, column %d, " % self._position
            error += "conditional statement expression must be Boolean. "
            error += "Found '%s' instead." % condition_type
            raise SetlanTypeError(error)
        return instruction_check and alt_instruction_check



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

    def _check(self, symtable):
        new_symtable = SymTable(father=symtable)
        new_symtable.insert(
            self._variable.getName(),
            IntegerType(position=self._position)
            )
        if not self._set._check(symtable).isSet():
            error  = "In line %d, column %d, " % self._position
            error += "For loop expression must be of Set type."
            raise SetlanTypeError(error)
        if self._instruction is not None:
            self._instruction._check(new_symtable)
        if symtable is None:
            return new_symtable
        else:
            return True


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
        string += "%s" % self._condition.print_ast(level+2)
        if self._instruction is not None:
            string += "\n%sInstruction:\n" % self._get_indentation(level+1)
            string += "%s" % self._instruction.print_ast(level+2)
        return string

    def _check(self, symtable):
        if self._prev_instruction is None and self._instruction is None:
            error  = "In line %d, column %d, " % self._position
            error += "Repeat-While-Loop must have at least one instruction."
            raise SetlanSyntaxError(error)
        if self._prev_instruction is not None:
            prev_inst_check = self._prev_instruction._check(symtable)
        else:
            prev_inst_check = True
        if self._instruction is not None:
            instruction_check = self._instruction._check(symtable)
        else:
            instruction_check = True
        condition_type = self._condition._check(symtable)
        if not condition_type.isBool():
            error  = "In line %d, column %d, " % self._position
            error += "conditional statement expression must be Boolean. "
            error += "Found '%s' instead." % condition_type
            raise SetlanTypeError(error)
        return prev_inst_check and instruction_check


class BinaryExpression(Expression):

    def __init__(self, left, op, right, *args, **kwargs):
        super(BinaryExpression, self).__init__(args,kwargs)
        self._position = kwargs.get('position', None)
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

    def _check(self, symtable):
        return "%s%s: Not Implemented" % (self.SPACE, self.__class__.__name__)


class SameTypeBinaryExpression(BinaryExpression):

    def __init__(self, left, op, right, *args, **kwargs):
        super(SameTypeBinaryExpression, self).__init__(left,op,right,args,kwargs)
        self._position = kwargs.get('position', None)
        self._expected_type = None
    
    def _check(self, symtable):
        left_type = self._left._check(symtable)
        right_type = self._right._check(symtable)
        if ((not isinstance(left_type, self._expected_type.__class__)) or
            left_type != right_type):
            error  = "In line %d, column %d, " % self._position
            error += "cannot make '%s' operation over %s and %s expressions." % (
                self._operation,
                left_type,
                right_type
                )
            raise SetlanTypeError(error)
        return left_type


class ComparationBinaryExpression(BinaryExpression):

    def __init__(self, left, op, right, *args, **kwargs):
        super(ComparationBinaryExpression, self).__init__(left,op,right,args,kwargs)
        self._position = kwargs.get('position', None)
    
    def _check(self, symtable):
        left_type = self._left._check(symtable)
        right_type = self._right._check(symtable)
        if left_type != right_type:
            error  = "In line %d, column %d, " % self._position
            error += "cannot make '%s' operation over %s and %s expressions." % (
                self._operation,
                left_type,
                right_type
                )
            raise SetlanTypeError(error)
        return BooleanType(position=self._position)


class IntSetSetExpression(BinaryExpression):

    def __init__(self, left, op, right, *args, **kwargs):
        super(IntSetSetExpression, self).__init__(left,op,right,args,kwargs)
        self._position = kwargs.get('position', None)
    
    def _check(self, symtable):
        left_type = self._left._check(symtable)
        right_type = self._right._check(symtable)
        if ((not isinstance(left_type, IntegerType)) or
           (not isinstance(right_type, SetType))):
            error  = "In line %d, column %d, " % self._position
            error += "cannot make '%s' operation over %s and %s expressions. " % (
                self._operation,
                left_type,
                right_type
                )
            error += "Expected: Integer and Set, in this order."
            raise SetlanTypeError(error)
        return right_type


class IntSetBooleanExpression(BinaryExpression):

    def __init__(self, left, op, right, *args, **kwargs):
        super(IntSetBooleanExpression, self).__init__(left,op,right,args,kwargs)
        self._position = kwargs.get('position', None)
    
    def _check(self, symtable):
        left_type = self._left._check(symtable)
        right_type = self._right._check(symtable)
        if ((not isinstance(left_type, IntegerType)) or
           (not isinstance(right_type, SetType))):
            error  = "In line %d, column %d, " % self._position
            error += "cannot make '%s' operation over %s and %s expressions. " % (
                self._operation,
                left_type,
                right_type
                )
            error += "Expected: Integer and Set, in this order."
            raise SetlanTypeError(error)
        return BooleanType(position=self._position)


class UnaryExpression(Expression):

    def __init__(self, op, expression, *args, **kwargs):
        super(UnaryExpression, self).__init__(args,kwargs)
        self._position = kwargs.get('position', None)
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


class IntUnaryExpression(UnaryExpression):

    def __init__(self, op, expression, *args, **kwargs):
        super(IntUnaryExpression, self).__init__(op,expression,args,kwargs)
        self._position = kwargs.get('position', None)
    
    def _check(self, symtable):
        type_class = self._expression._check(symtable)
        if not isinstance(type_class, IntegerType):
            error  = "In line %d, column %d, " % self._position
            error += "cannot make '%s' operation over %s expression. " % (
                self._operation,
                type_class
                )
            error += "Expected: Integer."
            raise SetlanTypeError(error)
        return type_class


class SetUnaryExpression(UnaryExpression):

    def __init__(self, op, expression, *args, **kwargs):
        super(SetUnaryExpression, self).__init__(op,expression,args,kwargs)
        self._position = kwargs.get('position', None)
    
    def _check(self, symtable):
        type_class = self._expression._check(symtable)
        if not isinstance(type_class, SetType):
            error  = "In line %d, column %d, " % self._position
            error += "cannot make '%s' operation over %s expression. " % (
                self._operation,
                type_class
                )
            error += "Expected: Set."
            raise SetlanTypeError(error)
        return type_class


class BoolUnaryExpression(UnaryExpression):

    def __init__(self, op, expression, *args, **kwargs):
        super(BoolUnaryExpression, self).__init__(op,expression,args,kwargs)
        self._position = kwargs.get('position', None)
    
    def _check(self, symtable):
        type_class = self._expression._check(symtable)
        if not isinstance(type_class, BooleanType):
            error  = "In line %d, column %d, " % self._position
            error += "cannot make '%s' operation over %s expression. " % (
                self._operation,
                type_class
                )
            error += "Expected: Boolean."
            raise SetlanTypeError(error)
        return type_class


class Sum(SameTypeBinaryExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(Sum, self).__init__(left, None, right, args, kwargs)
        self._position = kwargs.get('position', None)
        self._operation = "Sum"
        self._expected_type = IntegerType(position=self._position)


class Subtraction(SameTypeBinaryExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(Subtraction, self).__init__(left, None, right, args, kwargs)
        self._position = kwargs.get('position', None)
        self._operation = "Subtraction"
        self._expected_type = IntegerType(position=self._position)


class Times(SameTypeBinaryExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(Times, self).__init__(left, None, right, args, kwargs)
        self._position = kwargs.get('position', None)
        self._operation = "Times"
        self._expected_type = IntegerType(position=self._position)


class Division(SameTypeBinaryExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(Division, self).__init__(left, None, right, args, kwargs)
        self._position = kwargs.get('position', None)
        self._operation = "Division"
        self._expected_type = IntegerType(position=self._position)


class Modulus(SameTypeBinaryExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(Modulus, self).__init__(left, None, right, args, kwargs)
        self._position = kwargs.get('position', None)
        self._operation = "Modulus"
        self._expected_type = IntegerType(position=self._position)


class Union(SameTypeBinaryExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(Union, self).__init__(left, None, right, args, kwargs)
        self._position = kwargs.get('position', None)
        self._operation = "Union"
        self._expected_type = SetType(position=self._position)


class Difference(SameTypeBinaryExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(Difference, self).__init__(left, None, right, args, kwargs)
        self._position = kwargs.get('position', None)
        self._operation = "Difference"
        self._expected_type = SetType(position=self._position)


class Intersection(SameTypeBinaryExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(Intersection, self).__init__(left, None, right, args, kwargs)
        self._position = kwargs.get('position', None)
        self._operation = "Intersection"
        self._expected_type = SetType(position=self._position)


class SetSum(IntSetSetExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(SetSum, self).__init__(left, None, right, args, kwargs)
        self._position = kwargs.get('position', None)
        self._operation = "SetSum"


class SetSubtraction(IntSetSetExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(SetSubtraction, self).__init__(left, None, right, args, kwargs)
        self._position = kwargs.get('position', None)
        self._operation = "SetSubtraction"


class SetTimes(IntSetSetExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(SetTimes, self).__init__(left, None, right, args, kwargs)
        self._position = kwargs.get('position', None)
        self._operation = "SetTimes"


class SetDivision(IntSetSetExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(SetDivision, self).__init__(left, None, right, args, kwargs)
        self._position = kwargs.get('position', None)
        self._operation = "SetDivision"


class SetModulus(IntSetSetExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(SetModulus, self).__init__(left, None, right, args, kwargs)
        self._position = kwargs.get('position', None)
        self._operation = "SetModulus"


class GreaterThan(ComparationBinaryExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(GreaterThan, self).__init__(left, None, right, args, kwargs)
        self._position = kwargs.get('position', None)
        self._operation = "GreaterThan"


class GreaterOrEqual(ComparationBinaryExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(GreaterOrEqual, self).__init__(left, None, right, args, kwargs)
        self._position = kwargs.get('position', None)
        self._operation = "GreaterOrEqual"


class LessThan(ComparationBinaryExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(LessThan, self).__init__(left, None, right, args, kwargs)
        self._position = kwargs.get('position', None)
        self._operation = "LessThan"


class LessOrEqual(ComparationBinaryExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(LessOrEqual, self).__init__(left, None, right, args, kwargs)
        self._position = kwargs.get('position', None)
        self._operation = "LessOrEqual"


class Equals(ComparationBinaryExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(Equals, self).__init__(left, None, right, args, kwargs)
        self._position = kwargs.get('position', None)
        self._operation = "Equals"


class NotEquals(ComparationBinaryExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(NotEquals, self).__init__(left, None, right, args, kwargs)
        self._position = kwargs.get('position', None)
        self._operation = "NotEquals"


class And(SameTypeBinaryExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(And, self).__init__(left, None, right, args, kwargs)
        self._position = kwargs.get('position', None)
        self._operation = "And"
        self._expected_type = BooleanType(position=self._position)


class Or(SameTypeBinaryExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(Or, self).__init__(left, None, right, args, kwargs)
        self._position = kwargs.get('position', None)
        self._operation = "Or"
        self._expected_type = BooleanType(position=self._position)


class IsIn(IntSetBooleanExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(IsIn, self).__init__(left, None, right, args, kwargs)
        self._position = kwargs.get('position', None)
        self._operation = "IsIn"


class Minus(IntUnaryExpression):

    def __init__(self, expression, *args, **kwargs):
        super(Minus, self).__init__(None, expression, args, kwargs)
        self._position = kwargs.get('position', None)
        self._operation = "Minus"


class GetMax(SetUnaryExpression):

    def __init__(self, expression, *args, **kwargs):
        super(GetMax, self).__init__(None, expression, args, kwargs)
        self._position = kwargs.get('position', None)
        self._operation = "GetMax"


class GetMin(SetUnaryExpression):

    def __init__(self, expression, *args, **kwargs):
        super(GetMin, self).__init__(None, expression, args, kwargs)
        self._position = kwargs.get('position', None)
        self._operation = "GetMin"


class GetSize(SetUnaryExpression):

    def __init__(self, expression, *args, **kwargs):
        super(GetSize, self).__init__(None, expression, args, kwargs)
        self._position = kwargs.get('position', None)
        self._operation = "GetSize"


class Not(BoolUnaryExpression):

    def __init__(self, expression, *args, **kwargs):
        super(Not, self).__init__(None, expression, args, kwargs)
        self._position = kwargs.get('position', None)
        self._operation = "Not"


class TrueValue(Expression):

    def __init__(self, *args, **kwargs):
        super(TrueValue, self).__init__(args, kwargs)
        self._position = kwargs.get('position', None)
        self._value = True

    def print_ast(self, level):
        string = "%sBoolean: True" % self._get_indentation(level)
        return string

    def _check(self, symtable):
        return BooleanType(position=self._position)


class FalseValue(Expression):

    def __init__(self, *args, **kwargs):
        super(FalseValue, self).__init__(args, kwargs)
        self._position = kwargs.get('position', None)
        self._value = False

    def print_ast(self, level):
        string = "%sBoolean: False" % self._get_indentation(level)
        return string

    def _check(self, symtable):
        return BooleanType(position=self._position)


class Number(Expression):

    def __init__(self, value, *args, **kwargs):
        super(Number, self).__init__(args, kwargs)
        self._position = kwargs.get('position', None)
        self._value = value

    def print_ast(self, level):
        string = "%sNumber: %s" % (self._get_indentation(level), str(self._value))
        return string

    def _check(self, symtable):
        return IntegerType(position=self._position)


class Set(Expression):

    def __init__(self, elements, *args, **kwargs):
        super(Set, self).__init__(args, kwargs)
        self._position = kwargs.get('position', None)
        self._input = elements

    def print_ast(self, level):
        string = "%sSet:\n%s{" % (
            self._get_indentation(level), self._get_indentation(level+1))
        for index, element in enumerate(self._input):
            string += "\n%sElement[%d]:" % (
                self._get_indentation(level+2),
                index
                )
            string += "\n%s" % element.print_ast(level+3)
        string += "\n%s}" % self._get_indentation(level+1)
        return string

    def _check(self, symtable):
        return SetType(position=self._position)
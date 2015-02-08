#!/usr/bin/env python
# ------------------------------------------------------------
# syntax_specs.py
#
# Setlan language syntactic specifications. Every grammar,
# precedence and associativity rule for Setlan are specified
# here.
#
# Author:
# Victor De Ponte, 05-38087, <rdbvictor19@gmail.com>
# ------------------------------------------------------------
from exceptions import SetlanSyntaxError

from lexical_specs import tokens
#from ast import *

##########
## List of tokens to be used by ply.yacc
tokens = tokens
##########

################################################################################
###################### Precedence and associative rules ########################
################################################################################

precedence = (    
    ('left', 'TkOr'),
    ('left', 'TkAnd'),
    ('nonassoc', 'TkGreatOrEq', 'TkLessOrEq', 'TkGreat', 'TkLess'),
    ('nonassoc', 'TkEquals', 'TkNotEq'),
    ('nonassoc', 'TkIsIn'),
    ('left', 'TkPlus', 'TkMinus'),
    ('left', 'TkTimes', 'TkDiv', 'TkMod'),
    ('left', 'TkUnion', 'TkDiff', 'TkInter'),
    ('left', 'TkSPlus', 'TkSMinus'),
    ('left', 'TkSTimes', 'TkSDiv', 'TkSMod'),
    ('right', 'TkNot'),
    ('right', 'UMINUS'),
    ('right', 'TkGetMax', 'TkGetMin', 'TkSize')
   )

################################################################################
################### End of Precedence and associative rules ####################
################################################################################

################################################################################
################################ Grammar rules #################################
################################################################################
start = 'Setlan'

#Gramatic Definitions
def p_Trinity(p):
    '''
    Setlan : TkProgram Instruction
    '''
    pass

def p_Instruction(p):
    '''
    Instruction : Assignment
                | Block
                | Input
                | Output
                | Conditional
                | For
                | While
    '''
    pass

def p_Assignment(p):
    '''
    Assignment : TkId TkAssign Expression
    '''
    pass

def p_Block(p):
    '''
    Block : TkOBrace VariableDeclarations InstructionsList TkCBrace
    '''
    pass

def p_VariableDeclarations(p):
    '''
    VariableDeclarations : TkUsing VariableDeclarationList TkIn
                         | lambda
    '''
    pass

def p_VariableDeclarationList(p):
    '''
    VariableDeclarationList : VariableDeclarationList VariableDeclaration TkSColon
                            | VariableDeclaration TkSColon
    '''
    pass

def p_VariableDeclaration(p):
    '''
    VariableDeclaration : Type VariableList
    '''
    pass

def p_Type(p):
    '''
    Type : TkInt
         | TkBool
         | TkSet
    '''
    pass

def p_VariableList(p):
    '''
    VariableList : VariableList TkComma TkId
                 | TkId
    '''
    pass

def p_InstructionList(p):
    '''
    InstructionsList : InstructionsList Instruction TkSColon
                     | Instruction TkSColon
    '''
    pass

def p_Input(p):
    '''
    Input : TkScan TkId
    '''
    pass

def p_Output(p):
    '''
    Output : Println
           | Print
    '''
    pass

def p_Println(p):
    '''
    Println : TkPrintLn PrintableList 
    '''
    pass

def p_Print(p):
    '''
    Print : TkPrint PrintableList
    '''
    pass

def p_PrintableList(p):
    '''
    PrintableList : PrintableList TkComma Printable
                  | Printable
    '''
    pass

def p_Printable(p):
    '''
    Printable : Expression
              | TkString
    '''
    pass

def p_Conditional(p):
    '''
    Conditional : TkIf TkOPar Expression TkCPar Instruction TkElse Instruction
    '''
    pass

def p_For(p):
    '''
    For : TkFor TkId Ordering Expression Do
    '''
    pass

def p_Ordering(p):
    '''
    Ordering : TkMin
             | TkMax
    '''
    pass

def p_While(p):
    '''
    While : Repeat TkWhile TkOPar Expression TkCPar Do
    '''
    pass

def p_Repeat(p):
    '''
    Repeat : TkRepeat Instruction
           | lambda
    '''
    pass

def p_Do(p):
    '''
    Do : TkDo Instruction
    '''
    pass


def p_Expression(p):
    '''
    Expression : TkOPar Expression TkCPar
               | BinaryExpression
               | UnaryExpression
               | Literal
               | TkId
    '''
    pass

def p_BinaryExpression_Sum(p):
    '''
    BinaryExpression : Expression TkPlus Expression
    '''
    pass

def p_BinaryExpression_Subtraction(p):
    '''
    BinaryExpression : Expression TkMinus Expression
    '''
    pass

def p_BinaryExpression_Times(p):
    '''
    BinaryExpression : Expression TkTimes Expression
    '''
    pass

def p_BinaryExpression_Division(p):
    '''
    BinaryExpression : Expression TkDiv Expression
    '''
    pass

def p_BinaryExpression_Modulus(p):
    '''
    BinaryExpression : Expression TkMod Expression
    '''
    pass

def p_BinaryExpression_Union(p):
    '''
    BinaryExpression : Expression TkUnion Expression
    '''
    pass

def p_BinaryExpression_Difference(p):
    '''
    BinaryExpression : Expression TkDiff Expression
    '''
    pass

def p_BinaryExpression_Intersection(p):
    '''
    BinaryExpression : Expression TkInter Expression
    '''
    pass

def p_BinaryExpression_SSum(p):
    '''
    BinaryExpression : Expression TkSPlus Expression
    '''
    pass

def p_BinaryExpression_SSubtraction(p):
    '''
    BinaryExpression : Expression TkSMinus Expression
    '''
    pass

def p_BinaryExpression_STimes(p):
    '''
    BinaryExpression : Expression TkSTimes Expression
    '''
    pass

def p_BinaryExpression_SDivision(p):
    '''
    BinaryExpression : Expression TkSDiv Expression
    '''
    pass

def p_BinaryExpression_SModulus(p):
    '''
    BinaryExpression : Expression TkSMod Expression
    '''
    pass

def p_BinaryExpression_Boolean_GreaterThan(p):
    '''
    BinaryExpression : Expression TkGreat Expression
    '''
    pass

def p_BinaryExpression_Boolean_GreaterOrEqual(p):
    '''
    BinaryExpression : Expression TkGreatOrEq Expression
    '''
    pass

def p_BinaryExpression_Boolean_LessThan(p):
    '''
    BinaryExpression : Expression TkLess Expression
    '''
    pass

def p_BinaryExpression_Boolean_LessOrEqual(p):
    '''
    BinaryExpression : Expression TkLessOrEq Expression
    '''
    pass

def p_BinaryExpression_Boolean_Equals(p):
    '''
    BinaryExpression : Expression TkEquals Expression
    '''
    pass

def p_BinaryExpression_Boolean_NotEquals(p):
    '''
    BinaryExpression : Expression TkNotEq Expression
    '''
    pass

def p_BinaryExpression_Boolean_And(p):
    '''
    BinaryExpression : Expression TkAnd Expression
    '''
    pass

def p_BinaryExpression_Boolean_Or(p):
    '''
    BinaryExpression : Expression TkOr Expression
    '''
    pass

def p_BinaryExpression_Boolean_IsIn(p):
    '''
    BinaryExpression : Expression TkIsIn Expression
    '''
    pass

def p_UnaryExpression_UMinus(p):
    '''
    UnaryExpression : TkMinus Expression %prec UMINUS
    '''
    pass

def p_UnaryExpression_GetMax(p):
    '''
    UnaryExpression : TkGetMax Expression
    '''
    pass

def p_UnaryExpression_GetMin(p):
    '''
    UnaryExpression : TkGetMin Expression
    '''
    pass

def p_UnaryExpression_GetSize(p):
    '''
    UnaryExpression : TkSize Expression
    '''
    pass

def p_UnaryExpression_Boolean_Not(p):
    '''
    UnaryExpression : TkNot Expression
    '''
    pass

def p_Literal_Num(p):
    '''
    Literal : TkNum
    '''
    pass

def p_Literal_True(p):
    '''
    Literal : TkTrue
    '''
    pass

def p_Literal_False(p):
    '''
    Literal : TkFalse
    '''
    pass

def p_Literal_Set(p):
    '''
    Literal : Set
    '''
    pass

def p_Set(p):
    '''
    Set : TkOBrace ExpressionList TkCBrace
    '''
    pass

def p_ExpressionList(p):
    '''
    ExpressionList : ExpressionList TkComma Expression
                   | Expression
    '''
    pass

def p_lambda(p):
    '''
    lambda : 
    '''
    p[0] = []

################################################################################
############################ End of Grammar rules ##############################
################################################################################

# Error handling
def p_error(p):
    error = ""
    if p is None:
        error = "Unexpected End Of File (EOF)."
    else:
        error = "Unexpected %s." % p
    raise SetlanSyntaxError(error)
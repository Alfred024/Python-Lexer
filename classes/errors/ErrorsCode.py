from enum import Enum


class LexicalErrorCode(Enum):
    '''
    Errors of lexical analysis, range from 4000 - 4099
    '''
    IDENTIFIER_MALFORMED = 4000
    UNDEFINED_TOKEN = 4001
    IDENTIFIER_TOO_LONG = 4002
    IDENTIFIER_KEYWORD = 4003
    VAR_ALREADY_DECLARED = 4004
    VAR_NOT_DECLARED = 4005
    INVALID_KEYWORD = 4006
    MALFORMED_LITERAL = 4007
    # Reservados para futuros errores
    ERROR_4008 = 4008
    ERROR_4009 = 4009
    ERROR_4010 = 4010
    ERROR_UNDEFINED = 4011


class SintacticErrorCode(Enum):
    '''
    Errors of syntactic analysis, range from 4100 - 4199
    '''
    ERROR_4100 = 4100
    ERROR_4101 = 4101
    ERROR_4102 = 4102
    ERROR_4103 = 4103
    ERROR_4104 = 4104
    ERROR_4105 = 4105
    ERROR_4106 = 4106
    ERROR_4107 = 4107
    ERROR_4108 = 4108
    ERROR_4109 = 4109
    ERROR_4110 = 4110
    ERROR_UNDEFINED = 4111


class SemanticErrorCode(Enum):
    '''
    Errors of semantic analysis, range from 4200 - 4299
    '''
    ERROR_4200 = 4200
    ERROR_4201 = 4201
    ERROR_4202 = 4202
    ERROR_4203 = 4203
    ERROR_4204 = 4204
    ERROR_4205 = 4205
    ERROR_4206 = 4206
    ERROR_4207 = 4207
    ERROR_4208 = 4208
    ERROR_4209 = 4209
    ERROR_4210 = 4210
    ERROR_UNDEFINED = 4211
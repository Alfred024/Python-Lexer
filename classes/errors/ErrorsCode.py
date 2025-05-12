from enum import Enum

class LexicalErrorCode(Enum):
    '''
        Errors of lexical analize, range from 4000 - 4099
    '''
    
    ERROR_4000 = 4000
    ERROR_4001 = 4001
    ERROR_4002 = 4002
    ERROR_4003 = 4003
    ERROR_4004 = 4004
    ERROR_4005 = 4005
    ERROR_4006 = 4006
    ERROR_4007 = 4007
    ERROR_4008 = 4008
    ERROR_4009 = 4009
    ERROR_4010 = 4010
    ERROR_UNDEFINED = 4011
    
class SintacticErrorCode(Enum):
    '''
        Errors of sintactic analize, range from 4100 - 4199
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
        Errors of sintax analize, range from 4200 - 4299
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
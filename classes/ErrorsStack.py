from enum import Enum
from Token import TokenError

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


class SintaxErrors(Enum):
    '''
        Errors of sintax analize, range from 4100 - 4199
    '''
    pass

class SintacticErrors(Enum):
    '''
        Errors of sintactic analize, range from 4200 - 4299
    '''
    pass

class ErrorsStack:
    def __init__(self):
        self.lexical_errors   = []
        self.sintax_errors    = []
        self.semantic_errors  = []
        
        self.stack = []

    def push(self, error):
        """Agrega un error a la pila."""
        self.stack.append(error)

    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        return None

    def peek(self):
        if not self.is_empty():
            return self.stack[-1]
        return None

    def is_empty(self):
        return len(self.stack) == 0

    def get_all(self):
        return list(self.stack)

    def clear(self):
        self.stack.clear()
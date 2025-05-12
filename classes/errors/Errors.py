from classes.errors.ErrorsCode import LexicalErrorCode, SintacticErrorCode, SemanticErrorCode

class LexicalError:
    '''
        Class that defines a LexicalError error
    '''
    def __init__(self, error_code : LexicalErrorCode = LexicalErrorCode.ERROR_UNDEFINED, message: str = '', line: int = -1, column: int = -1) -> None:
        self._code = error_code
        self._message = message
        self._line = line
        self._column = column

    def __str__(self) -> str:
        return (f'''ERROR {self._code}: ___({self._message})____[{self._line}, {self._column}]''')

class SintacticError:
    '''
        Class that defines a SintacticError error
    '''
    def __init__(self, error_code : SintacticErrorCode = SintacticErrorCode.ERROR_UNDEFINED, message: str = '', line: int = -1, column: int = -1) -> None:
        self._code = error_code
        self._message = message
        self._line = line
        self._column = column

    def __str__(self) -> str:
        return (f'''ERROR {self._code}: ___({self._message})____[{self._line}, {self._column}]''')

class SintaxError:
    '''
        Class that defines a SintaxError error
    '''
    def __init__(self, error_code : SemanticErrorCode = SemanticErrorCode.ERROR_UNDEFINED, message: str = '', line: int = -1, column: int = -1) -> None:
        self._code = error_code
        self._message = message
        self._line = line
        self._column = column

    def __str__(self) -> str:
        return (f'''ERROR {self._code}: ___({self._message})____[{self._line}, {self._column}]''')

from classes.errors.ErrorsCode import LexicalErrorCode, SintacticErrorCode, SemanticErrorCode
import os


class LexicalError:
    '''
    Class that defines a LexicalError
    '''
    def __init__(self, error_code: LexicalErrorCode = LexicalErrorCode.ERROR_UNDEFINED, line: int = -1, column: int = -1) -> None:
        self._code = error_code
        self._line = line
        self._column = column
        self._message_cache = None

    @property
    def _message(self):
        if self._message_cache is None:
            self._message_cache = self._load_message()
        return self._message_cache

    def _load_message(self):
        error_file = "data/errors.txt"
        try:
            with open(error_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip() and ':' in line:
                        code, message = line.strip().split(':', 1)
                        if code.strip() == str(self._code.value):
                            return message.strip()
            return f"Error léxico no definido (código {self._code.value})"
        except FileNotFoundError:
            return f"No se encontró el archivo data/errors.txt (código {self._code.value})"
        except ValueError:
            return f"Formato inválido en data/errors.txt (código {self._code.value})"
        except Exception as e:
            return f"Error al leer data/errors.txt: {str(e)} (código {self._code.value})"

    def __str__(self) -> str:
        return f"ERROR {self._code.value}: ___({self._message})____[{self._line}, {self._column}]"


class SintacticError:
    '''
    Class that defines a SintacticError
    '''
    def __init__(self, error_code: SintacticErrorCode = SintacticErrorCode.ERROR_UNDEFINED, message: str = '', line: int = -1, column: int = -1) -> None:
        self._code = error_code
        self._message = message
        self._line = line
        self._column = column

    def __str__(self) -> str:
        return f"ERROR {self._code}: ___({self._message})____[{self._line}, {self._column}]"


class SemanticError:
    '''
    Class that defines a SemanticError
    '''
    def __init__(self, error_code: SemanticErrorCode = SemanticErrorCode.ERROR_UNDEFINED, message: str = '', line: int = -1, column: int = -1) -> None:
        self._code = error_code
        self._message = message
        self._line = line
        self._column = column

    def __str__(self) -> str:
        return f"ERROR {self._code}: ___({self._message})____[{self._line}, {self._column}]"
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
            errors = {}
            with open(error_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and ':' in line:
                        try:
                            try:
                                code, message = line.split(' : ', 1)  # Intenta con ' : '
                            except ValueError:
                                code, message = line.split(':', 1)  # Intenta con ':'
                            errors[code.strip()] = message.strip()
                        except ValueError as e:
                            print(f"Error al dividir línea '{line}': {str(e)}")  # Depuración
                            continue
            code_str = str(self._code.value).strip()
            return errors.get(code_str, f"Error léxico no definido (código {code_str})")
        except FileNotFoundError:
            return f"No se encontró el archivo {error_file} (código {self._code.value})"
        except Exception as e:
            return f"Error al leer {error_file}: {str(e)} (código {self._code.value})"

    def __str__(self) -> str:
        return f"ERROR {self._code.value}: ___({self._message})____[{self._line}, {self._column}]"


class SintacticError:
    '''
    Class that defines a SintacticError
    '''
    def __init__(self, error_code: SintacticErrorCode = SintacticErrorCode.ERROR_UNDEFINED, line: int = -1, column: int = -1) -> None:
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
            errors = {}
            with open(error_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and ':' in line:
                        try:
                            try:
                                code, message = line.split(' : ', 1)  # Intenta con ' : '
                            except ValueError:
                                code, message = line.split(':', 1)  # Intenta con ':'
                            errors[code.strip()] = message.strip()
                        except ValueError as e:
                            print(f"Error al dividir línea '{line}': {str(e)}")  # Depuración
                            continue
            code_str = str(self._code.value).strip()
            return errors.get(code_str, f"Error sintáctico no definido (código {code_str})")
        except FileNotFoundError:
            return f"No se encontró el archivo {error_file} (código {self._code.value})"
        except Exception as e:
            return f"Error al leer {error_file}: {str(e)} (código {self._code.value})"

    def __str__(self) -> str:
        return f"ERROR {self._code.value}: ___({self._message})____[{self._line}, {self._column}]"


class SemanticError:
    '''
    Class that defines a SemanticError
    '''
    def __init__(self, error_code: SemanticErrorCode = SemanticErrorCode.ERROR_UNDEFINED, line: int = -1, column: int = -1) -> None:
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
            errors = {}
            with open(error_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and ':' in line:
                        try:
                            try:
                                code, message = line.split(' : ', 1)  # Intenta con ' : '
                            except ValueError:
                                code, message = line.split(':', 1)  # Intenta con ':'
                            errors[code.strip()] = message.strip()
                        except ValueError as e:
                            print(f"Error al dividir línea '{line}': {str(e)}")  # Depuración
                            continue
            code_str = str(self._code.value).strip()
            return errors.get(code_str, f"Error semántico no definido (código {code_str})")
        except FileNotFoundError:
            return f"No se encontró el archivo {error_file} (código {self._code.value})"
        except Exception as e:
            return f"Error al leer {error_file}: {str(e)} (código {self._code.value})"

    def __str__(self) -> str:
        return f"ERROR {self._code.value}: ___({self._message})____[{self._line}, {self._column}]"
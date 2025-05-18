from enum import Enum
from classes.errors.Errors import LexicalError, SintacticError, SemanticError


class ErrorsStack:
    def __init__(self):
        self.lexical_errors = []
        self.sintax_errors = []
        self.semantic_errors = []
        self.stack = []

    def push(self, error):
        """Agrega un error a la pila."""
        self.stack.append(error)
        if isinstance(error, LexicalError):
            self.lexical_errors.append(error)
        elif isinstance(error, SintacticError):
            self.sintax_errors.append(error)
        elif isinstance(error, SemanticError):
            self.semantic_errors.append(error)

    def pop(self):
        if not self.is_empty():
            error = self.stack.pop()
            if isinstance(error, LexicalError):
                self.lexical_errors.remove(error)
            elif isinstance(error, SintacticError):
                self.sintax_errors.remove(error)
            elif isinstance(error, SemanticError):
                self.semantic_errors.remove(error)
            return error
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
        self.lexical_errors.clear()
        self.sintax_errors.clear()
        self.semantic_errors.clear()
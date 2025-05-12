from enum import Enum

class ErrorsStack:
    def __init__(self):
        self.lexical_errors   = []
        self.sintax_errors    = []
        self.semantic_errors  = []
        
        self.stack = [] # TODO: Reemplazar por 

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
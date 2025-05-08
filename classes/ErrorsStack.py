class ErrorsStack:
    def __init__(self):
        self.stack = []

    def push(self, error):
        """Agrega un error a la pila."""
        self.stack.append(error)

    def pop(self):
        """Elimina y devuelve el último error de la pila."""
        if not self.is_empty():
            return self.stack.pop()
        return None

    def peek(self):
        """Devuelve el último error sin eliminarlo."""
        if not self.is_empty():
            return self.stack[-1]
        return None

    def is_empty(self):
        """Verifica si la pila está vacía."""
        return len(self.stack) == 0

    def get_all(self):
        """Devuelve todos los errores en la pila."""
        return list(self.stack)

    def clear(self):
        """Limpia todos los errores de la pila."""
        self.stack.clear()
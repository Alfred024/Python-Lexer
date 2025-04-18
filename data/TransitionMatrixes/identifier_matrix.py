letras = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
digitos = "0123456789"

identifier_matrix = {
    0: {'@': 1},  # El estado 0 solo acepta el símbolo '@'
    1: {c: 2 for c in letras},  # El estado 1 acepta letras, y pasa al estado 2
    2: {c: 2 for c in letras + digitos + '_'},  # El estado 2 acepta letras, números o guion bajo, se queda en 2
}

def is_palindrome(array):
    """
    Verifica recursivamente se um array é um palíndromo.

    Args:
        array (list): Lista de elementos a ser verificada.

    Returns:
        bool: True se o array é palíndromo, False caso contrário.
    """
    if len(array) <= 1:
        return True

    if array[0] != array[-1]:
        return False

    return is_palindrome(array[1:-1])


if __name__ == "__main__":
    test_arrays = [
        [0, 1, 2, 3, 2, 1, 0],
        ["a", "b", "b", "a"],
        ["a", "b", "c", "b", "a"],
        ["a", "b", "c", "f", "b", "a"]
    ]

    for array in test_arrays:
        if is_palindrome(array):
            print(f"{array} -> É palíndromo")
        else:
            print(f"{array} -> Não é palíndromo")
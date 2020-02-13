from collections import stack

def is_braces_sequence_correct(seq: str) -> bool:
    """
    :param seq:
    :return:
    >>> is_braces_sequence_correct("()(())")
    True
    >>> is_braces_sequence_correct("()[()]")
    True
    >>> is_braces_sequence_correct(")")
    False
    >>> is_braces_sequence_correct("[()")
    False
    >>> is_braces_sequence_correct("[(])")
    False
    """
    return True

if __name__ == "__main__":
    import doctest
    doctest.testmod()


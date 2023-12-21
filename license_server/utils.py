import secrets

def generate_random_sequence(length=32):
    """
    Generate a random sequence.

    Parameters:
    - length (int): The length of the sequence (default is 32).

    Returns:
    - str: The generated sequence.
    """
    return secrets.token_hex(length // 2)
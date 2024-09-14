import operator
from functools import reduce


def compute_checksum(sentence: str) -> str:
    """
    Calculates the checksum for an LC29H instruction string.

    This is the same as the NMEA checksum calculation.

    Args:
        sentence (str): The LC29H instruction string.

    Returns:
        str: The calculated checksum in hexadecimal format.
    """
    from functools import reduce
    import operator

    sentence = sentence.strip("$\n")
    checksum = reduce(operator.xor, (ord(s) for s in sentence), 0)
    return int(checksum).__format__("02X")


def validate_checksum(sentence: str) -> str:
    """
    Checks the validity of an LC29H string using its checksum.

    Args:
        sentence (str): The NMEA string to validate.

    Returns:
        str: The data part of the NMEA string if the checksum is valid.

    Raises:
        ValueError: If the NMEA data does not match its checksum.
    """
    sentence = sentence.strip("$\n")
    data, checksum = sentence.split("*", 1)
    calculated_checksum = int(compute_checksum(data), base=16)
    if int(checksum, base=16) == calculated_checksum:
        return data
    else:
        raise ValueError("The NMEA data does not match its checksum")

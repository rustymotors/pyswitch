def bin2hex(bin_str):
    return "".join(format(x, "02x") for x in bin_str)


def assert_enough_data(data_length: int, expected_length: int):
    if data_length < expected_length:
        raise ValueError(
            f"Expected at least {expected_length} bytes, got {data_length} bytes"
        )


def is_msb_set(byte):
    """
    Checks if the most significant bit (MSB) of the given byte is set.

    Parameters:
    - byte: An integer representing the byte to check.

    Returns:
    - A boolean value indicating whether the MSB is set (True) or not (False).
    """
    return byte & 0x80 == 0x80

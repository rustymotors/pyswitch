def bin2hex(bin_str):
    return "".join(format(x, "02x") for x in bin_str)

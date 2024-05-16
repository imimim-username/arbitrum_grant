# converts 256 bit signed in hex number to decimal, including negative hex numbers

def twos_complement(hex_value, bit_length=256):

    if hex_value[2] == 'f':
        # Convert hex number to binary string padded up to bit_length
        binary_value = bin(int(hex_value, 16))[2:].zfill(bit_length)

        # Convert binary string to decimal
        decimal_value = int(binary_value, 2)

        # Check if the number is negative and apply two's complement if necessary
        if binary_value[0] == '1':  # Checking the most significant bit (MSB)
            decimal_value -= 1 << bit_length

        return decimal_value

    else:
        return int(hex_value,16)


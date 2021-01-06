def is_valid_hex_code(input):
    if len(input) != 6:
        return False
    valid_chars = ['0', '1', '2', '3', '4', '5', '6',
                   '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    for char in input:
        if not char in valid_chars:
            return False
    return True


class color:
    r = 0
    b = 0
    g = 0

    def __init__(self, color_identifier):
        if type(color_identifier) is str:
            if is_valid_hex_code(color_identifier):
                self.r = int(color_identifier[0:2], base=16)
                self.g = int(color_identifier[2:4], base=16)
                self.b = int(color_identifier[4:6], base=16)
            else:
                raise ValueError(str(color_identifier) +
                                 " is not a valid hex code")
        elif type(color_identifier) is list:
            self.r = int(color_identifier[0] * 255)
            self.g = int(color_identifier[1] * 255)
            self.b = int(color_identifier[2] * 255)
        if self.r > 255 or self.g > 255 or self.b > 255:
            raise ValueError(
                "Invalid Input provided to color constructor: One or more values exceed 255")

    def get_hex(self):
        return '%02x%02x%02x' % (int(self.r), int(self.g), int(self.b))

    def get_rgb_255(self):
        return [self.r, self.g, self.b]

    def get_rgb_1(self):
        return [self.r / 255, self.g / 255, self.b / 255]

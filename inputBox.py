from cmu_112_graphics import *
import string
class InputBox(object):
    def __init__(self, name, defaultVal, coord):
        self.name = name
        self.coord = coord
        self.defaultVal = defaultVal
        self.value = defaultVal

    def set_name(self):
        self.name = name

    def get_name(self):
        return self.name

    def get_coord(self):
        return self.coord
    
    def set_coord(self, coord):
        self.coord = coord
    
    def set_defaultVal(self, defaultVal):
        self.defaultVal = defaultVal

    def get_defaultVal(self):
        return self.defaultVal

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value 

class RectButton(InputBox):
    def __init__(self, name, redirect, defaultVal, coord):
        super().__init__(name, defaultVal, coord)
        self.redirect = redirect

    def get_redirect(self):
        return self.redirect 

class TextBox(InputBox):
    def __init__(self, name, defaultVal, coord, valid_characters):
        super().__init__(name, defaultVal, coord)
        self.valid_characters = valid_characters

    def set_valid_characters(self, characters):
        self.valid_characters = characters
    
    def get_valid_characters(self):
        return self.valid_characters

class NumTextBox(TextBox):
    def __init__(self, name, defaultVal, coord):
        super().__init__(name, defaultVal, coord, string.digits)

    def set_value(self, value):
        try:
            value = int(value)
            self.value = value
        except:
            self.value = 0

    def get_value(self):
        return int(self.value)
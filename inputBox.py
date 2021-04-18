from cmu_112_graphics import *

class InputBox(object):
    def __init__(self, name, coord):
        self.name = name
        self.coord = coord

    def set_name(self):
        self.name = name

    def get_name(self):
        return self.name

    def get_coord(self):
        return self.coord
    
    def set_coord(self, coord):
        self.coord = coord

class RectButton(InputBox):
    def __init__(self, name, redirect, coord):
        super().__init__(name, coord)
        self.redirect = redirect

    def on_redirect(self):
        return self.redirect 

class TextBox(InputBox):
    def __init__(self, name, coord, defaultVal):
        super().__init__(name, coord)
        self.defaultVal = defaultVal
        self.value = defaultVal

    def set_defaultVal(self, defaultVal):
        self.defaultVal = defaultVal

    def get_defaultVal(self):
        return self.defaultVal

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value 
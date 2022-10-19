#Library containing debugging features, such as different types of exceptions

#When errors are present in a layout file
class LayoutError(Exception):
    pass

class PresetError(Exception):
    pass
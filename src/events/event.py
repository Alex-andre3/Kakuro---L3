class Event:

    def __init__(self, coord=[]):
        self._coord = coord

    def get_coord(self):
        return self._coord

    def set_coord(self, coord):
        self._coord = coord

    coord = property(fget=get_coord, fset=set_coord)

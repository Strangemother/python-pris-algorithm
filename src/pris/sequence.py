"""
s = Sequence('window', 'w', 'i', 'n', 'd', 'o', 'w'), # Args
s = Sequence(name='window', path=('w', 'i', 'n', 'd', 'o', 'w')), # kwrgs
s = Sequence('window') # only args
s = Sequence(path='window') # only kwarg path
"""

class Path(tuple):

    def __new__ (cls, *a):
        # return super(Path, cls).__new__(cls, a)
        return super().__new__(cls, a)

    def __init__(self, *a):
        # print('Init', a)
        super().__init__()


class Sequence(object):
    """
        Sequence('window')
        Sequence(path='window')
        Sequence('window', Path('w', 'i', 'n', 'd', 'o', 'w'))
        Sequence(name='window', path=('w', 'i', 'n', 'd', 'o', 'w'))
        Sequence('w', 'i', 'n', 'd', 'o', 'w', name='window')
    """
    def __init__(self, iterable=None, *extras, name=None, path=None):
        rname, rpath = self.construct(iterable, *extras, name=name, path=path)
        self.path = rpath
        self.name = rname

    def __getitem__(self, item):
        return self.path[item]

    def __len__(self):
        return len(self.path)

    def construct(self, iterable=None, *extras, name=None, path=None):
        args = iterable
        has_extra = len(extras) > 0
        if has_extra:
            args = (iterable, ) + extras
            iterable = (iterable, ) + extras

        if path is None:
            # reverse unpack args
            path = args
            am1 = args[-1]
            if type(am1) is Path:
                path = am1
                name = args[0]

        rpath = Path(*path)

        if name is None:
            name = args or path

        return name, rpath

    def __iter__(self):
        return iter(self.path)

    def stringify(self, path):
        return str(path)

    def __str__(self):
        return self.name

    def __repr__(self):
        c = self.__class__.__name__
        return f'<{c} "{self.name}">'
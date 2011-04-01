from contextlib import contextmanager

from ..image import Image
from . import Rect, PackedBoxes, print_packed_size

class SpriteNode(Rect):
    def __init__(self, im, width, height, fname=None, pad=(0, 0)):
        Rect.__init__(self, (0, 0, width, height))
        self.im = im
        self.fname = fname
        (self.pad_x, self.pad_y) = pad
        self.close = im.close

    def __str__(self):
        clsnam = type(self).__name__
        arg = self.fname if self.fname else self.im
        args = (clsnam, arg, self.width, self.height)
        return "<%s %s (%dx%d)>" % args

    def calc_box(self, pos):
        x1, y1 = pos
        return (x1, y1, x1 + self.width, y1 + self.height)

    @classmethod
    def from_image(cls, im, *args, **kwds):
        args = im.size + args
        return cls(im, *args, **kwds)

    @classmethod
    def load_file(cls, fo, fname=None, pad=(0, 0), **kwds):
        if not hasattr(fo, "read"):
            if not fname:
                fname = fo
            fo = open(fo, "rb")
        elif not fname and hasattr(fo, "name"):
            fname = fo.name
        return cls.from_image(Image.load(fo), fname=fname, pad=pad)

@contextmanager
def open_sprites(fnames, **kwds):
    fs = [(fn, open(fn, "rb")) for fn in fnames]
    try:
        yield [SpriteNode.load_file(fo, fname=fn, **kwds) for (fn, fo) in fs]
    finally:
        for fn, fo in fs:
            fo.close()

def _load_input(fp, conf=None):
    import sys
    import json
    from .. import SpriteMap

    # TODO Set padding from configuration
    pad = (1, 1)

    for (smap_fn, sprite_fns) in json.load(fp):
        print >>sys.stderr, "packing sprites for map", smap_fn
        with open_sprites(sprite_fns, pad=pad) as sprites:
            smap = SpriteMap(smap_fn, sprites)
            packed = PackedBoxes(smap)
            print_packed_size(packed, out=sys.stderr)
            import pprint
            pprint.pprint(packed.save(None))

if __name__ == "__main__":
    import sys
    with open(sys.argv[1], "rb") as fp:
        _load_input(fp)

from collections import namedtuple

class Point(namedtuple('BasePoint', ['x', 'y'])):
    """Point in two-dimenstional space.

    Represents a point in two-dimensional space with offsets on the 'x'
    (horizontal) and 'y' (vertical) planes.
    """

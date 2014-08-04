# Author: Ryan Stuart <ryan@kapiche.com>
"""
Realisers are used to convert a ``Graph`` instance into text. It does this via Jinja2  templates. If you just want a
long english description then you want the ``english()`` function. Otherwise, there is support for a number of languages
via concrete implementations of the ``Realise`` class (see ``English`` or ``Spanish`` for example). The class approach
can also generate short descriptions.

If you use the realiser classes directly then you will probably be interested in ``short_description()`` and
``long_description()`` methods.

"""


def english(graph):
    """
    Shortcut for:

        r = English(graph)
        return r.long_description()

    """
    r = Realiser(graph)
    return r.long_description()


class Realiser(object):
    """
    Abstract class for turning a ``Graph`` into text.

    An implementer needs to implement ``long_description()`` and ``short_description()``.

    """
    def __init__(self, graph):
        """
        Default implementation of ``__init__()`` that saves the ``graph`` instance.

        :param graph: The ``Graph`` instance
        """
        self._graph = graph

    def long_description(self):
        """Return a str long description."""
        raise NotImplementedError()

    def short_description(self):
        """Return a str short description."""
        raise NotImplementedError()


class English(Realiser):
    """An English realiser implemented using Jinja2."""
    def long_description(self):
        """Returns the str long description using ``templates/en/long.txt``."""
        pass

    def short_description(self):
        """Returns the str short description using ``templates/en/short.txt``."""
        pass


class Spanish(Realiser):
    """An Spanish realiser that just uses a translation service on the output of the ``English`` realiser."""
    def long_description(self):
        pass

    def short_description(self):
        pass

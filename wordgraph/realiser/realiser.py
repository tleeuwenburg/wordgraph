# Copyright 2014 Tennessee Leeuwenburg

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# Author: Ryan Stuart <ryan.stuart.85@gmail.com>
"""
Realisers are used to convert a structured dict instance (created via
``Graph.as_dict()`` into text. It does this via Jinja2  templates. If you just
want a long english description then you want the ``english()`` function.
Otherwise, there is support for a number of languages via concrete
implementations of the ``Realiser`` class (see ``English`` or ``Spanish`` for
example). The class approach can also generate short descriptions.

If you use the realiser classes directly then you will probably be interested in
``short()`` and ``long()`` methods.

"""
from jinja2 import Environment, PackageLoader
import num2words

env = Environment(loader=PackageLoader('wordgraph.realiser', 'templates'))


def num_to_word(data):
    number = int(data)
    return num2words(number, ordinal=True)
env.filters['num_to_word'] = num_to_word


def english(graph):
    """
    Shortcut for:

        r = English(graph)
        return r.long()

    """
    r = English(graph)
    return r.long()


class Realiser(object):
    """
    Abstract class for turning a ``Graph`` into text.

    An implementer needs to implement ``long()`` and
    ``short()``.

    """
    def __init__(self, data):
        self._data = {}
        for k, v in data.items():
            if v != None:
                self._data[k] = v

    @property
    def data(self):
        return self._data

    def long(self):
        """Return a str long description."""
        raise NotImplementedError()

    def short(self):
        """Return a str short description."""
        raise NotImplementedError()


class English(Realiser):
    """
    An English realiser implemented using Jinja2.


    """
    def _single_data_series_with_one_point(self, data):
        for i, item in enumerate(data['series']):
            if item['num_values'] > 1 or i > 0:
                return False
        return True

    def long(self):
        """
        Returns the str long description using one of the
        ``templates/en/long-*.txt`` templates.
        """
        data = self._data
        if 'name' in data and data['name'] == "Unprocessable":
            return "Graph invalid, because %s" % data["result"]
        elif self._single_data_series_with_one_point(data):
            # If there's only one series and it consists of a single point, skip the part where we explain what the range of the data is, as it's meaningless. 
            template = env.get_template("en/long/single-point.txt")
        else:
            # But if there's more than one series, suddenly the range etc becomes relevant again, even if one of the series consists of a single data point.
            template = env.get_template("en/long/desc.txt")
        return template.render(data)

    def short(self):
        """
        Returns the str short description using one of the
        ``templates/en/short-*.txt`` templates.
        """

        data = self._data
        if 'name' in data and data['name'] == "Unprocessable":
            return "Graph may be invalid, because %s" % data["result"]
        elif self._single_data_series_with_one_point(data):
            template = env.get_template("en/short/single-point.txt")
        else:
            template = env.get_template("en/short/desc.txt")
        return template.render(data)


class Spanish(Realiser):
    """
    An Spanish realiser that just uses a translation service on the output
    of the ``English`` realiser.
    """
    def long(self):
        pass

    def short(self):
        pass

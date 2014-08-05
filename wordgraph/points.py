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

'''
This module just contains a simple class for representing cartesian points. 

It contains the Point class, and even that is just a named tuple!
'''


from collections import namedtuple

class Point(namedtuple('BasePoint', ['x', 'y'])):
    """Point in two-dimenstional space.

    Represents a point in two-dimensional space with offsets on the 'x'
    (horizontal) and 'y' (vertical) planes.
    """

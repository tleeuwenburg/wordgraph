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

import wordgraph
import py



@py.test.mark.xfail
def test_basic_matplotlib():

    """
    Based on the demo at: http://matplotlib.org/examples/lines_bars_and_markers/barh_demo.html
    Viewed on 4 August 2014

    Simple demo of a horizontal bar chart.
    """
    import matplotlib.pyplot as plt; plt.rcdefaults()
    import numpy as np
    import matplotlib.pyplot as plt

    # Example data
    people = ('Tom', 'Dick', 'Harry', 'Slim', 'Jim')
    y_pos = np.arange(len(people))
    performance = 3 + 10 * np.random.rand(len(people))
    error = np.random.rand(len(people))

    plt.barh(y_pos, performance, xerr=error, align='center', alpha=0.4)
    plt.yticks(y_pos, people)
    plt.xlabel('Performance')
    plt.title('How fast do you want to go today?')

    text = wordgraph.describe(plt, source='matplotlib')
    assert text is not None
    

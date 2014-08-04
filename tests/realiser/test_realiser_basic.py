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

import realiser_cases

def test_basic_realiser():
    
    input_case = realiser_cases.no_data_case

    short_description_expected = input_case.title
    long_description_expected = ''
    structured_parts_expected = {}

    r = realiser.English(input_case)

    assert r.short() == short_description_expected
    assert r.long() == long_description_expected
    assert r.parts() == structured_parts_expected

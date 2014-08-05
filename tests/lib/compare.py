import pprint

def assertDictionary(found, expected):
    
    found_keys = sorted(list(found.keys()))
    expected_keys = sorted(list(expected.keys()))

    if found == expected:
        return

    for found_key, expected_key in zip(found_keys, expected_keys):
        assert found_key == expected_key

    print("All top-level keys match between the two dictionaries")

    for found_key, expected_key in zip(found_keys, expected_keys):
        found_value = found[found_key]
        expected_value = expected[expected_key]


        assert found_value == expected_value, \
            'Mismatch between values for %s and %s . %s %s ' % \
            (found_key, expected_key, pprint.pformat(found), pprint.pformat(expected))
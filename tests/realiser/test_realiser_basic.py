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

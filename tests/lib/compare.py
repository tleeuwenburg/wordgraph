import pprint


def splitIntoSentences(para, ignore_empty_lines=True):

    lines = [p for p in para.split('\n') if p != '']



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


def assertParagraph(found, expected, strict=False):

    if found == expected:
        return

    msg = ''

    msg += "The two paragraphs are not strictly identical"

    found_sents = found.split('. ')
    expected_sents = expected.split('. ')

    # Ignore whitespaces and just compare sentences
    for f, e in zip(found_sents, expected_sents):
        f = f.strip()
        e = e.strip()
        if f == e:
            msg += '\nOK\t%s' % f
        else:
            msg += "\nBAD\t%s \nmismatch with \n\t%s" % (f, e)
            badly_broken = True

    msg += "\nFound >> [%s]" % (found)
    msg += "\nExpected >> [%s]" % (expected)

    if badly_broken:
        msg = "STATUS: Badly broken\n" + msg

    if strict or badly_broken:
        assert False, msg   

import pprint

'''
Wordgraph relies on some complex data type comparisons, in particular
  -- Nested dictionaries
  -- Paragraphs (or slightly longer) of English test

This module supports the intelligent comparison of these object types, together
with useful error analysis which is more useful than simple equality. The first
check in each comparison is straightforward equality. The rest of each comparison
consists of a more complex unpacking of the error.

Key methods:

assertDictionary: compare two medium-sized dicts
assertParagraph: compare two paragraphs of natural language (can contain newlines).
'''


def splitIntoSentences(para, ignore_empty_lines=True):
    '''
    Relatively simply approach to English sentence tokenising. A fuller approach
    might use NLTK, but we are only dealing with the sentences actually produced
    by wordgraph, which is fairly formulaic.

    This method will split sentences based on newlines and full-stop-followed-by-space.
    The returned sentences will contain the final punctuation mark, but not newlines.

    The results are returned as a list of strings.
    '''

    lines = [p for p in para.split('\n') if p != '']
    sents = []

    for line in lines:

        if ignore_empty_lines and not line:
            continue

        line_sents = [s for s in line.split('. ') if s != '']
        
        for s in line_sents:
            s = s.strip()
            if not s:
                continue
            if s[-1] != '.':
                s += '.'
            sents.append(s)

    return sents



def assertDictionary(found, expected):
    '''
    Assert that two dictionaries are the same. The comparison is strict,
    but in the event of failure, some additional descriptive messages 
    will be printed.

    If the dictionaries are equal, succeed. Otherwise, fail with a message.

    If the top-level keys are the same, print that as a message.
    If the values are different, print the keys associated with the mismatch.

    Pretty-format the two dictionaries for easy visual inspection.
    '''
    
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
                'Mismatch between values for %s and %s . Found is:\n %s\n\nExpected is:\n %s ' % \
            (found_key, expected_key, pprint.pformat(found), pprint.pformat(expected))


def assertParagraph(found, expected, strict=False):
    '''
    This method compares two chunks of English text, potentially including newlines. If "strict"
    mode is selected, then any difference at all will result in test failure. Otherwise,
    only the individual sentences must match (whitespace and newlines may vary).

    The message "STATUS: Badly broken" will be included if the sentences differ, the message
    will be omitted if only whitespace varies.

    The diagnotistic information printed should be quited useful. Matching lines are printed as "OK"
    while mismatching lines are printed together, clearly indicating which is which.
    '''

    if found == expected:
        return

    msg = ''

    msg += "The two paragraphs are not strictly identical"

    found_sents = splitIntoSentences(found)
    expected_sents = splitIntoSentences(expected)

    # Ignore whitespaces and just compare sentences
    badly_broken = False
    for f, e in zip(found_sents, expected_sents):
        f = f.strip()
        e = e.strip()
        if f == e:
            msg += '\nOK\t%s' % f
        else:
            msg += "\nFOUND\t%s \nmismatch with \nEXPECTED\t%s" % (f, e)
            badly_broken = True

    msg += "\nFound >> [%s]" % (found)
    msg += "\nExpected >> [%s]" % (expected)

    if badly_broken:
        msg = "STATUS: Badly broken\n" + msg

    if strict or badly_broken:
        assert False, msg   

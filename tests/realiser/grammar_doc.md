
LINEAR_GRAMMARS:

basic_linear_grammar_long = 
"This graph, <title>, shows the relationship between <xname> and <yname>. It contains n series. <The first> series describes <seried_name> . The data is <broadly> linear. It has a value of <blah> <at first>, and <increased/descreases> <fast/slowly> until reaching <blah> <at point> <blah>"

basic_linear_grammar_short_single: n_series == 1, = 
"
<title> shows the relationship between <name> and <yname>. . The data is broadly linear. The minimum is <value> at <point>. The maximum is <value> at <point>.
"

basic_linear_grammar_short_multi: n_series >1,  = 
"
<title> shows the relationship between <name> and <yname>. It contains n series. The data is broadly linear. [The minimum of <series_name>. is <value> at <point> and the maximum is <value> at <point>.]+
"


basic_linear_example =
"This graph, the Height of people in Brisbane, shows the relationship between height in metres and calendar year. It contains one series. This series describes average height. The data is broadly flat. It has a value of 1.4m in 1985, and increases slightly to 1.5m in 2014."


NORMAL_GRAMMARS:


RANDOM_GRAMMARS:

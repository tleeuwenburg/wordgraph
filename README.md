This is a thing that supports creating English-language text from a graph description. 

WHY
===

This project is intended to support anyone who is doing screen reading for any reason. This could be for vision-impaired people, or just people who like to listen to graphs while jogging, or just to get a handle on what's going on.

WHO
===

Kate Cunningham gave an amazing keynote at PyCon AU. Someone came up with the idea that graphs were a problem, and that maybe it would be possible to come up with a language description for those who wanted to understand the information, but couldn't see the graph.

ARCHITECTURE
============

A core library takes an abstract graph description and produces English-language text.

TODO:
  -- Create unit tests with example graph descriptions
  -- Support basic linear graphs
  -- Support scatter plots maybe
  -- Look at using some kind of auto-translate to support internationalisation
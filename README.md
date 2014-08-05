This is a thing that supports creating English-language text from a graph description. 
============

Why
---

This project is intended to support anyone who is doing screen reading for any reason. This could be for vision-impaired people, or just people who like to listen to graphs while jogging, or just to get a handle on what's going on. Could potentially be used for generic data description also.

Kate Cunningham gave an amazing keynote at PyCon AU. Someone came up with the idea that graphs were a problem, and that maybe it would be possible to come up with a language description for those who wanted to understand the information, but couldn't see the graph.

Who
---
Maintainer: Tennessee Leeuwenburg @tleeuwenburg

Code Contributors (in order of first contribution):

1. Tennessee Leeuwenburg
2. Aaron Iles
3. Nick Farrel
4. Ryan Stuart



Architecture
------------

A core library takes an abstract graph description and produces English-language text. 

The basic usage is:

	> import wordgraph
	> text = wordgraph.describe(data, source_type)

For further reading, please checkout wordgraph.readthedocs.org

Setup with Vagrant
------------------

If you have [vagrant](www.vagrantup.com) installed, you can just run `vagrant
up`. By default the base Ubuntu 14.04 box is used; change it in `Vagrantfile`
if you want to use a different box.

```bash
$ vagrant up
$ vagrant ssh
```

You'll now be logged into a machine with all the dependencies and wordgraph
installed in the system python:

```bash
$ python3
> import wordgraph
>
```

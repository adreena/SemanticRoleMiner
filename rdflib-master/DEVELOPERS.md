Continous Integration
---------------------

A Shining Panda instance for continuous integration and 
testing of RDFLib and RDFExtras is at: 

https://jenkins.shiningpanda.com/rdflib/

Compatibility
-------------

RDFLib 3.2.X tries to be compatible with python versions 2.4 - 3

Some of the limitations we've come across:

 * no collections.defaultdict => a fall-back implementation is in rdflib/compat, import this instead
 * no 'yield' without arguments => use 'yield None' instead
 * no ternary if (no X if A else B) => rewrite with normal if
 * no context handlers, i.e. not 'with file('blah'): ' => rewrite
 * No skipping tests using unittest, i.e. TestCase.skipTest and decorators are missing => use nose instead

We may drop 2.4 compatability for rdflib 4.X, but for now try to make sure the tests pass under 2.4 !

Releasing
---------

Set to-be-released version number in *rdflib/__init__.py* , *docs/index.rst* and *docs/conf.py*

Add CHANGELOG entry.

Commit this change, and tag it with `git tag -a -m 'tagged version' X.X.X`

When pushing, remember to `git push --tags`

Do `python setup.py sdist upload` to upload tarball to pypi

Upload *dist/rdflib-X.X.X.tar.gz* to downloads section at Github

Set new dev version number in the above locations, i.e. next release *-dev*: *8.9.2-dev* and commit again. 








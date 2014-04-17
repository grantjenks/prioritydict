Priority Dict
=============

**WARNING:** This is a work in progress. Not everything stated here is true.

PriorityDict is an Apache2 licensed implementation of a dictionary which
maintains key-value pairs in value sort order.

Features
--------

- Pure-Python
- Fast (depends on sortedcontainers module)
- Fully documented
- 100% test coverage
- Hours of stress testing
- Feature-rich (e.g. get the five largest keys in a priority dict: d.iloc[-5:])
- Developed on Python 2.7
- Tested on Python 2.6, 2.7, 3.2, 3.3, and 3.4

Quickstart
----------

Installing PriorityDict is simple with
`pip <http://www.pip-installer.org/>`_::

    > pip install prioritydict

You can access documentation in the interpreter with Python's built-in help
function:

::

    >>> from prioritydict import PriorityDict
    >>> help(PriorityDict)

Documentation
-------------

Complete documentation including performance comparisons is available at
http://www.grantjenks.com/docs/prioritydict/ .

Contribute
----------

Collaborators are welcome!

#. Check for open issues or open a fresh issue to start a discussion around a
   bug.  There is a Contributor Friendly tag for issues that should be used by
   people who are not very familiar with the codebase yet.
#. Fork `the repository <https://github.com/grantjenks/prioritydict>`_ on
   GitHub and start making your changes to a new branch.
#. Write a test which shows that the bug was fixed.
#. Send a pull request and bug the maintainer until it gets merged and
   published. :)

Useful Links
------------

- `PriorityDict Project @ GrantJenks.com`_
- `PriorityDict @ PyPI`_
- `PriorityDict @ Github`_
- `Issue Tracker`_

.. _`PriorityDict Project @ GrantJenks.com`: http://www.grantjenks.com/docs/prioritydict/
.. _`PriorityDict @ PyPI`: https://pypi.python.org/pypi/prioritydict
.. _`PriorityDict @ Github`: https://github.com/grantjenks/prioritydict
.. _`Issue Tracker`: https://github.com/grantjenks/prioritydict/issues

PriorityDict License
------------------------

Copyright 2014 Grant Jenks

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

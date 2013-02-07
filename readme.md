soUPerfind
==========

UPCAT results crawler using Python and BeautifulSoup.

Usage
-----
Simply run **python souperfind.py** and enter search query. Query may be a partial of the student's name, student id, campus, or degree program.

Requirements
------------
soUPerfind requires _Python 2.7_ with the _BeautifulSoup_ module installed. For instructions on installing BeautifulSoup, you may visit [BeautifulSoup's homepage](http://www.crummy.com/software/BeautifulSoup/#Download).

Notes
-----
- Due to a required Python module being named differently in Python 2.7 and 3+, soUPerfind only supports Python 2.7 for now.
- While soUPerfind utilizes multiple threads to do a linear search for your query, the general speed still relies on your internet connection speed: faster internet means faster search results.

Changelog:
----------
- v0.2: Added html generation for results, and opens your default web browser
- v0.1: First release
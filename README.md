 
# Groppy 

[![Python Versions](https://github.com/H4NM/Groppy/blob/main/img/pyversion.svg)](https://docs.python.org/3/howto/regex.html)
[![Packages](https://github.com/H4NM/Groppy/blob/main/img/packages.svg)](https://pypi.org/)
![License](https://github.com/H4NM/Groppy/blob/main/img/license.svg)

A desktop application written purely in python using [customtkinter](https://customtkinter.tomschimansky.com/) and [tksheet](https://github.com/ragardner/tksheet) (+ [pillow](https://pypi.org/project/Pillow/) and [requests](https://pypi.org/project/requests/)). Requires python 3.11 to be able to perform ![atomic grouping and possessive quantifiers](https://learnbyexample.github.io/python-regex-possessive-quantifier/). This application is meant to address the challenges of creating regex patterns and utilizing them efficiently with grok patterns. From my personal experience, creating the grok patterns is one thing, but realizing the already existing patterns is overlooked, whereas you may find an person creating the same regex pattern for a signature that may already be applicable. 

## Features

- Create and test regex
- Load local files such as log filesregex matching (Filters for unique rows)
- Load local grok patterns 
- Save created regex pattern to grok patterns file
- Test loaded or created grok patterns against data to get statistics on grok pattern applicabiltiy and efficiency
- Filter grok patterns to only test a selected group or instances
- Query data from an elasticsearch cluster. Support selecting a field to retrieve data from, create a query (e.g. tags: "_grokparsefailure"), HTTP Basic auth, API-Token.
- Dark and Light mode
  
### Light Mode
![user interface - Light Mode](https://github.com/H4NM/Groppy/blob/main/img/user_interface.png)

### Dark Mode
![user interface - Light Mode](https://github.com/H4NM/Groppy/blob/main/img/user_interface_dark.png)
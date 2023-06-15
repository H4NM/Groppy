 
# Groppy 

[![Python Versions](https://github.com/H4NM/Groppy/blob/main/img/pyversion.svg)](https://docs.python.org/3/howto/regex.html)
[![Packages](https://github.com/H4NM/Groppy/blob/main/img/packages.svg)](https://pypi.org/)
![License](https://github.com/H4NM/Groppy/blob/main/img/license.svg)

A desktop application written purely in python using [customtkinter](https://customtkinter.tomschimansky.com/) and [tksheet](https://github.com/ragardner/tksheet) (+ [pillow](https://pypi.org/project/Pillow/) and [requests](https://pypi.org/project/requests/)). Requires python 3.11 to be able to perform ![atomic grouping and possessive quantifiers](https://learnbyexample.github.io/python-regex-possessive-quantifier/). This application is meant to address the challenges of creating regex patterns and utilizing them efficiently with grok patterns. From my personal experience, creating the grok patterns is one thing, but realizing the already existing patterns is overlooked, whereas you may find an person creating the same regex pattern for a signature that may already be applicable. 

## Features

- Create and test regex
- Query data from an elasticsearch REST API. 
  - Select a field to retrieve data from, create a query (e.g. tags: "_grokparsefailure")
  - Auto discovers available indices and fields 
  - HTTP Basic auth, API-Token, SSL Cert
- Load local text files 
  - Filter to load unique rows
- Load local grok patterns 
- Test grok patterns to see how applicable they are
  - Tests every pattern towards every row 
  - Filter which grok patterns that should be tested (include/exclude) 
- Export grok patterns
- Dark and Light mode
  
### Light Mode
![user interface - Light Mode](https://github.com/H4NM/Groppy/blob/main/img/user_interface.png)

### Dark Mode
![user interface - Light Mode](https://github.com/H4NM/Groppy/blob/main/img/user_interface_dark.png)
<<<<<<< HEAD


#### Pending progress 2023-06-15

- Simplifying left sidebar by separating local file inclusions and elasticsearch data retrieval
- Adding the feature of loading a json file and enabling a similar field retrieval as for the query of field data from elasticsearch. i.e. you'll be able to specify which key from where data will be read from one or multiple json objects directly from a file.

#### Desired features

- Adding a config file where color schemas and other settings may be specified and loaded on application start.
=======
>>>>>>> 2920d8778aa9780538d7005b3995f2439b9020e6

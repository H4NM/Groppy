 
# Groppy 

[![Python Versions](https://github.com/H4NM/Groppy/blob/main/badges/pyversion.svg)](https://docs.python.org/3/howto/regex.html)
![Groppy version](https://github.com/H4NM/Groppy/blob/main/badges/groppyversion.svg)
[![Packages](https://github.com/H4NM/Groppy/blob/main/badges/packages.svg)](https://pypi.org/)
![License](https://github.com/H4NM/Groppy/blob/main/badges/license.svg)

A desktop application written purely in python using [customtkinter](https://customtkinter.tomschimansky.com/) and [tksheet](https://github.com/ragardner/tksheet) (and [requests](https://pypi.org/project/requests/)). This application is the ideal friend of someone who wants to create regex patterns. The application facilitates managing grok patterns, reading JSON-files and parsing fields in an ELK environment. 

### Details
The primary focus of this application was to facilitate working with regex. Although, i wrote this program with focus on minmal dependency on other libraries to make version control and code transparency better. This resulted in customtkinter, tksheet, requests, json, re and os being the main utilized libraries - all well known and trusted. Less is more.
The application requires python 3.11+ in order to perform [atomic grouping and possessive quantifiers](https://learnbyexample.github.io/python-regex-possessive-quantifier/). However, if no such regex is being used, the application can still be utilized given that included libraries support a lower version.


##  Features

- Create and test regex
- Query data from an elasticsearch REST API. 
  - Select a field to retrieve data from, create a query (e.g. tags: "_grokparsefailure")
  - Auto discovers available indices and fields 
  - HTTP Basic auth, API-Token, SSL Cert
- Load local text files 
  - Filter to load unique rows
- Load local grok patterns
- Load local JSON file
  - Specify which key to retrieve data from 
- Test grok patterns to see how applicable they are
  - Tests every pattern towards every row 
  - Filter which grok patterns that should be tested (include/exclude) 
- Export grok patterns
- Multiple different themes
  - Blue, Dark-Blue, DaynNight, FlipperZero, GhostTrain, Green, Greengage, GreyGhost, Hades, Harlequin, NightTrain, Oceanix, TestCard, TrojanBlue, Yellow 
- Dark and Light mode
- Configuration file to save settings such as mode, theme, elasticsearch details

## Themes

#### TrojanBlue
![TrojanBlue](https://github.com/H4NM/Groppy/blob/main/img/theme-7.png)

##### Hades
![Hades](https://github.com/H4NM/Groppy/blob/main/img/theme-1.png)

##### GhostTrain
![GhostTrain](https://github.com/H4NM/Groppy/blob/main/img/theme-5.png)

##### FlipperZero
![FlipperZero](https://github.com/H4NM/Groppy/blob/main/img/theme-2.png)

##### Greengage
![Greengage](https://github.com/H4NM/Groppy/blob/main/img/theme-6.png)

## Settings file

A file called settings.json will be created on first launch with the following settings that may be altered which are loaded upon start.
```
{
    "mode": "Light",
    "theme": "GhostTrain",
    "elastic_host": "localhost",
    "elastic_port": "9200",
    "elastic_auth": false,
    "elastic_user": "",
    "elastic_api_key_is_used": true,
    "elastic_api_key_value": "UmVnZXhpbmcgaXMgZnVuIQ==",
    "elastic_cert_is_used": false,
    "elastic_cert_path": ""
}
```

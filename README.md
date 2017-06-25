# Menu planning

## Overview
Menu planning API is an API for generating random menus using your common starters, lunches and dinners

## Requirements
* Python >= 3.3
* MySQL >= 5.6.5

## Install
* pip install -r requirements.txt

## How to use
* Create a env.json file with the following structure in the root directory

```json
{
  "mysql": {
    "database": "xxxx",
    "host": "xxxx",
    "user": "xxxx",
    "password": "xxxx",
    "charset": "xxxx"
  }
}
```

* Export variable FLASK_APP

```shell
export FLASK_APP=runserver.py
```

* Import migrations

```shell
flask db upgrade
```

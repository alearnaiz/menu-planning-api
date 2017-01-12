# Menu planning

## Overview
Menu planning API is an API for generating random menu using your common starters, lunches and dinners.

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

* Create the initial database. Import the db object from an interactive Python shell in the root directory to create the tables and database

```python
from menu_planning import db
db.create_all()
```

# Menu planning

## Overview
Menu planning is a random generator menu using your common starters, lunches and dinners

## Requirements
* Python 2.7
* MySQL >= 5.6.5

## Install
* pip install -r requirements.txt

## How to use
* Create a env.json file with the following structure in the root directory

```json
{
  "database": "xxxx",
  "host": "xxxx",
  "user": "xxxx",
  "password": "xxxx",
  "charset": "xxxx"
}
```

* Create the initial database. Import the db object from an interactive Python shell in the root directory to create the tables and database

```python
from menu_planning import db
db.create_all()
```

* Insert rows in starter, lunch and dinner tables

```sql
INSERT INTO starter (id, name) VALUES (1, 'Salmorejo/Gazpacho');
INSERT INTO dinner(id, name, days) VALUES (1, 'Sandwich de pollo', 1);
INSERT INTO lunch (id, name, days, need_starter, related_dinner_id) VALUES (1, 'Pollo asado', 1, true, 1);
```

* In the root directory run **python runserver.py**

* Open a browser with the URL http://127.0.0.1:5000/

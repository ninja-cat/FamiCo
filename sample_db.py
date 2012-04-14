#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from datetime import datetime
from uuid import uuid4


def get_id():
    return str(uuid4())
db = {}

id = get_id()
cart = {}

cart["s_name"] = "contra"
cart["o_name"] = "魂斗羅"
cart["e_name"] = "contra"
cart["group"] = "konami"
cart["ts"] = str(datetime.now().isoformat())
cart["cat"] = "RC826"
cart["img"] = ""

db[id] = cart

id = get_id()
cart = {}

cart["s_name"] = "super contra"
cart["o_name"] = "Super 魂斗羅"
cart["e_name"] = "super contra"
cart["group"] = "konami"
cart["ts"] = str(datetime.now().isoformat())
cart["cat"] = "KDS-UE"
cart["img"] = ""

db[id] = cart

id = get_id()
cart = {}

cart["s_name"] = "dead fox"
cart["o_name"] = "デッドフォックス"
cart["e_name"] = "dead fox"
cart["group"] = "capcom"
cart["ts"] = str(datetime.now().isoformat())
cart["cat"] = "CAP-VP"
cart["img"] = ""

db[id] = cart

id = get_id()
cart = {}

cart["s_name"] = "pizza pop!"
cart["o_name"] = "ピザポップ"
cart["e_name"] = "pizza pop!"
cart["group"] = "jaleco"
cart["ts"] = str(datetime.now().isoformat())
cart["cat"] = "JF-35"
cart["img"] = ""

db[id] = cart

print json.dumps(db)

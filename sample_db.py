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

cart["short_title"] = "contra"
cart["original_title"] = "魂斗羅"
cart["english_title"] = "contra"
cart["group"] = "konami"
cart["timestamp"] = str(datetime.now().isoformat())
cart["catalog_id"] = "RC826"
cart["img"] = ""

db[id] = cart

id = get_id()
cart = {}

cart["short_title"] = "super contra"
cart["original_title"] = "Super 魂斗羅"
cart["english_title"] = "super contra"
cart["group"] = "konami"
cart["timestamp"] = str(datetime.now().isoformat())
cart["catalog_id"] = "KDS-UE"
cart["img"] = ""

db[id] = cart

id = get_id()
cart = {}

cart["short_title"] = "dead fox"
cart["original_title"] = "デッドフォックス"
cart["english_title"] = "dead fox"
cart["group"] = "capcom"
cart["timestamp"] = str(datetime.now().isoformat())
cart["catalog_id"] = "CAP-VP"
cart["img"] = ""

db[id] = cart

id = get_id()
cart = {}

cart["short_title"] = "pizza pop!"
cart["original_title"] = "ピザポップ"
cart["english_title"] = "pizza pop!"
cart["group"] = "jaleco"
cart["timestamp"] = str(datetime.now().isoformat())
cart["catalog_id"] = "JF-35"
cart["img"] = ""

db[id] = cart

print json.dumps(db)

#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import csv
from datetime import datetime
from uuid import uuid4
import re

def get_id():
    return str(uuid4())

db = {}

csv_db = csv.reader(open('total.csv', 'rb'), delimiter=',', quotechar='"')


def load_famicomworld_db(fname):
    csv_db = csv.reader(open(fname, "rb"), delimiter=',', quotechar='"')
    fami_db = []
    for x in csv_db:
        fami_db.append(x)            
    return fami_db


def correct_dates_in_fami_db(fami_db):
    new_fami_db = []
    for x in range(len(fami_db)):
        row = fami_db[x]
        if "\xc2\xa0" == row[1]:
            row[1] = ""
        if "\xc2\xa0" == row[2]:
            row[2] = ""
        elif 3 == len(row[2].strip().replace('.','/').split('/')):
            month, day, year = row[2].strip().replace('.','/').split('/')
            if 2 == len(year):
                year = "19" + year
            row[2] = "/".join((day, month, year))
        if 1 < len(row[1].split(',')):
            id1, id2 = [ss.strip() for ss in row[1].split(',')]
            row1 = row
            row2 = row
            row1[1] = id1
            row2[1] = id2
            new_fami_db.append(row1)
            new_fami_db.append(row2)
        else:
            new_fami_db.append(row)
    return new_fami_db  

def search_for_release_date_and_publisher(fami_db, cart_id):
    if not cart_id:
        return {}
    for x in fami_db:
        if x[1] == cart_id:
            return {"name":x[0].strip(),
                     "released":x[2].strip(),
                     "publisher":x[3].strip()
                    }
    return {}     

def get_group_from_catalog_id(cat_id):
    if re.match("HFC-.*", cat_id):
        return "hudson soft"
    elif re.match("(KDS|RC|RV).*", cat_id):
        return "konami"
    elif re.match("BANDAI.*", cat_id):
        return "bandai"
    elif re.match("TAITO.*", cat_id):
        return "taito"
    elif re.match("CAP-.*", cat_id):
        return "capcom"
    elif re.match("HVC-.*", cat_id):
        return "nintendo"
    elif re.match("NAMCOT.*", cat_id):
        return "namco"
    elif re.match("JF-.*", cat_id):
        return "jaleco"
    elif re.match("TCF-.*", cat_id):
        return "tecmo"
    elif re.match("sunsoft.*", cat_id):
        return "sunsoft"
    elif re.match("SQF-.*", cat_id):
        return "square"
    elif re.match("TJC-.*", cat_id):
        return "technos"
    elif re.match("SFX-.*", cat_id):
        return "snk"
    return "other"

fami_db = load_famicomworld_db('famicomworld.csv')

fami_db = correct_dates_in_fami_db(fami_db)

for row in csv_db:
    cart = {}
    cart["catalog_id"] = row[3]
    cart["short_title"] = row[1]    
    cart["original_title"] = row[1]    
    cart["english_title"] = row[1]    
    #cart["timestamp"] = str(datetime.now().isoformat())
    cart["img"] = ""
    cart["group"] = get_group_from_catalog_id(cart["catalog_id"])
    entry = search_for_release_date_and_publisher(fami_db, cart["catalog_id"])
    if entry:
        if "released" in entry:
            cart["released"] = entry["released"]
        if "name" in entry:
            cart["english_title"] = entry["name"]
            cart["short_title"] = entry["name"]
        if "publisher" in entry:
            cart["publisher / developer"] = entry["publisher"]
    db[get_id()] = cart
    
print json.dumps(db)

#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import csv
from datetime import datetime
from uuid import uuid4
import re
import urllib

import lxml.html


def get_profile_id_at_bootgoddb(cart_id):
    url_path = "http://bootgod.dyndns.org:7777/search.php?"
    f = urllib.urlopen(url_path + urllib.urlencode({"keywords": cart_id, "kwtype": "game"}))
    html = f.read().replace('\n','').replace('\r','')

    m = re.match(".*(setTimeout\(\'window\.location=\"profile.php\?id=)(?P<profile_id>\d+)", html)
    if not m:
        return None
    else:
        return m.groupdict()['profile_id']


def get_all_info_from_profile(profile_id):
    f = urllib.urlopen("http://bootgod.dyndns.org:7777/profile.php?id=" + profile_id)
    cart_html = f.read().replace('\n','').replace('\r','').replace('\t','')
    for x in range(0, cart_html.count("<table >")):
        cart_html = cart_html.replace("<table >", "<table id=tid_%d" % (x + 1), 1)

    doc = lxml.html.document_fromstring(cart_html)


    def build_dict_from_list(li):
        if len(li) % 2:
            li = li[:-1]
        return dict((li[x].strip(),li[x+1].strip()) for x in xrange(0,len(li),2))


    pcb_info = build_dict_from_list(doc.xpath('//table[@id="tid_10"]//text()')[5:-1][0::2])
    general_info = build_dict_from_list(doc.xpath('//table[@id="tid_5"]//text()')[0::2][:-1])
    d = {}
    if len(doc.xpath('//td[@class="headingsubtitle"]/text()')):
        d['Original Title'] = doc.xpath('//td[@class="headingsubtitle"]/text()')[0].strip()
    if len(doc.xpath('//td[@class="headingmain"]/text()')):
        d['Romanized Title'] = doc.xpath('//td[@class="headingmain"]/text()')[0].strip()
    d['PCB Name'] = doc.xpath('//table[@id="tid_10"]//text()')[:1][0].strip()
    d.update(pcb_info)
    d.update(general_info)
    return d


def get_id():
    return str(uuid4())


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

def correct_date_bootgod(s):
    s = s.replace(',','').strip()
    month, day, year = s.split(' ')
    if re.match("Jan.*", month):
        month = "01"
    elif re.match("Feb.*", month):
        month = "02"
    elif re.match("Mar.*", month):
        month = "03"
    elif re.match("Apr.*", month):
        month = "04"
    elif re.match("May.*", month):
        month = "05"
    elif re.match("Jun.*", month):
        month = "06"
    elif re.match("Jul.*", month):
        month = "07"
    elif re.match("Aug.*", month):
        month = "08"
    elif re.match("Sep.*", month):
        month = "09"
    elif re.match("Oct.*", month):
        month = "10"
    elif re.match("Nov.*", month):
        month = "11"
    elif re.match("Dec.*", month):
        month = "12"

    return "/".join((day if len(day) > 1 else "0" + day, month, year))


if __name__ == "__main__":

    db = {}

    csv_db = csv.reader(open('total.csv', 'rb'), delimiter=',', quotechar='"')

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
        if cart["group"] in ("namco", "taito", "bandai", "sunsoft"):
            tmp = get_profile_id_at_bootgoddb(cart["original_title"])
        else:
            tmp = get_profile_id_at_bootgoddb(cart["catalog_id"])
        if tmp:
            entry = get_all_info_from_profile(tmp)
            if "Catalog ID" in entry:
                cart["catalog_id"] = entry['Catalog ID']
            if "Release Date" in entry:
                cart["released"] = correct_date_bootgod(entry["Release Date"])
            if "Original Title" in entry:
                cart["original_title"] = entry['Original Title']
            if "Romanized Title" in entry:
                cart["english_title"] = entry["Romanized Title"]
                cart["short_title"] = entry["Romanized Title"].split(':')[0].split('!')[0].strip()
            if "Publisher" in entry:
                cart["publisher"] = entry["Publisher"]
            if "Developer" in entry:
                cart["developer"] = entry["Developer"]
        else:
            entry = search_for_release_date_and_publisher(fami_db, cart["catalog_id"])
            if "released" in entry:
                cart["released"] = entry["released"]
            if "name" in entry:
                cart["english_title"] = entry["name"]
                cart["short_title"] = entry["name"].split(':')[0].split('!')[0].strip()
            if "publisher" in entry:
                cart["publisher"] = entry["publisher"]
        db[get_id()] = cart
        
    print json.dumps(db)

#!/usr/bin/python
# -*- coding: utf-8 -*-
import xapian
import sys
import string
from collections import defaultdict
from mmseg.search import seg_txt_search,seg_txt_2_dict

sys.path.append("..")

DBPATH = "/home/liyang/SearchDB"
SEARCH_DB = xapian.WritableDatabase(DBPATH,xapian.DB_CREATE_OR_OPEN)
SEARCH_ENQUIRE = xapian.Enquire(SEARCH_DB)

from models.database import session_connect,Task


def flush_db():
    SEARCH_DB.flush()

#建立索引：
def index_txt(tid,txt):
    doc = xapian.Document()
    for word,value in seg_txt_2_dict(txt).iteritems():
        if word:
            doc.add_term(word,value)
        else:
            pass
    key = ":%s"%str(tid)
    doc.add_term(key)
    print dir(doc)
    SEARCH_DB.replace_document(key,doc)

def search(keywords,offset=0,limit=35,enquire=SEARCH_ENQUIRE):
    query_list = []
    for word,value in seg_txt_2_dict(keywords).iteritems():
        print word
        query = xapian.Query(word,value)
        query_list.append(query)

    if len(query_list) != 1:
        query = xapian.Query(xapian.Query.OP_AND,query_list)

    else:
        query = query_list[0]

    enquire.set_query(query)
    matches = enquire.get_mset(offset,limit,None)
    return matches


if __name__ == "__main__":
    txt ="""署地最高长官站在街头，皱眉看着一队近卫军飞快地走过治安，他心中满是疑惑，立刻回到了署里地办公室，然后喊来了自己地一个部下"""
    
    for row in session_connect.query(Task).all():
        index_txt(row.id,str(row.content))

    flush_db()
    matches = search('something')
    for m in matches:
        print m.docid
        #print dir(m)
        #print dir(m.get_document())
        print m.document.get_data()
        print 
        


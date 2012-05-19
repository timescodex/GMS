#!/usr/bin/python
# -*- coding: utf-8 -*-
import xapian
import sys
import string
from collections import defaultdict
from mmseg.search import seg_txt_search,seg_txt_2_dict
from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


server = SimpleXMLRPCServer(("localhost", 8001), requestHandler=RequestHandler)

server.register_introspection_functions()

DBPATH = "/home/liyang/SearchDB"
SEARCH_DB = xapian.WritableDatabase(DBPATH,xapian.DB_CREATE_OR_OPEN)
SEARCH_ENQUIRE = xapian.Enquire(SEARCH_DB)

def flush_db():
    SEARCH_DB.flush()

#建立索引：
def index_txt(id,txt):
    print id
    doc = xapian.Document()
    for word,value in seg_txt_2_dict(txt).iteritems():
        doc.add_term(word,value)
        key = ":%s"%id
        doc.add_term(key)
        SEARCH_DB.replace_document(key,doc)

def search(keywords,offset=0,limit=35,enquire=SEARCH_ENQUIRE):
    import pdb
    print keywords
    #pdb.set_trace()
    query_list = []
    for word,value in seg_txt_2_dict(keywords).iteritems():
        query = xapian.Query(word,value)
        query_list.append(query)

    if len(query_list) != 1:
        query = xapian.Query(xapian.Query.OP_AND,query_list)

    else:
        query = query_list[0]

    enquire.set_query(query)
    matches = enquire.get_mset(offset,limit,None)
    
    dictsort = {}
     
    for m in matches:
        dictsort[m.docid] = m.rank
        print m.docid
        print dir(m)
        print m.get_docid()
        print dir(m.document)
        print m.document.get_docid()
    
    #print dictsort
    ids = sorted(dictsort,key=dictsort.get)
    ids.reverse()
    print ids
    return ids

server.register_function(search)

if __name__ == "__main__":
    
    flush_db()
    #matches = search("Test Test")
    #print matches
    #for m in matches:
    #    print "%i: %i%% docid=%i [%s]" % (m.rank + 1, m.percent, m.docid, m.document.get_data())
    print "the search server is running!"
    server.serve_forever()
    print "the search server out of run"



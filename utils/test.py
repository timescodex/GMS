#!/usr/bin/python
from flaskext.sqlalchemy import Pagination

a = [1,2,3,4]

p = Pagination(None,1,2,len(a),a)

for i in range(1,p.pages+1):
    for item in p.items[2*(i-1):(2*i)]:
        print item,i


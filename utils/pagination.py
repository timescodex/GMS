#! /usr/bin/env python
#coding=utf-8
from math import ceil

class InvalidPage(Exception):
    pass

class PageNotAnInteger(InvalidPage):
    pass

class EmptyPage(InvalidPage):
    pass


class Paginator(object):
    '''
    >>> objects = ['john', 'paul', 'george', 'ringo']
    >>> p = Paginator(objects, 2)
    
    >>> p.count
    4
    >>> p.num_pages
    2
    >>> p.page_range
    [1, 2]
    
    >>> page1 = p.page(1)
    >>> page1
    <Page 1 of 2>
    >>> page1.object_list
    ['john', 'paul']
    
    >>> page2 = p.page(2)
    >>> page2.object_list
    ['george', 'ringo']
    >>> page2.has_next()
    False
    >>> page2.has_previous()
    True
    >>> page2.has_other_pages()
    True
    >>> page2.next_page_number()
    3
    >>> page2.previous_page_number()
    1
    >>> page2.start_index() # The 1-based index of the first item on this page
    3
    >>> page2.end_index() # The 1-based index of the last item on this page
    4
    '''    
    def __init__(self,object_list,per_page,orphans=0):
        self.object_list = object_list
        self.per_page = per_page
        self.orphans = orphans
        self._num_pages = self._count = None
        
    def validate_number(self, number):
        "Validates the given 1-based page number."
        try:
            number = int(number)
        except ValueError:
            raise PageNotAnInteger('That page number is not an integer')
        if number < 1:
            raise EmptyPage('That page number is less than 1')
        if number > self.num_pages:
            if number == 1:
                pass
            else:
                raise EmptyPage('That page contains no results')
        return number
    
    def page(self,number):
        "Returns a Page object for the given 1-based page number."
        number = self.validate_number(number)
        bottom = (number - 1) * self.per_page
        top = bottom + self.per_page
        if top + self.orphans >= self.count:
            top = self.count
        return Page(self.object_list[bottom:top], number, self)
    
    def _get_count(self):
        if self._count is None:
            try:
                self._count = self.object_list.count()
            except (AttributeError, TypeError):
                self._count = len(self.object_list)
        return self._count
    count = property(_get_count)
    
    def _get_num_pages(self):
        "Returns the total number of pages."
        if self._num_pages is None:
            if self.count == 0:
                self._num_pages = 0
            else:
                hits = max(1, self.count - self.orphans)
                self._num_pages = int(ceil(hits / float(self.per_page)))
        return self._num_pages
    num_pages = property(_get_num_pages)
    
    def _get_page_range(self):
        return range(1, self.num_pages + 1)
    page_range = property(_get_page_range)
    
class Page(object):
    def __init__(self, object_list, number, paginator):
        self.object_list = object_list
        self.number = number
        self.paginator = paginator
 	
    def __repr__(self):
        return '<Page %s of %s>' % (self.number, self.paginator.num_pages)
	
    def has_next(self):
        return self.number < self.paginator.num_pages
 	
    def has_previous(self):
        return self.number > 1
 	
    def has_other_pages(self):
        return self.has_previous() or self.has_next()
	
    def next_page_number(self):
        return self.number + 1
 	
    def previous_page_number(self):
        return self.number - 1
 	
    def start_index(self):
        """
        Returns the 1-based index of the first object on this page,
        relative to total objects in the paginator.
        """
        # Special case, return zero if no items.
        if self.paginator.count == 0:
            return 0
        return (self.paginator.per_page * (self.number - 1)) + 1
 	
    def end_index(self):
        """
        Returns the 1-based index of the last object on this page,
        relative to total objects found (hits).
        """
        # Special case for the last page because there can be orphans.
        if self.number == self.paginator.num_pages: 
            return self.paginator.count 
        return self.number * self.paginator.per_page 

if __name__=="__main__":
    import doctest
    doctest.testmod()
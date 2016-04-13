#coding: utf-8

import os
import cgi
import json

import webapp2
import jinja2

from google.appengine.ext import ndb

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    variable_start_string='[%',
    variable_end_string='%]',
    autoescape=True)

def data2json(data):
    return json.dumps(
        data,
        indent=2,
        separators=(',', ': '),
        ensure_ascii=False
    )

def book_unicode_to_str(book):
    temp = {}
    for key in book.keys():
        temp[cgi.escape(key)] = (book[key])
    for i in range(len(temp['writers'])):
        temp['writers'][i] = cgi.escape(temp['writers'][i])

    return temp

class Book(ndb.Model):
    title = ndb.StringProperty()
    writers = ndb.PickleProperty()
    description = ndb.TextProperty()
    picUrl = ndb.StringProperty()
    price = ndb.FloatProperty()

    def to_dict(self):
        book = {"title": self.title, "writers": self.writers, "description": self.description, "picUrl": self.picUrl, "price": self.price}
        return book

class MainPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render({}))

class BookHandler(webapp2.RequestHandler):
    def get(self, title):
        book = Book.query(Book.title == title).get()
        self.response.write(simplejson.dumps(book.to_dict()))

    def put(self, title):
        new_book = json.loads(self.request.body)
        book_on_db = Book.query(Book.title == title).get() 

        temp = {}
        for key in new_book.keys():
            temp[cgi.escape(key)] = (new_book[key])

        for i in range(len(temp['writers'])):
            temp['writers'][i] = cgi.escape(temp['writers'][i])

        book_on_db.title = cgi.escape(temp["title"])
        book_on_db.writers = temp['writers']
        book_on_db.description = cgi.escape(temp["description"])
        book_on_db.picUrl = cgi.escape(temp["picUrl"])
        book_on_db.price = float(temp["price"])
        book_on_db.put()

    def delete(self):
        pass

class LibraryHandler(webapp2.RequestHandler):
    
    def get(self):
    	books = Book.query()
        URLBASE = self.request.host_url
        
        data = []
        for b in books:
            book = {"title": b.title, "writers": b.writers, "description": b.description, "picUrl": b.picUrl,"price": b.price}
            data.append(book)
        self.response.write(data2json(data))

    def post(self):
    	book = json.loads(self.request.body)
    	temp = {}

    	for key in book.keys():
    		temp[cgi.escape(key)] = (book[key])

    	for i in range(len(temp['writers'])):
            temp['writers'][i] = cgi.escape(temp['writers'][i])

    	new_book = Book()
    	new_book.title = cgi.escape(temp['title'])
    	new_book.writers = temp['writers']
    	new_book.description = cgi.escape(temp['description'])
    	new_book.picUrl = cgi.escape(temp['picUrl'])
    	new_book.price = float(temp['price'])
        
    	new_book.put()

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/books', LibraryHandler),
    ('/book/(.*)', BookHandler)
], debug=True)
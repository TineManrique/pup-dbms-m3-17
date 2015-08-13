import webapp2
from google.appengine.ext import ndb
import jinja2
import os
import logging
import json


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Thesis(ndb.Model):
    year = ndb.IntegerProperty(indexed=True)
    title = ndb.StringProperty(indexed=True)
    abstract = ndb.StringProperty(indexed=True)
    adviser = ndb.StringProperty(indexed=True)
    section = ndb.IntegerProperty(indexed=True)
    date = ndb.DateTimeProperty(auto_now_add=True)

class MainPageHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render())

    def post(self):
        thesis = Thesis()
        thesis.year = int(self.request.get('year'))
        thesis.title = self.request.get('title')
        thesis.abstract = self.request.get('abstract')
        thesis.adviser = self.request.get('adviser')
        thesis.section = int(self.request.get('section'))
        thesis.key = thesis.put()
        thesis.put()
        self.redirect('/')

class APIThesisHandler(webapp2.RequestHandler):
    def get(self):
        thesiss = Thesis.query().order(-Thesis.date).fetch()
        thesis_list = []

        for thesis in thesiss:
            thesis_list.append({
                'id': thesis.key.urlsafe(),
                'year' : thesis.year,
                'title' : thesis.title,
                'abstract' : thesis.abstract,
                'adviser' : thesis.adviser,
                'section' : thesis.section
                });
            
        response = {
             'result' : 'OK',
             'data' : thesis_list
        }
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(response))

        

    def post(self):
        thesis = Thesis()
        thesis.year = int(self.request.get('year'))
        thesis.title = self.request.get('title')
        thesis.abstract = self.request.get('abstract')
        thesis.adviser = self.request.get('adviser')
        thesis.section = int(self.request.get('section'))
        thesis.key = thesis.put()
        thesis.put()

        self.response.headers['Content-Type'] = 'application/json'
        response = {
        'result' : 'OK',
        'data':{
            'id': thesis.key.urlsafe(),
                'year' : thesis.year,
                'title' : thesis.title,
                'abstract' : thesis.abstract,
                'adviser' : thesis.adviser,
                'section' : thesis.section
        }
        }
        self.response.out.write(json.dumps(response))


app = webapp2.WSGIApplication([
    ('/api/thesis', APIThesisHandler),
    ('/home', MainPageHandler),
    ('/', MainPageHandler)
], debug=True)

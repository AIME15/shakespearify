import os
import sys
import cherrypy
from mako.template import Template
from mako.lookup import TemplateLookup

sys.path.append('../findAuthor')

import findAuthor

lookup = TemplateLookup(directories=['static'])

class Main:
  def index(self):
    tmpl = lookup.get_template("index.txt")
    return tmpl.render(author=None)
  
  index.exposed = True
  
  def analyze(self, sentenceReceived=None):
    print sentenceReceived
    authorFound = findAuthor.test_string(sentenceReceived)
    print authorFound
    tmpl = lookup.get_template("index.txt")
    return tmpl.render(author=authorFound)

  analyze.exposed=True

current_dir = os.path.dirname(os.path.abspath(__file__)) + os.path.sep

config = {
        'global': {
          'environment': 'production',
          'log.screen': True,
          'server.socket_host': '127.0.0.1',
          'server.socket_port': 2000,
          'engine.autoreload_on': True,
          'log.error_file': os.path.join(current_dir, 'errors.log'),
          'log.access_file': os.path.join(current_dir, 'access.log'),
        },
        '/':{
            'tools.staticdir.root' : current_dir,
          },
          '/static':{
              'tools.staticdir.on' : True,
              'tools.staticdir.dir' : 'static',
    },
          '/css' : {
              'tools.staticdir.on' : True,
              'tools.staticdir.dir' : 'static/css'
            },
          '/js' : {
              'tools.staticdir.on' : True,
              'tools.staticdir.dir' : 'static/js'
            }
}

cherrypy.quickstart(Main(), '/', config)

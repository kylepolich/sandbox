#!/usr/bin/python

import daemon
import web
import sys
import os

port=8081
header = '<html><body><a href="/car/list">List</a> | <a href="/car/set">Set</a> | <a href="/goodbye">Terminate Server</a><br/>'
footer = '</body></html>'

class hello:
  def GET(self):
    return header + footer

class car_list:
  def GET(self):
    bdy = header + 'Cars:<br/><br/>'
    if os.path.isfile(saveFile):
      f = open(saveFile, 'r')
      lines = f.readlines()
      for line in lines:
        bdy += line.replace('\n', '<br/>').replace('\t', ' = ')
    else:
      bdy += 'None yet'
    bdy += footer
    return bdy

class car_set:
  def GET(self):
    return header + '<form action="/car/set" method="post">Make and Model: <input name="name" /> Price: <input name="price" /><input type="submit" /></form>' + footer
  def POST(self):
    i = web.input()
    name = i.name
    price = i.price
    f = open(saveFile, 'a')
    f.write(name)
    f.write('\t')
    f.write(price)
    f.write('\n')
    return header + 'Done.  Do another.<br/><br/><form action="/car/set" method="post">Make and Model: <input name="name" /> Price: <input name="price" /><input type="submit" /></form>' + footer

class goodbye:
  def GET(self):
    app.stop()
    return '<html><body>Goodbye</body></html>'

class error:
  def GET(self, req):
    return 'error'
  def POST(self):
    return 'error'

class MyApplication(web.application):
  def run(self, port=port, *middleware):
    func = self.wsgifunc(*middleware)
    return web.httpserver.runsimple(func, ('0.0.0.0', port))

if __name__ == "__main__":
  if (len(sys.argv) != 2 or sys.argv[1]==''):
    print "USAGE: one parameter specifying the file where you want to store data"
    raise SystemExit
  
  global saveFile
  saveFile = sys.argv.pop()
  
  urls = (
    '/',            'hello',
    '/car/list',    'car_list',
    '/car/set',     'car_set',
    '/goodbye',     'goodbye',
    '/(.*)', 'error'
  )
  
  app = MyApplication(urls, globals())

  with daemon.DaemonContext():
    app.run(port=port)



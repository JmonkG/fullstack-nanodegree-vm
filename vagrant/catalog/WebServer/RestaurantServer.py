from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base,Restaurant
from urlparse import urlparse
import cgi

engine = create_engine('sqlite:///Restaurant.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def data():
    restaurant1= Restaurant(name= "Cocolon")
    restaurant2= Restaurant(name="Lo nuestro")
    restaurant3= Restaurant(name="Chop Chops")
    session.add(restaurant1)
    session.commit()
    session.add(restaurant2)
    session.commit()
    session.add(restaurant3)
    session.commit()

class webServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
                if self.path.endswith("/restaurants"):
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += '<html><body><h1><a href="/restaurants/new">Create a new Restaurant</a></h1><ul>'
                    list_restaurants = session.query(Restaurant).all()
                    for i in list_restaurants:
                        output+="<li> %s</li>" % i.name
                        output+='<div> <a href="/restaurants/%s/edit">Edit</a></div>'% i.id
                        output+='<div> <a href="/restaurants/%s/delete">Delete</a></div>' % i.id
                    output += "</ul></body></html>"
                    self.wfile.write(output)
                    #data()
                    if(len(list_restaurants) == 0):
                        print 'no hay nada'
                    else:
                        for i in list_restaurants:
                            print i.name
                    return
                
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)
        try:
                if self.path.endswith("/new"):
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "<h1>Hello!</h1>"
                    output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><h2>Create new restaurant</h2><input name="restaurant_name" type="text" ><input type="submit" value="Submit"> </form>'''
                    output += "</body></html>"
                    self.wfile.write(output)
                    print output
                    return
                
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)
        try:
                if self.path.endswith("/edit"):
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    rest_id = int(self.path.split('/')[2])
                    rest = session.query(Restaurant).filter(Restaurant.id == rest_id).first()
                    output = ""
                    output += "<html><body>"
                    output += "<h1>Hello!</h1>"
                    output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'><h2>Change its name</h2><input name="restaurant_name" type="text" value="%s"><input type="submit" value="Submit"> </form>'''% (rest.id,rest.name) 
                    output += "</body></html>"
                    self.wfile.write(output)
                    print output
                    return
                
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)
        try:
                if self.path.endswith("/delete"):
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    rest_id = int(self.path.split('/')[2])
                    rest = session.query(Restaurant).filter(Restaurant.id == rest_id).first()
                    output = ""
                    output += "<html><body>"
                    output += "<h1>Hello!</h1>"
                    output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'><h2>Are you sure you want to delete %s?</h2><input type="submit" value="Submit"> </form>'''% (rest.id,rest.name)
                    output += "</body></html>"
                    self.wfile.write(output)
                    print output
                    return
                
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)
       
        
    def do_POST(self):
        try:
            if self.path.endswith("/new"):
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                        fields=cgi.parse_multipart(self.rfile, pdict)
                        messagecontent = fields.get('restaurant_name')
                session.add(Restaurant(name= messagecontent[0]))
                session.commit()
                self.send_header('Location','/restaurants')
                self.end_headers()    
        except:
            print 'Error on POSTing'
            pass
        try:
            if self.path.endswith("/edit"):
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location','/restaurants')
                self.end_headers()
                rest_id = int(self.path.split('/')[2])
                rest = session.query(Restaurant).filter(Restaurant.id == rest_id).first()
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                        fields=cgi.parse_multipart(self.rfile, pdict)
                        messagecontent = fields.get('restaurant_name')
                rest.name = messagecontent[0]
                session.commit()
        except:
            print 'Error on Editing'
            pass
        try:
            if self.path.endswith("/delete"):
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                rest_id = int(self.path.split('/')[2])
                rest = session.query(Restaurant).filter(Restaurant.id == rest_id).first()
                session.delete(rest)
                session.commit()
                self.send_header('Location','/restaurants')
                self.end_headers()    
        except:
            print 'Error on Deleting'
            pass
def main():
    try:
        port = 80
        server = HTTPServer(('',port),webServerHandler)
        print "Web server runnin on port %s" % port
        server.serve_forever()
        
    except KeyboardInterrupt: #Ctrl c to interrupt the server
        print "Ctrl C entered, stopping web server..."
        server.socket.close()

if __name__ == '__main__':
    main()
        
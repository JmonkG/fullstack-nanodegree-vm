from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import cgi

class webServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
                if self.path.endswith("/hello"):
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "<h1>Hello!</h1>"
                    output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                    output += "</body></html>"
                    self.wfile.write(output)
                    print output
                    return
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)
       
        
    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                    fields=cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')
            output = ""
            output +=  "<html><body>"
            output += " <h2> Okay, how about this: </h2>"
            output += "<h1> %s </h1>" % messagecontent[0]
            output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            output += "</body></html>"
            self.wfile.write(output)
            print output
        except:
            print 'Error'
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
        
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base,Restaurant,MenuItem

engine = create_engine('sqlite:///resstaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class webserverHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			print 'Request from client...'
			if self.path.endswith('/hello'):
				print 'Hello request...'
				self.send_response(200)
				self.send_header('Content-type','text/html')
				self.end_headers()

				output = ''
				output += '<html><body>'
				output += '<h1>Hello!</h1>'
				output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
				output += '</body></html>'
				self.wfile.write(output)
				print output
				return
			elif self.path.endswith('/hola'):
				print 'Hello request...'
				self.send_response(200)
				self.send_header('Content-type','text/html')
				self.end_headers()

				output = ''
				output += '<html><body>'
				output += '<h1>&#161Hola!</h1>'
				output += '<a href="/hello">Back to hello</a>'
				output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
				output += '</body></html>'
				self.wfile.write(output)
				print output
				return
			elif self.path.endswith('/restaurants'):
				print 'restaurants query...'
				self.send_response(200)
				self.send_header('Content-type','text/html')
				self.end_headers()

				output = ''
				output += '<html><body>'
				output += self.listaRestaurantes()
				output += '<a href="/restaurants/new"><h2>New Restaurant</h2></a>'
				output += '</body></html>'
				self.wfile.write(output)
				print 'Fin Request'
			elif self.path.endswith('/restaurants/new'):
				print 'new restaurant query...'
				self.send_response(200)
				self.send_header('Content-type','text/html')
				self.end_headers()

				output = ''
				output += '<html><body>'
				output += '<h1>New Restaurant</h1>'
				output += '<form method=\'POST\' enctype=\'multipart/form-data\' action=\'/restaurants\'><h2>Name</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'
				#output += self.listaRestaurantes()
				#output += '<a href="/restaurants/new"><h2>New Restaurant</h2></a>'
				output += '</body></html>'
				self.wfile.write(output)
				print 'Fin Request'

		except IOError:
			self.send_error(404,"File Not Found: %s" % self.path)
	def do_POST(self):
		try:
			print 'Post from client'
			self.send_response(302)
			self.send_header('Location', '/restaurants')
			self.end_headers()
			ctype,pdict = cgi.parse_header(self.headers.getheader('content-type'))
			if ctype == 'multipart/form-data':
				fields = cgi.parse_multipart(self.rfile,pdict)
				messagecontent = fields.get('message')
				print 'adding new restaurant'
				self.addRestaurant(messagecontent[0])
				print 'restaurant added'
			#output = ''
			#output += "<html><body>"
			#output += '<h2> Restaurant Created! </h2>'
			#output += '<a href="/restaurants">Volver</a>'
			#output += '</body></html>'
			#self.wfile.write(output)
			#print output
		except:
		#	print 'ERROR!'
			pass

	def listaRestaurantes(self):
		output = ''
		output += '<h1>Lista de restaurantes</h1><hr>'
		restaurants = session.query(Restaurant).all()
		for item in restaurants:
			output += '<div style="padding:5px"><h3 style="margin-bottom:5px ">%s</h3><a href="#">Edit</a><br><a href="#">Delete</a></div>' % item.name
		output += '<hr>'
		return output

	def addRestaurant(self,x):
		temp = Restaurant(name=x)
		session.add(temp)
		session.commit()

def main():
	try:
		port = 8080
		server = HTTPServer(('',port), webserverHandler)
		print 'Server is running on port %s' % port
		server.serve_forever()
	except KeyboardInterrupt:
		print 'Stopping server...'
		server.socket.close()


if __name__ == '__main__':
	main()
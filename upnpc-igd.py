import os

class upnpIGD:
	def __init__(self,upnpccommand):
		self.igdfound = False	# default
		self.myip = self.myexternalip = ''
		self.command = upnpccommand
		cmd = self.command + ' -s'
		for thisline in os.popen(cmd).readlines():
			thisline = thisline.strip()
			if (thisline.startswith('No IGD UPnP Device found on the network') 
			   or thisline.startswith('GetConnectionTypeInfo failed')):
				# Note "No IGD UPnP Device found on the network !" seems to be printed to stderr :-(
				self.igdfound = False
			if thisline.startswith('Found valid IGD'):
				self.igdfound = True
			if thisline.find('Local LAN ip address')>=0:
				# Local LAN ip address : 192.168.1.111
				self.myip = thisline.split(':')[1].replace(' ','')
			if thisline.find('ExternalIPAddress')>=0:
				self.myexternalip = thisline.split('=')[1].replace(' ','')

	def setRedirect(self,port):
		redirectsuccess = True	# default is True
		cmd = self.command + ' -r ' + str(port) + ' tcp'
		for thisline in os.popen(cmd).readlines():
			thisline = thisline.strip()
			if thisline.startswith('AddPortMapping') or thisline.startswith('No IGD UPnP Device found on the network'):
				# Not good:
				# AddPortMapping(8080, 8080, 192.168.1.104) failed with code 501 (Action Failed)
				# ... meaning mapped to another device
				# AddPortMapping(11222, 11222, 192.168.1.111) failed with code 401 (Invalid Action)
				# ... meaning something went wrong
				# No IGD UPnP Device found on the network !
				# ... meaning ... no IGD UPnP device was found
				redirectsuccess = False
			'''
			if thisline.startswith('external'):
				if redirectsuccess:
					print "succesful mapping " + thisline.split()[7]
				else:
					print "external already mapped to " + thisline.split()[7]
			'''
		return redirectsuccess


	def deleteRedirect(self,port):
		deletesuccess = False	# default
		cmd = self.command + ' -d ' + str(port) + ' tcp'
		for thisline in os.popen(cmd).readlines():
			thisline = thisline.strip()
			#print thisline
			if thisline.startswith('UPNP_DeletePortMapping'):
				#print thisline
				if thisline.split()[-1] == '0':
					deletesuccess = True
		return deletesuccess

command = 'upnpc'
#command = '/usr/bin/upnpc'
#command = '/home/sander/git/miniupnp/miniupnpc/upnpc-static'
mysetting = upnpIGD(command)
if mysetting.igdfound:
	print "My IP is " + mysetting.myip
	print "My external IP is " + mysetting.myexternalip

	print "setting ... " + str(mysetting.setRedirect(4444))
	print "delete ... " + str(mysetting.deleteRedirect(4444))

######### END


'''
def setRedirect(port):

	redirectsuccess = True
	inblock = False
	cmd = 'upnpc -r ' + str(port) + ' tcp'
	for thisline in os.popen(cmd).readlines():
		thisline = thisline.strip()
		if thisline.find('Local LAN ip address')>=0:
			# Local LAN ip address : 192.168.1.111
			myip = thisline.split(':')[1].replace(' ','')
			print "My IP is " + myip
		if thisline.startswith('AddPortMapping') or thisline.startswith('No IGD UPnP Device found on the network'):
			# Not good:
			# AddPortMapping(8080, 8080, 192.168.1.104) failed with code 501 (Action Failed)
			# No IGD UPnP Device found on the network !
			print "Mapping did not happen: " + thisline
			redirectsuccess = False
		if thisline.startswith('external'):
			if redirectsuccess:
				print "succesful mapping " + thisline.split()[7]
			else:
				print "external already mapped to " + thisline.split()[7]
	return redirectsuccess
'''

'''
def deleteRedirect(port):
	deletesuccess = False	# default
	cmd = 'upnpc -d ' + str(port) + ' tcp'
	for thisline in os.popen(cmd).readlines():
		thisline = thisline.strip()
		#print thisline
		if thisline.startswith('UPNP_DeletePortMapping'):
			#print thisline
			if thisline.split()[-1] == '0':
				deletesuccess = True
	return deletesuccess
'''

#print setRedirect('4444')
#print setRedirect(4444)

#print deleteRedirect(4444)

		 

'''
### succesful redirect
$ upnpc -r 12345 tcp
upnpc : miniupnpc library test client. (c) 2006-2010 Thomas Bernard
Go to http://miniupnp.free.fr/ or http://miniupnp.tuxfamily.org/
for more information.
List of UPNP devices found on the network :
 desc: http://192.168.1.1:1900/igd.xml
 st: urn:schemas-upnp-org:device:InternetGatewayDevice:1

Found valid IGD : http://192.168.1.1:1900/ipc
Local LAN ip address : 192.168.1.104
ExternalIPAddress = 83.128.242.254
InternalIP:Port = 192.168.1.104:12345
external 83.128.242.254:12345 TCP is redirected to internal 192.168.1.104:12345
'''

		
'''
### unsuccesfull redirect; outside already used (probably by another device on the LAN)
$ upnpc -r 8080 tcp
upnpc : miniupnpc library test client. (c) 2006-2010 Thomas Bernard
Go to http://miniupnp.free.fr/ or http://miniupnp.tuxfamily.org/
for more information.
List of UPNP devices found on the network :
 desc: http://192.168.1.1:1900/igd.xml
 st: urn:schemas-upnp-org:device:InternetGatewayDevice:1

Found valid IGD : http://192.168.1.1:1900/ipc
Local LAN ip address : 192.168.1.104
ExternalIPAddress = 83.128.242.254
AddPortMapping(8080, 8080, 192.168.1.104) failed with code 501 (Action Failed)
InternalIP:Port = 192.168.1.111:8080
external 83.128.242.254:8080 TCP is redirected to internal 192.168.1.111:8080
'''

'''
### unsuccsefull redirect ... no UPnP IGD device
$ upnpc -r 11222 tcp
upnpc : miniupnpc library test client. (c) 2006-2011 Thomas Bernard
Go to http://miniupnp.free.fr/ or http://miniupnp.tuxfamily.org/
for more information.
List of UPNP devices found on the network :
 desc: http://192.168.1.111:8200/rootDesc.xml
 st: upnp:rootdevice

UPnP device found. Is it an IGD ? : http://192.168.1.111:8200/
Trying to continue anyway
Local LAN ip address : 192.168.1.111
GetExternalIPAddress failed.
AddPortMapping(11222, 11222, 192.168.1.111) failed with code 401 (Invalid Action)
GetSpecificPortMappingEntry() failed with code 401 (Invalid Action)
'''


'''
### succesful delete:
### Attention: this will try delete, no matter if directed to this device
$ upnpc -d 1234 tcp
upnpc : miniupnpc library test client. (c) 2006-2010 Thomas Bernard
Go to http://miniupnp.free.fr/ or http://miniupnp.tuxfamily.org/
for more information.
List of UPNP devices found on the network :
 desc: http://192.168.1.1:1900/igd.xml
 st: urn:schemas-upnp-org:device:InternetGatewayDevice:1

Found valid IGD : http://192.168.1.1:1900/ipc
Local LAN ip address : 192.168.1.104
UPNP_DeletePortMapping() returned : 0
'''


'''
### unsuccesful delete:
$ upnpc -d 1234 tcp
upnpc : miniupnpc library test client. (c) 2006-2010 Thomas Bernard
Go to http://miniupnp.free.fr/ or http://miniupnp.tuxfamily.org/
for more information.
List of UPNP devices found on the network :
 desc: http://192.168.1.1:1900/igd.xml
 st: urn:schemas-upnp-org:device:InternetGatewayDevice:1

Found valid IGD : http://192.168.1.1:1900/ipc
Local LAN ip address : 192.168.1.104
UPNP_DeletePortMapping() returned : 402
'''







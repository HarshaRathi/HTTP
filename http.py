import hashlib 
import os
from pymemcache.client import base
from socket import *
import threading
import sys
from PIL import Image 
import cv2
from time import gmtime, strftime
import time
import csv
import os.path
from os import path
import pytz
from datetime import datetime,timedelta
import random
import string
import hashlib
import base64
maxcon = 0
client = base.Client(('localhost', 11211))
serverport1 = ""
errorlog = ""
accesslog = ""
documentroot = ""
lock = threading.Lock()
#FileNotExistsErrorLog
def filenotexistserrorlog(words1,referer1,client_addr,port,errorlog):

	fileaccess2 = open(errorlog,"a")
	current = datetime.now()
	error = current.strftime("[%a %b %d %I:%M:%S.%f %Y]") + " [core:info]" + " [pid " + str(os.getpid()) + ":tid " +str(threading.current_thread().ident) + "]"+" [client "+str(client_addr)+":"+str(port)+"]"+" AH00128: File does not exist:"+words1
	if not referer1  == "":
		error += ", referer:" + referer1
	else:
		error += "\n"
		###print(error)	
		fileaccess2.write(error)
	fileaccess2.close()
		
#NotAllowedErrorLog
def notallowederrorlog(client_addr,port,words1,referer1,errorlog,method):
	fileaccess2 = open(errorlog,"a")
	current = datetime.now()
	error = current.strftime("[%a %b %d %I:%M:%S.%f %Y]") + " [core:debug]" + " [pid " + str(os.getpid()) + ":tid " +str(threading.current_thread().ident) + "]"+" protocol.c(887): "+" [client "+str(client_addr)+":"+str(port)+"]"+" AH03444: HTTP Request Line; Invalid method token: '"+method+"'"
	fileaccess2.write(error)
	fileaccess2.close()
	
		
#AccessLog		
def accesslogfn(client_addr,query,status_code,lenfile,referer,user_agent,accesslog):
	###print(accesslog)
	fileaccess = open(accesslog,"a")
	IST = pytz.timezone('Asia/Kolkata')
	current_datetime=datetime.now(IST)
	Date = current_datetime.strftime("[%d/%b/%Y:%H:%M:%S %z]")
	access_log = client_addr + " - " + " - " + Date  + " " +query  +" "
	access_log1 = str(status_code) + " " +str(lenfile) + " " +referer+" "+user_agent + "\n"
	fileaccess.write(access_log)
	fileaccess.write(access_log1)
	 ###print("accesslogfn")
	fileaccess.close()
	
#PermissionDeniedErrorLog	
def permissiondeniederrorlog(client_addr,port,words1,referer1,errorlog) :
	fileaccess1 = open(errorlog,"a")
	current = datetime.now()
	error = current.strftime("[%a %b %d %I:%M:%S.%f %Y]") + " [core:error]" + " [pid " + str(os.getpid()) + ":tid " +str(threading.current_thread().ident) + "]"+" (13)Permission denied:"+" [client "+str(client_addr)+":"+str(port)+"]"+" AH00132: file permissions deny server access:"+words1
	if not referer1  == "":
		error += ", referer:" + referer1
	else:
		error += "\n"	
	fileaccess1.write(error)
	fileaccess1.close()
	
#ErrorLogGranted	
def errorlogs(client_addr,port,referer1,errorlog):
	
	fileaccess1 = open(errorlog,"a")
	current = datetime.now()
	error = current.strftime("[%a %b %d %I:%M:%S.%f %Y]") + " [authz_core:debug] " + " [pid " + str(os.getpid()) + ":tid " +str(threading.current_thread().ident) + "]"+" mod_authz_core.c(817):"+" [client "+str(client_addr)+":"+str(port)+"]"+" AH01626: authorization result of Require all granted: granted"
	error1 = current.strftime("[%a %b %d %I:%M:%S.%f %Y]") + " [authz_core:debug] " + " [pid " + str(os.getpid()) + ":tid " +str(threading.current_thread().ident) + "]"+" mod_authz_core.c(817):"+" [client "+str(client_addr)+":"+str(port)+"]"+"  AH01626: authorization result of <RequireAny>: granted"
	if not referer1  == "":
		error = ", referer:" + referer1
		error1 = ", referer:" + referer1
	else:
		error += "\n"
		error1 += "\n"
	
	fileaccess1.write(error)
	fileaccess1.write(error1)
	fileaccess1.close()
	
#FileNotExists	
def filenotexists(method,connectionSocket,words,client_addr,port,query,referer,referer1,user_agent):
	global maxcon
	global errorlog
	global accesslog
	f = open("notfound.html")
	fileoutput = f.read()
	string = "HTTP/1.1 404 NOT FOUND\n"
	string += "Date: " + (time.strftime("%a, %d %b %Y %I:%M:%S %p %Z", time.gmtime()))
	string += "\nServer: Harsha/2.4.41 (Ubuntu)\n"
	string += "Content-Length: " +  str(len(fileoutput)) +"\n"
	string += "Content-Language: en\n" 
	string += "Connection: close\n"
	string += "Content-Type: text/html; charset=iso-8859-1\n\n"
	if not method=="HEAD":
		string = string + fileoutput
	else:
		string = string
	connectionSocket.send(string.encode())
	connectionSocket.close()
	maxcon-=1
	status_code=404
	#access log
	accesslogfn(client_addr,query,status_code,len(fileoutput),referer,user_agent,accesslog)						
	#error log
	filenotexistserrorlog(words[1],referer1,client_addr,port,errorlog)
	f.close()

#HTML for GET POST HEAD
def html(method,filename,cookieval,connectionSocket,client_addr,port,query,referer,referer1,user_agent,arange,ims):
	global maxcon
	global errorlog
	global accesslog
	f = open(filename,"r")
	fileoutput = f.read()
	l = len(fileoutput)
	l1 = l
	fileoutput1 = ""
	lmd = time.ctime(os.path.getmtime(filename))
	lmd = lmd.split(" ")
	lmd = lmd[0] +", "+lmd[2]+" "+lmd[1]+" "+lmd[4]+" "+lmd[3] + " "+"GMT"
	a = 0
	b = 0
	if arange and method == "GET" and (not ims):
		for row in arange:
			row=row.split("-")
			if row[0] == "" or row[0]=="\r":
				a = len(fileoutput)-int(row[1])
				b = len(fileoutput)
			elif row[1] == "\r" or row[1] == "":
				a = row[0]
				b = len(fileoutput)
			else:
				a = row[0]
				b = row[1]
			if int(a) > l or int(a) > int(b):
				break
			fileoutput1 += fileoutput[int(a)-1:int(b)]
		fileoutput = fileoutput1
		if int(a) > l1 or int(a) > int(b):
			status_code = 416
			string = "HTTP/1.1 416 Range Not Satisfiable\n"
			fileoutput = ""
			l = 0
		elif len(fileoutput) < l1:
			status_code = 206
			string = "HTTP/1.1 206 Partial Content\n"
			l = len(fileoutput)
		else:
			status_code = 200
			string = "HTTP/1.1 200 OK\n"
			l = l1
	elif ims and (not arange) and (method == "GET" or method == "HEAD"):
		if ims[0:len(ims)-1] == lmd:
			status_code = 304
			string = "HTTP/1.1 304 Not Modified\n"
			fileoutput = ""
			l = 0
		else:
			l = l1 
			status_code = 200
			string = "HTTP/1.1 200 OK\n"
	elif ims and arange and method == "GET":
		if ims[0:len(ims)-1] == lmd:
			status_code = 304
			string = "HTTP/1.1 304 Not Modified\n"
			fileoutput = ""
			l = 0
		else:
			
			for row in arange:
				row=row.split("-")
				if row[0] == "" or row[0]=="\r":
					a = len(fileoutput)-int(row[1])
					b = len(fileoutput)
				elif row[1] == "\r" or row[1] == "":
					a = row[0]
					b = len(fileoutput)
				else:
					a = row[0]
					b = row[1]
				if int(a) > l or int(a) > int(b):
					break
				fileoutput1 += fileoutput[int(a)-1:int(b)]
			fileoutput = fileoutput1
			l = len(fileoutput)
			if int(a) > l1 or int(a) > int(b):
				status_code = 416
				string = "HTTP/1.1 416 Range Not Satisfiable\n"
				fileoutput = ""
				l = 0
			elif len(fileoutput) < l1:
				status_code = 206
				string = "HTTP/1.1 206 Partial Content\n"
				l = len(fileoutput)
			else:
				l = l1
				status_code = 200
				string = "HTTP/1.1 200 OK\n"

	else:
		l = l1
		status_code = 200
		string = "HTTP/1.1 200 OK\n"	
	
	
	
	string += "Date: " +(time.strftime("%a, %d %b %Y %I:%M:%S %p %Z", time.gmtime()))
	string += "\nServer: Harsha/2.4.41 (Ubuntu)\n"
	
	
	string += "Last-Modified: " +lmd

	string += "\nAccept-Ranges: Bytes\n"
	string += "Content-Type: text/html\n"

	if method == "GET" or method == "POST" :
		string += "Content-Length: " + str(l) + "\n"
		data = fileoutput
		result = hashlib.md5(bytes(data,'utf-8'))
		result = result.digest()
		result = bytes(result)
		md5 = base64.b64encode(result)
		md5 = md5.decode('utf-8')
		string+="Content-md5: " + md5 + "\n"
	elif method == "HEAD":
		string += "Content-Length: " + str(l1) + "\n"
		l = l1
	
	
	if cookieval == "" or method == "POST" :
		pass
	else:
		string += "Set-Cookie: "+cookieval+"\n"
	
	string += "Connection: close\n\n"
	
	#for head method
	if method == "GET" or method == "POST" :		
		output = string + fileoutput
	else:
		output = string
		
	connectionSocket.send(output.encode())
	connectionSocket.close()
	maxcon-=1
	
					 
	#access log
					
	accesslogfn(client_addr,query,status_code,l,referer,user_agent,accesslog)
					
	#error log
				
	errorlogs(client_addr,port,referer1,errorlog)
	f.close()
	
	return
	
def deletemethod(words,errorlog,accesslog,query,client_addr,port,referer,referer1,user_agent):
	global client
	global maxcon
	
	extension =(words[1].split("."))[1]
	filename = words[1]
	filename = documentroot + filename
	if not path.exists(filename):
		f = open("notfound.html")
		fileoutput = f.read()
		string = "HTTP/1.1 404 NOT FOUND\n"
		string +="Date: " + (time.strftime("%a, %d %b %Y %I:%M:%S %p %Z", time.gmtime())) + "\n\n"
		string = string + fileoutput
		connectionSocket.send(string.encode())
		connectionSocket.close()
		maxcon-=1
		status_code=404
		accesslogfn(client_addr,query,status_code,len(fileoutput),referer,user_agent,accesslog)
		#error log
		
		filenotexists("GET",connectionSocket,words[1],client_addr,port,query,referer,referer1,user_agent)
		f.close()
					
	
	else:
		if os.access(filename, os.X_OK) and os.access(filename, os.W_OK) :
			os.remove(filename)
			f = open("filedeleted.html")
			fileoutput = f.read()
			string = "HTTP/1.1 200 OK\n"
			string += "Date: " +(time.strftime("%a, %d %b %Y %I:%M:%S %p %Z", time.gmtime())) + "\n\n"
			string = string + fileoutput
			###print(string)
			connectionSocket.send(string.encode())
			connectionSocket.close()
			maxcon-=1
			#access log
			status_code = 200
			accesslogfn(client_addr,query,status_code,len(fileoutput),referer,user_agent,accesslog)
						
			#error log
			errorlogs(client_addr,port,referer1,errorlog)
			f.close()
		else:
						
			f = open("forbidden.html")
			fileoutput = f.read()
			string = "HTTP/1.1 403 Forbidden\n"
			string += "Date: " + (time.strftime("%a, %d %b %Y %I:%M:%S %p %Z", time.gmtime())) + "\n\n"
			string+=fileoutput
			connectionSocket.send(string.encode())
			connectionSocket.close()
			maxcon-=1
			status_code=403
			accesslogfn(client_addr,query,status_code,len(fileoutput),referer,user_agent,accesslog)
			permissiondeniederrorlog(client_addr,port,words[1],referer1,errorlog)
			f.close()
	
	
def putmethod(sentence,words,errorlog,accesslog,query,client_addr,port,referer,referer1,user_agent):
	global client
	global maxcon
	##print("okok")
	data = sentence.split("\r\n\r")[1]
	filename = words[1]
	filename = documentroot + filename
	###print(data == "")
	###print(sentence.split("\r\n\r"))
	if data == "\n":
		string = "HTTP/1.1 204 No Content\n"
		string += "Content-Location: /" + filename + "\n\n"
		connectionSocket.send(string.encode())
		connectionSocket.close()
		maxcon-=1
		status_code=204
		accesslogfn(client_addr,query,status_code,0,referer,user_agent,accesslog)
					
		#error log
		errorlogs(client_addr,port,referer1,errorlog)
					
	else:
		if path.exists(filename):
			if not (os.access(filename, os.R_OK) and os.access(filename,os.W_OK)):
				f = open("forbidden.html")
				fileoutput = f.read()
				string = "HTTP/1.1 403 Forbidden\n"
				string += "\nContent-Length: " +  str(len(fileoutput)) +"\n"
				string += "Connection: close\n"
				string += "Content-Type: text/html; charset=iso-8859-1\n\n"
				string = string + fileoutput
				connectionSocket.send(string.encode())
				connectionSocket.close()
				maxcon-=1
				#access log
				status_code=403
				accesslogfn(client_addr,query,status_code,len(fileoutput),referer,user_agent,accesslog)
				#error log
				permissiondeniederrorlog(client_addr,port,words[1],referer1,errorlog)
				f.close()
				
			else:
				##print("okokok")
				f = open(filename,'w')
				f.write(data)
				string = "HTTP/1.1 200 OK\n"
				string +=  "Content-Location: /" + filename + "\n\n"
				connectionSocket.send(string.encode())
				connectionSocket.close()
			
				maxcon-=1
				status_code=200
				accesslogfn(client_addr,query,status_code,0,referer,user_agent,accesslog)
						
				#error log
				errorlogs(client_addr,port,referer1,errorlog)
				f.close()
		else:
			f = open(filename,'w')
			f.write(data)
			string = "HTTP/1.1 201 Created\n"
			string +=  "Content-Location: /" + filename + "\n\n"
			connectionSocket.send(string.encode())
			connectionSocket.close()
			maxcon-=1
			status_code=201
			accesslogfn(client_addr,query,status_code,0,referer,user_agent,accesslog)
						
			#error log
			errorlogs(client_addr,port,referer1,errorlog)
			f.close()
			
# CSV for GET POST HEAD		
def csv(method,connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims):
	###print(method)
	global client
	global accesslog
	global maxcon
	global errorlog
	f = open(filename)
	fileoutput = f.read()
	l = len(fileoutput)
	l1 = l
	lmd = time.ctime(os.path.getmtime(filename))
	lmd = lmd.split(" ")
	lmd = lmd[0] +", "+lmd[3]+" "+lmd[1]+" "+lmd[5]+" "+lmd[4] + " "+"GMT"
	a = 0
	b = 0
	fileoutput1=""
	if arange and method == "GET" and (not ims):
		for row in arange:
			row=row.split("-")
			if row[0] == "" or row[0]=="\r":
				a = len(fileoutput)-int(row[1])
				b = len(fileoutput)
			elif row[1] == "\r" or row[1] == "":
				a = row[0]
				b = len(fileoutput)
			else:
				a = row[0]
				b = row[1]
			if int(a) > l or int(a) > int(b):
				break
			fileoutput1 += fileoutput[int(a)-1:int(b)]
		fileoutput = fileoutput1
		
		if int(a) > l1 or int(a) > int(b):
			status_code = 416
			string = "HTTP/1.1 416 Range Not Satisfiable\n"
			fileoutput = ""
			l = 0
		elif len(fileoutput) < l1:
			status_code = 206
			string = "HTTP/1.1 206 Partial Content\n"
			l = len(fileoutput)
		else:
			status_code = 200
			string = "HTTP/1.1 200 OK\n"
			l = l1
	elif ims and (not arange) and (method == "GET" or method == "HEAD"):
		if ims[0:len(ims)-1] == lmd:
			status_code = 304
			string = "HTTP/1.1 304 Not Modified\n"
			fileoutput = ""
			l = 0
		else:
			status_code = 200
			string = "HTTP/1.1 200 OK\n"
			l = l1
	elif ims and arange and method == "GET":
		if ims[0:len(ims)-1] == lmd:
			status_code = 304
			string = "HTTP/1.1 304 Not Modified\n"
			fileoutput = ""
			l = 0
		else:
			for row in arange:
				row=row.split("-")
				if row[0] == "" or row[0]=="\r":
					a = len(fileoutput)-int(row[1])
					b = len(fileoutput)
				elif row[1] == "\r" or row[1] == "":
					a = row[0]
					b = len(fileoutput)
				else:
					a = row[0]
					b = row[1]
				if int(a) > l or int(a) > int (b):
					break
				fileoutput1 += fileoutput[int(a)-1:int(b)]
			fileoutput = fileoutput1
		
			if int(a) > l1 or int(a) > int(b):
				status_code = 416
				string = "HTTP/1.1 416 Range Not Satisfiable\n"
				fileoutput = ""
				l = 0
			elif len(fileoutput) < l1:
				status_code = 206
				string = "HTTP/1.1 206 Partial Content\n"
				l = len(fileoutput)
			else:
				status_code = 200
				string = "HTTP/1.1 200 OK\n"
				l = l1

	else:
		status_code = 200
		string = "HTTP/1.1 200 OK\n"	
		l = l1
	string += "Date: " +(time.strftime("%a, %d %b %Y %I:%M:%S %p %Z", time.gmtime()))
	string += "\nServer: Harsha/2.4.41 (Ubuntu)\n"
	lmd = time.ctime(os.path.getmtime(filename))
	lmd = lmd.split(" ")
	lmd = lmd[0] +", "+lmd[3]+" "+lmd[1]+" "+lmd[5]+" "+lmd[4] + " "+"GMT"
	string += "Last-Modified: " +lmd + "\n"
	string += "Content-Type: text/csv\n"
	
	
	if cookieval == "" or method == "POST":
		pass
	else:
		string += "Set-Cookie: "+cookieval+"\n"
		
	if method == "POST" or method == "GET":
		string += "Content-Length: " + str(l) + "\n"
		data = fileoutput
		result = hashlib.md5(bytes(data,'utf-8'))
		result = result.digest()
		result = bytes(result)
		md5 = base64.b64encode(result)
		md5 = md5.decode('utf-8')
		string+="Content-md5: " + md5 + "\n"
	elif method == "HEAD":
		string += "Content-Length: " + str(l1) + "\n"
		l = l1
		
	string += "Connection: close\n\n"
	
	if method == "POST" or method == "GET":
		output = string + fileoutput
	else:
		output = string
	connectionSocket.send(output.encode())
	connectionSocket.close()
	maxcon-=1
	#access log
	status_code=200
	accesslogfn(client_addr,query,status_code,l,referer,user_agent,accesslog)
					
	#error log
	errorlogs(client_addr,port,referer1,errorlog)
	f.close()

#PDF for GET POST HEAD	
def pdf(method,connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims):
	##print("ok")
	global client
	global accesslog
	global maxcon
	global errorlog
	lmd = time.ctime(os.path.getmtime(filename))
	lmd = lmd.split(" ")
	lmd = lmd[0] +", "+lmd[2]+" "+lmd[1]+" "+lmd[4]+" "+lmd[3] + " "+"GMT"
	##print("no")
	with open(filename, "rb") as image:
		f = image.read()
		b = bytearray(f)
	a=0	
	b2 = 0
	l = len(b)
	l1 = l
	b1 = bytearray()
	
	if arange and method == "GET" and (not ims):
		for row in arange:
					
			row=row.split("-")
			if row[0] == "" or row[0]=="\r":
				a = len(b)-int(row[1])
				b2 = len(b)
			elif row[1] == "\r" or row[1] == "":
				a = int(row[0])
				b2 = len(b)
			else:
				a = int(row[0])
				b2 = int(row[1])
			if int(a) > l or int(a) > int(b2): 
				break
			
			b1 = b1 + b[a-1:b2]
		b = b1
	
		if int(a) > l1 or int(a) > int(b2):
			status_code = 416
			string = "HTTP/1.1 416 Range Not Satisfiable\n"
			b = bytearray()
			l = 0
		elif len(b) < l1:
			#l = len(fileoutput)
			status_code = 206
			string = "HTTP/1.1 206 Partial Content\n"
			l = len(b)
		else:
			status_code = 200
			string = "HTTP/1.1 200 OK\n"
			l = l1
	elif ims and (not arange) and (method == "GET" or method == "HEAD"):
		if ims[0:len(ims)-1] == lmd:
			status_code = 304
			string = "HTTP/1.1 304 Not Modified\n"
			b = bytearray()
			l=0
		else:
			status_code = 200
			string = "HTTP/1.1 200 OK\n"
			l=l1
	elif ims and arange and method == "GET":
		if ims[0:len(ims)-1] == lmd:
			status_code = 304
			string = "HTTP/1.1 304 Not Modified\n"
			b = bytearray()
			l=0
		else:
			for row in arange:
					
				row=row.split("-")
				if row[0] == "" or row[0]=="\r":
					a = len(b)-int(row[1])
					b2 = len(b)
				elif row[1] == "\r" or row[1] == "":
					a = int(row[0])
					b2 = len(b)
				else:
					a = int(row[0])
					b2 = int(row[1])
				if int(a) > l or int(a) > int(b2) :
					break
				b1 = b1 + b[a-1:b2]
			b = b1
			
			if int(a) > l1 or int(a) > int(b2):
				status_code = 416
				string = "HTTP/1.1 416 Range Not Satisfiable\n"
				b = bytearray()
				l=0
			elif len(b) < l1:
				status_code = 206
				string = "HTTP/1.1 206 Partial Content\n"
				l=len(b)
			else:
				status_code = 200
				string = "HTTP/1.1 200 OK\n"
				l=l1

	else:
		status_code = 200
		string = "HTTP/1.1 200 OK\n"
		l=l1
	
	
	string += "Date: " +(time.strftime("%a, %d %b %Y %I:%M:%S %p %Z", time.gmtime()))
	string += "\nServer: Harsha/2.4.41 (Ubuntu)\n"
	string += "Last-Modified: " +lmd + "\n"
	string += "Content-Type: application/pdf\n"
	if cookieval == "" or method == "POST":
		pass
	else:
		string += "Set-Cookie: "+cookieval+"\n"
	if method == "POST" or method == "GET":
		string += "Content-Length: " + str(l) + "\n"
		data = str(b)
		result = hashlib.md5(bytes(data,'utf-8'))
		result = result.digest()
		result = bytes(result)
		md5 = base64.b64encode(result)
		md5 = md5.decode('utf-8')
		string+="Content-md5: " + md5 + "\n"
	elif method == "HEAD":
		string += "Content-Length: " + str(l1) + "\n"
		l=l1
	string += "Connection: close\n\n"
	if method == "POST" or method == "GET":
		output = string.encode() + b
	else:
		output = string.encode()
	##print(output)
	connectionSocket.send(output)
	connectionSocket.close()
	maxcon-=1
	#access log
	status_code=200
	accesslogfn(client_addr,query,status_code,len(b),referer,user_agent,accesslog)
					
	#error log
	errorlogs(client_addr,port,referer1,errorlog)
	
#PPT for HEAD GET POST
def ppt(method,connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims):
	###print(method)
	global client
	global accesslog
	global maxcon
	global errorlog
	lmd = time.ctime(os.path.getmtime(filename))
	lmd = lmd.split(" ")
	lmd = lmd[0] +", "+lmd[3]+" "+lmd[1]+" "+lmd[5]+" "+lmd[4] + " "+"GMT"
	with open(filename, "rb") as image:
		f = image.read()
		b = bytearray(f)	
	a=0	
	b2=0
	l = len(b)
	l1 = l
	b1 = bytearray()
	if arange and method == "GET" and (not ims):
		for row in arange:
					
			row=row.split("-")
			if row[0] == "" or row[0]=="\r":
				a = len(b)-int(row[1])
				b2 = len(b)
			elif row[1] == "\r" or row[1] == "":
				a = int(row[0])
				b2 = len(b)
			else:
				a = int(row[0])
				b2 = int(row[1])
			if int(a) > l or int(a) > int(b2):
				break			
			b1 = b1 + b[a-1:b2]
		b = b1
	
		if int(a) > l1 or int(a) > int(b2):
			status_code = 416
			string = "HTTP/1.1 416 Range Not Satisfiable\n"
			b = bytearray()
			l=0
		elif len(b) < l1:
			status_code = 206
			string = "HTTP/1.1 206 Partial Content\n"
			l = len(b)
		else:
			status_code = 200
			string = "HTTP/1.1 200 OK\n"
			l = l1
	elif ims and (not arange) and (method == "GET" or method == "HEAD"):
		if ims[0:len(ims)-1] == lmd:
			status_code = 304
			string = "HTTP/1.1 304 Not Modified\n"
			b = bytearray()
			l = 0
		else:
			status_code = 200
			string = "HTTP/1.1 200 OK\n"
			l = l1
	elif ims and arange and method == "GET":
		if ims[0:len(ims)-1] == lmd:
			status_code = 304
			string = "HTTP/1.1 304 Not Modified\n"
			b = bytearray()
			l = 0
		else:
			for row in arange:
					
				row=row.split("-")
				if row[0] == "" or row[0]=="\r":
					a = len(b)-int(row[1])
					b2 = len(b)
				elif row[1] == "\r" or row[1] == "":
					a = int(row[0])
					b2 = len(b)
				else:
					a = int(row[0])
					b2 = int(row[1])
				if int(a) > l or int(a) > int(b2):
					break
			
				b1 = b1 + b[a-1:b2]
			b = b1
			
			if int(a) > l1 or int(a) > int(b2):
				status_code = 416
				string = "HTTP/1.1 416 Range Not Satisfiable\n"
				b = bytearray()
				l = 0
			elif len(b) < l1:
				status_code = 206
				string = "HTTP/1.1 206 Partial Content\n"
				l = len(b)
			else:
				status_code = 200
				string = "HTTP/1.1 200 OK\n"
				l = l1
	else:
		status_code = 200
		string = "HTTP/1.1 200 OK\n"
	string += "Date: " +(time.strftime("%a, %d %b %Y %I:%M:%S %p %Z", time.gmtime()))
	string += "\nServer: Harsha/2.4.41 (Ubuntu)\n"
	string += "Last-Modified: " +lmd + "\n"
	string += "Content-Type: application/application/vnd.ms-powerpoint\n"
	if cookieval == "" or method == "POST":
		pass
	else:
		string += "Set-Cookie: "+cookieval+"\n"
	if method == "POST" or method == "GET":
		string += "Content-Length: " + str(l) + "\n"
		data = str(b)
		result = hashlib.md5(bytes(data,'utf-8'))
		result = result.digest()
		result = bytes(result)
		md5 = base64.b64encode(result)
		md5 = md5.decode('utf-8')
		string+="Content-md5: " + md5 + "\n"
	elif method == "HEAD":
		string += "Content-Length: " + str(l1) + "\n"
		l=l1
	string += "Connection: close\n\n"
	if method == "POST" or method == "GET":
		output = string.encode() + b
	else:
		output = string.encode()
	connectionSocket.send(output)
	connectionSocket.close()
	maxcon-=1

	#access log
	#status_code=200
	accesslogfn(client_addr,query,status_code,l,referer,user_agent,accesslog)
					
	#error log
	errorlogs(client_addr,port,referer1,errorlog)
	
def doc(method,connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims):
	###print(method)
	global client
	global accesslog
	global maxcon
	global errorlog
	lmd = time.ctime(os.path.getmtime(filename))
	lmd = lmd.split(" ")
	lmd = lmd[0] +", "+lmd[2]+" "+lmd[1]+" "+lmd[4]+" "+lmd[3] + " "+"GMT"
	with open(filename, "rb") as image:
		f = image.read()
		b = bytearray(f)	
	a=0	
	b2=0
	l = len(b)
	l1 = l
	b1 = bytearray()
	if arange and method == "GET" and (not ims):
		for row in arange:		
			row=row.split("-")
			if row[0] == "" or row[0]=="\r":
				a = len(b)-int(row[1])
				b2 = len(b)
			elif row[1] == "\r" or row[1] == "":
				a = int(row[0])
				b2 = len(b)
			else:
				a = int(row[0])
				b2 = int(row[1])
			if int(a) > l or int(a) > int(b2):
				break
			b1 = b1 + b[a-1:b2]
		b = b1
		
		if int(a) > l1 or int(a) > int(b2):
			status_code = 416
			string = "HTTP/1.1 416 Range Not Satisfiable\n"
			b = bytearray()
			l=0
		elif len(b) < l1:
			status_code = 206
			string = "HTTP/1.1 206 Partial Content\n"
			l=len(b)
		else:
			status_code = 200
			string = "HTTP/1.1 200 OK\n"
			l=l1
	elif ims and (not arange) and (method == "GET" or method == "HEAD"):
		if ims[0:len(ims)-1] == lmd:
			status_code = 304
			string = "HTTP/1.1 304 Not Modified\n"
			b = bytearray()
			l=0
		else:
			status_code = 200
			string = "HTTP/1.1 200 OK\n"
			l=l1
	elif ims and arange and method == "GET":
		if ims[0:len(ims)-1] == lmd:
			status_code = 304
			string = "HTTP/1.1 304 Not Modified\n"
			b = bytearray()
			l=0
		else:
			for row in arange:
					
				row=row.split("-")
				if row[0] == "" or row[0]=="\r":
					a = len(b)-int(row[1])
					b2 = len(b)
				elif row[1] == "\r" or row[1] == "":
					a = int(row[0])
					b2 = len(b)
				else:
					a = int(row[0])
					b2 = int(row[1])
				if int(a) > l or int(a) > int(b2):
					break
				b1 = b1 + b[a-1:b2]
			b = b1
		
			if int(a) > l1 or int(a) > int(b2): 
				status_code = 416
				string = "HTTP/1.1 416 Range Not Satisfiable\n"
				b = bytearray()
				l=0
			elif len(b) < l1:
				status_code = 206
				string = "HTTP/1.1 206 Partial Content\n"
				l=len(b)
			else:
				status_code = 200
				string = "HTTP/1.1 200 OK\n"
				l=l1

	else:
		status_code = 200
		string = "HTTP/1.1 200 OK\n"
	string += "Date: " +(time.strftime("%a, %d %b %Y %I:%M:%S %p %Z", time.gmtime()))
	string += "\nServer: Harsha/2.4.41 (Ubuntu)\n"
	string += "Last-Modified: " +lmd + "\n"
	string += "Content-Type: application/msword\n"
	if cookieval == "" or method == "POST":
		pass
	else:
		string += "Set-Cookie: "+cookieval+"\n"
	if method == "POST" or method == "GET":
		string += "Content-Length: " + str(l) + "\n"
		data = str(b)
		result = hashlib.md5(bytes(data,'utf-8'))
		result = result.digest()
		result = bytes(result)
		md5 = base64.b64encode(result)
		md5 = md5.decode('utf-8')
		string+="Content-md5: " + md5 + "\n"
	elif method == "HEAD":
		string += "Content-Length: " + str(l1) + "\n"
		l=l1
	string += "Connection: close\n\n"
	
	if method == "POST" or method == "GET":
		output = string.encode() + b
	else:
		output = string.encode()
	connectionSocket.send(output)
	connectionSocket.close()
	maxcon-=1

	#access log
	
	accesslogfn(client_addr,query,status_code,l,referer,user_agent,accesslog)
					
	#error log
	errorlogs(client_addr,port,referer1,errorlog)
	
def docx(method,connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims):
	###print(method)
	global client
	global accesslog
	global maxcon
	global errorlog
	with open(filename, "rb") as image:
		f = image.read()
		b = bytearray(f)	
	a=0	
	b2=0
	l = len(b)
	l1 = l
	b1 = bytearray()
	lmd = time.ctime(os.path.getmtime(filename))
	lmd = lmd.split(" ")
	lmd = lmd[0] +", "+lmd[2]+" "+lmd[1]+" "+lmd[4]+" "+lmd[3] + " "+"GMT"
	if arange and method == "GET" and (not ims):
		for row in arange:		
			row=row.split("-")
			if row[0] == "" or row[0]=="\r":
				a = len(b)-int(row[1])
				b2 = len(b)
			elif row[1] == "\r" or row[1] == "":
				a = int(row[0])
				b2 = len(b)
			else:
				a = int(row[0])
				b2 = int(row[1])
			if int(a) > l or int(a) > int(b2):
				break
			b1 = b1 + b[a-1:b2]
		b = b1
		
		if int(a) > l1 or int(a) > int(b2):
			status_code = 416
			string = "HTTP/1.1 416 Range Not Satisfiable\n"
			b = bytearray()
			l=0
		elif len(b) < l1:
			status_code = 206
			string = "HTTP/1.1 206 Partial Content\n"
			l=len(b)
		else:
			status_code = 200
			string = "HTTP/1.1 200 OK\n"
			l=l1
	elif ims and (not arange) and (method == "GET" or method == "HEAD"):
		if ims[0:len(ims)-1] == lmd:
			status_code = 304
			string = "HTTP/1.1 304 Not Modified\n"
			b = bytearray()
			l=0
		else:
			status_code = 200
			string = "HTTP/1.1 200 OK\n"
			l=l1
	elif ims and arange and method == "GET":
		if ims[0:len(ims)-1] == lmd:
			status_code = 304
			string = "HTTP/1.1 304 Not Modified\n"
			b = bytearray()
			l=0
		else:
			for row in arange:
				row=row.split("-")
				if row[0] == "" or row[0]=="\r":
					a = len(b)-int(row[1])
					b2 = len(b)
				elif row[1] == "\r" or row[1] == "":
					a = int(row[0])
					b2 = len(b)
				else:
					a = int(row[0])
					b2 = int(row[1])
				if int(a) > l or int(a) > int(b2):
					break
				b1 = b1 + b[a-1:b2]
			b = b1
			
			if int(a) > l1 or int(a) > int(b2):
				status_code = 416
				string = "HTTP/1.1 416 Range Not Satisfiable\n"
				b = bytearray()
				l=0
			elif len(b) < l1:
				status_code = 206
				string = "HTTP/1.1 206 Partial Content\n"
				l=len(b)
			else:
				status_code = 200
				string = "HTTP/1.1 200 OK\n"
				l=l1
	else:
		status_code = 200
		string = "HTTP/1.1 200 OK\n"
		l=l1
	string += "Date: " +(time.strftime("%a, %d %b %Y %I:%M:%S %p %Z", time.gmtime()))
	string += "\nServer: Harsha/2.4.41 (Ubuntu)\n"
	string += "Last-Modified: " +lmd + "\n"
	string += "Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document\n"
	if cookieval == "" or method == "POST":
		pass
	else:
		string += "Set-Cookie: "+cookieval+"\n"
	if method == "POST" or method == "GET":
		string += "Content-Length: " + str(l) + "\n"
		data = str(b)
		result = hashlib.md5(bytes(data,'utf-8'))
		result = result.digest()
		result = bytes(result)
		md5 = base64.b64encode(result)
		md5 = md5.decode('utf-8')
		string+="Content-md5: " + md5 + "\n"
	elif method == "HEAD":
		string += "Content-Length: " + str(l1) + "\n"
		l=l1	
	string += "Connection: close\n\n"
	if method == "POST" or method == "GET":
		output = string.encode() + b
	else:
		output = string.encode()
	connectionSocket.send(output)
	connectionSocket.close()
	maxcon-=1

	#access log
	accesslogfn(client_addr,query,status_code,l,referer,user_agent,accesslog)
					
	#error log
	errorlogs(client_addr,port,referer1,errorlog)
	
def pptx(method,connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims):
	global client
	global accesslog
	global maxcon
	global errorlog
	with open(filename, "rb") as image:
		f = image.read()
		b = bytearray(f)
	lmd = time.ctime(os.path.getmtime(filename))
	lmd = lmd.split(" ")
	lmd = lmd[0] +", "+lmd[3]+" "+lmd[1]+" "+lmd[5]+" "+lmd[4] + " "+"GMT"
		
	a=0	
	b2=0
	l = len(b)
	l1 = l
	b1 = bytearray()
	if arange and method == "GET" and (not ims):
		for row in arange:	
			row=row.split("-")
			if row[0] == "" or row[0]=="\r":
				a = len(b)-int(row[1])
				b2 = len(b)
			elif row[1] == "\r" or row[1] == "":
				a = int(row[0])
				b2 = len(b)
			else:
				a = int(row[0])
				b2 = int(row[1])
			if int(a) > l or int(a) > int(b2):
				break
			
			b1 = b1 + b[a-1:b2]
		b = b1
	
		if int(a) > l1 or int(a) > int(b2):
			status_code = 416
			string = "HTTP/1.1 416 Range Not Satisfiable\n"
			b = bytearray()
			l=0
		elif len(b) < l1:
			status_code = 206
			string = "HTTP/1.1 206 Partial Content\n"
			l=len(b)
		else:
			status_code = 200
			string = "HTTP/1.1 200 OK\n"
			l=l1
	elif ims and (not arange) and (method == "GET" or method == "HEAD"):
		if ims[0:len(ims)-1] == lmd:
			status_code = 304
			string = "HTTP/1.1 304 Not Modified\n"
			b = bytearray()
			l=0
		else:
			status_code = 200
			string = "HTTP/1.1 200 OK\n"
			l=l1
	elif ims and arange and method == "GET":
		if ims[0:len(ims)-1] == lmd:
			status_code = 304
			string = "HTTP/1.1 304 Not Modified\n"
			b = bytearray()
			l=0
		else:
			for row in arange:
				row=row.split("-")
				if row[0] == "" or row[0]=="\r":
					a = len(b)-int(row[1])
					b2 = len(b)
				elif row[1] == "\r" or row[1] == "":
					a = int(row[0])
					b2 = len(b)
				else:
					a = int(row[0])
					b2 = int(row[1])
				if int(a) > l or int(a) > int(b2):
					break
				b1 = b1 + b[a-1:b2]
			b = b1
			l = len(b)
			if int(a) > l1 or int(a) > int(b2):
				status_code = 416
				string = "HTTP/1.1 416 Range Not Satisfiable\n"
				b = bytearray()
				l=0
			elif len(b) < l1:
				status_code = 206
				string = "HTTP/1.1 206 Partial Content\n"
				l=len(b)
			else:
				status_code = 200
				string = "HTTP/1.1 200 OK\n"
				l=l1

	else:
		status_code = 200
		string = "HTTP/1.1 200 OK\n"
	string += "Date: " +(time.strftime("%a, %d %b %Y %I:%M:%S %p %Z", time.gmtime()))
	string += "\nServer: Harsha/2.4.41 (Ubuntu)\n"
	string += "Last-Modified: " +lmd + "\n"
	string += "Content-Type: application/application/vnd.ms-powerpoint\n"
	if cookieval == "" or method == "POST":
		pass
	else:
		string += "Set-Cookie: "+cookieval+"\n"
	if method == "POST" or method == "GET":
		string += "Content-Length: " + str(l) + "\n"
		data = str(b)
		result = hashlib.md5(bytes(data,'utf-8'))
		result = result.digest()
		result = bytes(result)
		md5 = base64.b64encode(result)
		md5 = md5.decode('utf-8')
		string+="Content-md5: " + md5 + "\n"
	elif method == "HEAD":
		string += "Content-Length: " + str(l1) + "\n"
		l1=l
	string += "Connection: close\n\n"
	if method == "POST" or method == "GET":
		output = string.encode() + b
	else:
		output = string.encode()
	connectionSocket.send(output)
	connectionSocket.close()
	maxcon-=1

	#access log
	accesslogfn(client_addr,query,status_code,len(b),referer,user_agent,accesslog)
					
	#error log
	errorlogs(client_addr,port,referer1,errorlog)
	

	
def zip1(method,connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims):
	###print(method)
	global client
	global accesslog
	global maxcon
	global errorlog
	with open(filename, "rb") as image:
		f = image.read()
		b = bytearray(f)	
	a=0	
	b2=0
	l = len(b)
	l1 = l
	b1 = bytearray()
	lmd = time.ctime(os.path.getmtime(filename))
	lmd = lmd.split(" ")
	lmd = lmd[0] +", "+lmd[3]+" "+lmd[1]+" "+lmd[5]+" "+lmd[4] + " "+"GMT"
	if arange and method == "GET" and (not ims):
		for row in arange:	
			row=row.split("-")
			if row[0] == "" or row[0]=="\r":
				a = len(b)-int(row[1])
				b2 = len(b)
			elif row[1] == "\r" or row[1] == "":
				a = int(row[0])
				b2 = len(b)
			else:
				a = int(row[0])
				b2 = int(row[1])
			if int(a) > l or int(a) > int(b2):
				break
			b1 = b1 + b[a-1:b2]
		b = b1
		if int(a) > l1 or int(a) > int(b2):
			status_code = 416
			string = "HTTP/1.1 416 Range Not Satisfiable\n"
			b = bytearray()
			l=0
		elif len(b) < l1:
			status_code = 206
			string = "HTTP/1.1 206 Partial Content\n"
			l=len(b)
		else:
			status_code = 200
			string = "HTTP/1.1 200 OK\n"
			l=l1
	elif ims and (not arange) and (method == "GET" or method == "HEAD"):
		if ims[0:len(ims)-1] == lmd:
			status_code = 304
			string = "HTTP/1.1 304 Not Modified\n"
			b = bytearray()
			l=0
		else:
			status_code = 200
			string = "HTTP/1.1 200 OK\n"
			l=l1
	elif ims and arange and method == "GET":
		if ims[0:len(ims)-1] == lmd:
			status_code = 304
			string = "HTTP/1.1 304 Not Modified\n"
			b = bytearray()
			l = 0
		else:
			for row in arange:
					
				row=row.split("-")
				if row[0] == "" or row[0]=="\r":
					a = len(b)-int(row[1])
					b2 = len(b)
				elif row[1] == "\r" or row[1] == "":
					a = int(row[0])
					b2 = len(b)
				else:
					a = int(row[0])
					b2 = int(row[1])
				if int(a) > l or int(a) > int(b2):
					break
				b1 = b1 + b[a-1:b2]
			b = b1
			
			if int(a) > l1 or int(a) > int(b2):
				status_code = 416
				string = "HTTP/1.1 416 Range Not Satisfiable\n"
				b = bytearray()
				l=0
			elif len(b) < l1:
				status_code = 206
				string = "HTTP/1.1 206 Partial Content\n"
				l=len(b)
			else:
				status_code = 200
				string = "HTTP/1.1 200 OK\n"
				l=l1
	else:
		status_code = 200
		string = "HTTP/1.1 200 OK\n"
	string += "Date: " +(time.strftime("%a, %d %b %Y %I:%M:%S %p %Z", time.gmtime()))
	string += "\nServer: Harsha/2.4.41 (Ubuntu)\n"
	string += "Last-Modified: " +lmd + "\n"
	string += "Content-Type: application/zip\n"
	if cookieval == "" or method == "POST":
		pass
	else:
		string += "Set-Cookie: "+cookieval+"\n"	
	if method == "POST" or method == "GET":
		string += "Content-Length: " + str(l) + "\n"
		data = str(b)
		result = hashlib.md5(bytes(data,'utf-8'))
		result = result.digest()
		result = bytes(result)
		md5 = base64.b64encode(result)
		md5 = md5.decode('utf-8')
		string+="Content-md5: " + md5 + "\n"
	elif method == "HEAD":
		string += "Content-Length: " + str(l1) + "\n"
		l=l1	
	string += "Connection: close\n\n"
	if method == "POST" or method == "GET":
		output = string.encode() + b
	else:
		output = string.encode()
	connectionSocket.send(output)
	connectionSocket.close()
	maxcon-=1

	#access log
	accesslogfn(client_addr,query,status_code,l,referer,user_agent,accesslog)
					
	#error log
	errorlogs(client_addr,port,referer1,errorlog)
	
def z7(method,connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims):
	###print(method)
	global client
	global accesslog
	global maxcon
	global errorlog
	with open(filename, "rb") as image:
		f = image.read()
		b = bytearray(f)
	a=0	
	b2=0
	l = len(b)
	l1 = l
	b1 = bytearray()
	lmd = time.ctime(os.path.getmtime(filename))
	lmd = lmd.split(" ")
	lmd = lmd[0] +", "+lmd[3]+" "+lmd[1]+" "+lmd[5]+" "+lmd[4] + " "+"GMT"
	if arange and method == "GET" and (not ims):
		for row in arange:		
			row=row.split("-")
			if row[0] == "" or row[0]=="\r":
				a = len(b)-int(row[1])
				b2 = len(b)
			elif row[1] == "\r" or row[1] == "":
				a = int(row[0])
				b2 = len(b)
			else:
				a = int(row[0])
				b2 = int(row[1])
			if int(a) > l or int(a) > int(b2):
				break
			b1 = b1 + b[a-1:b2]
		b = b1
		
		if int(a) > l1 or int(a) > int(b2):
			status_code = 416
			string = "HTTP/1.1 416 Range Not Satisfiable\n"
			b = bytearray()
			l=0
		elif len(b) < l1:
			status_code = 206
			string = "HTTP/1.1 206 Partial Content\n"
			l=len(b)
		else:
			status_code = 200
			string = "HTTP/1.1 200 OK\n"
			l=l1
	elif ims and (not arange) and (method == "GET" or method == "HEAD"):
		if ims[0:len(ims)-1] == lmd:
			status_code = 304
			string = "HTTP/1.1 304 Not Modified\n"
			b = bytearray()
			l=0
		else:
			status_code = 200
			string = "HTTP/1.1 200 OK\n"
			l=l1
	elif ims and arange and method == "GET":
		if ims[0:len(ims)-1] == lmd:
			status_code = 304
			string = "HTTP/1.1 304 Not Modified\n"
			b = bytearray()
			l=0
		else:
			for row in arange:
				row=row.split("-")
				if row[0] == "" or row[0]=="\r":
					a = len(b)-int(row[1])
					b2 = len(b)
				elif row[1] == "\r" or row[1] == "":
					a = int(row[0])
					b2 = len(b)
				else:
					a = int(row[0])
					b2 = int(row[1])
				if int(a) > l or int(a) > int(b2):
					break
				b1 = b1 + b[a-1:b2]
			b = b1
			l = len(b)
			if int(a) > l1 or int(a) > int(b2):
				status_code = 416
				string = "HTTP/1.1 416 Range Not Satisfiable\n"
				b = bytearray()
				l=0
			elif len(b) < l1:
				status_code = 206
				string = "HTTP/1.1 206 Partial Content\n"
				l=len(b)
			else:
				status_code = 200
				string = "HTTP/1.1 200 OK\n"
				l=l1
	else:
		status_code = 200
		string = "HTTP/1.1 200 OK\n"
	string += "Date: " +(time.strftime("%a, %d %b %Y %I:%M:%S %p %Z", time.gmtime()))
	string += "\nServer: Harsha/2.4.41 (Ubuntu)\n"
	string += "Last-Modified: " +lmd + "\n"
	string += "Content-Type: application/x-7z-compressed\n"
	if cookieval == "" or method == "POST":
		pass
	else:
		string += "Set-Cookie: "+cookieval+"\n"
		
	if method == "POST" or method == "GET":
		string += "Content-Length: " + str(l) + "\n"
		data = str(b)
		result = hashlib.md5(bytes(data,'utf-8'))
		result = result.digest()
		result = bytes(result)
		md5 = base64.b64encode(result)
		md5 = md5.decode('utf-8')
		string+="Content-md5: " + md5 + "\n"
	elif method == "HEAD":
		string += "Content-Length: " + str(l1) + "\n"
		l1=l
	string += "Connection: close\n\n"
	if method == "POST" or method == "GET":
		output = string.encode() + b
	else:
		output = string.encode()
	connectionSocket.send(output)
	connectionSocket.close()
	maxcon-=1

	#access log
	accesslogfn(client_addr,query,status_code,len(b),referer,user_agent,accesslog)
					
	#error log
	errorlogs(client_addr,port,referer1,errorlog)
	
def png(method,connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims):
	###print(method)
	global client
	global accesslog
	global maxcon
	global errorlog
	with open(filename, "rb") as image:
		f = image.read()
		b = bytearray(f)
	a=0	
	b2=0
	l = len(b)
	l1 = l
	b2 = bytearray()
	lmd = time.ctime(os.path.getmtime(filename))
	lmd = lmd.split(" ")
	lmd = lmd[0] +", "+lmd[2]+" "+lmd[1]+" "+lmd[4]+" "+lmd[3] + " "+"GMT"
	if arange and method == "GET" and (not ims):
		for row in arange:
					
			row=row.split("-")
			if row[0] == "" or row[0]=="\r":
				a = len(b)-int(row[1])
				b2 = len(b)
			elif row[1] == "\r" or row[1] == "":
				a = int(row[0])
				b2 = len(b)
			else:
				a = int(row[0])
				b2 = int(row[1])
			if int(a) > l or int(a) > int(b2):
				break
			b1 = b1 + b[a-1:b2]
		b = b1
		
		if int(a) > l1 or int(a) > int(b2):
			status_code = 416
			string = "HTTP/1.1 416 Range Not Satisfiable\n"
			b = bytearray()
			l=0
		elif len(b) < l1:
			status_code = 206
			string = "HTTP/1.1 206 Partial Content\n"
			l=len(b)
		else:
			status_code = 200
			string = "HTTP/1.1 200 OK\n"
			l=l1
	elif ims and (not arange) and (method == "GET" or method == "HEAD"):
		if ims[0:len(ims)-1] == lmd:
			status_code = 304
			string = "HTTP/1.1 304 Not Modified\n"
			b = bytearray()
			l=0
		else:
			status_code = 200
			string = "HTTP/1.1 200 OK\n"
			l=l1
	elif ims and arange and method == "GET":
		if ims[0:len(ims)-1] == lmd:
			status_code = 304
			string = "HTTP/1.1 304 Not Modified\n"
			b = bytearray()
			l=0
		else:
			for row in arange:
				row=row.split("-")
				if row[0] == "" or row[0]=="\r":
					a = len(b)-int(row[1])
					b2 = len(b)
				elif row[1] == "\r" or row[1] == "":
					a = int(row[0])
					b2 = len(b)
				else:
					a = int(row[0])
					b2 = int(row[1])
				if int(a) > l or int(a) > int(b2):
					break
				b1 = b1 + b[a-1:b2]
			b = b1
			
			if int(a) > l1 or int(a) > int(b2):
				status_code = 416
				string = "HTTP/1.1 416 Range Not Satisfiable\n"
				b = bytearray()
				l=0
			elif len(b) < l1:
				status_code = 206
				string = "HTTP/1.1 206 Partial Content\n"
				l=len(b)
			else:
				status_code = 200
				string = "HTTP/1.1 200 OK\n"
				l=l1
	else:
		status_code = 200
		string = "HTTP/1.1 200 OK\n"
		l=l1
	string += "Date: " +(time.strftime("%a, %d %b %Y %I:%M:%S %p %Z", time.gmtime()))
	string += "\nServer: Harsha/2.4.41 (Ubuntu)\n"
	string += "Last-Modified: " +lmd + "\n"
	string += "Content-Type: image/png\n"
	if cookieval == "" or method == "POST":
		pass
	else:
		string += "Set-Cookie: "+cookieval+"\n"
	if method == "POST" or method == "GET":
		string += "Content-Length: " + str(l) + "\n"
		data = str(b)
		result = hashlib.md5(bytes(data,'utf-8'))
		result = result.digest()
		result = bytes(result)
		md5 = base64.b64encode(result)
		md5 = md5.decode('utf-8')
		string+="Content-md5: " + md5 + "\n"
	elif method == "HEAD":
		string += "Content-Length: " + str(l1) + "\n"
		l=l1
	string += "Connection: close\n\n"
	if method == "POST" or method == "GET":
		output = string.encode() + b
	else:
		output = string.encode()
	connectionSocket.send(output)
	connectionSocket.close()
	maxcon-=1

	#access log
	accesslogfn(client_addr,query,status_code,len(b),referer,user_agent,accesslog)
					
	#error log
	errorlogs(client_addr,port,referer1,errorlog)
	
def jpg(method,connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims):
	###print(method)
	global client
	global accesslog
	global maxcon
	global errorlog
	with open(filename, "rb") as image:
		f = image.read()
		b = bytearray(f)	
	a=0	
	b2=0
	l = len(b)
	l1 = l
	b1 = bytearray()
	lmd = time.ctime(os.path.getmtime(filename))
	lmd = lmd.split(" ")
	lmd = lmd[0] +", "+lmd[2]+" "+lmd[1]+" "+lmd[4]+" "+lmd[3] + " "+"GMT"
	if arange and method == "GET" and (not ims):
		for row in arange:			
			row=row.split("-")
			if row[0] == "" or row[0]=="\r":
				a = len(b)-int(row[1])
				b2 = len(b)
			elif row[1] == "\r" or row[1] == "":
				a = int(row[0])
				b2 = len(b)
			else:
				a = int(row[0])
				b2 = int(row[1])
			if int(a) > l or int(a) > int(b2):
				break
			b1 = b1 + b[a-1:b2]
		b = b1
		if int(a) > l1 or int(a) > int(b2):
			status_code = 416
			string = "HTTP/1.1 416 Range Not Satisfiable\n"
			b = bytearray()
			l=0
		elif len(b) < l1:
			status_code = 206
			string = "HTTP/1.1 206 Partial Content\n"
			l=len(b)
		else:
			status_code = 200
			string = "HTTP/1.1 200 OK\n"
			l=l1
	elif ims and (not arange) and (method == "GET" or method == "HEAD"):
		if ims[0:len(ims)-1] == lmd:
			status_code = 304
			string = "HTTP/1.1 304 Not Modified\n"
			b = bytearray()
			l=0
		else:
			status_code = 200
			string = "HTTP/1.1 200 OK\n"
			l=l1
	elif ims and arange and method == "GET":
		if ims[0:len(ims)-1] == lmd:
			status_code = 304
			string = "HTTP/1.1 304 Not Modified\n"
			b = bytearray()
			l=0
		else:
			for row in arange:
					
				row=row.split("-")
				if row[0] == "" or row[0]=="\r":
					a = len(b)-int(row[1])
					b2 = len(b)
				elif row[1] == "\r" or row[1] == "":
					a = int(row[0])
					b2 = len(b)
				else:
					a = int(row[0])
					b2 = int(row[1])
				if int(a) > l or int(a) > int(b2):
					break
				b1 = b1 + b[a-1:b2]
			b = b1
			if int(a) > l1 or int(a) > int(b2):
				status_code = 416
				string = "HTTP/1.1 416 Range Not Satisfiable\n"
				b = bytearray()
				l=0
			elif len(b) < l1:
				status_code = 206
				string = "HTTP/1.1 206 Partial Content\n"
				l=len(b)
			else:
				status_code = 200
				string = "HTTP/1.1 200 OK\n"
				l=l1
	else:
		status_code = 200
		string = "HTTP/1.1 200 OK\n"
		l=l1
	string += "Date: " +(time.strftime("%a, %d %b %Y %I:%M:%S %p %Z", time.gmtime()))
	string += "\nServer: Harsha/2.4.41 (Ubuntu)\n"
	string += "Last-Modified: " +lmd + "\n"
	string += "Content-Type: image/jpg\n"
	if cookieval == "" or method == "POST":
		pass
	else:
		string += "Set-Cookie: "+cookieval+"\n"
	if method == "POST" or method == "GET":
		string += "Content-Length: " + str(l) + "\n"
		data = str(b)
		result = hashlib.md5(bytes(data,'utf-8'))
		result = result.digest()
		result = bytes(result)
		md5 = base64.b64encode(result)
		md5 = md5.decode('utf-8')
		string+="Content-md5: " + md5 + "\n"
	elif method == "HEAD":
		string += "Content-Length: " + str(l1) + "\n"
		l=l1
	string += "Connection: close\n\n"
	if method == "POST" or method == "GET":
		output = string.encode() + b
	else:
		output = string.encode()
	connectionSocket.send(output)
	connectionSocket.close()
	maxcon-=1

	#access log
	accesslogfn(client_addr,query,status_code,l,referer,user_agent,accesslog)
					
	#error log
	errorlogs(client_addr,port,referer1,errorlog)
	
def mp4(method,connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims):
	global client
	global accesslog
	global maxcon
	global errorlog
	with open(filename, "rb") as image:
		f = image.read()
		b = bytearray(f)
	a=0	
	b2=0
	l = len(b)
	l1 = l
	b1 = bytearray()
	lmd = time.ctime(os.path.getmtime(filename))
	lmd = lmd.split(" ")
	lmd = lmd[0] +", "+lmd[2]+" "+lmd[1]+" "+lmd[4]+" "+lmd[3] + " "+"GMT"
	if arange and method == "GET" and (not ims):
		for row in arange:
			row=row.split("-")
			if row[0] == "" or row[0]=="\r":
				a = len(b)-int(row[1])
				b2 = len(b)
			elif row[1] == "\r" or row[1] == "":
				a = int(row[0])
				b2 = len(b)
			else:
				a = int(row[0])
				b2 = int(row[1])
			if int(a) > l or int(a) > int(b2):
				break
			b1 = b1 + b[a-1:b2]
		b = b1
		if int(a) > l1 or int(a) > int(b2):
			status_code = 416
			string = "HTTP/1.1 416 Range Not Satisfiable\n"
			b = bytearray()
			l=0
		elif len(b) < l1:
			status_code = 206
			string = "HTTP/1.1 206 Partial Content\n"
			l=len(b)
		else:
			status_code = 200
			string = "HTTP/1.1 200 OK\n"
			l=l1
	elif ims and (not arange) and (method == "GET" or method == "HEAD"):
		if ims[0:len(ims)-1] == lmd:
			status_code = 304
			string = "HTTP/1.1 304 Not Modified\n"
			b = bytearray()
			l=0
		else:
			status_code = 200
			string = "HTTP/1.1 200 OK\n"
			l=l1
	elif ims and arange and method == "GET":
		if ims[0:len(ims)-1] == lmd:
			status_code = 304
			string = "HTTP/1.1 304 Not Modified\n"
			b = bytearray()
			l=0
		else:
			for row in arange:
					
				row=row.split("-")
				if row[0] == "" or row[0]=="\r":
					a = len(b)-int(row[1])
					b2 = len(b)
				elif row[1] == "\r" or row[1] == "":
					a = int(row[0])
					b2 = len(b)
				else:
					a = int(row[0])
					b2 = int(row[1])
				if int(a) > l or int(a) > int(b2): 
					break
				b1 = b1 + b[a-1:b2]
			b = b1
			if int(a) > l1 or int(a) > int(b1):
				status_code = 416
				string = "HTTP/1.1 416 Range Not Satisfiable\n"
				b = bytearray()
				l=0
			elif len(b) < l1 or int(a) > int(b2):
				status_code = 206
				string = "HTTP/1.1 206 Partial Content\n"
				l=len(b)
			else:
				status_code = 200
				string = "HTTP/1.1 200 OK\n"
				l=l1
	else:
		status_code = 200
		string = "HTTP/1.1 200 OK\n"
		l=l1
	string += "Date: " +(time.strftime("%a, %d %b %Y %I:%M:%S %p %Z", time.gmtime()))
	string += "\nServer: Harsha/2.4.41 (Ubuntu)\n"
	string += "Last-Modified: " +lmd + "\n"
	string += "Content-Type: video/mp4\n"
	if cookieval == "" or method == "POST":
		pass
	else:
		string += "Set-Cookie: "+cookieval+"\n"
	if method == "POST" or method == "GET":
		string += "Content-Length: " + str(l) + "\n"
		data = str(b)
		result = hashlib.md5(bytes(data,'utf-8'))
		result = result.digest()
		result = bytes(result)
		md5 = base64.b64encode(result)
		md5 = md5.decode('utf-8')
		string+="Content-md5: " + md5 + "\n"
	elif method == "HEAD":
		string += "Content-Length: " + str(l1) + "\n"
		l=l1	
	string += "Connection: close\n\n"
	if method == "POST" or method == "GET":
		output = string.encode() + b
	else:
		output = string.encode()
	connectionSocket.send(output)
	connectionSocket.close()
	maxcon-=1
	
	#accesslog
	accesslogfn(client_addr,query,status_code,l,referer,user_agent,accesslog)
					
	#error log
	errorlogs(client_addr,port,referer1,errorlog)
	
def gif(method,connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims):
	###print(method)
	global client
	global accesslog
	global maxcon
	global errorlog
	with open(filename, "rb") as image:
		f = image.read()
		b = bytearray(f)	
	a=0	
	b2=0
	l = len(b)
	l1 = l
	b1 = bytearray()
	lmd = time.ctime(os.path.getmtime(filename))
	lmd = lmd.split(" ")
	lmd = lmd[0] +", "+lmd[3]+" "+lmd[1]+" "+lmd[5]+" "+lmd[4] + " "+"GMT"
	if arange and method == "GET" and (not ims):
		for row in arange:
			row=row.split("-")
			if row[0] == "" or row[0]=="\r":
				a = len(b)-int(row[1])
				b2 = len(b)
			elif row[1] == "\r" or row[1] == "":
				a = int(row[0])
				b2 = len(b)
			else:
				a = int(row[0])
				b2 = int(row[1])
			if int(a) > l or int(a) > int(b2):
				break
			b1 = b1 + b[a-1:b2]
		b = b1
		if int(a) > l1 or int(a) > int(b2):
			status_code = 416
			string = "HTTP/1.1 416 Range Not Satisfiable\n"
			b = bytearray()
			l=0
		elif len(b) < l1 :
			status_code = 206
			string = "HTTP/1.1 206 Partial Content\n"
			l=len(b)
		else:
			status_code = 200
			string = "HTTP/1.1 200 OK\n"
			l=l1
	elif ims and (not arange) and (method == "GET" or method == "HEAD"):
		if ims[0:len(ims)-1] == lmd:
			status_code = 304
			string = "HTTP/1.1 304 Not Modified\n"
			b = bytearray()
			l=0
		else:
			status_code = 200
			string = "HTTP/1.1 200 OK\n"
			l=l1
	elif ims and arange and method == "GET":
		if ims[0:len(ims)-1] == lmd:
			status_code = 304
			string = "HTTP/1.1 304 Not Modified\n"
			b = bytearray()
			l=0
		else:
			for row in arange:
				row=row.split("-")
				if row[0] == "" or row[0]=="\r":
					a = len(b)-int(row[1])
					b2 = len(b)
				elif row[1] == "\r" or row[1] == "":
					a = int(row[0])
					b2 = len(b)
				else:
					a = int(row[0])
					b2 = int(row[1])
				if int(a) > l or int(a) > int(b2):
					break
				b1 = b1 + b[a-1:b2]
			b = b1
			if int(a) > l1 or int(a) > int(b2):
				status_code = 416
				string = "HTTP/1.1 416 Range Not Satisfiable\n"
				b = bytearray()
				l=0
			elif len(b) < l1:
				status_code = 206
				string = "HTTP/1.1 206 Partial Content\n"
				l=len(b)
			else:
				status_code = 200
				string = "HTTP/1.1 200 OK\n"
				l=l1
	else:
		status_code = 200
		string = "HTTP/1.1 200 OK\n"
	string += "Date: " +(time.strftime("%a, %d %b %Y %I:%M:%S %p %Z", time.gmtime()))
	string += "\nServer: Harsha/2.4.41 (Ubuntu)\n"
	string += "Last-Modified: " +lmd + "\n"
	string += "Content-Type: image/gif\n"
	if cookieval == "" or method == "POST":
		pass
	else:
		string += "Set-Cookie: "+cookieval+"\n"	
	if method == "POST" or method == "GET":
		string += "Content-Length: " + str(l) + "\n"
		data = str(b)
		result = hashlib.md5(bytes(data,'utf-8'))
		result = result.digest()
		result = bytes(result)
		md5 = base64.b64encode(result)
		md5 = md5.decode('utf-8')
		string+="Content-md5: " + md5 + "\n"
	elif method == "HEAD":
		string += "Content-Length: " + str(l1) + "\n"
		l=l1
	string += "Connection: close\n\n"
	if method == "POST" or method == "GET":
		output = string.encode() + b
	else:
		output = string.encode()
	connectionSocket.send(output)
	connectionSocket.close()
	maxcon-=1

	#access log
	accesslogfn(client_addr,query,status_code,l,referer,user_agent,accesslog)
					
	#error log
	errorlogs(client_addr,port,referer1,errorlog)
	
def mp3(method,connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims):
	global client
	global accesslog
	global maxcon
	global errorlog
	with open(filename, "rb") as image:
		f = image.read()
		b = bytearray(f)
	a=0	
	b2=0
	l = len(b)
	l1 = l
	b1 = bytearray()
	lmd = time.ctime(os.path.getmtime(filename))
	lmd = lmd.split(" ")
	lmd = lmd[0] +", "+lmd[2]+" "+lmd[1]+" "+lmd[4]+" "+lmd[3] + " "+"GMT"
	if arange and method == "GET" and (not ims):
		for row in arange:	
			row=row.split("-")
			if row[0] == "" or row[0]=="\r":
				a = len(b)-int(row[1])
				b2 = len(b)
			elif row[1] == "\r" or row[1] == "":
				a = int(row[0])
				b2 = len(b)
			else:
				a = int(row[0])
				b2 = int(row[1])
			if int(a) > l or int(a) > int(b2):
				break
			b1 = b1 + b[a-1:b2]
		b = b1
		if int(a) > l1 or int(a) > int(b2):
			status_code = 416
			string = "HTTP/1.1 416 Range Not Satisfiable\n"
			b = bytearray()
			l=0
		elif len(b) < l1:
			status_code = 206
			string = "HTTP/1.1 206 Partial Content\n"
			l=len(b)
		else:
			status_code = 200
			string = "HTTP/1.1 200 OK\n"
			l=l1
	elif ims and (not arange) and (method == "GET" or method == "HEAD"):
		if ims[0:len(ims)-1] == lmd:
			status_code = 304
			string = "HTTP/1.1 304 Not Modified\n"
			b = bytearray()
			l=0
		else:
			status_code = 200
			string = "HTTP/1.1 200 OK\n"
			l=l1
	elif ims and arange and method == "GET":
		if ims[0:len(ims)-1] == lmd:
			status_code = 304
			string = "HTTP/1.1 304 Not Modified\n"
			b = bytearray()
			l=0
		else:
			for row in arange:
				row=row.split("-")
				if row[0] == "" or row[0]=="\r":
					a = len(b)-int(row[1])
					b2 = len(b)
				elif row[1] == "\r" or row[1] == "":
					a = int(row[0])
					b2 = len(b)
				else:
					a = int(row[0])
					b2 = int(row[1])
				if int(a) > l or int(a) > int(b2):
					break
				b1 = b1 + b[a-1:b2]
			b = b1
			if int(a) > l1 or int(a) > int(b2):
				status_code = 416
				string = "HTTP/1.1 416 Range Not Satisfiable\n"
				b = bytearray()
				l=0
			elif len(b) < l1:
				status_code = 206
				string = "HTTP/1.1 206 Partial Content\n"
				l=len(b)
			else:
				status_code = 200
				string = "HTTP/1.1 200 OK\n"
				l=l1
	else:
		status_code = 200
		string = "HTTP/1.1 200 OK\n"
		l=l1
	string += "Date: " +(time.strftime("%a, %d %b %Y %I:%M:%S %p %Z", time.gmtime()))
	string += "\nServer: Harsha/2.4.41 (Ubuntu)\n"
	string += "Last-Modified: " +lmd + "\n"
	string += "Content-Type: audio/mp3\n"
	if cookieval == "" or method == "POST":
		pass
	else:
		string += "Set-Cookie: "+cookieval+"\n"	
	if method == "POST" or method == "GET":
		string += "Content-Length: " + str(l) + "\n"
		data = str(b)
		result = hashlib.md5(bytes(data,'utf-8'))
		result = result.digest()
		result = bytes(result)
		md5 = base64.b64encode(result)
		md5 = md5.decode('utf-8')
		string+="Content-md5: " + md5 + "\n"
	elif method == "HEAD":
		string += "Content-Length: " + str(l1) + "\n"
		l=l1
	string += "Connection: close\n\n"
	if method == "POST" or method == "GET":
		output = string.encode() + b
	else:
		output = string.encode()
	connectionSocket.send(output)
	connectionSocket.close()
	maxcon-=1

	#access log
	accesslogfn(client_addr,query,status_code,l,referer,user_agent,accesslog)
					
	#error log
	errorlogs(client_addr,port,referer1,errorlog)
	
def xml(method,connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims):
	global client
	global accesslog
	global maxcon
	global errorlog
	lmd = time.ctime(os.path.getmtime(filename))
	lmd = lmd.split(" ")
	lmd = lmd[0] +", "+lmd[2]+" "+lmd[1]+" "+lmd[4]+" "+lmd[3] + " "+"GMT"
	f = open(filename)
	fileoutput = f.read()
	l = len(fileoutput)
	l1 = l
	fileoutput1 = ""
	a=0
	b=0
	if arange and method == "GET" and (not ims):
		for row in arange:
			row=row.split("-")
			if row[0] == "" or row[0]=="\r":
				a = len(fileoutput)-int(row[1])
				b = len(fileoutput)
			elif row[1] == "\r" or row[1] == "":
				a = row[0]
				b = len(fileoutput)
			else:
				a = row[0]
				b = row[1]
			if int(a) > l or int(a) > int(b):
				break
			fileoutput1 += fileoutput[int(a)-1:int(b)]
		fileoutput = fileoutput1
		if int(a) > l1 or int(a) > int(b):
			status_code = 416
			string = "HTTP/1.1 416 Range Not Satisfiable\n"
			fileoutput = ""
			l=0
		elif len(fileoutput) < l1:
			status_code = 206
			string = "HTTP/1.1 206 Partial Content\n"
			l = len(fileoutput)
		else:
			status_code = 200
			string = "HTTP/1.1 200 OK\n"
			l=l1
	elif ims and (not arange) and (method == "GET" or method == "POST"):
		if ims[0:len(ims)-1] == lmd:
			status_code = 304
			string = "HTTP/1.1 304 Not Modified\n"
			fileoutput = ""
			l=0
		else:
			status_code = 200
			string = "HTTP/1.1 200 OK\n"
			l=l1
	elif ims and arange and method == "GET":
		if ims[0:len(ims)-1] == lmd:
			status_code = 304
			string = "HTTP/1.1 304 Not Modified\n"
			fileoutput = ""
			l=0
		else:
			for row in arange:
				row=row.split("-")
				if row[0] == "" or row[0]=="\r":
					a = len(fileoutput)-int(row[1])
					b = len(fileoutput)
				elif row[1] == "\r" or row[1] == "":
					a = row[0]
					b = len(fileoutput)
				else:
					a = row[0]
					b = row[1]
				if int(a) > l or int(a) > int(b):
					break
				fileoutput1 += fileoutput[int(a)-1:int(b)]
			fileoutput = fileoutput1
			l = len(fileoutput)
			if int(a) > l1 or int(a) > int(b):
				status_code = 416
				string = "HTTP/1.1 416 Range Not Satisfiable\n"
				fileoutput = ""
				l=0
			elif len(fileoutput) < l1:
				status_code = 206
				string = "HTTP/1.1 206 Partial Content\n"
				l = len(fileoutput)
			else:
				status_code = 200
				string = "HTTP/1.1 200 OK\n"
				l=l1
	else:
		status_code = 200
		string = "HTTP/1.1 200 OK\n"
		l=l1
	string += "Date: " +(time.strftime("%a, %d %b %Y %I:%M:%S %p %Z", time.gmtime()))
	string += "\nServer: Harsha/2.4.41 (Ubuntu)\n"
	string += "Last-Modified: " +lmd + "\n"
	string += "Content-Type: text/xml\n"
	if cookieval == "" or method == "POST":
		pass
	else:
		string += "Set-Cookie: "+cookieval+"\n"
	if method == "POST" or method == "GET":
		string += "Content-Length: " + str(l) + "\n"
		data = fileoutput
		result = hashlib.md5(bytes(data,'utf-8'))
		result = result.digest()
		result = bytes(result)
		md5 = base64.b64encode(result)
		md5 = md5.decode('utf-8')
		string+="Content-md5: " + md5 + "\n"
	elif method == "HEAD":
		string += "Content-Length: " + str(l1) + "\n"
		l=l1
	string += "Connection: close\n\n"
	if method == "POST" or method == "GET":
		output = string + fileoutput
	else:
		output = string
	connectionSocket.send(output.encode())
	connectionSocket.close()
	maxcon-=1

	#access log
	accesslogfn(client_addr,query,status_code,l,referer,user_agent,accesslog)
					
	#error log
	errorlogs(client_addr,port,referer1,errorlog)
	f.close()
	

#ConnectionThread
def connection(connectionSocket):
	cookieval = ""
	arange = None
	ims = None
	global client
	global maxcon
	global errorlog
	global accesslog
	global omg
	try:
		while True:
			#Receiving Data
			sentence = connectionSocket.recv(10240).decode()
			##print(sentence)
			#EXtracting User-Agent
			if "User-Agent" in sentence:
				user_agent = "\"" + ((sentence.split("User-Agent")[1]).split("\n")[0])[2:] 
				user_agent = user_agent[0:len(user_agent)-1] + "\""
			else:
				user_agent = "\"-\""

			#Referer	
			if "Referer" in sentence:
				referer = "\""+((sentence.split("Referer")[1]).split("\n")[0])[2:]
				referer = referer[0:len(referer)-1] + "\""
				referer1 = referer
			else:
				referer = "\"-\""
				referer1 = ""

			line = sentence.split("\n")
			query = "\"" + line[0][0:len(line[0])-1] +"\"" 		
			words = sentence.split(" ")

			#Client Address
			client_addr = ((str(connectionSocket).split(",")[6]).split("'")[1])

			#Port
			port = ((str(connectionSocket).split(","))[7].split(")>")[0])
			
			#RANGE
			if "Range" in sentence:
				arange = (((sentence.split("Range: Bytes = "))[1]).split("\n")[0]).split(",")

			#IF-MODIFIED-SINCE
			if "If-Modified-Since" in sentence:
				ims = ((sentence.split("If-Modified-Since: "))[1]).split("\n")[0]
	
			#COOKIE
			if ("Cookie" in sentence) or ("cookie" in sentence) or ("COOKIE" in sentence) :
				splitcookie = sentence.split("Cookie:")[1]
				splitid = splitcookie.split("id=")[1]
				cookie_id = splitid.split("\n")[0]
				cookie_id=cookie_id.strip()
				result1 = client.get(cookie_id)
				if result1 is not None:
					pass
				else:
					randomid = random.randint(1,10000000)
					new_date = datetime.now() + timedelta(30)
					msg = str(randomid).strip()+str(port).strip()
					client.set(msg,"id")
					cookieval="id="+msg+" ;Expires = " + new_date.strftime("%a, %d %b %Y %I:%M:%S GMT ")+" Domain:Localhost"
			else:
				randomid = random.randint(1,10000000)
				new_date = datetime.now() + timedelta(30)
				msg = str(randomid).strip()+str(port).strip()
				client.set(msg,"id")
				cookieval="id="+msg+" ;Expires = " + new_date.strftime("%a, %d %b %Y %I:%M:%S GMT ")+" Domain:Localhost"
				

			#GET Request
			if words[0] == "GET":
				##print(words[1])
				#Extracting File name  from a request
				if "/" == words[1]:
					filename = documentroot + "/"
				elif "?" in  words[1]:
					extension = (words[1].split("?"))[0]
					filename = extension
					extension =(extension.split("."))[1]
					filename = documentroot + filename
				else:
					extension =(words[1].split("."))[1]
					filename = words[1]
					filename = documentroot + filename

				if not path.exists(filename):
					filenotexists("POST",connectionSocket,words,client_addr,port,query,referer,referer1,user_agent)
					return
				elif not os.access(filename, os.R_OK):
					f = open("forbidden.html")
					fileoutput = f.read()
					string = "HTTP/1.1 403 Forbidden\n"
					string += "Date: " + (time.strftime("%a, %d %b %Y %I:%M:%S %p %Z", time.gmtime()))
					string += "\nServer: Harsha/2.4.41 (Ubuntu)\n"
					modifytime =  time.ctime(os.path.getmtime("forbidden.html"))
					string += "Last-Modified: " +modifytime
					string += "\nContent-Length: " +  str(len(fileoutput)) +"\n"
					string += "Connection: close\n"
					string += "Content-Type: text/html; charset=iso-8859-1\n\n"
					string = string + fileoutput
					connectionSocket.send(string.encode())
					connectionSocket.close()
					maxcon-=1
					#access log
					status_code=403
					accesslogfn(client_addr,query,status_code,len(fileoutput),referer,user_agent,accesslog)
					#error log
					permissiondeniederrorlog(client_addr,port,words[1],referer1,errorlog)
					f.close()
					return
				elif "/home/m/TY/CN_LAB/Project/Project/www/" == filename :
					fileaccess1 = open(errorlog,"w")
					f = open("index.html")
					fileoutput = f.read()
					string = "HTTP/1.1 200 OK\r\n"
					string += "Date: " +(time.strftime("%a, %d %b %Y %I:%M:%S %Z", time.gmtime()))+"\n"
					string += "Server: Harsha/2.4.41 (Ubuntu) \r\n"
					modifytime =  time.ctime(os.path.getmtime(filename))
					string += "Last-Modified: " +modifytime
					string += "\nAccept-Ranges: Bytes\r\n"
					string += "Content-Language: en\r\n"
					string += "Content-Length: " + str(len(fileoutput)) + "\r\n"
					string += "Connection: close\r\n"
					if cookieval == "":
						pass
					else:
						string += "Set-Cookie: "+cookieval+"\r\n"
					data = fileoutput
					result = hashlib.md5(bytes(data,'utf-8'))
					result = result.digest()
					result = bytes(result)
					md5 = base64.b64encode(result)
					md5 = md5.decode('utf-8')
					string+="Content-md5: " + md5 + "\r\n"
					string += "Content-Type: text/html\r\n\n"
					
					output = string + fileoutput
					connectionSocket.send(output.encode())
					connectionSocket.close()
					maxcon-=1
					status_code=200
					 
					#access log
					accesslogfn(client_addr,query,200,len(fileoutput),referer,user_agent,accesslog)
					#error log
					current = datetime.now()
					error = current.strftime("[%a %b %d %I:%M:%S.%f %Y]") + " [authz_core:debug] " + " [pid " + str(os.getpid()) + ":tid " +str(threading.current_thread().ident) + "]"+" mod_authz_core.c(817):"+" [client "+str(client_addr)+":"+str(port)+"]"+" AH01626: authorization result of Require all granted: granted"
					error1 = current.strftime("[%a %b %d %I:%M:%S.%f %Y]") + " [authz_core:debug] " + " [pid " + str(os.getpid()) + ":tid " +str(threading.current_thread().ident) + "]"+" mod_authz_core.c(817):"+" [client "+str(client_addr)+":"+str(port)+"]"+"  AH01626: authorization result of <RequireAny>: granted"
					if not referer1  == "":
						error = ", referer:" + referer1
						error1 = ", referer:" + referer1
					else:
						error += "\n"
						error1 += "\n"
					###print(error)	
					fileaccess1.write(error)
					fileaccess1.write(error1)	
					f.close()
					fileaccess1.close()
					return
				elif extension == "html" or extension == "HTML":
					##print("hello html")
					html("GET",filename,cookieval,connectionSocket,client_addr,port,query,referer,referer1,user_agent,arange,ims)
					return
				
					
				elif extension == "csv" or extension == "csv":
					csv("GET",connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims)
					return
				elif extension == "pdf" or extension == "PDF":
					pdf("GET",connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims)	
					return
				elif extension == "ppt" or extension == "PPT":
					ppt("GET",connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims)
					return
				elif extension == "doc" or extension == "DOC":
					doc("GET",connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims)
					return
				elif extension == "docx" or extension == "DOCX":
					docx("GET",connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims)
					return
				elif extension == "pptx" or extension == "PPTX":
					pptx("GET",connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims)
					return
				elif extension == "zip" or extension == "ZIP":
					zip1("GET",connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims)
					return
				elif extension == "7z" or extension == "7z":
					z7("GET",connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims)
					return
				elif extension == "xml" or extension == "XML":
					
					xml("GET",connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims)
					return
				elif extension == "png" or extension == "PNG":
					png("GET",connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims)
					return
				elif extension == "jpg" or extension == "jpeg" or  extension == "JPG" or extension == "JPEG":
					jpg("GET",connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims)
					return
				elif extension == "mp4" or extension == "MP4" :
					mp4("GET",connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims)
					return
				elif extension == "gif" or extension == "gif" :
					gif("GET",connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims)
					return
				elif extension == "mp3" or extension == "MP3" :
					mp3("GET",connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims)
					return
				else:
					f = open(filename)
					fileoutput = f.read()
					string = "HTTP/1.1 200 OK\n"
					string += "Date: " +(time.strftime("%a, %d %b %Y %I:%M:%S %p %Z", time.gmtime()))
					string += "\nServer: Harsha/2.4.41 (Ubuntu)\n"
					modifytime =  time.ctime(os.path.getmtime(filename))
					string += "Last-Modified: " +modifytime
					string += "\nContent-Length: " + str(len(fileoutput)) + "\n"
					string += "Connection: close\n"
					if cookieval == "":
						pass
					else:
						string += "Set-Cookie: "+cookieval+"\n"
					data = fileoutput
					result = hashlib.md5(bytes(data,'utf-8'))
					result = result.digest()
					result = bytes(result)
					md5 = base64.b64encode(result)
					md5 = md5.decode('utf-8')
					string+="Content-md5: " + md5 + "\n"
					string += "Content-Type: text/plain\n\n"
					output = string + fileoutput
					connectionSocket.send(output.encode())
					connectionSocket.close()
					maxcon-=1
					#access log
					status_code=200
					accesslogfn(client_addr,query,200,len(fileoutput),referer,user_agent,accesslog)
					
					#error log
					errorlogs(client_addr,port,referer1,errorlog)
					f.close()
					connectionSocket.close()
					return
			elif words[0] == "POST":
				if "/" == words[1]:
					filename = documentroot + "/"
				else:
					extension =(words[1].split("."))[1]
					filename = words[1]
					filename = documentroot + filename
				if not path.exists(filename):
					filenotexists("POST",connectionSocket,words[1],client_addr,port,query,referer,referer1,user_agent)
					return
				if not os.access(filename, os.R_OK):
					f = open("forbidden.html")
					fileoutput = f.read()
					string = "HTTP/1.1 403 Forbidden\n"
					string += "Date: " + (time.strftime("%a, %d %b %Y %I:%M:%S %p %Z", time.gmtime()))
					string += "\nServer: Harsha/2.4.41 (Ubuntu)\n"
					modifytime =  time.ctime(os.path.getmtime("forbidden.html"))
					string +="Last-Modified: " + modifytime
					string += "\nContent-Length: " +  str(len(fileoutput)) +"\n"
					string += "Connection: close\n"
					string += "Content-Type: text/html; charset=iso-8859-1\n\n"
					string = string + fileoutput
					
					connectionSocket.send(string.encode())
					connectionSocket.close()
					maxcon-=1
					status_code=403
					
					#accesslog
					accesslogfn(client_addr,query,status_code,len(fileoutput),referer,user_agent,accesslog)
					
					#error log
					permissiondeniederrorlog(client_addr,port,words[1],referer1,errorlog)
					f.close()
					return
				if "/home/m/TY/CN_LAB/Project/Project/www/" == filename :
					f = open("index.html")
					fileoutput = f.read()
					string = "HTTP/1.1 200 OK\n"
					string += "Date: " +(time.strftime("%a, %d %b %Y %I:%M:%S %p %Z", time.gmtime()))
					string += "\nServer: Harsha/2.4.41 (Ubuntu)\n"
					modifytime =  time.ctime(os.path.getmtime(filename))
					string += "Last-Modified: " +modifytime
					string += "\nContent-Length: " + str(len(fileoutput)) + "\n"
					string += "Connection: close\n"
					if cookieval == "":
						pass
					else:
						string += "Set-Cookie: "+cookieval+"\n"
					data = fileoutput
					result = hashlib.md5(bytes(data,'utf-8'))
					result = result.digest()
					result = bytes(result)
					md5 = base64.b64encode(result)
					md5 = md5.decode('utf-8')
					string+="Content-md5: " + md5 + "\n"
					string += "Content-Type: text/html\n\n"
					output = string + fileoutput
					connectionSocket.send(output.encode())
					connectionSocket.close()
					maxcon-=1

					#access log
					accesslogfn(client_addr,query,200,len(fileoutput),referer,user_agent,accesslog)
					
					#error log
					errorlogs(client_addr,port,referer1,errorlog)
					f.close()
					return
				elif extension == "html" or extension == "HTML":
					html("POST",filename,"",connectionSocket,client_addr,port,query,referer,referer1,user_agent,arange,ims)
					return
					
				elif extension == "csv" or extension == "csv":
					csv("POST",connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims)
					return
				elif extension == "pdf" or extension == "PDF":
					pdf("POST",connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims)
					return
					
				elif extension == "ppt" or extension == "PPT":
					ppt("POST",connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims)
					return
				elif extension == "doc" or extension == "DOC":
					doc("POST",connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims)
					return
					
				elif extension == "docx" or extension == "DOCX":
					docx("POST",connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims)
					return
				elif extension == "pptx" or extension == "PPTX":
					pptx("POST",connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims)
					return
				elif extension == "zip" or extension == "ZIP":
					zip1("POST",connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims)
					return
				elif extension == "7z" or extension == "7z":
					z7("POST",connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims)
					return
				elif extension == "xml" or extension == "XML":
					xml("POST",connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims)
					return
				elif extension == "png" or extension == "PNG":
					png("POST",connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims)
					return
				elif extension == "jpg" or extension == "jpeg" or  extension == "JPG" or extension == "JPEG":
					jpg("POST",connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims)
					return
				elif extension == "mp4" or extension == "MP4" :
					mp4("POST",connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims)
					return
				elif extension == "gif" or extension == "gif" :
					gif("POST",connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims)
					return
				elif extension == "mp3" or extension == "MP3" :
					mp3("POST",connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims)
					return
				else:
					f = open(filename)
					fileoutput = f.read()
					string = "HTTP/1.1 200 OK\n"
					string += "Date: " +(time.strftime("%a, %d %b %Y %I:%M:%S %p %Z", time.gmtime()))
					string += "\nServer: Harsha/2.4.41 (Ubuntu)\n"
					modifytime =  time.ctime(os.path.getmtime(filename))
					string += "Last-Modified: " + modifytime
					string += "\nContent-Length: " + str(len(fileoutput)) + "\n"
					string += "Connection: close\n"
					if cookieval == "":
						pass
					else:
						string += "Set-Cookie: "+cookieval+"\n"
					data = fileoutput
					result = hashlib.md5(bytes(data,'utf-8'))
					result = result.digest()
					result = bytes(result)
					md5 = base64.b64encode(result)
					md5 = md5.decode('utf-8')
					string+="Content-md5: " + md5 + "\n"
					string += "Content-Type: text/plain\n\n"
					output = string + fileoutput
					connectionSocket.send(output.encode())
					connectionSocket.close()
					maxcon-=1
					#access log
					status_code=200
					accesslogfn(client_addr,query,200,len(fileoutput),referer,user_agent,accesslog)
					
					#error log
					errorlogs(client_addr,port,referer1,errorlog)
					f.close()
					return
				#connectionSocket.close()
			elif words[0] == "PUT":
				putmethod(sentence,words,errorlog,accesslog,query,client_addr,port,referer,referer1,user_agent)
				return
			elif words[0] == "DELETE":
				deletemethod(words,errorlog,accesslog,query,client_addr,port,referer,referer1,user_agent)
				return
				
				
			elif words[0] == "HEAD":
				
				if words[1] == "/":
					filename = "/home/m/TY/CN_LAB/Project/index.html"
				elif "?" in  words[1]:
					extension = (words[1].split("?"))[0]
					filename = extension
					filename = documentroot + filename
					extension =(extension.split("."))[1]
					
				else:
					extension =(words[1].split("."))[1]
					filename = words[1]
					filename = documentroot + filename
				
				if not path.exists(filename):
					filenotexists("HEAD",connectionSocket,words[1],client_addr,port,query,referer,referer1,user_agent)
					return
				elif filename == "/home/m/TY/CN_LAB/Project/index.html":
					f = open("/home/m/TY/CN_LAB/Project/index.html")
					fileoutput = f.read()
					string = "HTTP/1.1 200 OK\n"
					string += "Date: " +(time.strftime("%a, %d %b %Y %I:%M:%S %p %Z", time.gmtime()))
					string += "\nServer: Harsha/2.4.41 (Ubuntu)\n"
					modifytime =  time.ctime(os.path.getmtime(filename))
					string += "Last-Modified: " +modifytime
					string += "\nContent-Length: " + str(len(fileoutput)) + "\n"
					string += "Connection: close\n"
					
					string += "Content-Type: text/html\n\n"
					output = string 
					connectionSocket.send(output.encode())
					connectionSocket.close()
					maxcon-=1

					#access log
					accesslogfn(client_addr,query,200,len(fileoutput),referer,user_agent,accesslog)
					
					#error log
					errorlogs(client_addr,port,referer1,errorlog)
					f.close()
					return
				elif not os.access(filename, os.R_OK):
					f = open("forbidden.html")
					fileoutput = f.read()
					string = "HTTP/1.1 403 Forbidden\n"
					string += "Date: " + (time.strftime("%a, %d %b %Y %I:%M:%S %p %Z", time.gmtime()))
					string += "\nServer: Harsha/2.4.41 (Ubuntu)\n"
					modifytime =  time.ctime(os.path.getmtime("forbidden.html"))
					string += "Last-Modified: "+modifytime
					string += "\nContent-Length: " +  str(len(fileoutput)) +"\n"
					string += "Content-Type: text/html; charset=iso-8859-1\n\n"
					if cookieval == "":
						pass
					else:
						string += "Set-Cookie: "+cookieval+"\n"
					string += "Connection: close\n"
					
					string = string 
					
					connectionSocket.send(string.encode())
					connectionSocket.close()
					maxcon-=1
					status_code=403
					accesslogfn(client_addr,query,status_code,len(fileoutput),referer,user_agent,accesslog)
					#error log
					permissiondeniederrorlog(client_addr,port,words[1],referer1,errorlog)
					f.close()
					return
					
				elif extension == "html" or extension == "HTML":
					
					html("HEAD",filename,cookieval,connectionSocket,client_addr,port,query,referer,referer1,user_agent,arange,ims)
					return
				elif extension == "csv" or extension == "csv":
					csv("HEAD",connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims)
					return
				elif extension == "pdf" or extension == "PDF":
					pdf("HEAD",connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims)
					return
				elif extension == "ppt" or extension == "PPT":
					ppt("HEAD",connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims)
					return
				elif extension == "doc" or extension == "DOC":
					doc("HEAD",connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims)
					return
				elif extension == "docx" or extension == "DOCX":
					docx("HEAD",connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims)
					return
				elif extension == "pptx" or extension == "PPTX":
					pptx("HEAD",connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims)
					return
				elif extension == "zip" or extension == "ZIP":
					zip1("HEAD",connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims)
					return
				elif extension == "7z" or extension == "7z":
					z7("HEAD",connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims)
					return
				elif extension == "xml" or extension == "XML":
					xml("HEAD",connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims)
					return
				elif extension == "png" or extension == "PNG":
					png("HEAD",connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims)
					return
				elif extension == "jpg" or extension == "jpeg" or  extension == "JPG" or extension == "JPEG":
					jpg("HEAD",connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims)
					return
				elif extension == "mp4" or extension == "MP4" :
					mp4("HEAD",connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims)
					return
				elif extension == "gif" or extension == "gif" :
					gif("HEAD",connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims)
					return
				elif extension == "mp3" or extension == "MP3" :
					mp3("HEAD",connectionSocket,filename,cookieval,client_addr,query,referer,user_agent,port,referer1,arange,ims)
					return
				else:
					f = open(filename)
					fileoutput = f.read()
					string = "HTTP/1.1 200 OK\n"
					string += "Date: " +(time.strftime("%a, %d %b %Y %I:%M:%S %p %Z", time.gmtime()))
					string += "\nServer: Harsha/2.4.41 (Ubuntu)\n"
					modifytime =  time.ctime(os.path.getmtime(filename))
					
					string += "Last-Modified: " + modifytime
					string += "\nContent-Length: " + str(len(fileoutput)) + "\n"
					string += "Connection: close\n"
					if cookieval == "":
						pass
					else:
						string += "Set-Cookie: "+cookieval+"\n"
					string += "Content-Type: text/plain\n\n"
					output = string 
					connectionSocket.send(output.encode())
					connectionSocket.close()
					maxcon-=1
					#access log
					status_code=200
					accesslogfn(client_addr,query,status_code,len(fileoutput),referer,user_agent,accesslog)
					
					#error log
					errorlogs(client_addr,port,referer1,errorlog)
					f.close()
					return
				
			elif words[0] == "PATCH" or words[0] == "COPY" or words[0] == "OPTIONS" or words[0] == "LINK" or words[0] == "UNLINK" or words[0] == "PURGE" or 			words[0] == "LOCK" or words[0] == "UNLOCK" or words[0] == "PROPFIND" or words[0] == "VIEW":
				###print("Not Allowed")
				f = open("notallowed.html")
				fileoutput = f.read()
				string = "HTTP/1.1 405 Not Allowed\n"
				string += "Date: " + (time.strftime("%a, %d %b %Y %I:%M:%S %p %Z", time.gmtime()))
				string += "\nServer: Harsha/2.4.41 (Ubuntu)\n"
				modifytime =  time.ctime(os.path.getmtime("notallowed.html"))
				string += "Last-Modified: " +modifytime
				string += "\nContent-Length: " +  str(len(fileoutput)) +"\n"
				string += "Connection: close\n"
				string += "Content-Type: text/html; charset=iso-8859-1\n\n"
				string = string + fileoutput
				connectionSocket.send(string.encode())
				connectionSocket.close()
				maxcon-=1
				#access log
				status_code=405
				accesslogfn(client_addr,query,status_code,len(fileoutput),referer,user_agent,accesslog)
				#error log
				notallowederrorlog(client_addr,port,words[1],referer1,errorlog,words[0])
				f.close()
				
				return
	
	except Exception as e:
		f = open("badrequest.html")
		fileoutput = f.read()
		string = "HTTP/1.1 200 OK\n"
		string += "Date : " +(time.strftime("%a, %d %b %Y %I:%M:%S %p %Z", time.gmtime()))
		string += "\nServer : Harsha/2.4.41 (Ubuntu)\n"
		modifytime =  time.ctime(os.path.getmtime("badrequest.html"))
				
		string += "Last-Modified: " + modifytime
		string += "\nContent-Length: " +  str(len(fileoutput)) +"\n"
		string += "Connection: close\n"
		string += "Content-Type: text/html; charset=iso-8859-1\n\n"
				
		string = string + fileoutput
		string += "Connection closed by foreign host."
		connectionSocket.send(string.encode())
		connectionSocket.close()
		maxcon-=1
		return
	
		
		
		
#os.popen("memcached")	
serverSocket = socket(AF_INET,SOCK_STREAM)


maxsimcon = 0
configfile = open("harsha.conf","r")
for line in  configfile.readlines():
	if line[0] == "#" or line[0] == "\n":
		continue
	else:
		line = line.split(" ")
		if line[0] == "ErrorLog":
			errorlog = (line[1].split("\n"))[0]
		elif line[0] == "AccessLog":
			accesslog = (line[1].split("\n"))[0]
		elif line[0] == "DocumentRoot":
			documentroot = (line[1].split("\n"))[0]
		elif line[0] == "LISTEN":
			serverport1 = int((line[1].split("\n"))[0])
		elif line[0] == "MaxSimultaneousConnection":
			maxsimcon = int((line[1].split("\n"))[0])
			
errorlog =  errorlog
accesslog = accesslog
configfile.close()
###print(errorlog,accesslog,documentroot,serverport1,maxsimcon)
		 

#serverport = int(sys.argv[1])
try:
	serverSocket.bind(('',serverport1))
	serverSocket.listen(1)

	while True:

		connectionSocket,addr = serverSocket.accept()

		###print(maxcon)
		if maxcon <= maxsimcon and maxcon >= 0:
			
			maxcon+=1
			t1 = threading.Thread(target = connection,args=(connectionSocket,))
			t1.daemon = True
			t1.start()
		else:
			###print("Shukriya")
			connectionSocket.close()
except KeyboardInterrupt:
		sys.stdout.flush()

		##print("Bye")
finally:
		serverSocket.close()

#serverSocket.close()
	
	

	

	
	
	
	
	
	
	
	
	
	
	
	
	
	

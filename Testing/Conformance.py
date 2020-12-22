#new.html 
#demo1.html
import requests
import threading
import random

#Five Concurrent GET Request
def concget():
    print(requests.get("http://localhost:13002/demo2.html"))

#Five Concurrent POST Request
def concpost():
    print(requests.post("http://localhost:13002/demo2.html"))

#Five Concurrent HEAD Request
def conchead():
    print(requests.head("http://localhost:13002/demo2.html"))

#Random Requests GET POST HEAD DELETE PUT
def conrandom():
    n = random.randint(0,7)
    if n == 0:
        print(requests.get("http://localhost:13002/demo2.html"))
    elif n == 1:
        print(requests.post("http://localhost:13002/demo2.html"))
    elif n == 2:
        print(requests.head("http://localhost:13002/demo2.html"))
    elif n == 3:
        print(requests.put("http://localhost:13002/new1.html","hello"))
    elif n == 4:
        print(requests.delete("http://localhost:13002/new1.html"))
    elif n == 5:
        print(requests.get("http://localhost:13002/demo3.html"))
    elif n == 6:
        print(requests.post("http://localhost:13002/demo3.html"))
    elif n == 7:
         print(requests.head("http://localhost:13002/demo3.html"))

print()
#1 Simple GET Request
response = requests.get("http://localhost:13002/demo2.html")
print("Simple GET Request")
print("Status Code = ", response.status_code)
print(response.headers)
print()

#2 Simple POST Request
response = requests.post("http://localhost:13002/demo2.html")
print("Simple POST Request")
print("Status Code = ", response.status_code)
print(response.headers)
print()

#3 Simple HEAD Request
response = requests.head("http://localhost:13002/demo2.html")
print("Simple HEAD Request")
print("Status Code = ", response.status_code)
print(response.headers)
print()

#4 Simple PUT Request
data = "<html>Hello</html>"
response = requests.put("http://localhost:13002/new.html",data)
print("Simple PUT Request")
print("Status Code = ", response.status_code)
print(response.headers)
print()

#5 Simple Delete Request
response = requests.delete("http://localhost:13002/demo1.html")
print("Simple Delete Request")
print("Status Code = ", response.status_code)
print(response.headers)
print()


#6 Five Concurrent GET Request
print("Concurrent GET Request")
i = 0
while i < 5:
    t1 = threading.Thread(target=concget)
    t1.start()
    i+=1
print()


#7 Five Concurrent POST Request
print("Concurrent POST Request")
i = 0
while i < 5:
    t1 = threading.Thread(target=concpost)
    t1.start()
    i+=1
print()

#8 Five Concurrent HEAD Request
print("Concurrent HEAD Request")
i = 0
while i < 5:
    t1 = threading.Thread(target=conchead)
    t1.start()
    i+=1
print()

#10 DocumentRoot Filename not specified
print("DocumentRoot/ Filename not specified")
response = requests.get("http://localhost:13002/")
print("Status_code = ",response.status_code)
print(response.headers)
print()

#11 GET File Permission not allowed
response = requests.get("http://localhost:13002/demo3.html")
print("GET File Permission not allowed")
print("Status Code = ", response.status_code)
print(response.headers)
print()

#12 POST File Permission not allowed
response = requests.post("http://localhost:13002/demo3.html")
print("POST File Permission not allowed")
print("Status Code = ", response.status_code)
print(response.headers)
print()

#13 HEAD File Permission not allowed
response = requests.head("http://localhost:13002/demo3.html")
print("HEAD File Permission not allowed")
print("Status Code = ", response.status_code)
print(response.headers)
print()


#14 DELETE File Permission not allowed
response = requests.delete("http://localhost:13002/demo3.html")
print("DELETE File Permission not allowed")
print("Status Code = ", response.status_code)
print(response.headers)
print()

#15 GET File Not Exists
response = requests.get("http://localhost:13002/demo302.html")
print("GET File Permission not allowed")
print("Status Code = ", response.status_code)
print(response.headers)
print()

#16 POST File Not Exists
response = requests.post("http://localhost:13002/demo302.html")
print("POST File Permission not allowed")
print("Status Code = ", response.status_code)
print(response.headers)
print()

#17 HEAD File File Not Exists
response = requests.head("http://localhost:13002/demo302.html")
print("HEAD File Permission not allowed")
print("Status Code = ", response.status_code)
print(response.headers)
print()


#18 DELETE File Not Exists
response = requests.delete("http://localhost:13002/demo302.html")
print("DELETE File Permission not allowed")
print("Status Code = ", response.status_code)
print(response.headers)
print()

#19 Simple GET Request - PDF
response = requests.get("http://localhost:13002/index.pdf")
print("Simple GET Request - PDF")
print("Status Code = ", response.status_code)
print(response.headers)
print()

#20 Simple GET Request - PNG
response = requests.get("http://localhost:13002/a.png")
print("Simple GET Request - PNG")
print("Status Code = ", response.status_code)
print(response.headers)
print()

#21 Simple GET Request - JPEG
response = requests.get("http://localhost:13002/index.jpeg")
print("Simple GET Request - JPEG")
print("Status Code = ", response.status_code)
print(response.headers)
print()

#22 Simple GET Request - PPT
response = requests.get("http://localhost:13002/a.ppt")
print("Simple GET Request - PPT")
print("Status Code = ", response.status_code)
print(response.headers)
print()


#23 Simple GET Request - PPTX
response = requests.get("http://localhost:13002/a.pptx")
print("Simple GET Request - PPTX")
print("Status Code = ", response.status_code)
print(response.headers)
print()


#24 Simple GET Request - DOC
response = requests.get("http://localhost:13002/a.doc")
print("Simple GET Request - DOC")
print("Status Code = ", response.status_code)
print(response.headers)
print()

#25 Simple GET Request - DOCX
response = requests.get("http://localhost:13002/a.docx")
print("Simple GET Request - DOCX")
print("Status Code = ", response.status_code)
print(response.headers)
print()

#26 Simple GET Request - ZIP
response = requests.get("http://localhost:13002/abc.zip")
print("Simple GET Request - ZIP")
print("Status Code = ", response.status_code)
print(response.headers)
print()

#26 Simple GET Request - 7z
response = requests.get("http://localhost:13002/abc.7z")
print("Simple GET Request - 7z")
print("Status Code = ", response.status_code)
print(response.headers)
print()

#27 Simple GET Request - MP3
response = requests.get("http://localhost:13002/a.mp3")
print("Simple GET Request - MP3")
print("Status Code = ", response.status_code)
print(response.headers)
print()

#28 Simple GET Request - MP4
response = requests.get("http://localhost:13002/a.mp4")
print("Simple GET Request - MP4")
print("Status Code = ", response.status_code)
print(response.headers)
print()

#29 Simple GET Request - XML
response = requests.get("http://localhost:13002/abc.xml")
print("Simple GET Request - XML")
print("Status Code = ", response.status_code)
print(response.headers)
print()

#30 Simple GET Request - CSV
response = requests.get("http://localhost:13002/input.csv")
print("Simple GET Request - CSV")
print("Status Code = ", response.status_code)
print(response.headers)
print()

#31 Range Header - 206
response = requests.get("http://localhost:13002/demo2.html",headers = {"Range": "Bytes = 10-20"})      #Problem
print("Range Header")
print("Status Code = ",response.status_code)
print(response.headers)
print()

#32 Range Header - 416
response = requests.get("http://localhost:13002/demo2.html",headers = {"Range": "Bytes = 1000000-20000000000"})      #Problem
print("Range Header")
print("Status Code = ",response.status_code)
print(response.headers)
print()

#33 Range Header - 416
response = requests.get("http://localhost:13002/demo2.html",headers = {"Range": "Bytes = 100-20"})
print("Range Header")
print("Status Code = ",response.status_code)
print(response.headers)
print() 

#34 If-Modified-SInce
response = requests.get("http://localhost:13002/demo2.html",headers = {"If-Modified-Since": "Wed, 11 Nov 2020 21:51:55 GMT"})
print("If-Modified-Since")
print("Status Code = ",response.status_code)
print(response.headers)
print() 

#35 If-Modified-SInce
response = requests.get("http://localhost:13002/demo2.html",headers = {"If-Modified-Since": "Wed, 1 Nov 2020 21:51:55 GMT"})
print("If-Modified-Since")
print("Status Code = ",response.status_code)
print(response.headers)
print()

#36 IF-Modified-Since and Range Header - 304
response = requests.get("http://localhost:13002/demo2.html",headers = {"If-Modified-Since": "Wed, 11 Nov 2020 21:51:55 GMT","Range": "Bytes = 100-200"})
print("If-Modified-Since and Range Header")
print("Status Code = ",response.status_code)
print(response.headers)
print()

#37 IF-Modified-Since and Range Header - 206
response = requests.get("http://localhost:13002/demo2.html",headers = {"If-Modified-Since": "Wed, 1 Nov 2020 21:51:55 GMT","Range": "Bytes = 10-20"})
print("If-Modified-Since and Range Header")
print("Status Code = ",response.status_code)
print(response.headers)
print()

#38 IF-Modified-Since and Range Header - 416
response = requests.get("http://localhost:13002/demo2.html",headers = {"If-Modified-Since": "Wed, 1 Nov 2020 21:51:55 GMT","Range": "Bytes = 100-20"})
print("If-Modified-Since and Range Header")
print("Status Code = ",response.status_code)
print(response.headers)
print()

#39 IF-Modified-Since and Range Header - 416
response = requests.get("http://localhost:13002/demo2.html",headers = {"If-Modified-Since": "Wed, 1 Nov 2020 21:51:55 GMT","Range": "Bytes = 10000000-20000000000"})
print("If-Modified-Since and Range Header")
print("Status Code = ",response.status_code)
print(response.headers)
print()

#40 If-Modified-Since (POST) 
response = requests.post("http://localhost:13002/demo2.html",headers = {"If-Modified-Since": "Wed, 11 Nov 2020 21:51:55 GMT"})
print("If-Modified-Since (POST) ")
print("Status Code = ",response.status_code)
print(response.headers)
print()

#41 If-Modified-Since (POST) 
response = requests.post("http://localhost:13002/demo2.html",headers = {"If-Modified-Since": "Wed, 1 Nov 2020 21:51:55 GMT"})
print("If-Modified-Since (POST) ")
print("Status Code = ",response.status_code)
print(response.headers)
print()

#42 If-Modified-Since and Range Header (POST)
response = requests.post("http://localhost:13002/demo2.html",headers = {"If-Modified-Since": "Wed, 11 Nov 2020 21:51:55 GMT","Range": "Bytes = 10-200"})
print("If-Modified-Since and Range Header")
print("Status Code = ",response.status_code)
print(response.headers)
print()

#43 If-Modified-Since and Range Header (POST)
response = requests.post("http://localhost:13002/demo2.html",headers = {"If-Modified-Since": "Wed, 1 Nov 2020 21:51:55 GMT","Range": "Bytes = 10-200"})
print("If-Modified-Since and Range Header")
print("Status Code = ",response.status_code)
print(response.headers)
print()

#44 PUT Method - 200
data = "<html><b>Hello</b></html>"
response = requests.put("http://localhost:13002/new.html",data)
print("PUT Method")
print("Status Code = ",response.status_code)
print(response.headers)
print()

#45 PUT Method - 204
response = requests.put("http://localhost:13002/new.html")
print("PUT Method")
print("Status Code = ",response.status_code)
print(response.headers)
print()

#46 Simple POST Request - PDF
response = requests.post("http://localhost:13002/index.pdf")
print("Simple POST Request - PDF")
print("Status Code = ", response.status_code)
print(response.headers)
print()

#47 Simple POST Request - PNG
response = requests.post("http://localhost:13002/a.png")
print("Simple POST Request - PNG")
print("Status Code = ", response.status_code)
print(response.headers)
print()

#48 Simple POST Request - JPEG
response = requests.post("http://localhost:13002/index.jpeg")
print("Simple POST Request - JPEG")
print("Status Code = ", response.status_code)
print(response.headers)
print()

#49 Simple POST Request - PPT
response = requests.post("http://localhost:13002/a.ppt")
print("Simple POST Request - PPT")
print("Status Code = ", response.status_code)
print(response.headers)
print()


#50 Simple POST Request - PPTX
response = requests.post("http://localhost:13002/a.pptx")
print("Simple POST Request - PPTX")
print("Status Code = ", response.status_code)
print(response.headers)
print()


#51 Simple POST Request - DOC
response = requests.post("http://localhost:13002/a.doc")
print("Simple POST Request - DOC")
print("Status Code = ", response.status_code)
print(response.headers)
print()

#52 Simple POST Request - DOCX
response = requests.post("http://localhost:13002/a.docx")
print("Simple POST Request - DOCX")
print("Status Code = ", response.status_code)
print(response.headers)
print()

#53 Simple POST Request - ZIP
response = requests.post("http://localhost:13002/abc.zip")
print("Simple GET Request - ZIP")
print("Status Code = ", response.status_code)
print(response.headers)
print()

#54 Simple POST Request - 7z
response = requests.post("http://localhost:13002/abc.7z")
print("Simple POST Request - 7z")
print("Status Code = ", response.status_code)
print(response.headers)
print()

#55 Simple POST Request - MP3
response = requests.post("http://localhost:13002/a.mp3")
print("Simple GET Request - MP3")
print("Status Code = ", response.status_code)
print(response.headers)
print()

#56 Simple POST Request - MP4
response = requests.get("http://localhost:13002/a.mp4")
print("Simple POST Request - MP4")
print("Status Code = ", response.status_code)
print(response.headers)
print()

#57 Simple POST Request - XML
response = requests.post("http://localhost:13002/abc.xml")
print("Simple POST Request - XML")
print("Status Code = ", response.status_code)
print(response.headers)
print()

#58 Simple POST Request - CSV
response = requests.post("http://localhost:13002/input.csv")
print("Simple POST Request - CSV")
print("Status Code = ", response.status_code)
print(response.headers)
print()

#59 Simple HEAD Request - PDF
response = requests.head("http://localhost:13002/index.pdf")
print("Simple HEAD Request - PDF")
print("Status Code = ", response.status_code)
print(response.headers)
print()

#60 Simple HEAD Request - PNG
response = requests.head("http://localhost:13002/a.png")
print("Simple HEAD Request - PNG")
print("Status Code = ", response.status_code)
print(response.headers)
print()

#61 Simple HEAD Request - JPEG
response = requests.head("http://localhost:13002/index.jpeg")
print("Simple HEAD Request - JPEG")
print("Status Code = ", response.status_code)
print(response.headers)
print()

#62 Simple HEAD Request - PPT
response = requests.head("http://localhost:13002/a.ppt")
print("Simple HEAD Request - PPT")
print("Status Code = ", response.status_code)
print(response.headers)
print()


#63 Simple HEAD Request - PPTX
response = requests.head("http://localhost:13002/a.pptx")
print("Simple HEAD Request - PPTX")
print("Status Code = ", response.status_code)
print(response.headers)
print()


#64 Simple HEAD Request - DOC
response = requests.head("http://localhost:13002/a.doc")
print("Simple HEAD Request - DOC")
print("Status Code = ", response.status_code)
print(response.headers)
print()

#65 Simple HEAD Request - DOCX
response = requests.head("http://localhost:13002/a.docx")
print("Simple HEAD Request - DOCX")
print("Status Code = ", response.status_code)
print(response.headers)
print()

#66 Simple HEAD Request - ZIP
response = requests.post("http://localhost:13002/abc.zip")
print("Simple GET Request - ZIP")
print("Status Code = ", response.status_code)
print(response.headers)
print()

#67 Simple HEAD Request - 7z
response = requests.head("http://localhost:13002/abc.7z")
print("Simple HEAD Request - 7z")
print("Status Code = ", response.status_code)
print(response.headers)
print()

#68 Simple HEAD Request - MP3
response = requests.head("http://localhost:13002/a.mp3")
print("Simple HEAD Request - MP3")
print("Status Code = ", response.status_code)
print(response.headers)
print()

#69 Simple HEAD Request - MP4
response = requests.head("http://localhost:13002/a.mp4")
print("Simple HEAD Request - MP4")
print("Status Code = ", response.status_code)
print(response.headers)
print()

#70 Simple HEAD Request - XML
response = requests.head("http://localhost:13002/abc.xml")
print("Simple HEAD Request - XML")
print("Status Code = ", response.status_code)
print(response.headers)
print()

#71 Simple HEAD Request - CSV
response = requests.head("http://localhost:13002/input.csv")
print("Simple HEAD Request - CSV")
print("Status Code = ", response.status_code)
print(response.headers)
print()

#72 POST With DATA
response = requests.post("http://localhost:13002/demo2.html","fname=harsha")
print("POST With Data")
print("Status Code = ", response.status_code)
print(response.headers)
print()

#73 GET With DATA
response = requests.get("http://localhost:13002/demo.html?fname=harsha")
print("GET With Data")
print("Status Code = ", response.status_code)
print(response.headers)
print()

#74 GET With /ab/abc.xml
response = requests.get("http://localhost:13002/ab/abc.xml")
print("GET With Data")
print("Status Code = ", response.status_code)
print(response.headers)
print()
 



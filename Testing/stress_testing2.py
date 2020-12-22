import requests
import threading
import random
def conn():
    n = random.randint(0,2)
    if n == 0:
        print(requests.get("http://localhost:13002/a.png"))
    elif n == 1:
        print(requests.post("http://localhost:13002/demo2.html"))
    elif n == 2:
        print(requests.head("http://localhost:13002/Harsha_Rathi.pdf"))
    

i = 0
while i < 100:
    t1 = threading.Thread(target = conn)
    t1.start()
    i+=1
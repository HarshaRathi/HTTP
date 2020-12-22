import requests
from concurrent.futures import ThreadPoolExecutor
def get_url(url):
    return requests.get(url)
list_url = ["http://localhost:13002/demo2.html","http://localhost:13002/a.png","http://localhost:13002/Harsha_Rathi.pdf","http://localhost:13002/Harsha_Rathi.jpeg","http://localhost:13002/abc.zip","http://localhost:13002/abc.7z","http://localhost:13002/a.doc","http://localhost:13002/","http://localhost:13002/a.ppt","http://localhost:13002/a.pptx","http://localhost:13002/a.docx","http://localhost:13002/a.mp3","http://localhost:13002/a.mp4","http://localhost:13002/tenor.gif"]
list_url = 7 * list_url
#print(list_url)
with ThreadPoolExecutor(max_workers=1000) as pool:
    print(list(pool.map(get_url,list_url)))

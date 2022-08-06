import shutil
from bs4 import BeautifulSoup
import requests
import os


html_file = open("./cubicus.html",mode="r")
domain_name = "http://vimbi.uk.w3pcloud.com"
filters = (".css",'.js','.jpeg','.png')
protocol = ("http","https")
soup = BeautifulSoup(html_file,"html.parser")

all_css = soup.find_all("link")
all_js  = soup.find_all("script")
all_image = soup.find_all("img")


def nameParser(name:str)->str:
    spliiter  = name.split("/")
    fileName = "test.txt"
    dirName  = "/fault"
    if not name.endswith(filters):
        dirName = "/".join(spliiter[0:len(spliiter)-1])
        extensionChecker = None
        name2 = spliiter[len(spliiter)-1]
        for i in filters:
            extensionChecker = name2.split(i)
            if(len(extensionChecker) > 0):
                fileName = extensionChecker[0]+i
                break
        
    else:
        fileName = spliiter[len(spliiter)-1]
        dirName = "/".join(spliiter[0:len(spliiter)-1]) 
    return fileName,dirName

def makeRequest(link:str):
    if link.startswith(protocol) and link.endswith(filters):
        request = requests.get(link,stream=True)
        splitted_name= link.replace(domain_name,"")
        fileName,dirName = nameParser(splitted_name)
        if not splitted_name.startswith(("http","https")) and len(splitted_name) >1:
            if not os.path.exists(os.path.abspath(".")+dirName):
                os.makedirs(os.path.abspath(".")+dirName)
            try:
                if fileName.endswith((".css",".js")):
                    with open(os.path.abspath(".")+dirName+"/"+fileName,mode="w+") as file:
                        file.write(request.text)
                else:
                    with open(os.path.abspath(".")+dirName+"/"+fileName,mode="wb+") as file:
                        shutil.copyfileobj(request.raw,file)
            except Exception as e:
                print(e)
    else:
        print(f"{link} not seems as a resourcable file")
        return
    


for i in all_css:
    link = i.get("href")
    if link is not None:
        makeRequest(link)
    else:
        pass


for i in all_js:
    link = i.get("src")
    if link is not None:
        makeRequest(link)
    else:
        pass


for i in all_image:
    link = i.get("src")
    if link is not None:
        makeRequest(link)
    else:
        pass
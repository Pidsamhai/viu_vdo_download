from art import tprint
from bs4 import BeautifulSoup as bs
import requests as rs
import os
import ctypes
from subprocess import Popen, CREATE_NEW_CONSOLE
from removeAds import removeAds

dummy_url = '''https%3A%2F%2Fwww.viu.com%2Fott%2Fth%2Fth%2Fvod%2F190303%2FBe-Melodramatic'''

_url = "https://www.viu.com/ott/th/th/vod/190303/Be-Melodramatic"
_list_vdo = []
_GRAB_VDO_URL = 'https://www.grabvdo.com/?url='
_VIU_URL = "https://www.viu.com"

_FILES = {}
_S_LANG = ['简体中文','English','繁體中文','Indo','ภาษาไทย']
_S_LANG_E = ['Simplified Chinese','English','traditional Chinese','Indo','Thai']

_HISTORY = []

def fetch(url):
    r = rs.get(url)
    return r.text 


def getUrl(url):
    url = url.replace("/","%2F")
    url = url.replace(":","%3A")
    return _GRAB_VDO_URL + url

def readHistory():
    if not os.path.isfile('./adscontent/history.txt'):
        file = open('./adscontent/history.txt','w+')
    else:
        with open('./adscontent/history.txt','r') as file:
            _HISTORY = file.readlines()
            for i,a in enumerate(_HISTORY):
                n = a.split("/")
                print(i+1,n[len(n)-1])
            file.close()
    return _HISTORY


def checkHistory(url):
    if not os.path.isfile('./adscontent/history.txt'):
        file = open('./adscontent/history.txt','w+')
    else:
        with open('./adscontent/history.txt','r') as file:
            history = file.readlines()
            file.close()
            for n in history:
                if url.split("/")[-1] == n.split("/")[-1]:
                    return
            c = str(input("New series fond. Add to history ? [y][n] : "))
            if(c == "y"):
                w = open('./adscontent/history.txt','a+')
                w.write("\n" + url)
                w.close()
            file.close()


def dlSub(url,file_name,lang):
    file_name = file_name.replace(':','')
    if not os.path.exists("./subtitle/"):
        os.makedirs("./subtitle")
    with open("./subtitle/{}({}).srt".format(file_name,lang), "wb") as file:
        response = rs.get(url)
        #print(response.text)
        file.write(response.content)
        file.close()

def dlVdo(command,ep_name):
    #print(command)
    if not os.path.exists("./vdo/"):
        os.makedirs("./vdo")
    command = command.split(" ")
    news = './vdo/' + command[len(command)-1].replace('"','') 
    news = '"{}"'.format(news)
    command[len(command)-1] = news
    command = " ".join(command)
    p1 = Popen(command,creationflags=CREATE_NEW_CONSOLE)


def getSubtitle_list(raw):
    s = bs(raw,"html.parser") 
    for tbody in s.find_all('tbody'):
        for tr in tbody.find_all('tr'):
            for td in tr.find_all('td'):
                if(td.text == 'ffmpeg code'): #get FFmpeg code
                    print("GET ffmpeg...",end="\r")
                    url = td.find('a')
                    ffmpeg_html = fetch(url['href'])
                    ff = bs(ffmpeg_html,"html.parser") 
                    ffmpeg_i = ff.find('code').text
                    #rint(ffmpeg_i)
                    _FILES['ffmpeg'] = ffmpeg_i
                    print("GET ffmpeg......OK")
                if(td.text.strip() in _S_LANG):
                    print("GET {} Subtitle Url...".format(td.text.strip()),end="\r")
                    _s = []
                    for a in tr.find_all('a'):
                        _s.append(a['href'])
                    _FILES[td.text.strip()] = _s
                    print("GET {} Subtitle Url......OK".format(td.text.strip()))               

def menu(ep_name): 
    while(True):
        os.system('cls')
        print(ep_name + "\n")
        print("1 Download Vdo only")
        print("2 Download Subtitle only")
        print("3 Download Vdo and Subtitle")
        print("4 Exit To Episode Select")
        c = int(input("\nPlease enter : ") or -1)
        if c == 1:
            dlVdo(_FILES['ffmpeg'],ep_name)
        if c == 2:
            os.system('cls')
            print("Select Langauge\n")
            for i,j in enumerate(_S_LANG_E,start=1): 
                print(i,j)
            print(len(_S_LANG)+1,"Download All")
            x = int(input("\n : "))
            if(x == len(_S_LANG)+1):
                for j,i in enumerate(_S_LANG,start=0):
                    print('Download {}...'.format(_S_LANG_E[j]))
                    try:
                        dlSub(_FILES[i][0],ep_name,_S_LANG_E[j])
                    except KeyError:
                        pass
            if x > 0 and x < len(_S_LANG) + 1:
                lang  = _S_LANG[x-1]
                dlSub(_FILES[lang][0],ep_name,_S_LANG_E[x-1])
        if c == 3:
            pass
        if c == 4:
            break

def getInfo(url=""):
    html = removeAds(url) #fetch html from grab vdo with remove ads
    print(url)
    s = bs(html,"html.parser")
    for ultag in s.find_all('ul', {'class': 'video-alllist clearfix common-panel'}):
        for litag in ultag.find_all('li'):
            for a in litag.find_all('a'):
                title_name = a['title'].replace('ตอนที่',"EP")
                title_name = title_name.replace('Watch Online on Viu',"")
                _list_vdo.append([title_name,a['href']])

def main():
    
    while(True):
        url = ""
        _HISTORY.clear()
        _list_vdo.clear()
        _FILES.clear()
        print("Enter [e] to Close Program")
        c = str(input('Select from history [h] , Input new url [u] : '))
        if(c == "h"):
            print("\n")
            h = readHistory()
            print("\n")
            index = int(input("Select series : "))
            url = h[index-1]
        elif(c == "u"):
            url = str(input("Enter Url : "))
        if c == "e":
            break
        checkHistory(url)
        getInfo(url)
        print("GET Vdo List...\n")
        print("Fond {} EP\n".format(len(_list_vdo)))
        while(True):
            os.system('cls')
            tprint('Select    Episode')
            for i,v in enumerate(reversed(_list_vdo),start=1):
                print(i,v[0]) 
            print("0 To Input url")
            c = int(input("\nPlease Select Episode : ") or -1)
            if(c == 0):
                os.system('cls')
                tprint("VIU    VDO    DOWNLOAD")
                break
            if c > 0 and c < len(_list_vdo)+1:
                grb_url = getUrl(_VIU_URL+_list_vdo[11-c][1])
                #print(grb_url)
                raw = fetch(_GRAB_VDO_URL + grb_url) #rs.get(_GRAB_VDO_URL + dummy_url)
                getSubtitle_list(raw)
                menu(_list_vdo[11-c][0])

if __name__ == '__main__':
    os.system("cls")
    tprint("VIU    VDO    DOWNLOAD")
    main()
    os.system('cls')
    tprint('GOOD  BYE')
    #https://www.viu.com/ott/th/th/vod/208032/Be-Melodramatic
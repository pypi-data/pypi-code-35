from bs4 import BeautifulSoup
import requests
import webbrowser


def toplink(search, open_in_browser=0):
    SearchUrl=str('https://www.youtube.com/results?search_query='+search)
    page=requests.get(SearchUrl)
    soup = BeautifulSoup(page.text, "lxml")
    # print(page)
    link=soup.findAll(attrs={'class':'yt-uix-tile-link'})
    print(link)
    # print(link)
    links=link[2]
    print(links)
    # print(links['title'])

    if not open_in_browser:
        print()
        url = 'https://www.youtube.com' + links['href']
        title = links['title']
        print({"title":title,"url":url})
        return {"title":title,"url":url}
    else:
        webbrowser.open_new('https://www.youtube.com' + links['href'])

def toplinks(search):
    SearchUrl=str('https://www.youtube.com/results?search_query='+search)
    page=requests.get(SearchUrl)
    soup = BeautifulSoup(page.text, "lxml")
    # print(page)
    link=soup.findAll(attrs={'class':'yt-uix-tile-link'})

    data = {}
    for vid in link:
        url='https://www.youtube.com' + vid['href']
        data[vid['title']]=url
        print(data)
    
    return data
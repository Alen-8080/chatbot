import requests
from bs4 import BeautifulSoup

def scrape():
    url = "https://ktu.edu.in/eu/core/announcements.htm"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find("table", {"class": "ktu-news"})
        tr_list = table.findAll("tr")

        tr = tr_list[1] # Retrieve only the second row (i.e., the first notification)

        links = []
        content = tr.findAll("b")
        try:
            links_all = tr.findAll("a")
            for link in links_all:
                text = link.find(text=True)
                link = str(link.get('href'))
                if link.startswith('/'):
                    link = "https://ktu.edu.in"+link
                links.append(dict({'url': link, 'text': text}))
        except:
            links = []
        date = content[0].text.split(':')[0][:-3]
        title = content[1].text

        texts = tr.find("li").findAll(text=True)
        content = ''
        for text in texts:
            if len(text) > 25 and text != title:
                content += text.replace('\n','').replace('\r','')+'\n'

        notification = dict({'date': date, 'title': title, 'link': links, 'content': content.strip()})
        return notification

    except Exception as e:
        print(str(e))

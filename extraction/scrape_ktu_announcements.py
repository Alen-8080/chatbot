import requests
from bs4 import BeautifulSoup


def scrape():
    url = 'https://ktu.edu.in/home.htm'

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the relevant elements containing the notification data
    announcement_elements = soup.find_all('div', class_='item')

    notifications = []
    for element in announcement_elements:
        date = element.find('div', class_='date').text.strip()
        title = element.find('a').text.strip()
        link = element.find('a')['href']

        notification = {
            'date': date,
            'title': title,
            'link': link
        }
        notifications.append(notification)

    return notifications

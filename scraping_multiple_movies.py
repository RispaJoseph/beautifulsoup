from bs4 import BeautifulSoup
import requests
import os

root = 'https://subslikescript.com'
website = f'{root}/movies'


result = requests.get(website)
content = result.text
soup = BeautifulSoup(content, 'lxml')

box = soup.find('article', class_='main-article')

links = []
for link in box.find_all('a', href=True):
    links.append(link['href'])
    
for link in links:
    result = requests.get(f'{root}{link}')
    content = result.text
    soup = BeautifulSoup(content, 'lxml')

    box = soup.find('article', class_='main-article')
    if not box:
        continue
    
    title = box.find('h1').get_text(strip=True)
    title = title.replace('/', '')
    script_div = box.find('div', class_='full-script')
    
    if not script_div:
        print(f"No transcript found for: {title}")
        continue
    
    transcript = script_div.get_text(strip=True, separator='\n')
    
    
    with open(f'scripts/{title}.txt', 'w') as file:
        file.write(transcript)
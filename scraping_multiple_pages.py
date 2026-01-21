from bs4 import BeautifulSoup
import requests
import os

root = 'https://subslikescript.com'
website = f'{root}/movies_letter-X'

os.makedirs("collection", exist_ok=True)

result = requests.get(website)
content = result.text
soup = BeautifulSoup(content, 'lxml')


pagination = soup.find('ul', class_='pagination')
pages = pagination.find_all('li', class_='page-item')
last_page = pages[-2].text

for page in range(1, int(last_page)+1):
    result = requests.get(f'{website}?page={page}')
    content = result.text
    soup = BeautifulSoup(content, 'lxml')
    
    box = soup.find('article', class_='main-article')
    
    links = []
    for link in box.find_all('a', href=True):
        links.append(link['href'])
        
    for link in links:
        try:
            result = requests.get(f'{root}{link}')
            content = result.text
            soup = BeautifulSoup(content, 'lxml')

            box = soup.find('article', class_='main-article')
            
            title = box.find('h1').get_text()
            transcript = box.find('div', class_='full-script').get_text(strip=True, separator='\n')
            
            with open(f'collection/{title}.txt', 'w') as file:
                file.write(transcript)
        except:
            print("---------------- LINK NOT WORKING ----------------")
            print(link)
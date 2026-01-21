from bs4 import BeautifulSoup
import requests
import os



#####################################################
# Extracting the links of multiple movie transcripts
##################################################### 

# How To Get The HTML
root = 'https://subslikescript.com'         # this is the homepage of the website
website = f'{root}/movies'                  # concatenating the homepage with the movies section

os.makedirs("scripts", exist_ok=True)

result = requests.get(website)
content = result.text
soup = BeautifulSoup(content, 'lxml')

# Locate the box that contains a list of movies
box = soup.find('article', class_='main-article')

# Store each link in "links" list (href doesn't consider root aka "homepage", so we have to concatenate it later)
links = []
for link in box.find_all('a', href=True):
    links.append(link['href'])
    
#################################################
# Extracting the movie transcript
#################################################

# Loop through the "links" list and sending a request to each link
    
for link in links:
    result = requests.get(f'{root}{link}')
    content = result.text
    soup = BeautifulSoup(content, 'lxml')

    # Locate the box that contains title and transcript
    box = soup.find('article', class_='main-article')
    
    # Locate title and transcript
    title = box.find('h1').get_text(strip=True)
    title = ''.join(title.split('/'))

    
    transcript = box.find('div', class_='full-script').get_text(strip=True, separator='\n')
    
    # Exporting data in a text file with the "title" name
    with open(f'scripts/{title}.txt', 'w') as file:
        file.write(transcript)
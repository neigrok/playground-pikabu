from bs4 import BeautifulSoup
from urllib.request import urlopen
import os
import os.path

html_doc = urlopen('https://pikabu.ru/new').read()
soup = BeautifulSoup(html_doc, 'lxml')

story = ''
links = []
titles =[]
stories = []
selected_links = []

for link in soup.find_all('a', class_='story__title-link'):
    links.append(link.get('href'))


if os.path.isdir('./stories') == True:
    print('')
else:
    os.makedirs('./stories')

wrong_characters = ['–', '*', '—', '.', "'", '"', '/', '<', '>', '»', '«', '?', '!', '#', '-', "\\", ';', '&', "//", ':', ',', '|', '[', ']']
q = 0
for link in links:
    html_doc = urlopen(link).read()
    soup = BeautifulSoup(html_doc, 'lxml')
    title = soup.find('title').text
    if title == 'Âàêàíñèÿ ðàçðàáîò÷èêà ìîáèëüíûõ ïðèëîæåíèé' or str(soup.find(class_='story__sponsor story__sponsor_bottom')) != 'None':
        continue
    else:
        title = str(title)
        while q < len(wrong_characters):
            title = title.replace(wrong_characters[q], '')
            q = q + 1
        q = 0
        for div in soup.findAll('div', class_='story-block story-block_type_text'):
            story = story + str(div.text)
        if str(story) != '':
            story = str(story)
            titles.append(title)
            stories.append(story)
            selected_links.append(link)
    story = ''

x = 0
while x < len(stories):
    isFile = os.path.isfile('stories/' + titles[x] + '.txt')
    if isFile == True:
        x = x + 1
        continue
    elif isFile == False:
        f = open('stories/' + titles[x] + '.txt', 'w', encoding='utf-8')
        f.write(stories[x])
        f.close()
        x = x + 1

isFile = os.path.isfile('linksxtitles.txt')

i = 0
if isFile == False:
    f =  open('linksxtitles.txt', 'w', encoding='utf-8')
    while i < len(selected_links):
        f.write(titles[i] +  ' — ' + selected_links[i] + '\n')
        i = i + 1
    f.close()
    f = open('linksxtitles.txt', 'r', encoding='utf-8')
    readed = list(f)
    f.close()
    readed = set(readed)
    readed = list(readed)
    readed.sort()
    f = open('linksxtitles.txt', 'w', encoding='utf-8')
    for string in readed:
        f.write(string)
    f.close()

elif isFile == True:
    f = open('linksxtitles.txt', 'r', encoding='utf-8')
    readed = list(f)
    f.close()
    while i < len(selected_links):
        readed.append(titles[i] + ' — ' + selected_links[i] + '\n')
        i = i + 1
    readed = set(readed)
    readed = list(readed)
    readed.sort()
    f = open('linksxtitles.txt', 'w', encoding='utf-8')
    for string in readed:
        f.write(string)
    f.close()
from bs4 import BeautifulSoup
import pandas as pd
import requests
from lxml import etree

publication_links = []
publication_title = []
#research_author = []
link_constant = "https://www.tu-chemnitz.de/informatik/ce/publications/index.php"
scrap_link_part_1 = "https://www.tu-chemnitz.de/informatik/ce/publications/index.php?page="
scrap_link_part_2 = "&count=100&Jahr_von=-1&Jahr_bis=-1&PersonID1=-1&PersonID2=-1&PersonID3=-1"


def scraping(link):
    website_url = requests.get(link).text
    soup = BeautifulSoup(website_url, 'html.parser')
    # print(soup.prettify())
    dom = etree.HTML(str(soup))
    #research_author = dom.xpath('//*[@id="listItem"]/text()[1]')
    #research_author.append(author)
    # publicationTitle = dom.xpath('//*[@id="listItem"]/b/a/text()')
    # publicationLinks = dom.xpath('//*[@id="listItem"]/a')
    for i in soup.findAll('div', attrs={'id': 'listItem'}):
        title_link = i.find('a', href=True)
        #author = dom.xpath('//*[@id="listItem"]/text()[1]')
        publication_title.append(title_link.text)
        publication_links.append(link_constant + title_link['href'])
    research_author = dom.xpath('//*[@id="listItem"]/text()[1]')
    df = pd.DataFrame({'Title': publication_title,
                       'Authors': research_author,
                       'Link': publication_links})
    df.to_csv('publication2.csv', index=False, encoding='utf-8')


#   for a in soup.find_all('a', href=True):
#      if a.text:
#         print('Link: ' + a['href'])
#        publication_links.append(a['href'])

for i in range(3, 4):
    link = scrap_link_part_1 + str(i) + scrap_link_part_2
    scraping(link)

print("FINISH")

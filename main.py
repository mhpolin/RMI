from bs4 import BeautifulSoup
import pandas as pd
import requests

book_title = []
book_author = []
research_field = []

#website_url = requests.get('https://vsr.informatik.tu-chemnitz.de/research/publications/').text
#soup = BeautifulSoup(website_url, "lxml")
#print(soup.prettify())

# for i in soup.findAll('div', attrs={'class':'media-body'}):
#     title = i.find('h4', attrs={'class':'media-heading'})
#     author_section = i.find('p')
#     author = author_section.find('span')
#     research_area = author_section.find('a',href=True)
#
#     book_title.append(title.text)
#     book_author.append(author.text)
#     if research_area != None:
#         research_field.append(research_area.text)
#     else:
#         research_field.append('Not found')

# df = pd.DataFrame()
# df["Title"] = book_title
# df["Authors"] = book_author
# df["Research Area"] = research_field
# df.to_csv('publication.csv', sep='\t', encoding='utf-8')

# df = pd.DataFrame({'Title':book_title,'Authors':book_author, 'Research Area':research_field})
# df.to_csv('publication.csv', index=False, encoding='utf-8')

#-----VSR Projects-----#
website_url = requests.get('https://vsr.informatik.tu-chemnitz.de/research/publications/').text
soup = BeautifulSoup(website_url, "lxml")
for i in soup.findAll('div', attrs={'class':'media-body'}):
    title = i.find('h4', attrs={'class':'media-heading'})
    author_section = i.find('p')
    author = author_section.find('span')
    research_area = author_section.find('a',href=True)

    book_title.append(title.text)
    book_author.append(author.text)
    if research_area != None:
        research_field.append(research_area.text)
    else:
        research_field.append('Not Found')

    df = pd.DataFrame({'Title': book_title, 'Authors': book_author, 'Research Area': research_field})
    df.to_csv('project.csv', index=False, encoding='utf-8')

print("FINISH")
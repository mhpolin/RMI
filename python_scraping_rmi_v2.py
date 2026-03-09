from bs4 import BeautifulSoup
import pandas as pd
import requests

book_title = []
book_author = []
research_field = []

website_url = requests.get('https://www.tu-chemnitz.de/mb/professuren.php.en').text
soup = BeautifulSoup(website_url, "lxml")
#print(soup.prettify())
professor_areas = []
professor_names = []
x = soup.find('ul', attrs={'class':'tucal-proflist'})

for i in x.findAll('li'):
    professorship_area1 = i.find('div')
    professorship_area2 = professorship_area1.find('strong')
    professorship_area3 = professorship_area2.find('a')
    professor_name = i.find('span')
    if professorship_area3 !=None:
       professor_areas.append(professorship_area3.text)
       professor_names.append(professor_name.text)

df = pd.DataFrame({'Professorship area':professor_areas,'professor name': professor_name})
df.to_csv('publication.csv', index=False, encoding='utf-8')




   # print(professor_name)



print("FINISH")

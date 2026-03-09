import requests
import lxml.html as lh
import pandas as pd
from rdflib import Graph, Literal, RDF, URIRef, Namespace  # basic RDF handling
from rdflib.namespace import FOAF, XSD  # most common namespaces
import urllib.parse  # for parsing strings to URI's

search = "web%20engineering"
url = "https://www.bibliothek.tu-chemnitz.de/uni_biblio/ergebnis.php?la=de&suchart=teil&Lines_Displayed=0&sort=o.date_year+DESC%2C+o.title&sprache=&suchfeld1=o.freitext&suchwert1=" + search + "&opt1=AND&suchfeld2=oa.person&suchwert2=&opt2=AND&suchfeld3=o.date_year&suchwert3=&startindex=0&page=0&dir=2&suche="
link_constant = "https://www.bibliothek.tu-chemnitz.de"
# Create a handle, page, to handle the contents of the website
page = requests.get(url)
# Store the contents of the website under doc
doc = lh.fromstring(page.content)
# parsing the html content
list_of_dfs = pd.read_html(url)
df = list_of_dfs[0] #list_of_dfs contains number of table, parsing index 0 indication taking first table only
indexes = df[0].tolist() #converting column number 0 into list
indexes.pop() #removing the garbage of last index
titles = df[1].tolist()
titles.pop()
authors = df[2].tolist()
authors.pop()
years = df[3].tolist()
years.pop()
alllinks = doc.xpath('//tr/td/a/@href')
alllinks.pop()
links = alllinks.pop(0)
full_link = link_constant+links

# dictionary of lists
dict = {'Index': indexes, 'Title': titles, 'URL': full_link, 'Author': authors, 'Year': years}

dframe = pd.DataFrame(dict) #coverting to data frame

#csv
dframe.to_csv('export_dataframe.csv', index=False, header=True)

#json
dframe.to_json('export_dataframe.json', orient='records', lines=True)

# RDF
# Define a graph 'g' and namespaces
g = Graph()
publication = Namespace('https://www.bibliothek.tu-chemnitz.de/')
schema = Namespace('http://schema.org/')

for index, row in dframe.iterrows():
    g.add((URIRef(publication), RDF.type, FOAF.Document))
    g.add((URIRef(publication), FOAF.homepage, URIRef(publication + Literal(row['URL']), Literal('String'))))
    g.add((URIRef(publication), FOAF.title, Literal(row['Title'], Literal('String'))))
    g.add((URIRef(publication), FOAF.name, Literal(row['Author'], Literal('String'))))
    g.add((URIRef(publication), URIRef(schema+'datePublished'), Literal(row['Year'], Literal('Date'))))

print(g.serialize(format='turtle').decode('UTF-8'))

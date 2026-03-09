from flask import Flask, request, render_template,jsonify
import requests
import lxml.html as lh
import pandas as pd

app = Flask(__name__)
def scrap_website(searchInput):
    search = searchInput.replace(" ", "%20")
    url = "https://www.bibliothek.tu-chemnitz.de/uni_biblio/ergebnis.php?la=de&suchart=teil&Lines_Displayed=0&sort=o.date_year+DESC%2C+o.title&sprache=&suchfeld1=o.freitext&suchwert1=" + search + "&opt1=AND&suchfeld2=oa.person&suchwert2=&opt2=AND&suchfeld3=o.date_year&suchwert3=&startindex=0&page=0&dir=2&suche="
    link_constant = "https://www.bibliothek.tu-chemnitz.de"

    page = requests.get(url)
    # Store the contents of the website under doc
    doc = lh.fromstring(page.content)
    # parsing the html content
    list_of_dfs = pd.read_html(url)
    df = list_of_dfs[0]  # list_of_dfs contains number of table, parsing index 0 indication taking first table only
    indexes = df[0].tolist()  # converting column number 0 into list
    indexes.pop()  # removing the garbage of last index
    titles = df[1].tolist()
    titles.pop()
    authors = df[2].tolist()
    authors.pop()
    years = df[3].tolist()
    years.pop()
    alllinks = doc.xpath('//tr/td/a/@href')
    alllinks.pop()
    links = alllinks.pop(0)
    full_link = link_constant + links

    # dictionary of lists
    dict = {'Index': indexes, 'Title': titles, 'URL': full_link, 'Author': authors, 'Year': years}

    dframe = pd.DataFrame(dict)  # coverting to data frame

    # json
    dframe.to_json('export_dataframe.json', orient='records', lines=True)

    return dframe.to_json(orient="records")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/scrap-data', methods=['GET','POST'])
def convert_output():
    keyword = request.form['keyword']
    result = scrap_website(keyword)
    print(result)
    output = {
        "output": result
    }
    response = {str(key): value for key, value in output.items()}
    return jsonify(result=response)

if __name__ == '__main__':
    app.run(debug=True)
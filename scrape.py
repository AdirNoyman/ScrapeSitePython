import requests
import datetime
from requests_html import HTML

url = 'https://www.boxofficemojo.com/year/world'

now = datetime.datetime.now()
year = now.year


def url_to_txt(url, filename="world.html", save=False):
    req = requests.get(url)
    if req.status_code == 200:
        html_text = req.text
        if save:
            with open(f"world-{year}.html", 'w') as f:
                f.write(html_text)
        return html_text
    return "Ooppsssss...Can't grab this site's data 🤷‍♂️"


html_text = url_to_txt(url)
req_html = HTML(html=html_text)
print(req_html.find("table"))

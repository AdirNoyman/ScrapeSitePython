import requests
import datetime as dt
import pandas as pd
from requests_html import HTML
import os

BASE_DIR = os.path.dirname(__file__)


def url_to_txt(url, filename="world.html", save=False):
    req = requests.get(url)
    if req.status_code == 200:
        html_text = req.text
        # if save:
        #     with open(f"world-{year}.html", 'w') as f:
        #         f.write(html_text)
        return html_text
    return "Ooppsssss...Can't grab this site's data 🤷‍♂️"

table_data = []
header_names = []

def parse_and_extract(url,name='2020'):
    html_text = url_to_txt(url)
    req_html = HTML(html=html_text)
    table_class = ".imdb-scroll-table"
    req_table = req_html.find(table_class)
    if len(req_table) == 1:
        parsed_table = req_table[0]
        rows = parsed_table.find("tr")
        print("rows: ", rows)
        header_row = rows[0]
        print("header row: ", type(header_row))
        header_cols = header_row.find('th')
        header_names = [x.text for x in header_cols]
        for row in rows[1:]:
            # print(row.text)
            cols = row.find("td")
            row_data = []
            for i, col in enumerate(cols):
                # print(i, col.text, '\n\n')
                row_data.append(col.text)
            table_data.append(row_data)
            df = pd.DataFrame(table_data, columns=header_names)
            path = os.path.join(BASE_DIR, 'data')
            os.makedirs(path, exist_ok=True)
            file_path = os.path.join('data', f'{name}.csv')
            df.to_csv(file_path, index=False)


def run(start_year=None, years_ago=5):
    if start_year is None:
        now = dt.datetime.now()
        start_year = now.year
# raise an error if the start year is not an Int
    assert isinstance(start_year, int)
    assert len(str(start_year)) == 4
    for i in range(0,years_ago):
        url = f'https://www.boxofficemojo.com/year/world/{start_year}'
        parse_and_extract(url, str(start_year))
        print(f"finished year {start_year}")
        start_year -= 1


if __name__ == "__main__":
    run(2020,4)


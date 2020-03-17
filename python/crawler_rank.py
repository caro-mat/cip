import requests
import csv
import pandas as pd
from bs4 import BeautifulSoup
from bs4 import ResultSet


def send_request(path):
    response = requests.get(path)
    if response.status_code != 200:
        print("Request failed ")
    else:
        print("Request successful ")
        return response

def collect_items(initial_path):

    path = initial_path
    raw_data = send_request(path)
    html = BeautifulSoup(raw_data.content, 'html.parser')
    return html

def extract_features(html):
    schools = []
    for element in html.select("tr",class_=["odd", "even"]):
        center = element.select("center")
        rank = []
        for i in center:
            rank.append(i.text)
        if rank:
            rank_overall = rank[0]
            rank_presence = rank[2]
            rank_impact = rank[3]
            rank_open = rank[4]
            rank_excellence = rank[5]

            school = [rank_overall, rank_presence, rank_impact, rank_open, rank_excellence]
            schools.append(school)

    content_data_frame = pd.DataFrame(schools)
    content_data_frame.columns = \
        ["rank_overall", "rank_presence", "rank_impact", "rank_open", "rank_excellence"]
    return content_data_frame


def export_to_file(data_frame, path, file_name):

    full_path = path + file_name
    with open(full_path, 'w', encoding='utf-8', newline='') as file:
        export = data_frame.to_csv(quoting=csv.QUOTE_NONNUMERIC, index=False, encoding='utf-8')
        file.write(export)

def main():

    html = collect_items("http://www.webometrics.info/en/world")
    content_data_frame = extract_features(html)
    export_to_file(content_data_frame, '../data/', 'test_ranking.csv') # Hier nach belieben den Pfad noch ändern

if __name__ == '__main__':
    main()


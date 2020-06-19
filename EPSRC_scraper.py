import requests
from bs4 import BeautifulSoup
import csv


# opens the text file which contains all the project refs we need. Project url is base_url + reference
def get_project_links():
    base_url = 'https://gow.epsrc.ukri.org/NGBOViewGrant.aspx?GrantRef='
    links_list = []
    with open('refs.txt') as f:
        for reference in f.readlines():
            full_url = base_url + reference
            links_list.append(full_url.strip())
    return links_list


# grabs the project data and returns a list
def get_project_data():
    full_data = []
    for link in get_project_links():
        try:
            page = requests.get(link)
            soup = BeautifulSoup(page.text, 'html.parser')

            award_data = []
            for table in soup.find_all('table', {'id': 'tblFound'}):
                for ref in table.find('span', {'id': 'lblGrantReference'}):
                    award_data.append(ref.strip())
                for scheme_info in soup.find('span', {'id': 'lblAwardType'}):
                    award_data.append(scheme_info)

            #I want topics and sectors to form one string each, and each topic to be separated by ";"
                topics = []
                for topic_table in table.find_all('table', {'summary': 'topic classifications'}):
                    for topics1 in topic_table.find_all('td', {'class': 'DetailValue'}):
                        topics.append(topics1.text.strip())
                    for topics2 in topic_table.find_all('td', {'class': 'DetailValueAlt'}):
                        topics.append(topics2.text.strip())
                award_data.append("; ".join(topics).strip().rstrip(";"))
                sectors = []
                for sector_table in table.find_all('table', {'summary': 'sector classifications'}):
                    for sectors1 in sector_table.find_all('td', {'class': 'DetailValueAlt'}):
                        sectors.append(sectors1.text.strip())
                    for sectors2 in sector_table.find_all('td', {'class': 'DetailValueAltAlt'}):
                        sectors.append(sectors2.text.strip())
                award_data.append("; ".join(sectors).strip().rstrip(';'))
                for panel_info in table.find_all('a', {'id': 'dgPanelHistory_ctl02_lnkPanelName'}):
                    award_data.append(panel_info.text)
            print(award_data)

            full_data.append(award_data)
        except TypeError:
            pass
    return full_data


headers = ['reference', 'scheme', 'topics', 'sectors', 'panel']

with open('EPSRC_info.csv', encoding='utf-8', mode='w') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(get_project_data())


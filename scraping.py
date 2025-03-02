from datetime import datetime

import requests
from bs4 import BeautifulSoup


def get_petition_list() -> list:
    """ Get the list of the petitions from the wallonie parlement website """
    url = "https://www.parlement-wallonie.be/pwpages?p=petition-list&d=all"

    response = requests.get(url, verify=False)

    soup = BeautifulSoup(response.content, 'html.parser')
    petitions = []

    for div_petition in soup.find_all('div', class_='panel_petitions_list'):
        # get the link
        a = div_petition.find('a', href=True)
        # extract the id of the petition
        petition_id = a['href'].split('=')[-1]

        # get the text of the link
        a_text = a.get_text(strip=True)

        is_open = False
        if a_text == 'Voir et signer':
            is_open = True

        petitions.append({
            'id': petition_id,
            'is_open': is_open
        })

    return petitions


def get_petition_info(petition_id: int) -> dict:
    """ Get the information of a petition from the wallonie parlement website """
    url = f"https://www.parlement-wallonie.be/pwpages?p=petition-detail&id={petition_id}"

    petition_dict = {'id': petition_id}

    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.content, 'html.parser')

    # get title
    title = soup.find('div', class_='row page').find('h4').get_text(strip=True)
    petition_dict['title'] = title

    # get author, date of deposit and vote count
    basic_info_div = soup.find('div', class_='col-xs-12 col-sm-8 col-md-8 col-lg-8')
    if basic_info_div:
        basic_info = basic_info_div.find('p').get_text(strip=True)
        basic_info = basic_info[11:]  # remove "Déposée par"
        author, basic_info_next = basic_info.rsplit("le", 1)
        author = author.strip()
        petition_dict['author'] = author

        open_date_str, basic_info_next = basic_info_next.split("|", 1)
        open_date_str = open_date_str.strip()

        open_date = datetime.strptime(open_date_str, "%d/%m/%Y")
        petition_dict['open_date'] = open_date

        # spans for vote count and end date
        spans = basic_info_div.find_all('span', class_='label')

        vote_count = spans[0].get_text(strip=True)
        petition_dict['vote_count'] = int(vote_count)

        close_date_str = spans[1].get_text(strip=True)

        closed = False
        if "pétition clôturée" in basic_info_div.get_text(strip=True):
            closed = True
            close_date_str = close_date_str.replace(': pétition clôturée automatiquement', '')
            close_date_str = close_date_str.replace(': pétition clôturée', '')
            close_date_str = close_date_str.strip()

        # convert to datetime
        close_date = datetime.strptime(close_date_str, "%d/%m/%Y")
        petition_dict['close_date'] = close_date

        petition_dict['closed'] = closed

    # get email
    email_div = soup.find('div', class_='col-xs-12 col-sm-4 col-md-4 col-lg-4 text-right')
    if email_div:
        email_link = email_div.find('a', href=True)
        email = None
        if email_link:
            email = email_link['href'].replace('mailto:', '')

        petition_dict['email'] = email

    # get description
    espace_top_bg_div = soup.find('div', class_='col-xs-12 espace-top-bg')
    description = None
    if espace_top_bg_div:
        # Trouver le div précédent qui est son frère
        description_div = espace_top_bg_div.find_previous_sibling('div', class_='col-xs-12')
        if description_div:
            description = description_div.get_text(strip=True)

    petition_dict['description'] = description
    return petition_dict


import re
from collections import defaultdict
import requests
from bs4 import BeautifulSoup
import pandas as pd

from pharma_track.models import Drug
from scripts.pfizer_header import HIT_URL, IPAYLOAD, CRAWL_URL, PAYLOAD, HEADERS, MAX_LOOP_PAGE


def _fetch_data(request_url, regex):
    """
    Make request and fetch data

    :param request_url: request url
    :param regex: regex string to get data
    :return: list
    """
    r = requests.get(request_url)
    soup = BeautifulSoup(r.content, features="lxml")
    return soup.find_all("div", {"class": regex})


def _roche_scrap():
    """ Crawling from roche

    :return: pandas data
    """
    regex = re.compile('row item phase*')
    g_data = _fetch_data("https://www.roche.com/research_and_development/who_we_are_how_we_work/pipeline.html", regex)

    data = defaultdict(list)
    for content in g_data:
        name = content.find("span", {"class": "compound"}).find("strong")
        subName = content.find("span", {"class": "generic"})
        indication = content.find("div", {"class": "cell indication"})
        phase = content.find("div", {"class": "cell phase"}).find("span", {"class": "access"})
        company = content.find("dd", {"class": "managedBy"})

        # Parse name
        try:
            data['name'].append(name.text.strip())
        except Exception as e:
            print(e)
            data['name'].append(None)

        # Parse subName
        try:
            data['sub_name'].append(subName.text.strip())
        except Exception as e:
            data['sub_name'].append(None)

        # Parse Indication
        try:
            data['indication'].append(indication.text.strip())
        except Exception as e:
            print(e)
            data['indication'].append(None)

        # Parse Phase
        try:
            phase_text = phase.text.strip().split(". ")[1].strip()
            data['phase'].append(phase_text)
        except Exception as e:
            print(e)
            data['phase'].append(None)

        # Parse Company
        try:
            company_text = company.text.strip().split(". ")[1].strip()
            data['company'].append(company_text)
        except Exception as e:
            print(e)
            data['company'].append(None)

        data['source'].append('Roche')

    df = pd.DataFrame(data)
    print(df)
    return df


def _gilead_get_phase(p):
    return {
        'phase-1': 'Phase 1',
        'phase-2': 'Phase 2',
        'phase-3': 'Phase 3',
        'phase-4': 'Phase 4',
    }.get(p, p)


def _gilead_scrap():
    """ Crawling from gilead

    :return: pandas data
    """

    regex = re.compile('row*')
    g_data = _fetch_data("http://www.gilead.com/research/pipeline", regex)


    data = defaultdict(list)
    for content in g_data:
        name = content.find("div", {"class": "description"}).find("h4")

        # raw name, subName
        name_tuple = name.text.split('\n')
        raw_name = name_tuple[0]
        raw_name = raw_name.replace("\xa0", " ").split(" (")

        # raw Indication
        raw_indication = [t for t in name_tuple if t and 'Potential Indication' in t]

        # raw Phase
        p_regex = re.compile('phase')
        phase = content.find("div", {"class": p_regex})

        # Parse name
        try:
            data['name'].append(raw_name[0].strip())
        except Exception as e:
            print(e)
            data['name'].append(None)

        # Parse subName
        try:
            data['sub_name'].append(raw_name[1].strip().strip(')').strip())
        except Exception as e:
            print(e)
            data['sub_name'].append(None)

        # Parse Indication
        try:
            indication = raw_indication[0].replace("Potential Indication:", "").strip()
            data['indication'].append(indication)
        except Exception as e:
            print(e)
            data['indication'].append(None)

        # Parse Phase
        try:
            p = phase.attrs['class'][1]
            data['phase'].append(_gilead_get_phase(p))
        except Exception as e:
            print(e)
            data['phase'].append(None)

        # Parse Company
        # @TODO: Check company name from crawled data for company
        company = 'Gilead Sciences'
        data['company'].append(company)

        data['source'].append('Gilead')

    df = pd.DataFrame(data)
    print (df.encode('utf-8'))
    return df

def _pfizer_fetch_data(crawl_data):
    regex = re.compile('odd|even')
    soup = BeautifulSoup(crawl_data, features="lxml")
    g_data = soup.find_all("tr", {"class": regex})
    data = defaultdict(list)

    for content in g_data:
        name = content.find("div", {"class": "compound-name"})
        sub_name = content.find("td", {"class": "views-field views-field-field-ugcf-compound-type"})
        indication = content.find("td", {"class": "views-field views-field-field-ugcf-indication"})
        phase = content.find("td", {"class": "views-field views-field-field-ugcf-phase-of-development"})

        # Parse name
        try:
            data['name'].append(name.text.strip())
        except Exception as e:
            print(e)
            data['name'].append(None)

        # Parse subName
        try:
            data['sub_name'].append(sub_name.text.strip())
        except Exception as e:
            print(e)
            data['sub_name'].append(None)

        # Parse indication
        try:
            data['indication'].append(indication.text.strip())
        except Exception as e:
            print(e)
            data['indication'].append(None)

        # Parse phase
        try:
            pphase = {
                "Registration": "Phase 4"
            }.get(phase.text.strip(), phase.text.strip())

            data['phase'].append(pphase)

        except Exception as e:
            print(e)
            data['phase'].append(None)

        data['company'].append('Pfizer')
        data['source'].append('Pfizer')

    df = pd.DataFrame(data)
    print(df)
    return df

def _pfizer_scrap():
    """ Crawling from pf

    :return: pandas data
    """
    hit_url = HIT_URL
    crawl_url = CRAWL_URL
    init_payload = IPAYLOAD
    payload = PAYLOAD
    headers = HEADERS
    max_page = MAX_LOOP_PAGE

    session = requests.session()
    session.get(hit_url)

    for counter in range(max_page):
        if not counter:
            pload = init_payload
        else:
            pload = payload.format(counter)
        response = session.post(crawl_url, data=pload, headers=headers)
        crawl_data = ""
        if response.status_code == 200:
            data = response.json()
            for d in data:
                if d.get('command', '') == 'viewsLoadMoreAppend' or d.get('command', '') == 'insert':
                    if not d.get('data'):
                        break
                    crawl_data = ''.join(map(str, [crawl_data, d.get('data')]))

        if crawl_data:
            pfizer_data = _pfizer_fetch_data(crawl_data)
            for data in pfizer_data.itertuples():
                save_drug(data)
        elif not crawl_data and not counter:
            pass
        else:
            break

def save_drug(data):
    drug = Drug.objects.filter(name=data.name, sub_name=data.sub_name, indication=data.indication).first()
    if not drug:
        Drug(name=data.name, sub_name=data.sub_name, indication=data.indication, phase=data.phase,
             company=data.company, source=data.source).save()
    else:
        if not (drug.phase == data.phase and drug.company == data.company and drug.source == data.source):
            drug.phase = data.phase
            drug.company = data.company
            drug.source = data.source
            drug.version += 1
            drug.save()

def run(*args):
    if 'roche' in args:
        print('START CRAWLING FROM ROCHE')
        roche_data = _roche_scrap()
        for data in roche_data.itertuples():
            save_drug(data)

    if 'gilead' in args:
        print('START CRAWLING FROM GILEAD')
        gilead_data = _gilead_scrap()
        for data in gilead_data.itertuples():
            save_drug(data)

    if 'pfizer' in args:
        print('START CRAWLING FROM PFIZER')
        _pfizer_scrap()


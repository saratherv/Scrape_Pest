from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import pandas as pd

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

# function to process all data


def scrape_data(data):
    href_tags = data.find_all(href=True)
    url = href_tags[0]['href']
    url_call = 'http://www.agriculture.gov.au' + str(url) 
    r_html = simple_get(url_call)
    html1 = BeautifulSoup(r_html, 'html.parser')
    try:
        name = html1.find('div', class_='pest-header-content').find('h2').get_text()
        image_url = html1.find('div', class_ ='pest-header-image').find('img').get('src')
        origin = str(html1.find('div', class_='pest-header-content').find_all('p')[1].get_text()).split(' ')[3].split('Distribution')[0]
        temp_1 = html1.find('div', id ='collapsefaq')
        temp_1 = temp_1.find_all('div')
        suspect_specimen = str(temp_1[2].get_text())
        # ae = str(temp_1[0].get_text())
        identify = str(temp_1[1].get_text())
        # print(image_url,image_url,origin,suspect_specimen,identify)
        print('..')
        return {'name': name, 'image_url': image_url,'origin': origin, 'suspect_specimen': suspect_specimen, 'identify': identify}
    except : 
        # print('error here')
        return {'name': 'error', 'image_url': 'error', 'origin': 'error', 'suspect_specimen': 'error', 'identify': 'error'}






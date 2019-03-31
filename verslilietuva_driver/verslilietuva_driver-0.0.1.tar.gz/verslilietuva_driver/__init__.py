__site_url__ = 'https://edb.verslilietuva.lt'
__base_url__ = 'https://edb.verslilietuva.lt'

import bs4, json
from tqdm import tqdm
from urllib.parse import urljoin
from metadrive._requests import get_session
from metadrive._bs4 import get_soup, dictify_ul
from metadrive._selenium import get_drive

def _login():
    pass

def _harvest(limit=None):

    session = get_session()

    print("Landing and retrieving pagination.")
    url = urljoin(__site_url__, 'companie?perPage=100')
    soup = get_soup(url, session)
    pagination = parsers.get_pagination(soup)

    print('Retrieving listing pages. Pages:')
    records = []

    for page_id in tqdm(range(1, pagination['max_id'])):
        url = urljoin(__site_url__, 'companie/?perPage=100＆page={}'.format(page_id))
        soup = get_soup(url, session)

        for row in soup.find_all('tr', {'class': 'companyTab hoverTR'}):
            records.append(parsers.parse_list_row(row))

    print('Retrieving each company page content. Pages:')
    driver = get_drive(headless=True)
    for i, record in tqdm(enumerate(records)):
        url = record.get('profile_url')

        if url is not None:
            del record['profile_url']
            record['-'] = url

        if not url[-1].isdigit():
            skipped.append((i, url))
            print('SKIPPED:', i, url)
            continue
        soup = get_soup(url, driver, use='selenium')

        if soup.find('a', {'href': '#menu1'}):
            driver.find_element_by_link_text('Qualification').click()
            qualifications_soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
        else:
            qualifications_soup = None

        if soup.find('a', {'href': '#menu2'}):
            driver.find_element_by_link_text('Sectors').click()
            sectors_soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
        else:
            sectors_soup = None

        content = parsers.parse_page(
            soup, qualifications_soup, sectors_soup)

        records[i].update(content)


    driver.close()

    return records


# records = generate()

# df = pandas.io.json.json_normalize(records)

# df['min_employees'] = pandas.to_numeric(df['business.employees'].apply(lambda x: x.split(' - ')[0] if isinstance(x, str) else x))
# df['max_employees'] = pandas.to_numeric(df['business.employees'].apply(lambda x: x.split(' - ')[-1] if isinstance(x, str) else x))
# df['min_turnover'] = pandas.to_numeric(df['business.turnover_eur'].apply(lambda x: x.split(' - ')[0][:-1] if isinstance(x, str) else x))
# df['max_turnover'] = pandas.to_numeric(df['business.turnover_eur'].apply(lambda x: x.split(' - ')[-1][:-1] if isinstance(x, str) else x))
# df['business.export_as_percent_of_turnover'] = pandas.to_numeric(df['business.export_as_percent_of_turnover'])

# df.to_excel('verslilietuva-edb.xlsx')

# df = pandas.read_excel('verslilietuva-edb.xlsx')


# from crawls import db

# db['edb.verslilietuva.lt-companies'].insert_many(records)

class parsers:

    def get_pagination(soup):
        pagination = soup.find('ul', {'class': 'pagination'})
        pagelinks = pagination.find_all('li')
        max_id = int(pagelinks[-2].text) + 1
        return {'max_id': max_id}

    def parse_list_row(soup):
        record = {}
        img = soup.find('img')
        if img:
            record['list_image'] = __site_url__ + img['src']
        bio = soup.find('td', {'class': 'search_company_description'})
        if bio:
            record['list_description'] = bio.text.strip()
        sectors = soup.find('td', {'class': 'search_company_sectors'})
        if sectors:
            record['list_sectors'] = sectors.text.strip()

        record['profile_url'] = urljoin(__site_url__, 'profile/'+ bio.attrs['data-company'])

        return record

    def parse_page(soup,
                   qualifications_soup=None,
                   sectors_soup=None):
        # pages #

        record = {}
        record['contact'] = {}

        title = soup.find('h3', {'class': 'panel-title'})
        if title is not None:
            record['contact']['company_name'] = title.text

        contact = soup.find(
            'div', {
                'class': 'col-lg-3 col-md-3 col-sm-3 col-xs-12 left_col'})

        for p in contact.find_all('p'):
            if 'fa-user' in repr(p):
                record['contact']['contact_person_name'] = p.text.strip()
            if 'fa-briefcase' in repr(p):
                record['contact']['contact_person_role'] = p.text.strip()
            if 'fa-envelope' in repr(p):
                a = p.find('a')
                if a is not None:
                    record['contact']['email'] = a.text.strip()
            if 'fa-phone' in repr(p):
                a = p.find('a')
                if a is not None:
                    record['contact']['phone'] = a.attrs['href'].rsplit(':', 1)[-1]
            if 'fa-map-marker' in repr(p):
                record['contact']['address'] = p.text.strip()
            if 'fa-qrcode' in repr(p):
                record['contact']['company_code'] = p.text.strip()
            if 'fa-truck' in repr(p):
                record['contact']['export_markes'] = p.text.strip()
            if 'fa-globe' in repr(p):
                a = p.find('a')
                if a is not None:
                    url = a.attrs['href']
                    if url.startswith('http://www.rekvizitai.lt'):
                        record['contact']['rekvizitai_url'] = url
                    else:
                        record['contact']['website'] = a.attrs['href']

        record['business'] = {}
        main = soup.find('div', {'id': 'home'})

        for child in main.descendants:
            if '<h4 class="text-uppercase">Description</h4>' in repr(child):
                p = child.find('p')
                if p is not None:
                    record['business']['description'] = p.text.strip()
            if '<h4 class="text-uppercase">Business  Line</h4>' in repr(child):
                p = child.find('p')
                if p is not None:
                    record['business']['business_line'] = p.text.strip()
            if '<h4 class="profile_table_box_title">employees</h4>' in repr(child):
                div = child.find('div', {'class': 'profile_table_box_text'})
                if div is not None:
                    record['business']['employees'] = div.text.strip()
                    if record['business']['employees'] == '>1000':
                        record['business']['employees'] = '1001 - 9999'
            if '<h4 class="profile_table_box_title">turnover, <span class="color-blue">€</span></h4>' in repr(child):
                div = child.find('div', {'class': 'profile_table_box_text'})
                if div is not None:
                    record['business']['turnover_eur'] = div.text.strip()
            if '<h4 class="profile_table_box_title">Export as <span class="color-blue">%</span> of turnover</h4>' in repr(child):
                div = child.find('div', {'class': 'profile_table_box_text'})
                if div is not None:
                    record['business']['export_as_percent_of_turnover'] = div.text.strip()
            if '<h4 class="profile_table_box_title">Year of establishment</h4>' in repr(child):
                div = child.find('div', {'class': 'profile_table_box_text'})
                if div is not None:
                    record['business']['year_of_establishment'] = div.text.strip()
            if '<h4 class="text-uppercase">List of products</h4>' in repr(child):
                p = child.find('p')
                if p is not None:
                    record['business']['list_of_products'] = p.text.strip()

            if '<h4 class="text-uppercase">Video presentation</h4>' in repr(child):
                iframe = child.find('iframe')
                if iframe is not None:
                    record['business']['video_presentation_url'] = iframe.attrs['src']

            if '<h4 class="text-uppercase">Awards</h4>' in repr(child):
                p = child.find('p')
                if p is not None:
                    record['business']['awards'] = p.text.strip()

        extra_links = main.find_all('a', {'class': 'profile_a'})
        if extra_links is not None:
            record['business']['extra_product_links'] = []
            for link in extra_links:
                record['business']['extra_product_links'].append(
                    {'title': link.attrs['title'],
                     'url': link.attrs['href']}
                )

        download_pdf = main.find('a', {'class': 'btn-danger'})
        if download_pdf is not None:
            record['business']['summary_pdf_url'] = download_pdf.attrs['href']


        if qualifications_soup is not None:
            main = qualifications_soup.find('div', {'id': 'menu1'})

            for child in main.descendants:
                if '<h4 class="text-uppercase">Awards</h4>' in repr(child):
                    p = child.find('p')
                    if p is not None:
                        record['business']['awards'] = p.text.strip()
                if '<h4 class="text-uppercase">Asociations</h4>' in repr(child):
                    p = child.find('p')
                    if p is not None:
                        record['business']['associations'] = p.text.strip()
                if '<h4 class="text-uppercase">Certificates</h4>' in repr(child):
                    p = child.find('p')
                    if p is not None:
                        record['business']['certificates'] = p.text.strip()
                if '<h4 class="text-uppercase">Standards</h4>' in repr(child):
                    p = child.find('p')
                    if p is not None:
                        record['business']['standards'] = p.text.strip()

        if sectors_soup is not None:
            main = sectors_soup.find('div', {'id': 'menu2'})
            ul = main.find('ul')
            if ul is not None:
                record['business']['sectors'] = json.dumps([dictify_ul(ul)])

        return record

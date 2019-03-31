from metadrive._selenium import get_drive
from metadrive._selenium import ActionChains
from selenium.webdriver.common.keys import Keys
import bs4, time

driver = get_drive(proxies={'socks_proxy': '127.0.0.1:9999'})

driver.get('https://www.researchgate.net')
driver.get('https://www.researchgate.net/jobs/post/express/ExpressCheckoutJobSingleStep?wi=5c1e212db93ecda0422d9020&wf=express&cs=cover_')


def toggle_fields():
    driver.find_element_by_class_name('nova-e-tag-input__trigger-button').click()

def toggle_locations():
    driver.find_element_by_xpath("""//*[@id="rgw1_5c1e8916f2fc8"]/div/div/div/div[1]/div/div[3]/div/div/div/div[1]/div/div[2]/div[2]/div/div/div/div[2]/button""").click()

def get_field(i=0):
    toggle_fields()
    for _ in range(i):
        actions = ActionChains(driver)
        actions.send_keys(Keys.DOWN)
        actions.perform()
    actions = ActionChains(driver)
    actions.send_keys(Keys.ENTER)
    actions.perform()

def to_field(i=0):
    while True:
        get_field(i)
        time.sleep(1)
        soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
        field = soup.find('div', {'aria-labelledby': 'downshift-1-label'}).find('input', {'aria-labelledby': 'downshift-1-label'}).attrs['value']
        location = soup.find('div', {'aria-labelledby': 'downshift-2-label'}).find('input', {'aria-labelledby': 'downshift-2-label'}).attrs['value']
        researchers = soup.find('div', {'class': 'job-reach-tool__main-count'})

        if field:
            break

    researchers = int(researchers.find('strong').text.replace(',',''))
    print(researchers)

    statistics = soup.find('div', {
        'class': 'job-reach-tool__stats-results'}).find_all('strong')

    statistics = {item[1]: item[0].text
                  for item in zip(statistics, ['senior', 'experienced', 'early'])}

    statistics.update({'count': researchers, 'field': field, 'location': location})

    return statistics

def get_location(i=0):
    toggle_locations()
    for _ in range(i):
        actions = ActionChains(driver)
        actions.send_keys(Keys.DOWN)
        actions.perform()
    actions = ActionChains(driver)
    actions.send_keys(Keys.ENTER)
    actions.perform()

def to_location(i=0):
    while True:
        get_location(i)
        soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
        field = soup.find('div', {'aria-labelledby': 'downshift-1-label'}).find('input', {'aria-labelledby': 'downshift-1-label'}).attrs['value']
        location = soup.find('div', {'aria-labelledby': 'downshift-2-label'}).find('input', {'aria-labelledby': 'downshift-2-label'}).attrs['value']
        researchers = soup.find('div', {'class': 'job-reach-tool__main-count'})

        if location:
            break

    researchers = int(researchers.find('strong').text.replace(',',''))
    print(researchers)

    statistics = soup.find('div', {
        'class': 'job-reach-tool__stats-results'}).find_all('strong')

    statistics = {item[1]: item[0].text
                  for item in zip(statistics, ['senior', 'experienced', 'early'])}

    statistics.update({'count': researchers, 'field': field, 'location': location})

    return statistics



records = []

# field = 55
# location = 255

for field in range(325):
    data = to_field(field)
    records.append(data)

    for location in range(286):
        data = to_location(location)
        records.append(data)

len(records)

from crawls import db

#db['researchgate.net-statistics'].insert_many(records)

#         records.append(
#             {'location': None,
#              'field': None,
#             'researchers': {
#                 'count': None,
#                 'senior_pct': None,
#                 'experienced_pct': None,
#                 'early_career_pct': None
#             }}
#         )

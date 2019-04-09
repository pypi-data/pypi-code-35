import requests
from bs4 import BeautifulSoup






def scrape_website_main():
    home_page = requests.get("https://www.factorio.com/")
    if(home_page.status_code == 200):
        soup = BeautifulSoup(home_page.content, 'html.parser')
        latest_release_content              = soup.find_all('div', class_='span4 index-sidebar')
        latest_release_content              = soup.find_all('dd')
        latest_stable_version_string        = str(latest_release_content[0])
        latest_experimental_version_string  = str(latest_release_content[1])

        latest_stable_version               = latest_stable_version_string[4:11]
        latest_experimental_version         = latest_experimental_version_string[4:11]
        return(latest_stable_version, latest_experimental_version)

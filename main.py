import random
import time

from selenium.webdriver.common.by import By
from Utils.bs4_selenium import FirefoxBrowser
from Utils.csv_saver import bussiness_csv_saver
from Utils.directory_creator import directory_creator
from Utils.logger import logger
from constants import url, base_url

firefox_browser = FirefoxBrowser()
firefox_browser.driver.get(url)

# region :Search button click

time.sleep(5)
element = firefox_browser.driver.find_element(By.CSS_SELECTOR,
                                              '.js-view-dom-id-ebf276740bf00a58475dfaf81711812ba4f5cc9d3d3f63ff74a6741de816a3d9 > div:nth-child(1) > form:nth-child(4) > div:nth-child(6) > input:nth-child(1)')
element.click()

# endregion :Search button click

temp = []
result = {}
page = 1
unique_id = 1


def extract_data():
    global next_link
    data = {}
    soup = firefox_browser.get_current_soup()

    section = soup.find('tbody')
    rows = section.find_all('tr')

    for row in rows:
        cells = row.find_all('td')
        if len(cells) == 5:

            link = base_url + cells[1].find("a")['href']

            time.sleep(random.randint(10, 15))
            soup = firefox_browser.get_soup(link)

            detail_section = soup.find('tbody')
            detail_rows = detail_section.find_all('tr')
            for detail_row in detail_rows:
                desc = detail_row.find('td', class_='aiSosDetailDesc').text.strip()
                value = detail_row.find('td', class_='aiSosDetailValue').text.strip() or "No Data Available"
                data[desc] = value
                data['Link'] = link
            temp.append(data)
            data = {}

        elif len(cells) == 1:
            if cells[0].find_all('a')[-1].text.strip().startswith("Next"):
                next_link = base_url + '/cgi/corpname.mbr/' + cells[0].find_all('a')[-1]['href']
            else:
                next_link = "https://arc-sos.state.al.us/CGI/CORPNAME.MBR/INPUT"
    return next_link


# Pagination
while True:
    try:
        logger.info(f"Page: ({page})")
        next_link = extract_data()
        firefox_browser.get_url(next_link)
        page += 1
    except Exception as e:
        logger.error(f"Error: {e}")
        break

# Dictionary maker
for item in temp:
    result[unique_id] = item
    unique_id += 1

# Save report
created_direcctory = directory_creator('../csv_files/')
bussiness_csv_saver(result, created_direcctory + 'Government_entities.csv')

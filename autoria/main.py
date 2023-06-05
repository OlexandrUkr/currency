import csv
import sqlite3
import random
from time import sleep

import requests
from bs4 import BeautifulSoup

VEHICLE_DETAILS = [
        'Марка, модель, рік',
        'Двигун',
        'Кількість власників'
    ]


def random_sleep():
    sleep(random.randint(8, 30))


def get_page_content(page: int, size: int = 100) -> str:
    query_parameters = {
        'indexName': 'auto,order_auto,newauto_search',
        'country.import.usa.not': '-1',
        'price.currency': '1',
        'abroad.not': '-1',
        'custom.not': '-1',
        'page': page,
        'size': size
    }
    base_url = 'https://auto.ria.com/uk/search/'
    response = requests.get(base_url, params=query_parameters)
    response.raise_for_status()
    return response.text


def get_vehicle_details(data_link_to_view: str) -> str:
    # car_details_url = f"https://auto.ria.com/uk/{vehicle_id}.html"
    car_details_url = f"https://auto.ria.com/uk{data_link_to_view}"

    response = requests.get(car_details_url)

    car_page_content = response.text

    soup = BeautifulSoup(car_page_content, features="html.parser")

    vehicle_all_details = soup.find("main", {"class": "auto-content"})

    vehicle_info_checked_html = vehicle_all_details.find("div", {"class": "technical-info ticket-checked"})

    try:
        vehicle_info_checked_items = vehicle_info_checked_html.find_all("dd")
    except AttributeError:
        # потрібної інформаціїї нема у данного авто
        return

    vehicle_info = []

    for item in vehicle_info_checked_items:
        a = item.find("span", {"class": "label"})
        b = item.find("span", {"class": "argument"})

        if a and b and a.get_text() in VEHICLE_DETAILS:
            vehicle_info.append(b.get_text())

    return vehicle_info


class CSVWriter:
    def __init__(self, filename, headers):
        self.filename = filename
        self.headers = headers

        with open(self.filename, 'w', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(self.headers)

    def write(self, row: list):
        with open(self.filename, 'a', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(row)


class StdOutWriter:

    def write(self, row: list):
        print(row)  # noqa: T201


class SQLiteWriter:
    def __init__(self, table):
        self.table = table
        con = sqlite3.connect("work.db")
        cur = con.cursor()

        sql = f'''
        CREATE TABLE IF NOT EXISTS '{table}' (
            adsID INTEGER PRIMARY KEY,
            car_brand varchar(255),
            car_engine varchar(255),
            car_numb_owners smallint
        );
        '''
        cur.execute(sql)
        con.commit()
        con.close()

    def write(self, data):
        con = sqlite3.connect("work.db")
        cur = con.cursor()

        sql = f'''
                INSERT INTO '{self.table}' (car_brand, car_engine, car_numb_owners)
                VALUES (?, ?, ?);
                '''

        cur.execute(sql, data)
        con.commit()
        con.close()


def main():
    writers = (
        CSVWriter('cars.csv', ['car_id', 'data_link_to_view']),
        # CSVWriter('cars2.csv', ['car_id', 'data_link_to_view']),
    )
    writers_item = (
        CSVWriter('cars_info.csv', VEHICLE_DETAILS),
        SQLiteWriter('Autoria_ads'),
        SQLiteWriter('Autoria_ads_2')
    )

    page = 0
    # page = 21314

    while True:
        # print(f'Page: {page}')
        page_content = get_page_content(page)
        page += 1

        soup = BeautifulSoup(page_content, features="html.parser")

        search_results = soup.find("div", {"id": "searchResults"})
        ticket_items = search_results.find_all("section", {"class": "ticket-item"})

        if not ticket_items:
            break

        for ticket_item in ticket_items:
            car_details = ticket_item.find("div", {"class": "hide"})
            car_id = car_details['data-id']
            data_link_to_view = car_details['data-link-to-view']

            for writer in writers:
                writer.write([car_id, data_link_to_view])

            random_sleep()

            vehicle_data = get_vehicle_details(data_link_to_view)
            # print(vehicle_data)
            if vehicle_data:
                for writer_item in writers_item:
                    writer_item.write(vehicle_data)

        random_sleep()


if __name__ == '__main__':
    main()

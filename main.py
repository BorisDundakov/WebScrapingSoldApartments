from bs4 import BeautifulSoup
import requests
import Apartment
import re
from csv import writer


def save_csv(list_appartments):
    # encoding cyrilic
    with open('recently_sold_houses.csv', 'w', encoding='windows-1251', newline='') as f:
        thewriter = writer(f)
        headers = ['City', 'Address', 'Number of Bedrooms', 'Square meters']
        # city, address, n_bedrooms, sq_m
        thewriter.writerow(headers)
        for appartment in list_appartments:
            city = appartment["city"]
            address = appartment["address"]
            n_bedrooms = appartment["n_bedrooms"]
            sq_m = appartment["sq_m"]
            appartment_info = [city, address, n_bedrooms, sq_m]
            thewriter.writerow(appartment_info)


def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def export_data():
    url = "https://home2u.bg/"
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')
    # _class indicates a html class
    location = soup.find_all('div', class_="article__body-main")
    appartment_details = soup.find_all('div', class_="article__body-inner")

    list_appartments = []

    for location_details in location:
        current_appartment = {}
        city = location_details.find_next('h5').text
        address = location_details.find_next('p').text  # <p>
        current_appartment["city"] = city
        current_appartment["address"] = address
        list_appartments.append(current_appartment)

    for details in appartment_details:
        n_bedrooms = details.find_next('p')  # <p>
        sq_m = n_bedrooms.find_next_siblings('p')

        str_n_bedrooms = remove_html_tags(str(n_bedrooms))
        str_sq_m = remove_html_tags(str(*sq_m))

        for apartment in list_appartments:
            if "n_bedrooms" not in apartment:
                apartment["n_bedrooms"] = str_n_bedrooms
                apartment["sq_m"] = str_sq_m
                break

    return list_appartments


if __name__ == '__main__':
    appartments = export_data()
    save_csv(appartments)

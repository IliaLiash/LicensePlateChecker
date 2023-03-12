import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime


def filter_licence_number(license_number):
    filtered_number = ''.join(filter(str.isdigit, license_number))
    if 7 <= len(filtered_number) <= 8:
        return filtered_number
    return False


def get_plate_status(license_number='3839065'):
    try:
        filtered_license = filter_licence_number(license_number)
        if filtered_license:
            r = requests.get(f"https://www.find-car.co.il/car/private/{filtered_license}")
            soup = BeautifulSoup(r.text, 'html.parser', from_encoding='utf-8')
            license_status = soup.find("div", {'class': re.compile(r"^important_details$")}, partial=False)
            license_status = [div.text for div in license_status][3]
            recycled_status = soup.find(soup.find_all('span', {'class': 'bad'}), partial=False)
            car_brand = soup.find('title').text.split('|')[1].strip()
            car_brand = re.sub(r'[^A-Za-z0-9 ]+', '', car_brand)
            if 'תאריך הורדה' in str(recycled_status):
                return 'The vehicle was recycled'
            pattern = r'\d{2}.\d{2}.\d{4}'
            license_expiry_date = datetime.strptime(re.findall(pattern, license_status)[0], "%d/%m/%Y").date()
            if license_expiry_date >= datetime.now().date():
                return license_expiry_date, car_brand
            return False
        else:
            return 'Incorrect License number'
    except Exception as e:
        return e


if __name__ == "__main__":
    print(get_plate_status('493:47-601'))

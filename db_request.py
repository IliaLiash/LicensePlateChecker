import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime


def filter_licence_number(license_number):
    filtered_number = ''.join(filter(str.isdigit, license_number))
    if 7 <= len(filtered_number) <= 8:
        return True
    return False


def get_plate_status(license_number='3839065'):
    try:
        if filter_licence_number(license_number):
            r = requests.get(f"https://www.find-car.co.il/car/private/{license_number}")
            soup = BeautifulSoup(r.text, 'html.parser')
            divs = soup.find("div", {'class': re.compile(r"^important_details$")}, partial=False)
            divs = [div.text for div in divs][3]
            span = soup.find(soup.find_all('span', {'class': 'bad'}), partial=False)
            if 'תאריך הורדה' in str(span):
                return 'The vehicle was recycled'
            pattern = r'\d{2}.\d{2}.\d{4}'
            license_expiry_date = datetime.strptime(re.findall(pattern, divs)[0], "%d/%m/%Y").date()
            if license_expiry_date >= datetime.now().date():
                return license_expiry_date
            return False
        else:
            return 'Incorrect License number'
    except Exception as e:
        return e


if __name__ == "__main__":
    print(get_plate_status())

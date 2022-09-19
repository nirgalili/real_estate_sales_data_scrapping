# imports

from bs4 import BeautifulSoup
import pandas as pd
import os

# globals

GOVMAP_URL = 'https://www.govmap.gov.il/'
GOVMAP_DEMO_VIDEO_URL = 'https://drive.google.com/file/d/1nGzsG02YW-eDYimibP7hbLHaY2bMWO5P/view?usp=sharing'


# functions


def script_manual_instractions():
    print('')
    print(f'Follow the workflow shown in this video {GOVMAP_DEMO_VIDEO_URL}.\n\
    The steps are:\n\
    1. go to govmap site {GOVMAP_URL}\n\
    2. create polygon on area of interest real estate.\n\
    3. after table with info of latest deals open press F12.\n\
    4. copy the class "realsestate-items-wrapper table-mode scrollWrapper"\n\
    5. create txt file with the copied text.\n\
    6. put the file in the directory.'
          )
    print('')
    input('Press any key after finish all steps: ')


def create_list_for_column(class_name: str, key:str):
    temp_list_not_in_text = soup.find_all(class_=class_name)
    new_list = []
    for item in temp_list_not_in_text:
        if class_name == "price-deal cell":
            new_list.append(item.get_text().split()[0])
        elif key == "gush":
            gush_helka_list = item.get_text().split("-")[0]
            new_list.append(gush_helka_list)
        elif key == "helka":
            gush_helka_list = item.get_text().split("-")[1]
            new_list.append(gush_helka_list)
        else:
            new_list.append(item.get_text())
    return new_list


def create_dataframe_from_dictionary(dictionary):
    temp_df = pd.DataFrame.from_dict(dictionary, orient='index')
    temp_df = temp_df.transpose()
    return temp_df


def open_excel_file(filename_in_directory_with_xlsx):
    os.system(f'start "excel.exe" {filename_in_directory_with_xlsx}')


if __name__ == "__main__":

    script_manual_instractions()

    with open('new.txt', encoding="utf8") as file:
        site_text = file.read()

    soup = BeautifulSoup(site_text, "lxml")

    column_classes_dict = {
        "sale date": "first sale-date cell",
        "address": "address-text",
        "neighborhood": "neighborhood-text",
        "gush": "gush-helka cell",
        "helka": "gush-helka cell",
        "asset-type": "asset-type cell",
        "rooms": "rooms cell",
        "floor": "floor cell ellipsis-text",
        "area": "mr cell",
        "price": "price-deal cell",
    }

    new_dict = {}
    for key, value in column_classes_dict.items():
        new_list = create_list_for_column(value, key)
        new_dict[key] = new_list

    df = create_dataframe_from_dictionary(new_dict)

    df.to_excel("output.xlsx")

    open_excel_file("output.xlsx")
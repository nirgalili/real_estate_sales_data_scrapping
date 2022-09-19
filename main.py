# imports

from bs4 import BeautifulSoup
import pandas as pd
import os


# globals

GOVMAP_URL = 'https://www.govmap.gov.il/'
GOVMAP_DEMO_VIDEO_URL = 'https://drive.google.com/file/d/1nGzsG02YW-eDYimibP7hbLHaY2bMWO5P/view?usp=sharing'


# functions

def show_video():
    os.startfile("demo.mp4")


def script_manual_instructions():
    print('')
    print(f'Please refer to the README.md for graphical explanation\n\
The steps are:\n\
    1. go to govmap site {GOVMAP_URL}\n\
    2. Browse the map to find a place of interest.\n\
    3. Highlight real estate deals layer.\n\
    4. In application menu go to regional analysis.\n\
    5. Create polygon on area of interest real estate.\n\
    6. After table with info of latest deals open press F12.\n\
    7. Copy the class "realsestate-items-wrapper table-mode scrollWrapper"\n\
    8. Create txt file with the copied text.\n\
    9. Save the file in the project path.'
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

    try:
        show_video()

    except FileNotFoundError:
        pass

    script_manual_instructions()

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
"""

This code uses whatsapp web to add number
"""
# Importing relevant Modules
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import time
import pandas as pd

"""
Opening whatsapp using options
"""

"""!!!!!!!!!!!!!!!! Change this Path acccording to your system !!!!!!!!!!!!!!!!"""
user_data_dir = "C:/Users/<YOUR_USERNAME>/AppData/Local/Google/Chrome/User Data/Default"

# if already logged in then no need to login again this way
# setting up the chrome options
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={user_data_dir}")
driver = webdriver.Chrome(options=options)

# opening whatsapp web
driver.get('https://web.whatsapp.com/')
check_list = None
# waiting for the page to load
while True:
    try:
        chat_list = driver.find_element(By.ID, 'pane-side')
        break
    except Exception as e:
        time.sleep(2)

"""
Finding Group name
"""

"""!!!!!!!!!!!!!!!! Change this Name to your WP group name !!!!!!!!!!!!!!!!"""
gname = "<GROUP_NAME>"
while True:
    try:
        search_box = driver.find_element(By.XPATH, '//div[@aria-label="Search"][@role="textbox"]')
        search_box.click()  # Click to activate the search box
        search_box.send_keys(gname)  # Type the group name
        search_box.send_keys(Keys.ENTER)  # Press Enter to search
        time.sleep(3)
        # Check if the group is opened by looking for the chat header
        chat_header = driver.find_element(By.XPATH, f'//*[@id="pane-side"]/div[1]/div/div/div[2]/div/div/div/div[2]/div[1]/div[1]/span/span')
        chat_header.click()
        break

    except Exception as e:
        print("Group not found, enter exact group name!! - ")
        gname = input()
        cross = driver.find_element(By.XPATH, '//*[@id="side"]/div[1]/div/div[2]/span/button/span')
        cross.click()
        time.sleep(1)

print("Group name validation done!")

"""
Opening Add participant screen
"""
group_details = driver.find_element(By.XPATH, '//*[@id="main"]/header/div[2]/div[1]/div/span')
group_details.click()
time.sleep(1.5)
add_screen = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[3]/div/div[5]/span/div/span/div/div/div/section/div[7]/div[2]/div[1]/div[2]/div/div')
add_screen.click()

"""
Bringing data from google spreadsheets
"""
# Authenticate with your Google account
gauth = GoogleAuth()
gauth.LocalWebserverAuth()  # Follow the authentication steps in your web browser

# Create a GoogleDrive instance
drive = GoogleDrive(gauth)

# Search for the file by name
"""!!!!!!!!!!!!!!!! Change file name to your file name in Gdrive !!!!!!!!!!!!!!!!"""
file_name = "<GDRIVE_FILE_NAME>"
file_list = drive.ListFile({'q': f"title = '{file_name}'"}).GetList()

if len(file_list) == 0:
    print(f"File '{file_name}' not found in Google Drive.")
else:
    csv_file = file_list[0]

# Download the CSV file
csv_file.GetContentFile("../Data/responses.csv", mimetype="text/csv")
df = pd.read_csv("../Data/responses.csv")

"""
Finding data
"""
# Correcting data
ph_list = df['Phone No.'].to_list()
added_list = pd.read_csv("../Data/added.csv")['Phone No.'].to_list()

to_add = []
for i in ph_list:
    if i not in added_list:
        to_add.append(int(i))
        

"""
Functions
"""
def click_cross():
    cross = driver.find_element(By.XPATH, '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div/div[1]/div/div[2]/span/button/span')
    cross.click()

def add_participants(numbers):
    for num in numbers:
        search_box = driver.find_element(By.XPATH, '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div/div[1]/div/div[2]/div[2]/div/div/p')
        search_box.click()
        time.sleep(0.5)
        search_box.send_keys(str(num))
        time.sleep(1)
        try:
            try:
                contact = driver.find_element(By.XPATH, '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div/div[2]/div/div/div/div[1]/div/div[2]/div')
            except:
                contact = driver.find_element(By.XPATH, '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div/div[2]/div/div/div/div[2]/div/div[2]/div')
            contact.click()
            click_cross()
            time.sleep(1)
        except Exception as e:
            print(f"Error while adding {num} - \n{e}")
            click_cross()
            pass

add_participants(to_add)

"""
Updating added.csv
"""
add_csv = [df.set_index("Phone No.").loc[row, "Name"] for row in to_add]
add_csv = list([(addName, addPhone) for addName, addPhone in zip(add_csv, to_add)])
import csv
with open('../Data/added.csv', 'a', newline="\n") as f:
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerow("\n")
    write.writerows(add_csv)
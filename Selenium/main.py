# %% [markdown]
# ### This code uses whatsapp web to add number

# %% [markdown]
# ### Importing relevant Modules

# %%
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager

import time, os
import pandas as pd

# %% [markdown]
# ### Global Variables

# %%
"""!!!!!!!!!!!!!!!! Change these acccording to your system !!!!!!!!!!!!!!!!"""
timeout = 10
your_username = "<YOUR_USERNAME>"  # Replace with your actual username of the system

if os.name == 'nt': # Windows
    user_data_dir = f"C:/Users/{your_username}/AppData/Local/Microsoft/Edge/User Data/Default" # Replace with your actual profile path
elif os.name == 'posix': # Linux
    user_data_dir = f"/home/{your_username}/.config/microsoft-edge/Default"  # Replace with your actual profile path
else:
    raise Exception("Unsupported OS. Please update the user_data_dir path accordingly.") 

# Specify Edge exec/binary location
if os.name == 'nt': # Windows
    exec_path= r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" # Replace with your actual profile path
else: # Linux
    exec_path = "/usr/bin/microsoft-edge-stable" # Replace with your actual profile path


# %% [markdown]
# ### Opening whatsapp using options

# %%
def setup_driver():
        """Set up and configure the WebDriver"""
        edge_options = Options()
        
        # Add common options to avoid detection
        edge_options.add_argument("--disable-dev-shm-usage")
        edge_options.add_argument("--disable-blink-features=AutomationControlled")
        edge_options.add_argument("--disable-extensions")
        edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        edge_options.add_experimental_option("useAutomationExtension", False)
        edge_options.add_experimental_option("detach", True)
        
        # Set user agent
        edge_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) edge/119.0.0.0 Safari/537.36")
        
        # Use user data directory for session persistence
        edge_options.add_argument(f"--user-data-dir={user_data_dir}")

        # Use user Edge exec/binary location
        edge_options.binary_location = exec_path
        
        # Initialize the driver
        service = Service(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=edge_options)
        # driver.set_window_size(1280, 800)
        
        # Set page load timeout
        driver.set_page_load_timeout(timeout)
        
        # Disable webdriver detection
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        return driver

# %%
# if already logged in to whatsapp then no need to login again this way
driver = setup_driver()

# opening whatsapp web
driver.get('https://web.whatsapp.com/')
check_list=None
# waiting for the page to load
while True:
    try:
        chat_list = driver.find_element(By.ID, 'pane-side')
        break
    except Exception as e:
        time.sleep(2)

# %% [markdown]
# ### Finding Group name

# %%
"""!!!!!!!!!!!!!!!! Change this Name to your WP group name !!!!!!!!!!!!!!!!"""
gname = "<GROUP_NAME>"  # Replace with your actual group name
while True:
    try:
        search_box = driver.find_element(By.XPATH, '//*[@id="side"]/div[1]/div/div[2]/div/div/div[1]/p')
        search_box.click()  # Click to activate the search box
        search_box.send_keys(gname)  # Type the group name
        search_box.send_keys(Keys.ENTER)  # Press Enter to search
        time.sleep(3)
        # Check if the group is opened by looking for the chat header
        chat_header = driver.find_element(By.XPATH, f'//*[@id="main"]/header/div[2]/div[1]/div/span')
        break

    except Exception as e:
        print("Group not found, enter exact group name!! - ")
        gname=input()
        cross=driver.find_element(By.XPATH, '//*[@id="side"]/div[1]/div/div[2]/span/button/span')
        cross.click()
        time.sleep(1)

print("Group name validation done!")


# %% [markdown]
# ### Opening Add participant screen

# %%
group_details = driver.find_element(By.XPATH, '//*[@id="main"]/header/div[2]/div[1]/div/span')
group_details.click()
time.sleep(1)
add_screen = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[3]/div/div[5]/span/div/span/div/div/div/section/div[11]/div[2]/div[1]/div/div[2]/div/div/div')
add_screen.click()

# %% [markdown]
# ### Bringing data from google spreadsheets

# %%
# Remember to put your clients_secrets.json in 'pwd'
# Authenticate with your Google account
gauth = GoogleAuth()
gauth.LocalWebserverAuth()  # Follow the authentication steps in your web browser

# Create a GoogleDrive instance
drive = GoogleDrive(gauth)

# %%
"""!!!!!!!!!!!!!!!! Change file name to your file name in Gdrive !!!!!!!!!!!!!!!!"""
# Search for the file by name
file_name = "<GDRIVE_FILE_NAME>"
file_list = drive.ListFile({'q': f"title = '{file_name}'"}).GetList()
df = pd.DataFrame()
if len(file_list) == 0:
    print(f"File '{file_name}' not found in Google Drive.")
else:
    csv_file = file_list[0]

    # Download the CSV file
    csv_file.GetContentFile("../Data/responses.csv", mimetype="text/csv")
    df = pd.read_csv("../Data/responses.csv")
    print(f"File '{file_name}' downloaded successfully.")

# %% [markdown]
# ### Finding data

# %%
print(df.head(2))

# %%
# Correcting data
ph_list = df['Phone No.'].to_list()
added_list = pd.read_csv("../Data/added.csv")['Phone No.'].to_list()

to_add = []
for i in ph_list:
    if i not in added_list:
        to_add.append(int(i))
        
to_add=list(set(to_add))  # Remove duplicates
print(f"Total {len(to_add)} members to be added to the group.")
if len(to_add) == 0:
    print("No new members to add.")

print(to_add)

# %% [markdown]
# ### Functions

# %%
def click_cross():
    try:
        cross = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div/div[1]/div/div[2]/span/button/span'))
        )
        cross.click()
    except Exception as e:
        print(f"[!] Failed to click cross: {e}")

def add_participants(numbers):
    for num in numbers:
        try:
            # Wait for the search box to be clickable
            search_box = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div/div[1]/div/div[2]/div/div/div[1]/p'))
            )
            search_box.click()
            search_box.clear()
            search_box.send_keys(str(num))

            # Wait for the contact result section to load
            WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/span[2]/div/span/div/div/div/div/div/div/div[2]/div/div/div[1]'))
            )

            try:
                # First option: contact found
                contact = WebDriverWait(driver, 2).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div/div[2]/div/div/div/div[1]/div/div[2]'))
                )
            except:
                # Second option: contact not saved
                contact = WebDriverWait(driver, 2).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div/div[2]/div/div/div/div[2]/div/div[2]'))
                )

            contact.click()
            click_cross()

        except Exception as e:
            print(f"Error while adding {num}:\n{e}")
            click_cross()
            continue
def count_added_participants():
    try:
        # Wait for the participants container to be present
        container = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div/span[1]'))
        )

        # Find all direct child divs (each one representing a participant)
        participant_divs = container.find_elements(By.XPATH, './div')

        print(f"[✓] Total participants added: {len(participant_divs)-1}")
        return len(participant_divs)-1 # Subtracting 1 for the extra div that is present

    except Exception as e:
        print(f"[!] Error counting participants: {e}")
        return 0


# %%
add_participants(to_add)
total = count_added_participants()
if total != len(to_add):
    print(f"[!] Some participants were not added. Expected: {len(to_add)}, Actual: {total}")


# %% [markdown]
# ### Manual step (for now)

# %%
# will automate this later

"""
click the tick icon to confirm adding participants
then you may need to invite them to the group
"""

# %% [markdown]
# ### Updating added.csv

# %%
import csv

filename = '../Data/added.csv'
headers = ['Name', 'Phone No.']

# Prepare add_csv as before
add_csv = [df.set_index("Phone No.").loc[row, "Name"] for row in to_add]
add_csv = list([(addName, addPhone) for addName, addPhone in zip(add_csv, to_add)])

# Check if file exists
file_exists = os.path.isfile(filename)

if not file_exists:
    # Create file with headers
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
else:
    # Check if headers exist
    with open(filename, 'r', newline='') as f:
        reader = csv.reader(f)
        first_row = next(reader, None)
        if first_row != headers:
            # Read existing data
            data = list(reader)
            # Rewrite file with headers
            with open(filename, 'w', newline='') as fw:
                writer = csv.writer(fw)
                writer.writerow(headers)
                writer.writerows(data)

# Append new rows
with open(filename, 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(add_csv)

print(add_csv)


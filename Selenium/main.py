
# ### This code uses whatsapp web to add number

# ### Importing relevant Modules

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

import time, os, csv, json
import pandas as pd
from tkinter import filedialog
import tkinter as tk

# ### Selenium Variables

"""!!!!!!!!!!!!!!!! Change these acccording to your system !!!!!!!!!!!!!!!!"""
timeout = 10

home_dir = os.path.expanduser("~")  # User home directory (C:/Users/<name> on Windows, /home/<name> on Linux)

if os.name == 'nt': # Windows
    user_data_dir = os.path.join(home_dir, "AppData/Local/Microsoft/Edge/User Data/Default")
elif os.name == 'posix': # Linux
    user_data_dir = os.path.join(home_dir, ".config/microsoft-edge/Default")
else:
    raise Exception("Unsupported OS. Please update the user_data_dir path accordingly.") 

# Specify Edge exec/binary location
if os.name == 'nt': # Windows
    exec_path= r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" # Replace with your actual profile path
else: # Linux
    exec_path = "/usr/bin/microsoft-edge-stable" # Replace with your actual profile path


# ### Opening whatsapp using options


CONFIG_FILE = "config.json"
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}
def get_edge_driver_path():
    config = load_config()
    driver_path = config.get("driver_path")

    if driver_path and os.path.exists(driver_path):
        print(f"[INFO] Using saved Edge driver path: {driver_path}")
        return driver_path
    else:
        root = tk.Tk()
        root.withdraw() # Hide the main window
        if os.name == "nt": # Windows
            print("[WARN] Edge driver path not found or invalid. Please select the msedgedriver.exe file.")
            file_path = filedialog.askopenfilename(
                title="Select msedgedriver.exe",
                filetypes=[("Edge Driver Executable", "msedgedriver.exe")]
            )
        else: # Linux
            print("[WARN] Edge driver path not found or invalid. Please select the msedgedriver file.")
            file_path = filedialog.askopenfilename(
                title="Select msedgedriver",
                filetypes=[("Edge Driver Bin", "msedgedriver")]
            )
        root.destroy() # Destroy the Tkinter root window
        if file_path:
            config["driver_path"] = file_path
            with open(CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=4)
                print(f"[INFO] Saved Edge driver path: {file_path}")
            return file_path
        else:
            print("[!] No Edge driver selected. Exiting.")
            exit()
            
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
        edge_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0")
        
        # Use user data directory for session persistence
        edge_options.add_argument(f"--user-data-dir={user_data_dir}")

        # Use user Edge exec/binary location
        edge_options.binary_location = exec_path
        
        # Initialize the driver
        try:
            service = Service(EdgeChromiumDriverManager().install())
        except Exception as e:
            print("[!] Error installing Edge driver")
            print("[!] Rolling back to using user defined Edge driver path.")
            service = Service(executable_path=get_edge_driver_path())
        driver = webdriver.Edge(service=service, options=edge_options)
        driver.set_window_size(1280, 800)
        
        # Set page load timeout
        driver.set_page_load_timeout(timeout)
        
        # Disable webdriver detection
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        return driver

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

# ### Finding Group name

"""!!!!!!!!!!!!!!!! Change this Name to your WP group name !!!!!!!!!!!!!!!!"""
gname = "Optus Placement Drive X IIIT Ranchi"  # Replace with your actual group name

SEARCH_BOX_LOCATORS = [
    (By.CSS_SELECTOR, '#side input[aria-label="Search or start a new chat"]'),
    (By.CSS_SELECTOR, '#side input[data-tab]'),
    (By.CSS_SELECTOR, '#side input[type="text"]'),
    (By.CSS_SELECTOR, '#side div[contenteditable="true"]'),
]

def get_search_box(timeout=10):
    deadline = time.time() + timeout
    last_err = None
    for loc in SEARCH_BOX_LOCATORS:
        try:
            remaining = max(deadline - time.time(), 1)
            return WebDriverWait(driver, remaining).until(EC.element_to_be_clickable(loc))
        except Exception as e:
            last_err = e
    raise last_err # type: ignore

def clear_search_box():
    try:
        box = get_search_box(3)
        box.click()
        box.send_keys(Keys.CONTROL, "a")
        box.send_keys(Keys.DELETE)
    except Exception:
        pass

while True:
    try:
        search_box = get_search_box()
        search_box.click()  # Click to activate the search box
        search_box.send_keys(Keys.CONTROL, "a")
        search_box.send_keys(Keys.DELETE)
        search_box.send_keys(gname)  # Type the group name
        time.sleep(2)

        # Find exact match among the search results and click it
        results = driver.find_elements(By.CSS_SELECTOR, '#pane-side [title]')
        match = next((r for r in results if r.get_attribute('title').strip().lower() == gname.strip().lower()), None)  # type: ignore
        if match is None:
            raise Exception(f"No search result found for '{gname}'")
        match.click()
        time.sleep(3)

        # Check if the group is opened by looking for the chat header
        chat_header = driver.find_element(By.XPATH, '//*[@id="main"]/header/div[1]/div[2]/div[1]/div/span')
        break

    except Exception as e:
        print(f"[!] {e}")
        print("Group not found, enter exact group name!! - ", end="")
        gname = input().strip()
        clear_search_box()
        time.sleep(1)

print("Group name validation done!")

# ### Opening Add participant screen

group_details = driver.find_element(By.XPATH, '//*[@id="main"]/header/div[1]/div[2]/div[1]/div/span')
group_details.click()
time.sleep(1)
add_screen = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[3]/div/div[6]/span/div/span/div/div/div/div/section/div[11]/div/div[1]/div')
add_screen.click()

# ### Loading data (Google Drive or local CSV)

def load_from_gdrive(file_name, dest_path):
    # Remember to put your client_secrets.json in 'pwd'
    # Authenticate with your Google account
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  # Follow the authentication steps in your web browser

    # Create a GoogleDrive instance
    drive = GoogleDrive(gauth)

    # Search for the file by name
    file_list = drive.ListFile({'q': f"title = '{file_name}'"}).GetList()
    if len(file_list) == 0:
        raise FileNotFoundError(f"File '{file_name}' not found in Google Drive.")

    # Download the CSV file
    file_list[0].GetContentFile(dest_path, mimetype="text/csv")
    print(f"File '{file_name}' downloaded successfully to '{dest_path}'.")

def load_from_local_csv(csv_path):
    """Validate a local CSV file (absolute or relative path) and return its absolute path."""
    if not csv_path:
        raise ValueError("local_csv_file is empty. Set a path to your CSV file.")
    csv_path = os.path.abspath(os.path.expanduser(csv_path))
    if not os.path.isfile(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    print(f"[INFO] Using local CSV: {csv_path}")
    return csv_path

# ### Data source settings

"""!!!!!!!!!!!!!!!! Change these acccording to your system !!!!!!!!!!!!!!!!"""
data_mode = "csv"  # "gdrive" (Google Drive file) or "csv" (local CSV file)
gdrive_file_name = "Scriveners Club Old form Response"  # File name in Google Drive (used when data_mode == "gdrive")
local_csv_file = r"../Data/numbers.csv"  # Path to local CSV with a 'Phone No.' column, absolute or relative (used when data_mode == "csv")
responses_file = "../Data/responses.csv"  # Local copy read later (gdrive download target)

if data_mode == "gdrive":
    load_from_gdrive(gdrive_file_name, responses_file)
elif data_mode == "csv":
    responses_file = load_from_local_csv(local_csv_file)
else:
    raise ValueError(f"Unknown data_mode '{data_mode}'. Use 'gdrive' or 'csv'.")

# ### Finding data

df = pd.read_csv(responses_file)
df.head(2)

# Check if file exists
filename = '../Data/added.csv'
headers = ['Name', 'Phone No.']

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

# ### Functions

# For Testing
to_add = ["0000000000", "1111111111", "2222222222"]  # Example phone numbers to add

ADD_SEARCH_LOCATORS = [
    (By.CSS_SELECTOR, 'input[aria-label="Search name, number or @username"]'),
    (By.CSS_SELECTOR, 'input[placeholder*="Search name"]'),
    (By.CSS_SELECTOR, 'div[role="dialog"] input[type="text"]'),
]

def find_first(locators, timeout=5):
    deadline = time.time() + timeout
    last_err = Exception("no locator matched")
    for loc in locators:
        try:
            remaining = max(deadline - time.time(), 1)
            return WebDriverWait(driver, remaining).until(EC.element_to_be_clickable(loc))
        except Exception as e:
            last_err = e
    raise last_err

def get_add_search_box(timeout=5):
    return find_first(ADD_SEARCH_LOCATORS, timeout)

def clear_field(el):
    el.click()
    el.send_keys(Keys.CONTROL, "a")
    el.send_keys(Keys.DELETE)

def click_cross():
    """Clear the add-participant search field (replaces the old X button)."""
    try:
        clear_field(get_add_search_box(2))
    except Exception:
        print("[!] Failed to clear search box")

def is_already_added():
    """The 'Already added to group' note only shows for the current search result."""
    xpath = '//*[contains(normalize-space(.), "Already added to group") and not(.//*[contains(normalize-space(.), "Already added to group")])]'
    for note in driver.find_elements(By.XPATH, xpath):
        try:
            if note.is_displayed():
                return True
        except Exception:
            pass
    return False

def find_result_row(num):
    num = str(num)
    xpaths = [
        f'//*[@id="app"]//div[@role="button"][.//*[contains(normalize-space(.),"{num}")]]',
        f'//*[@id="app"]//div[@role="listitem"][.//*[contains(normalize-space(.),"{num}")]]',
        f'//span[(normalize-space()="{num}" or @title="{num}") and not(ancestor::*[@id="pane-side"]) and not(ancestor::*[@id="main"])]',
    ]
    for xp in xpaths:
        for row in driver.find_elements(By.XPATH, xp):
            try:
                if row.is_displayed():
                    return row
            except Exception:
                pass
    return None

def add_participants(numbers):
    click_cross()
    for num in numbers:
        try:
            search_box = get_add_search_box()
            clear_field(search_box)
            search_box.send_keys(str(num))
            time.sleep(2)

            if is_already_added():
                print(f"Contact {num} was already added, skipping click.")
                time.sleep(1)
                continue

            row = find_result_row(num)
            if row is None:
                # No labelled row found: let the combobox pick the first result
                search_box.send_keys(Keys.ENTER)
                time.sleep(1)
                print(f"Contact {num} selected via Enter.")
            else:
                row.click()
                time.sleep(1)
                print(f"Contact {num} clicked successfully.")

        except Exception as e:
            print(f"Error while adding {num}:\n{e}")
        finally:
            click_cross()  # Clear the search field before the next number

def count_added_participants():
    try:
        # Wait for the participants container to be present
        container = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/span[2]/div/span/div/div/div/div/div/div/div/div[2]'))
        )

        # Find all direct child divs (each one representing a participant)
        participant_divs = container.find_elements(By.XPATH, './div')

        print(f"[✓] Total participants added: {len(participant_divs)}")
        return len(participant_divs) # Subtracting 1 for the extra div that is present

    except Exception as e:
        print(f"[!] Error counting participants: {e}")
        return 0


add_participants(to_add)
total = count_added_participants()
if total != len(to_add):
    print(f"[!] Some participants were not added. Expected: {len(to_add)}, Actual: {total}")


# ### Manual step (for now)

# will automate this later

"""
click the tick icon to confirm adding participants
then you may need to invite them to the group
"""

# ### Updating added.csv

# Prepare add_csv as before
add_csv = [df.set_index("Phone No.").loc[row, "Name"] for row in to_add]
add_csv = list([(addName, addPhone) for addName, addPhone in zip(add_csv, to_add)])

# Append new rows
with open(filename, 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(add_csv)

print(add_csv)



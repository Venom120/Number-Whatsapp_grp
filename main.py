# This is a program to add phone Numbers to a whatsapp group
# the numbers will be taken from google drive file (spreedsheet file)
# i have used the numbers that are filled in google forms
# And then i have created 2 csv files which will store all the spredsheet data ----- (reponses.csv)
# and the data of the people which are added in the whatsapp grp **by this program**

# Please do not use it for spam purposes



from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Authenticate with your Google account
gauth = GoogleAuth()
gauth.LocalWebserverAuth()  # Follow the authentication steps in your web browser

# Create a GoogleDrive instance
drive = GoogleDrive(gauth)

# Search for the file by name
file_name = "" # Remember to change your file name here
file_list = drive.ListFile({'q': f"title = '{file_name}'"}).GetList()

if len(file_list) == 0:
    print(f"File '{file_name}' not found in Google Drive.")
else:
    csv_file = file_list[0]

# Download the CSV file
csv_file.GetContentFile("Data/responses.csv", mimetype="text/csv")

import pandas as pd
import numpy as np
df = pd.read_csv("Data/responses.csv")

# Correcting the data
ph = df['Phone No.']
ph = ph.str.replace(' ','')
ph = ph.str.replace(',','')
ph = ph.str[:10] # taking the first 10 digits bcz, sometimes use forget to restrict user to only add one number

# converting dataframe of numbers into list
ph_list = ph.to_list()
for i in range(len(ph_list)):
    ph_list[i] = int(ph_list[i])

# checking the already addeed numbers by this program from csv file so that the program prevents duplicates
added = pd.read_csv("Data/added.csv")
added = added['Phone No.']
added_list = added.to_list()

# finding the numbers to add
to_add = []
for i in range(len(ph_list)):
    if ph_list[i] not in added_list:
        to_add.append(ph_list[i])

if (len(to_add) != 0):
    # import relevant modules
    import pyautogui as gui
    import time
    gui.FAILSAFE=True

    # defining function to use them to find the position of clicks
    def position():
        time.sleep(3)
        print(gui.position())
    def click(x,y):
        time.sleep(1.5)
        gui.click(x,y,button="left")
    def add_participants(to):
        for i in range(len(to)):
            if(i==0):
                time.sleep(1)
                gui.write(f"{to[i]}", interval=0.2)
                time.sleep(10)
                click(544, 121) # type the x, y of the number which pops up when selected a new number
#                                  i have a resolution of 1366, 768 of my laptop and these are the positions
#                                  i got in my laptop after screen mirroring
            else:
                time.sleep(1)
                gui.write(f"{to[i]}", interval=0.2)
                time.sleep(10)
                click(543, 222) # type the x, y of the number which pops up when you have already selected a number 


    #  Open add aparticipants screen in your mobile using your laptop via screen mirroring
    to = to_add
    print("Open add_participants of you grp ")
    print("DO NOT Click the search icon")
     print("You have 10 seconds")
    time.sleep(10)


    click(831, 72) # this the position of the search icon
    add_participants(to)
    time.sleep(3)


    # UPDATING added.csv FILE
    import csv


    x = df['Name'].to_list()
    # merging name and thier respective phone number
    add_csv = []
    for i in range(len(x)):
        add_csv.append([x[i],ph_list[i]])

    # field names
    fields = ['Name', 'Phone No.']

    with open('Data/added.csv', 'w') as f:
        
        # using csv.writer method from CSV package
        write = csv.writer(f)
        
        write.writerow(fields)
        write.writerows(add_csv)
    print("Click on the invite to group textbox!! if shown")
    print("Rest the numbers are Added :)")

else:
     print("There are no new Numbers to add!")



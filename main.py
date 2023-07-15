# This script goes through usernames , and run the scrapper ("InstaAuto-RowScroll") for each
################################################################################################
import os

from InstaAutoRowScroll import scrapper

# The list of ID's to go through
usernamesListFile = open ("usernames.txt","r")
usernamesList = usernamesListFile.readlines()

for username in usernamesList :
    username = username.replace("\n","")
    new_folder_path = r"IDs\_"+username
    os.makedirs(new_folder_path, exist_ok=True)
    #scrapper funtion here <<<
    scrapper(username)

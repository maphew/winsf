'''List all User Shell Folders via ID number.

An alternative to the usual

    objShell = win32com.client.Dispatch("WScript.Shell")
    allUserProgramsMenu = objShell.SpecialFolders("AllUsersPrograms")

because "These special folders do not work in all language locales, a preferred
method is to query the value from User Shell folders"

Sources:

https://stackoverflow.com/questions/2063508/find-system-folder-locations-in-python
https://ss64.com/vb/special.html
https://ss64.com/nt/shell-folders-vbs.txt
https://docs.microsoft.com/en-gb/windows/win32/api/shldisp/ne-shldisp-shellspecialfolderconstants#constants
'''
import win32com.client
import csv

shapp = win32com.client.Dispatch("Shell.Application")

csvfile = "special-folder-constants.csv"

## ----------------------------------------
from collections import namedtuple
UserFolder = namedtuple('UserFolder', 'id, description')

ndata = map(UserFolder._make, csv.reader(open(csvfile)))


## ----------------------------------------
data = list(csv.DictReader(open(csvfile)))

def get_description(name):
    '''Return description as str'''
    for row in data:
        if name.upper() == row["UserFolder"]:
            return row["Description"]

def get_names(data):
    '''Return list of user special folder names from data'''
    names = []
    for row in data:
        names.append(row["UserFolder"])
    return names

def get_path_by_name(name):
    # print(name.upper())
    for row in data:
        if name.upper() == row["UserFolder"]:
            # print(row["ID"])
            return shapp.namespace(int(row["ID"])).self.path
    return None

def print_data(data):
    '''Display user folder Names and Paths'''
    print('{:<20} {}'.format('Name', 'Path'))
    for row in data:
        name = row["UserFolder"]
        path = shapp.namespace(int(row["ID"])).self.path
        print(f'{name:<20} {path}')

if __name__ == "__main__":
    print("-"*40)
    name = 'startmenu'
    path = get_path_by_name(name)
    print("Name:\t{}".format(name))
    print("Path:\t{}".format(path))
    print("Desc:\t{}".format(get_description(name)))
    print("-"*40)


    # print("-"*40)
    # print(get_names(data))

    # print("-"*40)
    # print_data(data)

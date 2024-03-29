r'''Windows user "special folders" (Desktop, Start Menu, Documents, ...) info

    fpath(x)        full path for folder name `x`
    description(x)  description for folder name `x`
    names()         list all special folder names we know about
    print_all()     display all SF names and paths

Example output:

    ----------------------------------------
    Search:	startmenu
    ----------------------------------------
    Name:	STARTMENU
    Path:	C:\Users\mattw\AppData\Roaming\Microsoft\Windows\Start Menu
    Desc:	File system directory that contains Start menu items. A typical path is C:\Users\username\AppData\Roaming\Microsoft\Windows\Start Menu.
    ----------------------------------------

This module is an alternative to the usual

    objShell = win32com.client.Dispatch("WScript.Shell")
    allmenu = objShell.SpecialFolders("AllUsersPrograms")

because "These special folders do not work in all language locales, a preferred
method is to query the value from User Shell folders". So we do that using the
integer IDs from "ShellSpecialFolderConstants Enumeration", published 4/12/2018.

Additionally it turns out using Shell.Application returns more folders than
Wscript.Shell, 38 vs 16.

Sources:

https://stackoverflow.com/questions/2063508/find-system-folder-locations-in-python
https://ss64.com/vb/special.html
https://ss64.com/nt/shell-folders-vbs.txt
https://docs.microsoft.com/en-gb/windows/win32/api/shldisp/ne-shldisp-shellspecialfolderconstants#constants
'''
import win32com.client
import csv
from os import path

shapp = win32com.client.Dispatch("Shell.Application")

here = path.abspath(path.dirname(__file__))

csvfile = path.join(here, "special-folder-constants.csv")
data = tuple(csv.DictReader(open(csvfile)))
    # we wrap in a tuple so the rows are available all the time, and immutable
    # otherwise content of `data` can change in every call, e.g. early return
    # after finding our vaue.

def names(data=data):
    '''Return list of possible user special folder names'''
    names = []
    for row in data:
        names.append(row["Sfname"])
    return names

def description(name):
    '''Return description for `name` as string'''
    for row in data:
        if name.upper() == row["Sfname"]:
            return row["Description"]

def get_sfname(name):
    '''Return Windows special folder for `name` as string or None'''
    for row in data:
        if name.upper() == row["Sfname"]:
            return row["Sfname"]

def fpath(name):
    '''Return full path for `name`. Virtual folders begin with `::`'''
    for row in data:
        if name.upper() == row["Sfname"]:
            return shapp.namespace(int(row["ID"])).self.path

def print_all(data=data):
    '''Display all user special folder names and paths'''
    print('{:<20} {}'.format('Name', 'Path'))
    for row in data:
        id = row["ID"]
        name = row["Sfname"]
        path = shapp.namespace(int(row["ID"])).self.path
        print(f'{id:<2} {name:<20} {path}')

def hunter(start=0, stop=50):
    for i in range(start, stop+1):
        try:
            sf = shapp.namespace(i).self
            ret = i, sf.name, sf.path
        except AttributeError:
            ret = i, None, None
        print(ret)

def demo():
    search = 'startmenu'
    sfname = get_sfname(search)
    path = fpath(search)
    desc = description(search)
    print("-"*40)
    print("Search:\t{}".format(search))
    print("-"*40)
    print("Name:\t{}".format(sfname))
    print("Path:\t{}".format(path))
    print("Desc:\t{}".format(desc))
    print("-"*40)

from knownfolders import folders as kf
# kf.get = kf.get_known_folder_path

if __name__ == "__main__":
    demo()
    # print(kf.get(kf.FOLDERID.StartMenu))
    # print(kf.table['StartMenu'])
    print('Desktop: ', kf.Desktop)
    print('Programs: ', kf.Programs)
    print('Profile: ', kf.Profile)
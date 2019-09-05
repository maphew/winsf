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

try:
    here = path.abspath(path.dirname(__file__))
except NameError:
    here = r"C:\Users\mattw\code\utils\winsf\winsf"

csvfile = path.join(here, "special-folder-constants.csv")
data = tuple(csv.DictReader(open(csvfile)))
    # we wrap in a tuple so the rows are available all the time, and immutable
    # otherwise content of `data` can change in every call, e.g. early return
    # after finding our vaue.

def names(data=data):
    '''Return list of possible user special folder names'''
    names = []
    for row in data:
        names.append(row["UserFolder"])
    return names

def description(name):
    '''Return description for `name` as string'''
    for row in data:
        if name.upper() == row["UserFolder"]:
            return row["Description"]

def get_sfname(name):
    '''Return Windows special folder for `name` as string or None'''
    for row in data:
        if name.upper() == row["UserFolder"]:
            return row["UserFolder"]

def fpath(name):
    '''Return full path for `name`. Virtual folders begin with `::`'''
    for row in data:
        if name.upper() == row["UserFolder"]:
            return shapp.namespace(int(row["ID"])).self.path

def print_all(data=data):
    '''Display all user special folder names and paths'''
    print('{:<20} {}'.format('Name', 'Path'))
    for row in data:
        name = row["UserFolder"]
        path = shapp.namespace(int(row["ID"])).self.path
        print(f'{name:<20} {path}')

def hunter(start=0, stop=50):
    for i in range(start, stop+1):
        try:
            sf = shapp.namespace(i).self
            ret = i, sf.name, sf.path
        except AttributeError:
            ret = i, None, None
        print(ret)


if __name__ == "__main__":
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

    # print("-"*40)
    # print(names())

    # print("-"*40)
    # print_all()

#!/usr/bin/env python3
#Python 3 Linux System Update Script
#Cody Kankel
#Started Jul 11, 2016

import subprocess, sys

def main():
    """Script to update the system of Linux platforms using Python 3, plan on adding sys-info as well."""
    distro = subprocess.getoutput("lsb_release -sd")
    user = subprocess.getoutput("whoami")
    print("Welcome {0}, you are currently running {1}".format((user), (distro)))
    last_update = get_last_update(user)
    yn = input("The last update was {0}, would you like to update now? [y/n]: ".format(last_update))
    if yn == 'Y' or yn == 'y':
        update(user)
    else:
        no_update(yn)
    #Here I plan to add some sys info formatted nice and pretty(free -h etc)
    sys.exit()
#^----------------------------------------------------------------------------- main()
    
def get_last_update(user_name):
    """Method to obtain previous update, path is specified as update_file"""
    update_file = ("/home/" + user_name + "/.mystuff/last_update.txt")
    file_ob = open(update_file, 'r')
    last_update = file_ob.readline()
    file_ob.close()
    return last_update.rstrip()
#^----------------------------------------------------------------------------- get_last_update()

def update(user_name):
    """Updating the system, this is where it is debian-based/apt-get specific, could possibly change"""
    print("Proceeding to update system. . .")
    apt_update = subprocess.Popen(['sudo', 'apt-get', 'update'])
    apt_update.communicate() #making the script wait
    apt_update.wait()
    apt_upgrade = subprocess.Popen(['sudo', 'apt-get', 'dist-upgrade'])
    apt_upgrade.wait()
    apt_remove = subprocess.Popen(['sudo', 'apt-get', 'autoremove'])
    apt_remove.wait()
    save_update(user_name)
    return
#^----------------------------------------------------------------------------- update()

def save_update(user_name):
    """If Y is chosen for update, the time and date will be saved to a file, able to be viewed again"""
    update_file = ("/home/" + user_name + "/.mystuff/last_update.txt")
    file_ob = open(update_file, 'w')
    date = subprocess.getoutput('date')
    file_ob.write(str(date))
    file_ob.close()
    return
#^----------------------------------------------------------------------------- save_update()

def no_update(yn):
    if yn == 'N' or yn == 'n':
        print("We won't update right now.")
    else:
        print("Something other than 'Y' or 'N' was entered, skipping the update.")
    return
#^----------------------------------------------------------------------------- not_update(yn)

#Standard broiler plate to run as main    
if __name__ == '__main__':
    main()
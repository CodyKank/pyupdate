#!/usr/bin/env python3

"""//////////////////////////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"""
  //                           Python 3 Linux System Update Script                              \\
 //                                         Cody Kankel                                          \\  
||                                      Started Jul 11, 2016                                      ||
||                                    Last update: July 14, 2016                                  ||
\\Currently only supports debian/ubuntu distros with apt-get, I plan on adding support for yum   //
 \\and pacman package managers. Still need to allow creation of the folder and file for update! //
  \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\///////////////////////////////////////////////"""


import subprocess, sys

def main():
    """Script to update the system of Linux platforms using Python 3, shows sys-info as well."""
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
    show_sys_info(yn)
    sys.exit()
#^----------------------------------------------------------------------------- main()
    
def get_last_update(user_name):
    """Method to obtain previous update, path is specified as update_file"""
    update_file = ("/home/" + user_name + "/.previous-update.txt")
    try:
        file_ob = open(update_file, 'r')
        last_update = file_ob.readline()
        file_ob.close()
    except FileNotFoundError:
        last_update = "This is the first update!"
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
    update_file = ("/home/" + user_name + "/.previous-update.txt")
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
#^----------------------------------------------------------------------------- no_update(yn)

def show_sys_info(yn):
    """Showing some info, plan to add more"""
    if yn == 'Y' or yn =="y":
        print('Update complete. . .')
        
    print("_".center(80, '_')) #Filling screen with line
    print("Printing System Info".center(80,'.')+ '\n')    
    cpu_proc = subprocess.getoutput("lscpu | grep 'Model name:'")
    cpu_name = " ".join((cpu_proc.split()[2:]))
    cores_proc = subprocess.getoutput("lscpu | grep 'CPU(s):'")
    cores = cores_proc.split()[1]
    arch = subprocess.getoutput("uname -i")

    
    mem_free_proc = subprocess.getoutput("free -h")
    temp = mem_free_proc.split()
    total_mem = temp[7]
    used_mem = temp[8]
    free_mem = temp[9]
    cached_mem = temp[11]
    
    print_info("CPU:", cpu_name)
    print_info("NUM CORES:", cores)
    print_info("ARCHITECTURE:", arch)
    print_seperator()
    
    print("MEMORY USAGE:".center(80))
    print_info("TOTAL MEMORY:", total_mem)
    print_info("USED MEMORY:", used_mem)
    print_info("CACHED MEMORY:", cached_mem)
    print_info("FREE MEMORY:", free_mem)
    print_seperator()
    
    show_gui_info()
    return
#^----------------------------------------------------------------------------- show_sys_info(yn)

def show_gui_info():
    """Will find and print desktop info"""
    desktop_environment = subprocess.getoutput("echo $XDG_CURRENT_DESKTOP")
    option = subprocess.getoutput("echo $GDMSESSION")
    distro = subprocess.getoutput("lsb_release -sd")
    
    print("DESKTOP INFO:".center(80))
    print_info("DISTROBUTION:", distro)
    print_info("SESSION:", option)
    print_info("DESKTOP ENVIRONMENT:", desktop_environment)
    print_seperator()
    return
#^----------------------------------------------------------------------------- show_gui_info()
    
def print_info(str_name, result):
    """Prints the information given as the str_name to be the designator and result being what
    the designator will be. (free mem = str_name, 4K = result)"""
    str_size = 40
    print(str_name.ljust(str_size) + str(result).ljust(str_size))
#^----------------------------------------------------------------------------- print_info(str_name, result)

def print_seperator():
    """Simply prints a separator on screen with periods...."""
    print(".".center(80, '.'))
#^----------------------------------------------------------------------------- print_separator()    

#Standard broiler plate to run as main    
if __name__ == '__main__':
    main()
#!/usr/bin/env python3

"""//////////////////////////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
  //                              Python 3 Linux System Update Script                           \\
 //                                         Cody Kankel                                          \\  
||                                      Started Jul 11, 2016                                      ||
||                                 Last update: September 11th, 2016                              ||
\\Currently only supports debian/ubuntu distros with apt-get, and Arch based distros with pacman.//
 \\                            !RHEL based distros have not been tested yet!                    //
  \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\///////////////////////////////////////////////"""

import subprocess, sys

def main():
    """Gathering user and desktop session, asks user for desire to update."""
    #distro = subprocess.getoutput("lsb_release -sd")
    session = subprocess.getoutput("env | grep 'DESKTOP_SESSION'").split('\n')[0]
    # Getting the first string after the '=' which would in theory be the desktop session name i.e. gnome
    session = session[session.find('=') +1:]
    user = subprocess.getoutput("whoami")
    print("Welcome {0}, you are currently running {1}".format((user), (session)))
    last_update = get_last_update(user)
    user_response = input("The last update was: {0}. \nWould you like to update now? [y/n]: ".format(last_update))
    if user_response == 'Y' or user_response == 'y':
        update(user)
    else:
        no_update(user_response)
    show_sys_info(user_response)
    sys.exit()
#^----------------------------------------------------------------------------- main()
    
def get_last_update(user_name):
    """Method to obtain previous update, path is specified as update_file.
    If the file is not found, assuming this is the first time running the script.
    The file will then be created if 'y' is chosen (executing the update)."""
    # Update-file will contain the date/time of the last update. It is hidden hence the prefix '.'
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
    """Method which actually updates the system. Checks if system is Arch, Debian, etc.
    then properly updates the system. For Arch systems, performs full system upgrade."""
    system = get_system_type()
    print("System identified as, or based on: {0}".format(system))
    print("Proceeding to update system. . .")
    
    if system == 'arch':
        pacman = subprocess.Popen(['sudo', 'pacman', '-Syyu'])
        pacman.wait()
        save_update(user_name)
    elif system == 'debian':
        apt_update = subprocess.Popen(['sudo', 'apt-get', 'update'])
        apt_update.communicate() #making the script wait
        apt_update.wait()
        apt_upgrade = subprocess.Popen(['sudo', 'apt-get', 'dist-upgrade'])
        apt_upgrade.wait()
        apt_remove = subprocess.Popen(['sudo', 'apt-get', 'autoremove'])
        apt_remove.wait()
        save_update(user_name)
    elif system == 'rhel':
        yum = subprocess.Popen(['su', '-c', 'yum', 'update'])
        yum.wait()
        save_update(user_name)
    return
#^----------------------------------------------------------------------------- update()

def get_system_type():
    """Method to discover what distro the system is, i.e. if system is Debian, Red Hat, Arch
    etc. Will look for the ID in /etc/os-release. This means it will discover Antergos, Manjaro
    and others as Arch, and Xubuntu, Ubuntu, and others asd Debian, and Scientific, CentOs, Fedora
    and others  as Red Hat. Method returns the base system as a string."""
    
    system_id = subprocess.getoutput("cat /etc/os-release | grep 'ID'").split()[0]
    system_id.replace('"', '') # Some systems produce (")'s  others do not!
    system_id = system_id[system_id.find('=') + 1:]
    
    # switch statement wanna-be
    distro_choices = {'fedora': 'rhel', 'centos': 'rhel', 'scientific': 'rhel', 'rhel': 'rhel', \
                      'debian': 'debian', 'ubuntu': 'debian', 'xubuntu': 'debian', 'arch': 'arch', \
                      'antergos': 'arch', 'majaro': 'arch'}
    default = 'Unknown'
    system = distro_choices.get(system_id, default)
    return system
#^----------------------------------------------------------------------------- find_system_type()

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
    """Showing some info, plan to add more. Currently shows:
    Number of Cores, CPU"""
    if yn == 'Y' or yn =="y":
        print('Update complete. . .')
        
    print("_".center(80, '_')) #Filling screen with line
    print("Printing System Info".center(80,'.')+ '\n')    
    cpu_proc = subprocess.getoutput("lscpu | grep 'Model name:'")
    cpu_name = " ".join((cpu_proc.split()[2:]))
    cores_proc = subprocess.getoutput("lscpu | grep 'CPU(s):'")
    cores = cores_proc.split()[1]
    arch = subprocess.getoutput("uname -m")

    
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
    distro = subprocess.getoutput("cat /etc/os-release | grep 'PRETTY'")
    distro = distro.split('=')[1].replace('"', '') # Grabbing just the pretty-name
    
    print("DESKTOP INFO:".center(80))
    print_info("DISTRIBUTION:", distro)
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
    return
#^----------------------------------------------------------------------------- print_info(str_name, result)

def print_seperator():
    """Simply prints a separator on screen with periods. 80 chars long."""
    print(".".center(80, '.'))
    return
#^----------------------------------------------------------------------------- print_separator()    

#Standard broiler plate to run as main    
if __name__ == '__main__':
    main()
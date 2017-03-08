#!/usr/bin/env python3

"""//////////////////////////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
  //                              Python 3 Linux System Update Script                           \\
 //                                         Cody Kankel                                          \\
||                                      Started Jul 11, 2016                                      ||
||                                 Last update: Mar 7th, 2017                                     ||
\\Currently only supports debian/ubuntu distros with apt-get, and Arch based distros with pacman.//
 \\                            Also supports the independent distro Solus                       //
  \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\///////////////////////////////////////////////"""

import subprocess, sys

def main():
    """Gathering user and desktop session, asks user for desire to update."""
    if len(sys.argv) > 1:
        if sys.argv[1] == "-s":
            show_sys_info("n")
    user = subprocess.getoutput("whoami")
    print("Welcome {0}".format(user))
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

    if system != 'Unknown':

        print("System identified as, or based on: {0}".format(system))
        print("Proceeding to update system. . .")

        if system == 'arch':
            pacman = subprocess.Popen(['sudo', 'pacman', '-Syyu'])
            pacman.wait()
            save_update(user_name)
            print("\nUpdate complete. . .\n")
        elif system == 'debian':
            apt_update = subprocess.Popen(['sudo', 'apt-get', '-y', 'update'])
            apt_update.communicate() #making the script wait
            apt_update.wait()
            apt_upgrade = subprocess.Popen(['sudo', 'apt-get', '-y', 'dist-upgrade'])
            apt_upgrade.wait()
            apt_remove = subprocess.Popen(['sudo', 'apt-get', '-y', 'autoremove'])
            apt_remove.wait()
            save_update(user_name)
            print("Update complete. . .")
        elif system == 'rhel':
            yum = subprocess.Popen(['su', '-c', 'yum', '-y', 'update'])
            yum.wait()
            save_update(user_name)
            print("Update complete. . .")
        elif system == 'solus':
            update = subprocess.Popen((['sudo', '-S', 'eopkg', '-y', 'up']))
            update.wait()
            save_update(user_name)
            print("Update complete. . .")
    else:
        print("\nSystem is not recognized currently. If you feel as if this is an error,\n"\
                + "please report it on Github.\n")
    return
#^----------------------------------------------------------------------------- update()

def get_system_type():
    """Method to discover what distro the system is, i.e. if system is Debian, Red Hat, Arch
    etc. Will look for the ID in /etc/os-release. This means it will discover Antergos, Manjaro
    and others as Arch, and Xubuntu, Ubuntu, and others as Debian, and Scientific, CentOs, Fedora
    and others  as Red Hat. Method returns the base system as a string."""

    system_id = (subprocess.getoutput("cat /etc/os-release | grep 'ID='")).split('\n')[0]
    system_id = system_id.replace('"','') # Some systems produce (")'s  others do not!
    system_id = system_id[system_id.find('=') + 1:]

    # switch statement wanna-be
    distro_choices = {'fedora': 'rhel', 'centos': 'rhel', 'scientific': 'rhel', 'rhel': 'rhel', \
                      'debian': 'debian', 'ubuntu': 'debian', 'xubuntu': 'debian', 'galliumos': 'debian', \
                      'elementary': 'debian', 'arch': 'arch', 'antergos': 'arch', 'manjaro': 'arch', \
                      'solus': 'solus'}
    default = 'Unknown'
    system = distro_choices.get(system_id, default)
    if system == default:
        system_id = subprocess.getoutput("cat /etc/os-release | grep'ID_LIKE=").split('\n')[0]
        system_id = system_id.replace('"', '')

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
        print("\nAn update will not be applied at this time. . .\n")
    else:
        print("\n|Error:| Something other than 'Y' or 'N' was entered, skipping the update.")
    return
#^----------------------------------------------------------------------------- no_update(yn)

def show_sys_info(yn):
    """Showing some info, plan to add more. Currently shows:
    Number of Cores, CPU"""

    cpu_proc = subprocess.getoutput("lscpu | grep 'Model name:'")
    cpu_name = " ".join((cpu_proc.split()[2:]))
    cores_proc = subprocess.getoutput("lscpu | grep 'CPU(s):'")
    cores = cores_proc.split()[1]
    arch = subprocess.getoutput("uname -m")
    kernel = subprocess.getoutput("uname -r")
    hostname = subprocess.getoutput("uname -n")
    kernelType = subprocess.getoutput("uname -s")


    mem_free_proc = subprocess.getoutput("free -h")
    temp = mem_free_proc.split()
    total_mem = temp[7]
    used_mem = temp[8]
    free_mem = temp[9]
    cached_mem = temp[11]

    
    print_seperator()
    print(("INFO FOR {0}".format(hostname)).center(80," "))
    print_seperator()

    print("SYS INFO:".center(80))
    print_info("CPU:", cpu_name)
    print_info("NUM CORES:", cores)
    print_info("ARCHITECTURE:", arch)
    print_info("KERNEL TYPE:", kernelType)
    print_info("KERNEL:", kernel)
    #print("") # a simple line
    print_seperator()

    print("MEMORY USAGE:".center(80))
    print_info("TOTAL MEMORY:", total_mem)
    print_info("USED MEMORY:", used_mem)
    print_info("CACHED MEMORY:", cached_mem)
    print_info("FREE MEMORY:", free_mem)
    print_seperator()

    show_gui_info()
    sys.exit()
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

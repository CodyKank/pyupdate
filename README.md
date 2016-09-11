#Pyupdate
**Pyupdate** is a small project created to learn the subprocess module and practice using python 3.
The script will probe your system to find the distribution, desktop environment, CPU, and memory
usage. If I think of anything else useful I may end up adding that as well (disk usage?). Cuurently
the script is targeted at the popular distros and their updating schemes. So, the supported distros
are: Arch, Debian, RHEL. This also includes distros based on those, as long as they are using the
default package manger their parent distro uses (pacman, yum, and dpkg/apt-get). 
* The sys-info isn't all too appealing right now. I'm hoping I change that.

* Must be using Arch, Debian, or RHEL (and their children distros) for this to work. See above.

* Must have python 3 installed, with the subprocess module (should be there by default).

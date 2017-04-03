# Pyupdate
**Pyupdate** is a small project to ease the troubles of keeping a system up to date.
The script attempts to make it easy to update a good portion of Linux distributions.
Python 3 is the future of Python, and it is installed on most bleeding edge style
distros and so it was the choice for this project. It will record the last update
if the update was applied through Pyupdate, and display it before updating again.
It works on the principle of inheritance, that most distributions are based on another.
Look at Debian for example, there are hundreds of different distros based off Debian alone.
Thus, this script will search in itself for the detected distribution and find what it is
based off of and use that package manager to update the system. The supported distros are as
follows:

#### Supported Derived distributions
| Distro          | Derived From     |
| --------------- | ---------------- |
| Ubuntu          | Debian           |
| Xubuntu         | Debian           |
| GalliumOs       | Debian           |
| Elementary      | Debian           |
| Antergos        | Arch             |
| Manjaro         | Arch             |
| Fedora          | RHEL             |
| CentOs          | RHEL             |
| Scientific      | RHEL             |

#### Supported Independent/Parent distributions
| Distro          | Supported        |
| --------------- | ---------------- |
| RHEL            | Yes              |
| Arch            | Yes              |
| Debian          | Yes              |
| Solus           | Yes              |

#### Options
* The script can be run with the optional argument of -s to skip the update
** The result is only printing the system information.

#### Requirements
* Must have Python 3 installed
* Must have one of the above distributions of Linux.

#### Future Goals
* Provide better information post-update
* Option to show available updates

# pw
*pw* is a simple script used to control a
[Digital Logger Ethernet Power Switch](http://www.digital-loggers.com/lpc.html "website").
It uses a configuration file stored in the user's home directory and allows the user
to control multiple power switches.

**NOTE:** This tool was mostly tested on firmware version : *1.7.2*

## Requirements
This script uses :
 * [requests](http://docs.python-requests.org/en/latest/user/quickstart/)
 * beautifulSoup
 * [docopt](https://github.com/docopt/docopt)

## Configuration files
`pw` uses a configuration file to access the power switch's web interface.
If a symlink of `pw` is made, the tool will use another conf file.

Example:
```
$ ln -s ~/dev/pw/python/pw.py ~/bin/pw
$ ln -s ~/bin/pw ~/bin/p1
# You can now use the tool on two different switches.
# One will use ~/.pw.conf and the other ~/.p1.conf.
```
`pw` first looks for it's configuration in your home directory (user specific) then in `/etc/pw` (system wide). If no file is found, you'll be asked to fill the config and it'll be stored in your home directory.

## Usage
```
Usage:
        pw set OUTLET STATE
        pw get [OUTLET]
        pw tgl OUTLET
        pw ccl OUTLET [--delay=SEC]
        pw rename OUTLET NAME
        pw reset OUTLET
        pw -h | --help | --version

The most commonly used commands are:
        set                     Set the outlet to a given state
        get                     Get the name and state of the outlets
        tgl                     Toggle the state of an outlet
        ccl                     Power cycle a given outlet
        reset                   Rename an outlet to a default value
        rename                  Rename a given outlet.
                                If outlet is 'ctrl' this will rename the PowerSwitch

Arguments:
        OUTLET                  outlet number (or name) to be controlled
        STATE                   can be on, off, ccl

Options:
        --version               show version and exit
        -h, --help              show this help message and exit
        -v, --verbose           print status messages
        --delay                 set number of seconds when power cycling
```

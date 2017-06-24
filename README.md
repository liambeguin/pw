# pw
*pw* is a simple bash script used to control a
[Digital Logger Ethernet Power Switch](http://www.digital-loggers.com/lpc.html "website").
It uses a configuration file stored in the user's home directory and allows the user
to control multiple power switches.

# Usage

```
USAGE
        pw [-v] [OPTION]

DESCRIPTION
        -v | verbose .......................... Enable verbose output
        -h | help [-v] ........................ Display this message
        [names | state | -s ] ................. Get the name and state of all outlets
        [1-8 | all | name]  [on | off | ccl] .. Activate, Deactivate or powercycle outlets
        [-d | delay] sec ...................... Set time to wait when power cycling
        [-w | whois | state | names]  [0-8] ... Get the name of a specific outlet
        rename  [1-8]  name ................... Rename an outlet

CONFIGURATION FILE
        By default, pw will use ~/.pw.conf as a configuration file.
        The configuration file contains three variable :
           * USER
           * PASSWORD
           * POWER_SWITCH_IP

        Creating a synlink of "pw" will allow you to use the same tool but with
        a different configuration thus allowing you to control another power swith.

```

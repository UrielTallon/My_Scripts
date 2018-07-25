## Scripts

A small collection of scripts for various tasks...

### Python Scripts:

#### CheckHex

This is a simple script that can be used to check an Intel HEX file. The following tests are performed:

* Missing end of file
* Checksum verification
* Data length verification

The script relies on argparse library and can be called from the command line with the following arguments:

* gui/g: the .hex file is selected through a standard Qt visual interface; only .hex files can be selected.
* file_name/f: the path to the .hex file is entered manually.
* verbose/v: the default working method for the script is to stop at the first error; in verbose mode, the script 
won't stop until all the lines have been checked; the total number of errors is counted and displayed.

#### PCBThermal

A simple script to determine the temperature increase on MOSFET with respect to the flowing current through them.
This is a very basic script that only take the internal resistance of the MOSFET and the die thermal resistance
in account but it is still useful for 'quick and dirty' analysis.

This is mostly aimed at power switches for Lithium battery packs.

At the time, parameters must be changed inside the source directly.

#### CreateApp

A script to create the basic project development tree for a Python `Flask` application. It is mostly inspired by *Miguel Grinberg*
[Flask Mega Tutorial.](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
Check it out! 

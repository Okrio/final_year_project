Last updated 2014-05-13.

General Information
====================
This folder contains 32-bit and 64-bit Linux libraries as well as a sample
application.  They were all compiled on Debian Squeeze, which uses eglibc
2.11.3-4.  As such, they are expected to work on most distributions shipped
since 2011.  They are also tested against the latest LTS version of Ubuntu
and the latest version of Fedora to ensure operation on those distros.

If you encounter errors, please contact InterSense technical support and 
include the output of 'uname -a' as well as the name of your distribution.
The x86 directory contains a 32-bit version of the library, and the x86_64
contains the 64-bit x86 version.  The sample directory contains source code
as well as pre-compiled 32 and 64-bit binaries (ismain32 and ismain64).


Installation
====================
Copy the file corresponding to your architecture to the /lib directory (or any 
other directory named in /etc/ld.so.conf or specified in your LD_LIBRARY_PATH
variable).  The library needs to be named libisense.so or it will not be
found, and it may be necessary to run the ldconfig program after copying the
library into the library directory.

If any problems are encountered, please contact InterSense technical support
at techsupport@intersense.com or call +1 781-541-7624.


Example Application
====================
The ismain application is provided as an example application that can access
an InterSense device and output position/orientation data for it.  To compile
it, simply run the command "make" from the Sample directory, and then type 
"./ismain" to run it.

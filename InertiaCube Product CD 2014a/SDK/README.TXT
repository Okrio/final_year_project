InterSense DLL/Shared Library version 4.2401
   File last updated: 2014-05-22
======================================================================
The DLL included in this distribution provides an easy to
use API that can detect, configure and retrieve data from all models of 
InterSense trackers. A sample application is provided to illustrate 
the use of most functions. See isense.h for explanations and function 
prototypes. A significant portion of the API and the sample application 
is not relevant when used with the InterTrax (which is no longer
supported by InterSense). 


DOCUMENTATION
======================================================================
API documentation is provided in the dll_api.pdf and dll_api.doc files
(identical) as well as via comments in the isense.h file in the same 
directory as this README.TXT file.  Additionally, the API is documented
in the user manuals of most products, near the end of the documentation.


OS SUPPORT
======================================================================
This release is tested/supported for use with the InertiaCube4 and
other InertiaCube products:

    Windows XP
	Windows 7
	Linux (glibc >= 2.11.3)
    Mac OS X (>= 10.4)

Other platforms (such as Windows Vista) are expected to work without
any issues, but have not been fully tested, and support for these
platforms may be limited.  Similarly, IS-900 devices are
expected to work with this DLL, but are not officially supported
configurations.


SERIAL PORT MAPPING (isports.ini)
======================================================================
Device names for serial ports vary on different versions of UNIX, and
on Windows COM ports greater than COM32 are not automatically detected.
The library uses default names for each of the supported operating 
systems, however, is not always sufficient, particularly when 
USB to Serial converters are used. To solve this, a configuration 
file called isports.ini can be used to specify port number to device
string mapping. 

The included sample file (in the "Configuration Samples" folder)
was produced for Linux and contains lines for an InterSense USB 
converter (/dev/ttyUSB0) and a standard serial port (/dev/ttyS0, 
which corresponds to COM1 in Windows). Please check your operating
system and hardware docuemtnation for specific device names. 

PortX = device:baudRate

X is replaced with the logical port number starting at 1. "device"
can be a path to the device driver, like /dev/ttyS0. Baud rate
parameter is optional. All baud rates are tested to detect the
tracker. By default, once tracker is detected, the baud rate is 
changed to 115200 for best performance. If you are using a very 
long serial cable, you may want to use this feature to force
the lower baud rate. This feature is only available for Windows
version in this release.

Note: If isports.ini file is found, all required ports must be 
defined in it. Only devices listed in the file will be searched,
and the file is limited to Port1 through Port32 (32 total ports).


BLUETOOTH SUPPORT
======================================================================
To use Bluetooth devices, such as the InertiaCube BT, requires the
library to increase latency/timeout values internally.  Because using
the timeout values would make detection time unacceptably long,
especially on PCs with many COM ports, Bluetooth devices must be
detected using a special tag in the isports.ini file, ":bluetooth".
For example, to connect to an InertiaCube BT detected as COM14:

Port1 = COM14:bluetooth

Linux Specific Issues
---------------------
Recent Linux distributions may cause you to encounter two potential
issues that may prevent proper operation (in these cases, a dump from
hcidump, e.g. "hcidump -w bluetooth-debug.pcap" along with the isense.log
file will be very helpful for InterSense to assist you).

Issue #1 - Modem Manager may try to send AT commands to your RFCOMM ports

      This can be resolved either by removing the package (if modems are
      not being used at all), such as with "sudo apt-get remove modemmanager"
      on Ubuntu, or via a udev rule.  This rule should specify the vendor
      and product ID, and set the ID_MM_DEVICE_IGNORE environment variable
      so that Modem Manager will ignore the device, such as:

      ATTRS{idVendor}=="0a12", ATTRS{idProduct}=="0001", ENV{ID_MM_DEVICE_IGNORE}="1"

      (The IDs can be obtained with lsusb or similar methods).  These IDs are
      for the Cirago BTA-6130 class 1 Bluetooth adapter.

Issue #2 - D-bus is now used by Bluez (the standard Bluetooth stack on Linux),
           and may require entering a pairing code (1234).
	       
      There are several GUI utilities to do this (gnome-bluetooth [GNOME],
	  bluedevil [KDE], blueman [GTK2]), as well as a command line utility,
	  bluetooth-agent that is part of Bluez (but may not always be installed).
	  KDE may use bluedevil-wizard to pair (you may need to pair twice),
	  after using rfcomm to bind the device to a port.  To use
      it, first associate the sensor using rfcomm and then use
      bluetooth-agent, for example:

      --------------------------
      user@host$ hcitool scan 
      Scanning ...
            00:06:66:4A:5B:3E       BTC-1234567-A
            00:06:66:07:67:F0       BTC-2345678-A
      user@host$ sudo rfcomm -i hci0 bind rfcomm0 00:06:66:07:67:F0
      user@host$ sudo rfcomm -i hci0 bind rfcomm1 00:06:66:4A:5B:3E
      user@host$ sudo bluetooth-agent 1234 00:06:66:07:67:F0
      Pincode request for device /org/bluez/929/hci0/dev_00_06_66_07_67_F0
      Agent has been released
      user@host$ sudo bluetooth-agent 1234 00:06:66:4A:5B:3E
      Pincode request for device /org/bluez/929/hci0/dev_00_06_66_4A_5B_3E
      Agent has been released
      --------------------------

      After this, the devices may be added to isports.ini, e.g.

      Port1=/dev/rfcomm0:blueooth

      And the devices should be detected/operate as expected.


TCP SUPPORT
======================================================================
All versions support communication to InterSense IS-900 tracking
devices over TCP/IP. To use this feature you must define the connection
string in the isports.ini file in following form: 

PortX = IP:Port, for example:

Port1 = 192.168.1.44:5005

  To configure port 5005 via TCP for 192.168.1.44.  UDP ports may be specified
using only the port number, such as:

Port1 = 5001

  To configure UDP port 5001.  The port must be allowed through any client
side firewalls as well.


INSTALLATION
======================================================================
1. Windows XP/7 (supported) and Windows Vista (unsupported/untested, but expected to work)
   Login as Administrator
   Copy Windows/x86_32/isense.dll to %SYSTEMROOT% (C:\WINDOWS\SYSTEM32)  (32-bit systems)
   Copy Windows/x86_64/isense.dll to %SYSTEMROOT% (C:\WINDOWS\SYSTEM32)  (64-bit systems)
   Copy Windows/x86_32/isense.dll to C:\WINDOWS\SYSWOW64                 (32-bit DLL on 64-bit systems)

2. Linux (systems with glibc >= 2.11.3)
   Login as root
   Copy Linux/x86_32/libisense.so to /lib directory  (32 bit systems)
   Copy Linux/x86_64/libisense.so to /lib64 directory  (64 bit systems)
   Note: It is also possible to specify the path with the LD_LIBRARY_PATH environment variable

3. Mac OS X (>= 10.4)
   Login as root
   Copy MacOSX/Universal/libisense.dylib to /usr/lib directory
   Note: It is also possible to specify the path with the DYLD_LIBRARY_PATH environment variable


CONTACT INFORMATION
======================================================================

InterSense
700 Technology Park Drive
Suite 102
Billerica, MA 01821
United States

Tel. +1 781-541-6330
Fax. +1 781-541-6329

http://www.intersense.com

For technical support with the library or SDK, please contact
techsupport@intersense.com.  In most cases of an apparent issue with the
InterSense library, it will be helpful to provide technical support with a
small example application that can be compiled using an included project in
Visual Studio, or a makefile for Linux/Mac OS X; this can significantly 
reduce the time it takes to reproduce and resolve your issue.

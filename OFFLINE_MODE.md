# CivilCvCAD Offline Mode

Offline-only behavior is mandatory in this distribution.

The application does not register web, forum, donation, bug-reporting, remote
debugging, online-library, or online-documentation commands. Addon Manager and
the Web workbench are excluded at configuration time. Built-in Qt download
paths, external URL launchers, and embedded-Python internet sockets are blocked.
Help content must be installed locally.

Local files, local directories, and operating-system local IPC remain available.
For defense against arbitrary native plugins or external child programs, apply
an operating-system outbound firewall rule to the CivilCvCAD executable.

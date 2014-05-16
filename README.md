LiteElementsHack
================

A Django web application to display information about the battery and WiFi
networks of an Ubuntu (12.04+) machine (_Tested on Ubuntu 13.10_).

![Screenshot](https://raw.githubusercontent.com/mmardini/LiteElementsHack/master/Screenshot.png)

Run project
-----------
#### And a note about sudo
`iwlist` needs to use `sudo` to scan WiFi networks properly. While the project
can detect if `sudo` can be used without asking the user for a password and
will only use it if it is avaiable, using `iwlist` without `sudo` will not give
proper results.

You can either add `iwlist` to `/etc/sudoers` to whitelist it, and run Django
development server with no root privileges:

    python manage.py runserver

Or without whitelisting it, you can run Django development server process with
root privileges so any subprocess it runs will inherit its privileges:

    sudo python manage.py runserver

Of course this is only suitable for a development environment.

After that, access the pages on:

    127.0.0.1:8000/wifi
    127.0.0.1:8000/battery

Run tests
---------
The project contains tests for most of its functionality, to run the tests:

    python manage.py test

Backend code
------------
The project follows the typical Django projects/apps structure, all the
backend functionality is coded in `BatteryWifiMonitor` app files, the most
important files are:
* `BatteryWifiMonitor\utils.py`: This is where the app talks with Ubuntu; it
runs the subprocesses that scan WiFi networks and get battery status. This code
also detect if `sudo` can be used.
* `BatteryWifiMonitor\api.py`: This file converts the various information
to a JSON format, to be used by jQuery/AJAX calls.
* `BatteryWifiMonitor\tests.py`: Test cases for the application functions.
* `BatteryWifiMonitor\views.py`: The application has two views to render the
initial HTML pages with the requested information, and another two views that 
return JSON responses to be used by the subsequent AJAX calls to update the
pages.

Frontend code
-------------
* HTML Templates: The templates (`BatteryWifiMonitor\templates\`) use Django's
template inheritance to avoid repetition of HTML and to load only the needed
Javascript code for each task. The battery meter uses a pure CSS solution
rather than an HTML5 `meter` element for backward browser compatibility.
* Javascript: `BatteryWifiMonitor\static\js\wifi.js` and
`BatteryWifiMonitor\static\js\battery.js` conatin the jQuery code that gets
the initial JSON and the subsequent updates JSON and display the data in WiFi
and battery pages, respectively.
* CSS: `base.html` uses one CSS file,
`BatteryWifiMonitor\static\css\style.css`.

Dependencies
------------
* Python 2.7
* Django 1.6
* jQuery 1.11 (included)

There's no need to run under `virtualenv` since the only package used is Django
which is most likely already installed on your machine.

Linux commands
--------------
The project uses the following Linux commands:
* General: `sudo`, `true`.
* WiFi scanning: `iwlist`.
* Battery status: `acpi` (this is the most robust and portable tool to get
battery status).
* Tests: `seq`, `echo`.

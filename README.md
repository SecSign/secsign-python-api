# SecSign ID Python Interface


**Overview**

SecSign ID Api is a two-factor authentication for python web applications.

This Python API allows a secure login using a private key on a smart phone running SecSign ID by SecSign Technologies Inc.


**Usage**

* Include the API `SecSignIDApi.py` in your project.
* Request an authentication session
* Show access pass to user and save session parameters 
* Get session state 
* React to the state and have the user logged in


Check out the included example `example.py` to see how it works or 
have a look at the how to use tutorial for PHP <https://www.secsign.com/en/php-integrate-tutorial.html>. The process is exactly the same in python.

Or visit <https://www.secsign.com> for more informations.

**Files**

* `SecSignIDApi.py` - the file contains two classes SecSignIDApi and AuthSession. The class SecSignIDApi will care about the communication with the ID server
* `example.py` - a small test script

**Requirements**

The communication with the ID server is done using pycurl. So the package `pycurl` must be installed on the system.


===============

SecSign Technologies Inc. official site: <https://www.secsign.com>
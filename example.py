#!/usr/bin/python


# $Id: example.py,v 1.6 2014/11/26 17:25:15 titus Exp $

#
# SecSign ID Api example in python.
#
# (c) 2014 SecSign Technologies Inc.
#

import time
from SecSignIDApi import SecSignIDApi
from SecSignIDApi import AuthSession
from SecSignIDApi import InputError
#
#
# Example how to retrieve an authentication session, ask its status and withdraw the authentication session.
#
#

#
# Create an instance of SecSignIDApi.
#
print("create new instance of SecSignIDApi.")
secSignIDApi = SecSignIDApi()

#
# The servicename and address is mandatory. It has to be send to the server.
# The value of servicename will be shown on the display of the smartphone. The user then can decide whether he accepts the authentication session shown on his mobile phone.
#
servicename = "Your Website Login";
serviceaddress = "http://www.yoursite.com/";
secsignid = "username";

#
# Get a auth session for the sepcified SecSign ID
#
# If secsignid is null or empty an exception is thrown.
# If servicename is null or empty an exception is thrown.
#

try:
    authSession = secSignIDApi.requestAuthSession(secsignid, servicename, serviceaddress)
    print("got authSession '" + str(authSession) + "'")

except InputError as e:
    print("could not get an authentication session for SecSign ID '" + secsignid + "' : " + e.strerror)
    exit(1)


#
# Get the auth session status
#
# If authSession is null or not an instance of AuthSession an exception is thrown
#
authSessionState = authSession.NOSTATE

try:
    authSessionState = secSignIDApi.getAuthSessionState(authSession)
    print("got auth session state: " + authSessionState);
except InputError as e:
    print("could not get status for authentication session '" + str(authSession.authSessionID) + "' : " + e.strerror)
    exit(1)


# If the script shall wait till the user has accepted the auth session or denied it,  it has to ask the server frequently
secondsToWaitUntilNextCheck = 10
noError = True

while noError and (int(authSessionState) == AuthSession.PENDING or int(authSessionState) == AuthSession.FETCHED):
    try:
        authSessionState = secSignIDApi.getAuthSessionState(authSession);
        print("auth session state: " + authSessionState)

        if int(authSessionState) == AuthSession.PENDING or int(authSessionState) == AuthSession.FETCHED:
          time.sleep(secondsToWaitUntilNextCheck)
    except InputError as e:
        print("could not get auth session status for auth session '" + authSession.authSessionID + "' : " + e.strerror)
        noError = False;




if int(authSessionState) == authSession.AUTHENTICATED:
    print("user has accepted the auth session '" + authSession.authSessionID + "'")

    # release auth session to free resources serverside
    secSignIDApi.releaseAuthSession(authSession)
    print("auth session '" + authSession.authSessionID + "' was released.")


elif int(authSessionState) == authSession.DENIED:
    print("user has denied the auth session '" + authSession.authSessionID + "'.")
    authSessionState = secSignIDApi.cancelAuthSession(authSession); # after the auth session is successfully canceled it is not possible to inquire the status again
    if authSessionState == authSession.CANCELED:
        print("authentication session successfully cancelled...")


else:
    print("auth session '" + authSession.authSessionID + "' has state " + authSessionState + ".")
    authSessionState = secSignIDApi.cancelAuthSession(authSession); # after the auth session is successfully canceled it is not possible to inquire the status again
    if int(authSessionState) == authSession.CANCELED:
        print("authentication session successfully cancelled...")



### end

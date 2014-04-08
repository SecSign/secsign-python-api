
#
# SecSign ID Api in python.
#
# (c) copyright SecSign Technologies Inc.
#

import string
import urllib
import os
import curl, pycurl
import cStringIO

SCRIPT_REVISION = '$Revision: 1.3 $'
    
class AuthSession:

        #
        # No State: Used when the session state is undefined. 
        #
        NOSTATE = 0;
        
        #
        # Pending: The session is still pending for authentication.
        #
        PENDING = 1;
        
        #
        # Expired: The authentication timeout has been exceeded.
        #
        EXPIRED = 2;
        
        #
        # Authenticated: The user was successfully authenticated.
        #
        AUTHENTICATED = 3;
        
        #
        # Denied: The user denied this session.
        #
        DENIED = 4;
		
        #
        # Suspended: The server suspended this session, because another authentication request was received while this session was still pending.
        #
        SUSPENDED = 5;
        
        #
        # Canceled: The service has canceled this session.
        #
        CANCELED = 6;
        
        #
        # Fetched: The device has already fetched the session, but the session hasn't been authenticated or denied yet.
        #
        FETCHED = 7;
    
        #
        # Invalid: This session has become invalid.
        #
        INVALID = 8;
        
        
        # 
        # the secsign id the authentication session has been craeted for
        #
        secSignID = None;
        
        #
        # authentication session id
        #
        authSessionID = None;
        
        #
        # the name of the requesting service. this will be shown at the smartphone
        #
        requestingServiceName = None;
        
        #
        # the address, a valid url, of the requesting service. this will be shown at the smartphone
        #
        requestingServiceAddress = None;
        
        #
        # the request ID is similar to a server side session ID. 
        # it is generated after a authentication session has been created. all other request like dispose, withdraw or to get the auth session state
        # will be rejected if a request id is not specified.
        #
        requestID = None;
        
        #
        # icon data of the so called access pass. the image data needs to be displayed otherwise the user does not know which access apss he needs to choose in order to accept the authentication session.
        #
        authSessionIconData = None;
        
        #
        # constructor
        #
        def __init__(self):
            pass
            
        #
        # method to get string representation of this authentication session object
        #
        def __toString(self):
            return "{0} ({1}, {2}, icondata={3})".format(authSessionID, secSignID, requestingServiceAddress, authSessionIconData);
        
        #
        # gets the auth session as pythons dictionary
        #
        def getAuthSessionAsArray(self):
            return {'secsignid':secSignID,'authsessionid':authSessionID,'servicename':requestingServiceName,'serviceaddress':requestingServiceAddress,'authsessionicondata':authSessionIconData,'requestid':requestID};
        
        
        #
        # Creates/Fills the auth session object using the given dictionary.
        #
        def createAuthSessionFromArray(self, authSessionDict, ignoreOptionalParameter):
            if authSessionDict is None:
                raise InputError("Parameter array is None.");
          

            # authSessionDict mandatory parameter
            if dict['secsignid'] is None:
                raise InputError("Parameter array does not contain a value 'secsignid'.")
            
            if authSessionDict['authsessionid'] is None:
                raise InputError("Parameter array does not contain a value 'authsessionid'.")
            
            if authSessionDict['servicename'] is None and not ignoreOptionalParameter:
                raise InputError("Parameter array does not contain a value 'servicename'.")
            
            if authSessionDict['serviceaddress'] is None and not ignoreOptionalParameter:
                raise InputError("Parameter array does not contain a value 'serviceaddress'.")
            

            if authSessionDict['requestid'] is None:
                raise InputError("Parameter array does not contain a value 'requestid'.")
            
            
            secSignID = authSessionDict['secsignid'];
            authSessionID = authSessionDict['authsessionid'];
            authSessionIconData = authSessionDict['authsessionicondata'];
            requestingServiceName = authSessionDict['servicename'];
            requestingServiceAddress = authSessionDict['serviceaddress'];
            requestID = authSessionDict['requestid'];


 
#
# Class to connect to a secsign id server. The class will check secsign id server certificate and request for authentication session generation for a given
# user id which is called secsign id. Each authentication session generation needs a new instance of this class.
#
# @version $Id: SecSignIDApi.py,v 1.3 2014/04/08 15:28:15 titus Exp $
# @author SecCommerce Informationssysteme GmbH, Hamburg
#
class SecSignIDApi:
    

    # once created the api can be used to create a single request for a certain specified userid
    __secSignIDServer = "https://httpapi.secsign.com"
    __secSignIDServerPort = 443;
    __secSignIDServer_fallback = "https://httpapi2.secsign.com";
    __secSignIDServerPort_fallback = 443;

    # numeric script version.
    __scriptVersion = 0;
    __referer = None;
    __pluginName = None;
    __lastResponse = None;

    #
    # constructor
    #
    def __init__(self):
        # script version from cvs revision string
        firstSpace = SCRIPT_REVISION.find(" ")
        lastSpace = SCRIPT_REVISION.find(" ", firstSpace+1)
        
        __scriptVersion = SCRIPT_REVISION[firstSpace:-lastSpace]
        __referer = self.__class__.__name___ + "_Python"

    #
    #
    #
    def __f(self):
        try:
            1/0
        finally:
            return 42

    #
    # logs a message if logger instance is not NULL
    #
    def __log(self, message):
       print(message)

    
    #
    # Sets an optional plugin name
    #
    def setPluginName(self, pn):
        self.__pluginName = pn

    #
    # Gets last response
    #
    def getResponse(self):
        return self.__lastResponse;
        

    #
    # Send query to secsign id server to create an authentication session for a certain secsign id. This method returns the authentication session itself.
    #
    def requestAuthSession(self, secsignid, servicename, serviceadress):
    
        __log("Call of function 'requestAuthSession'.")
                
        if servicename is None:
            __log("Parameter servicename must not be None.")
            raise InputError("Parameter servicename must not be None.")
        
                
        if serviceadress is None:
            __log("Parameter serviceadress must not be None.")
            raise InputError("Parameter serviceadress must not be None.")

                
        if secsignid is None:
            __log("Parameter secsignid must not be None.")
            raise InputError("Parameter secsignid must not be None.")
            
                
        requestParameter = dict({'request':'ReqRequestAuthSession', 'secsignid' : secsignid, 'servicename': servicename, 'serviceaddress' : serviceadress});
                
        if __pluginName is not None:
            requestParameter['pluginname'] = __pluginName
        
        response      = __send(requestParameter, None);
        
        authSession = AuthSession();
        authSession.createAuthSessionFromArray(response)
        return authSession

    #
    # Gets the authentication session state for a certain secsign id whether the authentication session is still pending or it was accepted or denied.
    #
    def getAuthSessionState(self, authSession):

        __log("Call of function 'getAuthSessionState'.");
    
        if authSession is None or type(authSession) is not AuthSession:
            message = "Parameter authSession is not an instance of AuthSession. type(authSession)={0}".format(type(authSession))
            __log(message)
            raise InputError(message)

    
        requestParameter = dict({'request':'ReqGetAuthSessionState'})
        response = __send(requestParameter, AuthSession)
        return response['authsessionstate']

    #
    # Cancel the given auth session.
    #
    def cancelAuthSession(self, authSession):
        
        __log("Call of function 'cancelAuthSession'.");
                
        if authSession is None or type(authSession) is not AuthSession:
            message = "Parameter authSession is not an instance of AuthSession. type(authSession)={0}".format(type(authSession))
            __log(message)
            raise InputError(message)
                
        requestParameter = dict({'request':'ReqCancelAuthSession'})
        response = __send(requestParameter, AuthSession)
        return response['authsessionstate']

    #
    # Releases an authentication session if it was accepted and not used any longer
    #
    def releaseAuthSession(self, authSession):
    
        __log("Call of function 'releaseAuthSession'.");
    
        if authSession is None or type(authSession) is not AuthSession:
            message = "Parameter authSession is not an instance of AuthSession. type(authSession)={0}".format(type(authSession))
            __log(message)
            raise InputError(message)
    

        requestParameter = dict({'request':'ReqReleaseAuthSession'})
        response = __send(requestParameter, AuthSession)
        return response['authsessionstate']

    #
    # sends given parameters to secsign id server and wait given amount
    # of seconds till the connection is timed out
    #
    def __send(self, parameter, authSession):

        requestQuery = urllib.urlencode(__buildParameterArray(parameter, authSession))
        timeout_in_seconds = 15
            
        # create cURL resource
        ch = __createCurlHandle(secSignIDServer, secSignIDServerPort, requestQuery, timeout_in_seconds)
        __log("curl init: " + ch)
    
        # output contains the output string
        __log("curl sent params: " + requestQuery)
        
        output = cStringIO.StringIO()
        ch.setopt(ch.WRITEFUNCTION, output.write)
        ch.perform() # pycurl.exec(ch)
            
        if ch.getinfo(pycurl.HTTP_CODE) is not 200:
            __log("curl error: " + ch.errstr())

    
        # close curl resource to free up system resources
        __log("curl.close(): " + ch)
        ch.close()
    
        # check if output is NULL. in that case the secsign id might not have been reached.
        if output.getvalue() is None:
    
            __log("curl: output is None. Server {0}:{1} has not been reached.".format(secSignIDServer, secSignIDServerPort))
        
            if secSignIDServer_fallback is not None:
            
                __log("curl: get new handle from fallback server.");
                ch = __createCurlHandle(secSignIDServer_fallback, secSignIDServerPort_fallback, requestQuery, timeout_in_seconds)
                
                output = cStringIO.StringIO()
                ch.setopt(ch.WRITEFUNCTION, output.write)
                
                __log("curl init: " + ch + " connecting to " + ch.getInfo(pycurl.EFFECTIVE_URL))
            
                # output contains the output string
                ch.perform();
                if output.getvalue() is None:
            
                    __log("output is None. Fallback server {0}:{1} has not been reached.".format(secSignIDServer_fallback, secSignIDServerPort_fallback))
                    __log("curl error: " + ch.errstr())
                    raise ConnectionError("curl.perform() error: can't connect to Server - " + ch.errstr())
            
                # close curl resource to free up system resources
                __log("curl.close(): " + ch)
                ch.close()
            else :
                __log("curl: no fallback server has been specified.")

        __lastResponse = output.getvalue()
        __log("curl.perform() response: {}".format(__lastResponse))

            
        output.close()
        return  __checkResponse(__lastResponse);


    #
    # build an array with all parameters which has to be send to server
    #
    def __buildParameterArray(self, parameter, authSession):

        # mandatoryParams = array('apimethod' => referer, 'scriptversion' => scriptVersion);
        mandatoryParams = {'apimethod':referer};
                        
        if authSession is not None:
            # add auth session data to mandatory parameter array
            authSessionData = {'secsignid' : authSession.secSignID, 'authsessionid' : authSession.authSessionID, 'requestid' : authSession.requestID}
            mandatoryParams.update(authSessionData)

        result = dict(parameter).copy()
        result.update(mandatoryParams)
        return result

            
    #
    # checks the secsign id server response string
    #
    def __checkResponse(self, response):
        if response is None:
            message = "Could not connect to host '{0}:{1}'".format(secSignIDServer, secSignIDServerPort)
            __log(message)
            raise ConnectionError(message)
    
        # server send parameter strings like:
        # var1=value1&var2=value2&var3=value3&...
        responseDict = {};
        

        valuePairs = string.split(response, '&');
        for pair in valuePairs:
            key_value = string.split(pair, '=', 2);
            responseDict[key_value[0]] = key_value[1];

    
        # check if server send a parameter named 'error'
        if responseDict['error'] is not None:
            __log("SecSign ID server sent error. code=" + responseDict['error'] + " message=" + responseDict['errormsg'])
            raise InputError(responseDict['errormsg'], responseDict['error'])

        return responseDict

    #
    # Gets a cURL resource handle.
    #
    # http://www.angryobjects.com/2011/10/15/http-with-python-pycurl-by-example/
    # http://pycurl.sourceforge.net/
    #
    def __createCurlHandle(self, server, port, parameter, timeout_in_seconds):

        c = pycurl.Curl()
        c.setopt(c.URL, server)
        c.setopt(c.PORT, port)
        c.setopt(c.CONNECTTIMEOUT, timeout_in_seconds)
        c.setopt(c.FRESH_CONNECT, 1)
        
        # return the transfer as a string
        c.setopt(c.RETURNTRANSFER, 1)
        
        # value 0 will strip header information in response 
        c.setopt(c.HEADER, 0)
        
        # make sure the common name of the certificate's subject matches the server's host name
        c.setopt(c.SSL_VERIFYHOST, 2)
        # validate the certificate chain of the server
        c.setopt(c.SSL_VERIFYPEER, true)
        # the CA certificates
        c.setopt(c.SSL_CAINFO, os.path.dirname(os.path.abspath(__file__)) + '/curl-ca-bundle.crt')

        # add all parameter and change request mode to POST
        c.setopt(c.POST, 2)
        c.setopt(c.POSTFIELDS, parameter)
            
        return c
    
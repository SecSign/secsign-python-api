# $Id: SecSignIDApi.py,v 1.6 2014/11/26 17:25:15 titus Exp $

#
# SecSign ID Api in python.
#
# (c) 2014 SecSign Technologies Inc.
#

import string
import urllib
import os
import curl, pycurl
import cStringIO

SCRIPT_REVISION = '$Revision: 1.6 $'
    
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
            if authSessionDict['secsignid'] is None:
                raise InputError("Parameter array does not contain a value 'secsignid'.")
            
            if authSessionDict['authsessionid'] is None:
                raise InputError("Parameter array does not contain a value 'authsessionid'.")
            
            if authSessionDict['servicename'] is None and not ignoreOptionalParameter:
                raise InputError("Parameter array does not contain a value 'servicename'.")
            
            if authSessionDict['serviceaddress'] is None and not ignoreOptionalParameter:
                raise InputError("Parameter array does not contain a value 'serviceaddress'.")
            
            if authSessionDict['requestid'] is None:
                raise InputError("Parameter array does not contain a value 'requestid'.")
            
            
            self.secSignID = authSessionDict['secsignid'];
            self.authSessionID = authSessionDict['authsessionid'];
            self.authSessionIconData = authSessionDict['authsessionicondata'];
            self.requestingServiceName = authSessionDict['servicename'];
            self.requestingServiceAddress = authSessionDict['serviceaddress'];
            self.requestID = authSessionDict['requestid'];



 
#
# Class to connect to a secsign id server. The class will check secsign id server certificate and request for authentication session generation for a given
# user id which is called secsign id. Each authentication session generation needs a new instance of this class.
#
# @version $Id: SecSignIDApi.py,v 1.6 2014/11/26 17:25:15 titus Exp $
# @author SecSign Technologies Inc.
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
        
        self.__scriptVersion = SCRIPT_REVISION[firstSpace:-lastSpace]
        #self.__referer = self.__class__.__name___ + "_Python"
        self.__referer = "SecSignIDApi_Python"

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
        __pluginName = pn

    #
    # Gets last response
    #
    def getResponse(self):
        return self.__lastResponse;
        

    #
    # Send query to secsign id server to create an authentication session for a certain secsign id. This method returns the authentication session itself.
    #
    def requestAuthSession(self, secsignid, servicename, serviceadress):
    
        self.__log("Call of function 'requestAuthSession'.")
                
        if servicename is None:
            self.__log("Parameter servicename must not be None.")
            raise InputError("Parameter servicename must not be None.")
        
                
        if serviceadress is None:
            self.__log("Parameter serviceadress must not be None.")
            raise InputError("Parameter serviceadress must not be None.")

                
        if secsignid is None:
            self.__log("Parameter secsignid must not be None.")
            raise InputError("Parameter secsignid must not be None.")
            
                
        requestParameter = dict({'request':'ReqRequestAuthSession', 'secsignid' : secsignid, 'servicename': servicename, 'serviceaddress' : serviceadress});
                
        if self.__pluginName is not None:
            requestParameter['pluginname'] = self.__pluginName
        
        response      = self.__send(requestParameter, None);
        
        authSession = AuthSession();
        authSession.createAuthSessionFromArray(response, True)
        return authSession

    #
    # Gets the authentication session state for a certain secsign id whether the authentication session is still pending or it was accepted or denied.
    #
    def getAuthSessionState(self, authSession):

        self.__log("Call of function 'getAuthSessionState'.");
    
        if authSession is None:
            message = "Parameter authSession is not an instance of AuthSession. type(authSession)={0}".format(type(authSession))
            self.__log(message)
            raise InputError(message)

    
        requestParameter = dict({'request':'ReqGetAuthSessionState'})
        response = self.__send(requestParameter, authSession)
        return response['authsessionstate']

    #
    # Cancel the given auth session.
    #
    def cancelAuthSession(self, authSession):
        
        self.__log("Call of function 'cancelAuthSession'.");
                
        if authSession is None:
            message = "Parameter authSession is not an instance of AuthSession. type(authSession)={0}".format(type(authSession))
            self.__log(message)
            raise InputError(message)
                
        requestParameter = dict({'request':'ReqCancelAuthSession'})
        response = self.__send(requestParameter, authSession)
        return response['authsessionstate']

    #
    # Releases an authentication session if it was accepted and not used any longer
    #
    def releaseAuthSession(self, authSession):
    
        self.__log("Call of function 'releaseAuthSession'.");
    
        if authSession is None:
            message = "Parameter authSession is not an instance of AuthSession. type(authSession)={0}".format(type(authSession))
            self.__log(message)
            raise InputError(message)
    

        requestParameter = dict({'request':'ReqReleaseAuthSession'})
        response = self.__send(requestParameter, authSession)
        return response['authsessionstate']

    #
    # sends given parameters to secsign id server and wait given amount
    # of seconds till the connection is timed out
    #
    def __send(self, parameter, authSession):

        requestQuery = urllib.urlencode(self.__buildParameterArray(parameter, authSession))
        timeout_in_seconds = 15
            
        # create cURL resource
        ch = self.__createCurlHandle(self.__secSignIDServer, self.__secSignIDServerPort, requestQuery, timeout_in_seconds)
        self.__log("curl init: " + str(ch))
    
        # output contains the output string
        self.__log("curl sent params: " + requestQuery)
        
        output = cStringIO.StringIO()
        ch.setopt(ch.WRITEFUNCTION, output.write)
        ch.perform() # pycurl.exec(ch)
            
        if ch.getinfo(pycurl.HTTP_CODE) is not 200:
            self.__log("curl error: " + ch.errstr())

    
        # close curl resource to free up system resources
        self.__log("curl.close(): " + str(ch))
        ch.close()
    
        # check if output is NULL. in that case the secsign id might not have been reached.
        if output.getvalue() is None:
    
            self.__log("curl: output is None. Server {0}:{1} has not been reached.".format(secSignIDServer, secSignIDServerPort))
        
            if secSignIDServer_fallback is not None:
            
                self.__log("curl: get new handle from fallback server.");
                ch = self.__createCurlHandle(secSignIDServer_fallback, secSignIDServerPort_fallback, requestQuery, timeout_in_seconds)
                
                output = cStringIO.StringIO()
                ch.setopt(ch.WRITEFUNCTION, output.write)
                
                self.__log("curl init: " + ch + " connecting to " + ch.getInfo(pycurl.EFFECTIVE_URL))
            
                # output contains the output string
                ch.perform();
                if output.getvalue() is None:
            
                    self.__log("output is None. Fallback server {0}:{1} has not been reached.".format(secSignIDServer_fallback, secSignIDServerPort_fallback))
                    self.__log("curl error: " + ch.errstr())
                    raise ConnectionError("curl.perform() error: can't connect to Server - " + ch.errstr())
            
                # close curl resource to free up system resources
                self.__log("curl.close(): " + ch)
                ch.close()
            else :
                self.__log("curl: no fallback server has been specified.")

        __lastResponse = output.getvalue()
        self.__log("curl.perform() response: {}".format(__lastResponse))

            
        output.close()
        return  self.__checkResponse(__lastResponse);


    #
    # build an array with all parameters which has to be send to server
    #
    def __buildParameterArray(self, parameter, authSession):

        # mandatoryParams = array('apimethod' => referer, 'scriptversion' => scriptVersion);
        mandatoryParams = {'apimethod':self.__referer}
		
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
            self.__log(message)
            raise InputError(message)
    
        # server send parameter strings like:
        # var1=value1&var2=value2&var3=value3&...
        responseDict = {};
        

        valuePairs = string.split(response, '&');
        for pair in valuePairs:
            key_value = string.split(pair, '=', 2);
            if len(key_value) > 1:
	            responseDict[key_value[0]] = key_value[1];

    
        # check if server send a parameter named 'error'
        #if responseDict['error'] is not None:
        if 'error' in responseDict.keys():
            self.__log("SecSign ID server sent error. code=" + responseDict['error'] + " message=" + responseDict['errormsg'])
            raise InputError(responseDict['errormsg'])

        return responseDict

    #
    # Gets a cURL resource handle.
    #
    # http://www.angryobjects.com/2011/10/15/http-with-python-pycurl-by-example/
    # http://pycurl.sourceforge.net/
    # https://github.com/pycurl/pycurl
    #
    def __createCurlHandle(self, server, port, parameter, timeout_in_seconds):

        c = pycurl.Curl()
        c.setopt(c.URL, server)
        c.setopt(c.PORT, port)
        c.setopt(c.CONNECTTIMEOUT, timeout_in_seconds)
        c.setopt(c.FRESH_CONNECT, 1)
        
        # return the transfer as a string
        #c.setopt(c.RETURNTRANSFER, 1)
        
        # value 0 will strip header information in response 
        c.setopt(c.HEADER, 0)
        
        # make sure the common name of the certificate's subject matches the server's host name
        c.setopt(c.SSL_VERIFYHOST, 2)
        # validate the certificate chain of the server
        c.setopt(c.SSL_VERIFYPEER, True)
        # the CA certificates
        #c.setopt(pycurl.SSL_CAINFO, os.path.dirname(os.path.abspath(__file__)) + '/curl-ca-bundle.crt')

        # add all parameter and change request mode to POST
        c.setopt(c.POST, 2)
        c.setopt(c.POSTFIELDS, parameter)
            
        return c
  
  
# definitions of our error classes
class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class InputError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expr -- input expression in which the error occurred
        msg  -- explanation of the error
    """

    def __init__(self, msg):
        self.strerror = msg

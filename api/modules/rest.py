from flask import jsonify
from flask import make_response

from modules.logging_config import logger


########## REST functions ##########


# Function: Build a 200-OK response
def buildResponse200(isWelcome, config, properties):
    '''
    Function to build a simple OK response.
    Input parameters:
        isWelcome: boolean -> Indicates if it refers to a Welcome message or not.
        config: ConfigParser -> The data in the configuration file.
        properties: ConfigParser -> The data in the properties file.
    '''

    # Build the message
    message = properties['IDESIGNRES-MESSAGES']['idesignres.message.success']
    if isWelcome:
        message = properties['IDESIGNRES-MESSAGES']['idesignres.message.welcome'].replace('{1}',config['IDESIGNRES']['idesignres.version'])

    # Build the header
    headerTypeHeader = properties['IDESIGNRES-REST']['idesignres.rest.content.type.header']
    headerTypeValue = properties['IDESIGNRES-REST']['idesignres.rest.content.type.value']

    # Build the body
    body = {
        'code': properties['IDESIGNRES-REST']['idesignres.rest.ok.code'],
        'message': message,
        'value': True,
        'error': None
    }
    
    # Build and return the response
    response = make_response(jsonify(body), int(properties['IDESIGNRES-REST']['idesignres.rest.ok.code']))
    response.headers[headerTypeHeader] = headerTypeValue
    return response


# Function: Build a 200-OK response with value
def buildResponse200Value(value, properties):
    '''
    Function to build an OK response, including a customized value.
    Input parameters:
        value: text -> The customized text value.
        properties: ConfigParser -> The data in the properties file.
    '''
    
    # Build the header
    headerTypeHeader = properties['IDESIGNRES-REST']['idesignres.rest.content.type.header']
    headerTypeValue = properties['IDESIGNRES-REST']['idesignres.rest.content.type.value']

    # Build the body
    body = {
        'code': properties['IDESIGNRES-REST']['idesignres.rest.ok.code'],
        'message': properties['IDESIGNRES-MESSAGES']['idesignres.message.success'],
        'value': value,
        'error': None
    }
    
    # Build and return the response
    response = make_response(jsonify(body), int(properties['IDESIGNRES-REST']['idesignres.rest.ok.code']))
    response.headers[headerTypeHeader] = headerTypeValue
    return response


# Function: Build a 200-OK response with time series
def buildResponse200TimeSeries(value, properties):
    '''
    Function to build an OK response, including a time series.
    Input parameters:
        value: text -> The time series.
        properties: ConfigParser -> The data in the properties file.
    '''

    # Build the header
    headerTypeHeader = properties['IDESIGNRES-REST']['idesignres.rest.content.type.header']
    headerTypeValue = properties['IDESIGNRES-REST']['idesignres.rest.content.type.value']
    
    # Build and return the response
    response = make_response(jsonify(value), int(properties['IDESIGNRES-REST']['idesignres.rest.ok.code']))
    response.headers[headerTypeHeader] = headerTypeValue
    return response


# Function: Build a 400-Bad request response
def buildResponse400(errorMessage, properties):
    '''
    Function to build a Bad Request response.
    Input parameters:
        errorMessage: text -> The customized error message.
        properties: ConfigParser -> The data in the properties file.
    '''

    # Build the header
    headerTypeHeader = properties['IDESIGNRES-REST']['idesignres.rest.content.type.header']
    headerTypeValue = properties['IDESIGNRES-REST']['idesignres.rest.content.type.value']

    # Build the body
    body = {
        'code': properties['IDESIGNRES-REST']['idesignres.rest.bad.request.code'],
        'value': False,
        'error': errorMessage
    }
    
    # Build and return the response
    response = make_response(jsonify(body), int(properties['IDESIGNRES-REST']['idesignres.rest.bad.request.code']))
    response.headers[headerTypeHeader] = headerTypeValue
    return response


#Function: Build a 401-Unauthorized request response
def buildResponse401(properties):
    '''
    Function to build an Unauthorized Request response.
    Input parameters:
        properties: ConfigParser -> The data in the properties file.
    '''

    # Build the header
    headerTypeHeader = properties['IDESIGNRES-REST']['idesignres.rest.content.type.header']
    headerTypeValue = properties['IDESIGNRES-REST']['idesignres.rest.content.type.value']

    # Build the body
    body = {
        'code': properties['IDESIGNRES-REST']['idesignres.rest.unauthorized.code'],
        'value': False,
        'error': properties['IDESIGNRES-REST']['idesignres.rest.unauthorized.message']
    }
    
    # Build and return the response
    response = make_response(jsonify(body), int(properties['IDESIGNRES-REST']['idesignres.rest.unauthorized.code']))
    response.headers[headerTypeHeader] = headerTypeValue
    return response


import logging
import paramiko

import modules.io as io

from modules.logging_config import logger


########## SFTP functions ##########


# Function: Build the connection parameters
def buildConnectionParameters(config):
    '''
    Function to build the SFTP connection parameters.
    Input parameters:
        config: ConfigParser -> The data in the configuration file.
    '''

    obj = { 'hostname': config['IDESIGNRES-SFTP']['idesignres.sftp.host'],
            'port': int(config['IDESIGNRES-SFTP']['idesignres.sftp.port']),
            'username': config['IDESIGNRES-SFTP']['idesignres.sftp.username'],
            'password': config['IDESIGNRES-SFTP']['idesignres.sftp.password'],
            'timeout': int(config['IDESIGNRES-SFTP']['idesignres.sftp.timeout'])
          }
    return obj


# Function: Checks a user directory
def checkUserDirectory(username, config):
    '''
    Function to check the user directory.
    Input parameters:
        username: text -> The name of the user to check his/her directory.
        config: ConfigParser -> The data in the configuration file.
    '''

    try:
        # Build the path
        userDirectoryPath = io.retrieveOutputBasePath(False, config).replace('{1}', username)
        logger.info('  SFTP Server/> Checking if the user is authorized to execute the process...')
        logger.info('')
            
        # Retrieve the connection parameters
        conn = buildConnectionParameters(config)
            
        # Open the SSH client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname = conn['hostname'],
            port = conn['port'],
            username = conn['username'],
            password = conn['password'],
            timeout = conn['timeout'])
        
        # Open the SFTP channel
        sftp = client.open_sftp()

        # Check the directory
        sftp.stat(userDirectoryPath)
        logger.info('')
        logger.info('  SFTP Server/> Authorized!')
        return True
    except FileNotFoundError as fnfError:
        logger.info('')
        logger.info('  SFTP Server/> Not authorized!')
        return False
    except IOError as ioError:
        logger.info('')
        logger.info('  SFTP Server/> Not authorized!')
        return False
    except Exception as error:
        raise


# Function: Retrieve the layer files stored in the SFTP Server
def retrieveLayerFiles(layerList, config):
    '''
    Function to retrieve the layer files.
    Input parameters:
        layerList: list -> The list of layers to be retrieved.
        config: ConfigParser -> The data in the configuration file.
    '''

    try:
        if layerList and len(layerList) > 0:
            # Retrieve the base path
            basePath = io.retrieveBasePath(config)
            
            # Retrieve the connection parameters
            conn = buildConnectionParameters(config)
            
            # Open the SSH client
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname = conn['hostname'],
                port = conn['port'],
                username = conn['username'],
                password = conn['password'],
                timeout = conn['timeout'])
        
            # Open the SFTP channel
            sftp = client.open_sftp()

            # Retrieve the files
            logger.info('')
            for layer in layerList:
                if io.fileExists(basePath + layer['path']):
                    logger.info('  SFTP Server/> The file "' + layer['name'] + '" is already locally stored.')
                else:
                    logger.info('  SFTP Server/> Downloading the file "' + layer['name'] + '"...')
                    sftp.get(layer['path'], basePath + layer['path'])
            logger.info('')
        
            # Close the SSH client and return
            client.close()
            return True
        return False
    except Exception as error:
        raise


# Function: Retrieve the data files stored in the SFTP Server
def retrieveDataFiles(fileList, config):
    '''
    Function to retrieve the data files.
    Input parameters:
        fileList: list -> The list of files to be retrieved.
        config: ConfigParser -> The data in the configuration file.
    '''

    try:
        if fileList and len(fileList) > 0:
            # Retrieve the base path
            basePath = io.retrieveBasePath(config)
            
            # Retrieve the connection parameters
            conn = buildConnectionParameters(config)
            
            # Open the SSH client
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname = conn['hostname'],
                port = conn['port'],
                username = conn['username'],
                password = conn['password'],
                timeout = conn['timeout'])
        
            # Open the SFTP channel
            sftp = client.open_sftp()

            # Retrieve the files
            logger.info('')
            for fil in fileList:
                if io.fileExists(basePath + fil['path']):
                    logger.info('  SFTP Server/> The file "' + fil['name'] + '" is already locally stored.')
                else:
                    logger.info('  SFTP Server/> Downloading the file "' + fil['name'] + '"...')
                    sftp.get(fil['path'], basePath + fil['path'])
            logger.info('')
        
            # Close the SSH client and return
            client.close()
            return True
        return False
    except Exception as error:
        raise


# Function: Retrieve the dbase files stored in the SFTP Server
def retrieveDbaseFiles(config):
    '''
    Function to retrieve all the dbase files.
    Input parameters:
        config: ConfigParser -> The data in the configuration file.
    '''

    try:
        # Retrieve the base path
        basePath = io.retrieveBasePath(config)
            
        # Retrieve the connection parameters
        conn = buildConnectionParameters(config)
            
        # Open the SSH client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname = conn['hostname'],
            port = conn['port'],
            username = conn['username'],
            password = conn['password'],
            timeout = conn['timeout'])
        
        # Open the SFTP channel
        sftp = client.open_sftp()
        
        # List all files in the remote folder
        logger.info('')
        fileList = sftp.listdir(config['IDESIGNRES-SFTP']['idesignres.sftp.path.dbase'])
        fileList.sort()
        result = []
        for fil in fileList:
            if io.fileExists(basePath + config['IDESIGNRES-SFTP']['idesignres.sftp.path.dbase'] + fil):
                logger.info('  SFTP Server/> The file "' + fil + '" is already locally stored.')
            else:
                logger.info('  SFTP Server/> Downloading the file "' + (config['IDESIGNRES-SFTP']['idesignres.sftp.path.dbase'] + fil) + '"...')
                sftp.get(config['IDESIGNRES-SFTP']['idesignres.sftp.path.dbase'] + fil,
                    basePath + config['IDESIGNRES-SFTP']['idesignres.sftp.path.dbase'] + fil)
            result.append({'name': fil, 'path': basePath + config['IDESIGNRES-SFTP']['idesignres.sftp.path.dbase'] + fil})
        
        # Close the SSH client and return
        client.close()
        return result
    except Exception as error:
        raise


# Function: Retrieve a single file stored in the SFTP Server
def retrieveSingleFile(filePath, fileName, config):
    '''
    Function to retrieve a single file.
    Input parameters:
        filePath: text -> The path of the file to be retrieved.
        fileName: text -> The name of the file to be retrieved.
        config: ConfigParser -> The data in the configuration file.
    '''

    try:
        # Retrieve the connection parameters
        conn = buildConnectionParameters(config)
            
        # Open the SSH client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname = conn['hostname'],
            port = conn['port'],
            username = conn['username'],
            password = conn['password'],
            timeout = conn['timeout'])
        
        # Open the SFTP channel
        sftp = client.open_sftp()
        
        # Download the file
        logger.info('')
        logger.info('  SFTP Server/> Downloading the file "' + (filePath + fileName) + '"...')
        sftp.get(filePath + fileName, io.retrieveFilesTmpPath(config) + '/' + fileName)
        
        # Close the SSH client and return
        client.close()
        return True
    except Exception as error:
        return False


# Function: Downloads a resource stored in the SFTP Server
def downloadResource(resource, config):
    '''
    Function to download a resource.
    Input parameters:
        resource: text -> The resource to be retrieved.
        config: ConfigParser -> The data in the configuration file.
    '''

    try:
        if resource:
            # Retrieve the connection parameters
            conn = buildConnectionParameters(config)
            
            # Open the SSH client
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname = conn['hostname'],
                port = conn['port'],
                username = conn['username'],
                password = conn['password'],
                timeout = conn['timeout'])
        
            # Open the SFTP channel
            sftp = client.open_sftp()

            # Retrieve the files
            logger.info('')
            logger.info('  SFTP Server/> Downloading the file "' + resource['name'] + '"...')
            local_path = io.retrieveFilesTmpPath(config) + '/' + resource['name']
            sftp.get(resource['sftp'], local_path)
            logger.info('')
        
            # Close the SSH client and return
            client.close()
            return local_path
        return None
    except Exception as error:
        raise


# Function: Checks if a file exists in the SFTP Server
def fileExists(remoteFilePath, config):
    '''
    Function to check if a file exists in the SFTP Server.
    Input parameters:
        remoteFilePath: text -> The remote file path to be checked.
        config: ConfigParser -> The data in the configuration file.
    '''

    try:
        if remoteFilePath:
            # Retrieve the connection parameters
            conn = buildConnectionParameters(config)
            
            # Open the SSH client
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname = conn['hostname'],
                port = conn['port'],
                username = conn['username'],
                password = conn['password'],
                timeout = conn['timeout'])
        
            # Open the SFTP channel
            sftp = client.open_sftp()

            # Check if the file exists
            sftp.stat(remoteFilePath)
        
            # Close the SSH client and return
            client.close()
            return True
        return False
    except FileNotFoundError as fnfError:
        logger.error(str(fnfError))
        return False
    except IOError as ioError:
        logger.error(str(ioError))
        return False
    except Exception as error:
        logger.error(str(error))
        raise
 
 
 # Function: Upload an output file to the SFTP Server
def uploadOutputFile(localFilePath, remoteFilePath, config):
    '''
    Function to upload an output file to the SFTP Server.
    Input parameters:
        localFilePath: text -> The local file path to be uploaded.
        remoteFilePath: text -> The remote file path to store the local file.
        config: ConfigParser -> The data in the configuration file.
    '''

    try:
        if localFilePath and remoteFilePath:
            # Retrieve the connection parameters
            conn = buildConnectionParameters(config)
            
            # Open the SSH client
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname = conn['hostname'],
                port = conn['port'],
                username = conn['username'],
                password = conn['password'],
                timeout = conn['timeout'])
        
            # Open the SFTP channel
            sftp = client.open_sftp()

            # Upload the file
            logger.info('')
            if io.fileExists(localFilePath):
                logger.info('  SFTP Server/> Uploading the output file...')
                sftp.put(localFilePath, remoteFilePath)
            logger.info('')
        
            # Close the SSH client and return
            client.close()
            return True
        return False
    except Exception as error:
        logger.error(str(error))
        raise



import json
import os
import requests
import sys

import pandas as pd
import numpy as np

from datetime import datetime


URL_AUTH = 'https://idesignres.digital.tecnalia.dev/api/qgis/authenticate'
URL_PROCESS  = 'https://idesignres.digital.tecnalia.dev/api/qgis/building-energy-simulation-process'
BUILDING_USES = ['Apartment Block',
                 'Single family- Terraced houses',
                 'Hotels and Restaurants',
                 'Health',
                 'Education',
                 'Offices',
                 'Trade',
                 'Other non-residential buildings',
                 'Sport']


# Function: Execute the Building Energy Simulation process
def executeBuildingEnergySimulationProcess(authPayload: dict, processPayload: dict, startTime: str, endTime: str, buildingUse: str):
    ''' Function to execute the Building Energy Simulation process. '''

    try:
        # Authenticate
        print('Process/>  Authenticating...')
        response = requests.post(URL_AUTH, json = authPayload)
        if response.status_code != 200:
            raise Exception('Process/>  Authentication error!')
        print('Process/>  Authentication [OK]')

        # Obtain the security token from the response
        token = response.json()['value']
        if token:
            headers = {'Authorization': 'Bearer ' + token,
                        'Content-Type': 'application/json',
                        'X-Julia': 'True'
            }

            # Execute the process
            print('Process/>  Executing the Building Energy Simulation process (please wait)...')
            response = requests.post(URL_PROCESS, json = processPayload, headers = headers)
            if response.status_code != 200:
                raise Exception()
            print('Process/>  [Process OK]')

            # Return the result (filtered)
            data = pd.DataFrame(response.json()[buildingUse])
            data['Datetime'] = pd.to_datetime(data['Datetime'])
            start = pd.to_datetime(datetime.strptime(startTime, '%Y-%m-%dT%H:%M:%S'))
            end = pd.to_datetime(datetime.strptime(endTime, '%Y-%m-%dT%H:%M:%S'))
            dataFiltered = data[(data['Datetime'] >= start) & (data['Datetime'] <= end)]
            solidsCoal = dataFiltered['Solids|Coal'].to_numpy()
            liquidsGas = dataFiltered['Liquids|Gas'].to_numpy()
            liquidsOil = dataFiltered['Liquids|Oil'].to_numpy()
            gasesGas = dataFiltered['Gases|Gas'].to_numpy()
            solidsBiomass = dataFiltered['Solids|Biomass'].to_numpy()
            electricity = dataFiltered['Electricity'].to_numpy()
            heat = dataFiltered['Heat'].to_numpy()
            liquidsBiomass = dataFiltered['Liquids|Biomass'].to_numpy()
            gasesBiomass = dataFiltered['Gases|Biomass'].to_numpy()
            hydrogen = dataFiltered['Hydrogen'].to_numpy()
            heatSolar = dataFiltered['Heat|Solar'].to_numpy()
            variableCost = dataFiltered['Variable cost [€/KWh]'].to_numpy()
            emissions = dataFiltered['Emissions [KgCO2/KWh]'].to_numpy()
            return solidsCoal, liquidsGas, liquidsOil,gasesGas, solidsBiomass,\
                electricity, heat, liquidsBiomass, gasesBiomass, hydrogen,\
                heatSolar, variableCost, emissions
    except Exception as error:
        print('Process/>  An error occurred executing the Building Energy Simulation process!')
        print(error)
    

# Function: Main
def main():
    ''' Main function '''

    try:
        # Read input parameters:
        # [0]: client file name
        # [1]: auth file path
        # [2]: input data file path
        # [3]: start datetime (yyyy-MM-ddTHH:mm:ss)
        # [4]: end datetime (yyyy-MM-ddTHH:mm:ss)
        # [5]: building use
        if len(sys.argv) < 6:
            raise Exception('The number of input parameters is incorrect! (6)')
        if not os.path.exists(sys.argv[1].strip()):
            raise Exception('The authorization file does not exist!')
        if not os.path.exists(sys.argv[2].strip()):
            raise Exception('The input data file does not exist!')
        
        # Load the authorization payload
        with open(sys.argv[1].strip(), 'r') as authPayloadFile:
            authPayload = json.load(authPayloadFile)
        if not authPayload or authPayload is None:
            raise Exception('Could not load the authorization payload!')

        # Load the process payload
        with open(sys.argv[2].strip(), 'r') as payloadFile:
            processPayload = json.load(payloadFile)
        if not processPayload or processPayload is None:
            raise Exception('Could not load the process payload!')
        
        # Validate the datetime objects
        try:
            startTime = datetime.strptime(sys.argv[3], "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            raise Exception('The third input parameter (start datetime) has an incorrect format (yyyy-MM-ddTHH:mm:ss)')
        try:
            endTime = datetime.strptime(sys.argv[4], "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            raise Exception('The fourth input parameter (end datetime) has an incorrect format (yyyy-MM-ddTHH:mm:ss)')
        if (endTime <= startTime):
            raise Exception('The end time cannot be less than the start time!')
        
        # Validate the building use
        if not sys.argv[5] or sys.argv[5].strip() not in BUILDING_USES:
            raise Exception('The building use must be one of the following: "Apartment Block", "Single family- Terraced houses", "Hotels and Restaurants", "Health", "Education", "Offices", "Trade", "Other non-residential buildings", "Sport"')

        # Execute the processs
        executeBuildingEnergySimulationProcess(authPayload, processPayload, sys.argv[3], sys.argv[4], sys.argv[5])
    except Exception as exception:
        print(f'Process/>  {exception}') 
    
    

if __name__ == "__main__":
    main()

# iDesignRES Models: Examples

&nbsp;

## Authentication
All the functions that the REST API exposes are JWT secured, so before executing a process, invoke the authentication function to obtain the security token.

Any REST client can be used (Postman, Bruno, Insomnia, cUrl...) with the following data:

```
URL: https://idesignres.digital.tecnalia.dev/api/qgis/authenticate
Verb: POST
Body:
{
  "username": "xxxxxx",
  "password": "xxxxxx"
}
```

Consult the component to obtain valid credentials.

The function returns the following response (if login is successful):
```
{
  "code": "200",
  "error": null,
  "message": "Success!",
  "value": "The security token"
}
```

The "value" field contains the security token required to invoke any process-related function.


## iDesignRES Solar Energy Model example
To execute this process, it is only necessary to call the REST API function that the application exposes. Any REST client can be used:
```
URL: https://idesignres.digital.tecnalia.dev/api/qgis/solar-process
Verb: POST
Body:
{
  "nutsid": "XXXX"
}
Authentication:
Use the JWT token as a "Bearer" token.
```


## iDesignRES Building Stock Energy Model example
To execute the process, follow the procedure described for the previous process with the following data:
```
URL: https://idesignres.digital.tecnalia.dev/api/qgis/building-process
Verb: POST
Body:
{
  "nutsid": "XXXX"
}
Authentication:
Use the JWT token as a "Bearer" token.
```


## iDesignRES Building Stock Energy Simulation process example
To execute the process, follow the procedure described for the previous process with the following data:
```
URL: https://idesignres.digital.tecnalia.dev/api/qgis/building-energy-simulation-process
Verb: POST
Body:
{
	"nutsid": "XXXX",
	"year": yyyy,
	"scenario": {
		"increase_residential_built_area": 0,
		"increase_service_built_area": 0,
		"solar_thermal_surface_m2": 0,
		"passive_measures": [
			{
				"building_use": "Apartment Block",
				"ref_level": "Low",
				"percentages_by_periods": [0, 0, 0, 0, 0, 0, 0]
			},
			{
				"building_use": "Single family- Terraced houses",
				"ref_level": "Low",
				"percentages_by_periods": [0, 0, 0, 0, 0, 0, 0]
			},
			{
				"building_use": "Offices",
				"ref_level": "Low",
				"percentages_by_periods": [0, 0, 0, 0, 0, 0, 0]
			},
			{
				"building_use": "Education",
				"ref_level": "Low",
				"percentages_by_periods": [0, 0, 0, 0, 0, 0, 0]
			},
			{
				"building_use": "Health",
				"ref_level": "Low",
				"percentages_by_periods": [0, 0, 0, 0, 0, 0, 0]
			},
			{
				"building_use": "Trade",
				"ref_level": "Low",
				"percentages_by_periods": [0, 0, 0, 0, 0, 0, 0]
			},
			{
				"building_use": "Hotels and Restaurants",
				"ref_level": "Low",
				"percentages_by_periods": [0, 0, 0, 0, 0, 0, 0]
			},
			{
				"building_use": "Other non-residential buildings",
				"ref_level": "Low",
				"percentages_by_periods": [0, 0, 0, 0, 0, 0, 0]
			},
			{
				"building_use": "Sport",
				"ref_level": "Low",
				"percentages_by_periods": [0, 0, 0, 0, 0, 0, 0]
			}
		]
	}
}
Authentication:
Use the JWT token as a "Bearer" token.

Clarifications:
1) The fields "building_use" can only have the values:
   - Apartment Block
   - Single family- Terraced houses
   - Offices
   - Education
   - Health
   - Trade
   - Hotels and Restaurants
   - Other non-residential buildings
   - Sport
2) The fields "ref_level" can only have the values:
   - "Low"
   - "Medium"
   - "High"
3) The values in the arrays "percentages_by_periods" correspond to the periods:
   - Position 0: "Pre-1945"
   - Position 1: "1945 - 1969"
   - Position 2: "1970 - 1979"
   - Position 3: "1980 - 1989"
   - Position 4: "1990 - 1999"
   - Position 5: "2000 - 2010"
   - Position 6: "Post-2010"
```


## iDesignRES PV Power Plants Model example
To execute the process, follow the procedure described for the previous process with the following data:
```
URL: https://idesignres.digital.tecnalia.dev/api/qgis/pv-power-plants-process
Verb: POST
Body:
{
  "to_be_defined"
}
Authentication:
Use the JWT token as a "Bearer" token.
```
 




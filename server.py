# importing the requests library
import requests
import time
import pickle;



token="lIBPUqiLkEt3R0kDt0cMn3p5X5suse_k"
pumpPin="v0";
soilPin="v1"
temperaturePin="v2"
humidityPin="v3";


weather_api="http://api.weatherbit.io/v2.0/forecast/agweather?lat=23.2756&lon=77.4560&key=c0cebec5f6594632acdfc4b8347014f9";
loaded_model=pickle.load(open("finalized_model.sav", 'rb'));

def required_soilMoisture(temperature,humidity,avg_pres,evapotranspiration):
	return loaded_model.predict([[temperature,humidity,avg_pres,evapotranspiration]])[0][0]+50;


def isThePumpNeedsToBeOn(curSoilMoisture,requiredSoilMoisture):
	if(curSoilMoisture/10>requiredSoilMoisture):
		return False
	else:
		return True
	

while True:
	URL = "https://blynk.cloud/external/api/get?token="+token+"&"+pumpPin+"&"+soilPin+"&"+temperaturePin+"&"+humidityPin;
	URLupdate="https://blynk.cloud/external/api/update?token="+token+"&"
	# sending get request and saving the response as response object
	r = requests.get(url = URL)
	u=requests.get(url=weather_api);
	# extracting data in json format
	data = r.json()
	data2=u.json();
	evapotranspiration=data2['data'][0]['evapotranspiration'];
	avg_pres=data2['data'][0]['pres_avg'];
	print(avg_pres);
	requests.get(url=URLupdate+"V4="+str(avg_pres));
	requests.get(url=URLupdate+"V5="+str(evapotranspiration));
	print(data);
	print(required_soilMoisture(data['v2'], data['v3'], avg_pres, evapotranspiration))
	time.sleep(10);




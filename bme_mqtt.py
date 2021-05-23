import bme280
import schedule
import time
import paho.mqtt.client as mqtt
import json
import sys
import requests
from influxdb import InfluxDBClient
from datetime import datetime

client = None
influx_client = None

def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	client.subscribe("/IoTmanager")
	print("subscribed")

def on_message(client, userdata, msg):
	if msg.payload.decode('UTF-8') == "HELLO":
		try:		
			job()
		except OSError as err:
			data ={
                		"descr": "temperature",
                		"widget": "anydata",
                		"topic": "/IoTmanager/demo/outdoor",
                		"after": "",
                		"icon": "thermometer",
                		"status": str(err)
        		}
			client.publish("/IoTmanager/home/config", json.dumps(data))
	elif msg.payload.decode('UTF-8') == "EPD":
		temperature = ""
		try:
                	temperature,pressure,humidity = bme280.readBME280All()
		except OSError as err:
			temperature = "error"
		print("EPD: " + str(temperature))
		client.publish("/IoTmanager/epd/temperature", str(temperature))
		
def job():
	temperature,pressure,humidity = bme280.readBME280All()
	data ={
                "descr": "temperature",
                "widget": "anydata",
                "topic": "/IoTmanager/demo/outdoor",
                "after": " " + chr(176) + "C",
                "icon": "thermometer",
		"status": temperature
        }
	client.publish("/IoTmanager/home/config", json.dumps(data))
	data ={
                "descr": "humidity",
                "widget": "fillgauge",
                "topic": "/IoTmanager/demo/humidity",
                "status": "{:.2f}".format(humidity)
        }
	client.publish("/IoTmanager/home/config", json.dumps(data))
	data ={
                "descr": "ip",
                "widget": "anydata",
                "topic": "/IoTmanager/demo/ip",
                "icon": "globe",
                "status": requests.get('https://checkip.amazonaws.com').text.strip()
        }
	client.publish("/IoTmanager/home/config", json.dumps(data))
	result = influx_client.query('select temperature from bme280 order by desc limit 12;')
	data ={
                "descr": "sensor3",
                "widget": "chart",
                "topic": "/IoTmanager/demo/chart",
                "series": "Temperature " + chr(176) + "C",
                "dateFormat": "YYYY-MM-dd HH:mm",
                "status": []
        }
	result = list(result.get_points())
	result.reverse()
	now_start = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
	for item in result:
		date_value = datetime.strptime(item['time'], "%Y-%m-%dT%H:%M:%S.%fZ" )
		if date_value >= now_start:
			data["status"].append({"x": date_value.strftime("%Y-%m-%d %H:%M"), "y1": item['temperature']})
	client.publish("/IoTmanager/home/config", json.dumps(data))

def main():
	global client
	global influx_client
	influx_client = InfluxDBClient('localhost', 8086, 'root', 'root', 'pi')
	client = mqtt.Client()
	client.on_connect = on_connect
	client.on_message = on_message
	#client.username_pw_set("pi", "1")
	#client.connect("localhost", 1883, 60)
	client.username_pw_set("jkhziofl", "dz2D_Rs18CWS")
	client.connect("hairdresser.cloudmqtt.com", 15593, 60)
	client.loop_forever()
	#schedule.every().minute.do(foo)
	#while True:
		#schedule.run_pending()
		#time.sleep(1)

if __name__ == '__main__':
	main()


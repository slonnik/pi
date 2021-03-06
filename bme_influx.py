import bme280
import json
import schedule
import time
from influxdb import InfluxDBClient
from datetime import datetime

def job():
	
	temperature,pressure,humidity = bme280.readBME280All()
	points = [
	{
		"measurement": "bme280",
		"tags": {
			"region": "flat"
		},
		"time": datetime.now(),
		"fields": {
			"temperature": temperature,
			"pressure": pressure,
			"humidity": humidity
		}
	}]

	client = InfluxDBClient('localhost', 8086, 'root', 'root', 'pi')
	client.write_points(points)

def main():
	schedule.every().hour.do(job)
	while True:
		schedule.run_pending()
		time.sleep(1)

if __name__ == '__main__':
	main()


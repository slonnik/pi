from influxdb import InfluxDBClient

client = InfluxDBClient('localhost', 8086, 'root', 'root', 'example')
client.create_database('pi')

from influxdb import InfluxDBClient

client = InfluxDBClient('localhost', 8086, 'root', 'root', 'pi')

result = client.query('select temperature from bme280 order by desc limit 12;')
print("Result: {0}".format(result))

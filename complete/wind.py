#!/usr/bin/env python

import pymysql
import serial
import time

#CONNECT DATABASE
host = 'localhost'
user = 'user1'
password = 'Moscow2022'
db_name = 'weather'

connection = pymysql.connect(
	host=host,
        port=3306,
        user=user,
        password=password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )

#START SERIAL COMMUNICATION
device = serial.Serial('/dev/ttyUSB0', baudrate = 19200, parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE, bytesize = serial.EIGHTBITS, interCharTimeout = 1)

try:
	while 1: 
		#REQUEST WIND DATA
		device.write(bytes.fromhex('30 52 31 0D 0A'))
		#GET REPLY
		str = device.readline()
		#CONVERT TO STRING
		dec = str.decode("utf-8")
		#GET VALUES IN FLOAT
		dir_min = int(dec[dec.find('Dn') + 3 : dec.find('Dn') + 6])
		dir_avg = int(dec[dec.find('Dm') + 3 : dec.find('Dm') + 6])
		dir_max = int(dec[dec.find('Dx') + 3 : dec.find('Dx') + 6])
		speed_min = float(dec[dec.find('Sn') + 3 : dec.find('Sn') + 8])
		speed_avg = float(dec[dec.find('Sm') + 3 : dec.find('Sm') + 8])
		speed_max = float(dec[dec.find('Sx') + 3 : dec.find('Sx') + 8])
		#SEND DATA TO DATABASE
		with connection.cursor() as cursor:
			insert_query = "INSERT INTO WEATHER_MEASUREMENT (WIND_DIRECTION_MIN, WIND_DIRECTION_AVG,"\
			" WIND_DIRECTION_MAX, WIND_SPEED_MIN, WIND_SPEED_AVG, WIND_SPEED_MAX) VALUES ({},{},{},{},{},{});".format(dir_min, dir_avg, dir_max, speed_min, speed_avg, speed_max) 
			args = (dir_min, dir_avg, dir_max, speed_min, speed_avg, speed_max)
			cursor.execute(insert_query)
			connection.commit()
		with connection.cursor() as cursor:
			select_all_rows = "SELECT * FROM WEATHER_MEASUREMENT"
			cursor.execute(select_all_rows)
			rows = cursor.fetchall()
			for row in rows:
				print(row)
		print("#" * 20)
		with connection.cursor() as cursor:
			delete_query = "DELETE FROM WEATHER_MEASUREMENT"
			cursor.execute(delete_query)
			connection.commit()
		#PRINT VALUES IN COMMAND LINE
		print('Wind direction (min):', dir_min, '\n','Wind direction (avg):', dir_avg, '\n','Wind direction (max):', dir_max, '\n','Wind speed (min):', speed_min, '\n','Wind speed (avg):', speed_avg, '\n','Wind speed (max):', speed_max, '\n')
		#WAIT FOR 1 SECOND
		time.sleep(1)

except KeyboardInterrupt:
	#CLOSE SERIAL CONNECTION IN CASE OF INTERRUPT
	device.close()
	connection.close()

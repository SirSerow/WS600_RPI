host = 'localhost'
user = 'user1'
password = 'Moscow2022'
db_name = 'weather'

from datetime import datetime
import pymysql

now = datetime.now()
formatted_date = now.strftime('%Y-%m-%d %H:%M%S')

try:
	connection = pymysql.connect(
		host=host,
		port=3306,
		user=user,
		password=password,
		database=db_name,
		cursorclass=pymysql.cursors.DictCursor
	)
	print("successfully connected")
	print("#" * 20)

	try:
		with connection.cursor() as cursor:
			insert_query = "INSERT INTO WEATHER_MEASUREMENT (REMOTE_ID, WIND_DIRECTION_MIN, WIND_DIRECTION_AVG, WIND_DIRECTION_MAX, WIND_SPEED_MIN, WIND_SPEED_AVG, WIND_SPEED_MAX) VALUES (2,3,4,5,6,7,8);"
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

	finally:
		connection.close()

except Exception as ex:
	print("connection refused")
	print(ex)

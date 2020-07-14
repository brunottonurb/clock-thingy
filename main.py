#!/usr/bin/env python3
import RPi.GPIO as GPIO
import requests
from datetime import datetime

import epd2in7b
import images
import apis

def main():
	try:
		epd = epd2in7b.EPD()
		epd.init()

		# is this necessary?
		# epd.Clear()
		# time.sleep(1)

		data = apis.getOpenWeatherOneCall()

		if data != None:
			now = datetime.fromtimestamp(data['current']['dt'])
			sunrise = datetime.fromtimestamp(data['current']['sunrise'])
			sunset = datetime.fromtimestamp(data['current']['sunset'])

			temp = str(int(data['current']['temp'])) + '°c'
			weather = data['current']['weather'][0]['description']
			icon = data['current']['weather'][0]['icon']

			blackImage, redImage = images.getImages(now=now, sunrise=sunrise, sunset=sunset, temp=temp, weather=weather, icon=icon)
		else:
			blackImage, redImage = images.getImages(now=datetime.now(), sunrise=None, sunset=None, temp='...', weather='...', icon="unknown")

		epd.display(epd.getbuffer(blackImage), epd.getbuffer(redImage))

		epd.sleep()

	except IOError as e:
		print(e)

	except KeyboardInterrupt:
		print("ctrl + c:")
		epd2in7b.epdconfig.module_exit()
		exit()

if __name__ == '__main__':
	main()

from PIL import Image, ImageDraw
from datetime import datetime

import apis
import images

def main():
	data = apis.getOpenWeatherOneCall()

	print(data)

	if data != None:
		now = datetime.fromtimestamp(data['current']['dt'])
		sunrise = datetime.fromtimestamp(data['current']['sunrise'])
		sunset = datetime.fromtimestamp(data['current']['sunset'])

		temp = str(int(data['current']['temp'])) + '°c'
		weather = data['current']['weather'][0]['description']
		icon = data['current']['weather'][0]['icon']

		print(now)
		print(sunrise)
		print(sunset)
		print(temp)
		print(weather)
		print(icon)

		blackImage, redImage = images.getImages(now=now, sunrise=sunrise, sunset=sunset, temp=temp, weather=weather, icon=icon)
	else:
		blackImage, redImage = images.getImages(now=datetime.now(), sunrise=None, sunset=None, temp='...', weather='...', icon="unknown")

	testImage = Image.new("RGB", (176, 264), "#fff")

	for x in range(testImage.width):
		for y in range(testImage.height):
			if blackImage.getpixel((x, y)) != 255:
				testImage.putpixel((x,y), (0,0,0))
			# red overwrites black
			if redImage.getpixel((x, y)) != 255:
				testImage.putpixel((x,y), (255,0,0))

	testImage.show("test.png")


if __name__ == "__main__":
	main()

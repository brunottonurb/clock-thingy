from PIL import Image, ImageDraw
from datetime import datetime
import math

def getImages(now, sunrise, sunset, temp, weather, icon):
	# image sizes
	maxWidth = 176
	maxHeight = 264

	# position of the clock, move according to time to prevent burn in
	originX = maxWidth / 2
	originY = maxHeight / 2 + (now.hour - 12) * 2

	# image setup
	blackImage = Image.new("1", (maxWidth, maxHeight), 255)
	redImage = Image.new("1", (maxWidth, maxHeight), 255)
	drawblack = ImageDraw.Draw(blackImage)
	drawred = ImageDraw.Draw(redImage)

	totalMinutes = 24 * 60

	# convert time to [0, 365]l
	currentMinutes = now.hour * 60 + now.minute
	currentDegree = currentMinutes / totalMinutes * 360

	if (sunrise == None or sunset == None):
		sunrise = datetime(2020, 12, 24, 6, 0)
		sunset = datetime(2020, 12, 24, 18, 0)

	# assuming sunrise and sunset are the same today as they are tomorrow
	sunriseMinutes = sunrise.hour * 60 + sunrise.minute
	sunriseDegree = sunriseMinutes / totalMinutes * 360
	sunsetMinutes = sunset.hour * 60 + sunset.minute
	sunsetDegree = sunsetMinutes / totalMinutes * 360

	# adapt to current time (rotate)
	sunriseDegree = (sunriseDegree - currentDegree) % 360
	sunsetDegree = (sunsetDegree - currentDegree) % 360

	# size of the clock
	radius = 73

	# draw black and red arcs
	# arc sets 0 degrees to 3 o'clock...so -90
	drawblack.arc(
		xy=[
			(originX - radius - 2, originY - radius - 2),
			(originX + radius + 2, originY + radius + 2),
		],
		start=sunsetDegree - 90,
		end=sunriseDegree - 90,
		fill=0,
		width=4,
	)
	drawred.arc(
		xy=[
			(originX - radius - 2, originY - radius - 2),
			(originX + radius + 2, originY + radius + 2),
		],
		start=sunriseDegree - 90,
		end=sunsetDegree - 90,
		fill=0,
		width=4,
	)
	

	# draw dusk and dawn separators
	# need to calculate coordinates from radius, degree and center
	# x = cx + r * cos(a)
	# y = cy + r * sin(a)

	# drawblack.arc(xy=[(15, 15), (maxWidth - 15, maxWidth - 15)], start=sunsetDegree -90, end=sunsetDegree -89, fill=0, width=6)
	# drawblack.arc(xy=[(15, 15), (maxWidth - 15, maxWidth - 15)], start=sunriseDegree -90, end=sunriseDegree -89, fill=0, width=6)

	# draw pointer
	drawblack.polygon(
		xy=[
			(originX, originY - 90 + 25),
			(originX - 15, originY - 90 + 45),
			(originX, originY - 90 + 33),
			(originX + 15, originY - 90 + 45),
		],
		fill=0,
	)
	# drawred.polygon(
	# 	xy=[
	# 		(originX - 15, originY - 90 + 45),
	# 		(originX, originY - 90 + 33),
	# 		(originX + 15, originY - 90 + 45),
	# 		(originX, originY - 90 + 38),
	# 	],
	# 	fill=0,
	# )
	drawblack.polygon(
		xy=[
			(originX - 15, originY - 90 + 45),
			(originX, originY - 90 + 40),
			(originX + 15, originY - 90 + 45),
			(originX, originY - 90 + 38),
		],
		fill=0,
	)

	"""
	# draw center
	drawblack.arc(
		[(originX - 2, originY - 2), (originX + 2, originY + 2)],
		start=0,
		end=360,
		fill=0,
		width=4,
	)
	drawblack.arc(
		[(originX - 6, originY - 6), (originX + 6, originY + 6)],
		start=0,
		end=360,
		fill=0,
		width=1,
	)
	"""

	# draw noon, midnight
	noonDegree = ((12 * 60 / totalMinutes * 360) - currentDegree) % 360
	x = originX + radius * math.cos(math.radians(noonDegree - 90))
	y = originY + radius * math.sin(math.radians(noonDegree - 90))
	drawred.arc(xy=[(x - 5, y - 5), (x + 5, y + 5)], start=0, end=360, fill=0, width=6)
	midnightDegree = -currentDegree
	x = originX + radius * math.cos(math.radians(midnightDegree - 90))
	y = originY + radius * math.sin(math.radians(midnightDegree - 90))
	drawblack.arc(
		xy=[(x - 5, y - 5), (x + 5, y + 5)], start=0, end=360, fill=0, width=6
	)

	"""
	# show date
	month = now.strftime("%B")
	date = now.strftime("%d")
	day = now.strftime("%A")
	w, _h = drawblack.textsize(date)
	drawblack.text((originX - w // 2, originY + radius + 30), text=date, align="center")
	drawred.rectangle(
		[
			(originX - w // 2 - 30, originY + radius + 10),
			(originX - w // 2 + 40, originY + radius + 63),
		],
		outline=0,
		width=1,
	)
	w, _h = drawblack.textsize(day)
	drawblack.text((originX - w // 2, originY + radius + 15), text=day, align="center")
	w, _h = drawblack.textsize(month)
	drawblack.text(
		(originX - w // 2, originY + radius + 45), text=month, align="center"
	)
	"""

	# show weather
	iconImage = Image.open('weather_icons/' + icon + '.png')
	blackImage.paste(iconImage, box=(maxWidth // 2 - iconImage.width // 2, int(originY - iconImage.height // 2 - 15)))
	weatherText = temp + '\n' + weather
	textWidth, textHeight = drawblack.textsize(weatherText)
	drawblack.text((maxWidth // 2 - textWidth // 2, originY + textHeight - 20), text=weatherText, align="center")

	return blackImage, redImage

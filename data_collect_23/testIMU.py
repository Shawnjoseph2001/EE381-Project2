import time

import adafruit_bmp3xx
import board
import busio
import adafruit_bno08x
from adafruit_bno08x.i2c import BNO08X_I2C

i2c = busio.I2C(board.SCL, board.SDA, frequency=800000)
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)

bmp.sea_level_pressure = 1019
bmp.temperature_oversampling = 1
bmp.pressure_oversampling = 1
bmp.filter_coefficient = 128

print("Pressure: {:6.1f}".format(bmp.pressure))
print("Raw pressure: " + str(bmp.pressure))
print("Temperature: {:5.2f}".format(bmp.temperature))
print("Raw Temperature: " + str(bmp.temperature))

# cython: infer_types=True
# cython: language_level=3
from time import time
import adafruit_bmp3xx
import board
import busio
import csv
import os
import shutil
import adafruit_icm20x
import adafruit_bno08x
from adafruit_bno08x.i2c import BNO08X_I2C

# Number of minutes for program to run
numMinutes = 0.01

# I2C setup
i2c = busio.I2C(board.SCL, board.SDA)

# set up sensors
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)  # BMP388 or BMP390L connected over I2C
icm = adafruit_icm20x.ICM20649(i2c)  # ICM-20649 connected over I2C
bno = BNO08X_I2C(i2c)  # BNO080 or BNO085 connected over I2C

# BNO085 configuration
bno.enable_feature(adafruit_bno08x.BNO_REPORT_ACCELEROMETER)
bno.enable_feature(adafruit_bno08x.BNO_REPORT_GYROSCOPE)
bno.enable_feature(adafruit_bno08x.BNO_REPORT_MAGNETOMETER)
bno.enable_feature(adafruit_bno08x.BNO_REPORT_LINEAR_ACCELERATION)
bno.enable_feature(adafruit_bno08x.BNO_REPORT_ROTATION_VECTOR)
bno.enable_feature(adafruit_bno08x.BNO_REPORT_GEOMAGNETIC_ROTATION_VECTOR)
bno.enable_feature(adafruit_bno08x.BNO_REPORT_GAME_ROTATION_VECTOR)
bno.enable_feature(adafruit_bno08x.BNO_REPORT_STABILITY_CLASSIFIER)
bno.enable_feature(adafruit_bno08x.BNO_REPORT_RAW_ACCELEROMETER)
bno.enable_feature(adafruit_bno08x.BNO_REPORT_RAW_GYROSCOPE)
bno.enable_feature(adafruit_bno08x.BNO_REPORT_RAW_MAGNETOMETER)

# BMP390L configuration
bmp.sea_level_pressure = 1019
# higher oversampling = less data per second so oversampling is at the min value
bmp.temperature_oversampling = 1
bmp.pressure_oversampling = 1
bmp.filter_coefficient = 128

# ICM-20649 configuration

# Accelerometor configuration
icm.accelerometer_range = adafruit_icm20x.AccelRange.RANGE_30G
icm.accelerometer_data_rate_divisor = 0
icm.accel_dlpf_cutoff = adafruit_icm20x.AccelDLPFFreq.FREQ_246_0HZ_3DB

# Gyroscope configuration
icm.gyro_range = adafruit_icm20x.GyroRange.RANGE_1000_DPS
icm.gyro_data_rate_divisor = 0
icm.gyro_dlpf_cutoff = adafruit_icm20x.GyroDLPFFreq.FREQ_196_6HZ_3DB

# Sets up tuples to store sensor data
lastBMP = (bmp.pressure, bmp.temperature, bmp.altitude)
lastICM = (icm.acceleration, icm.gyro)
lastBNO = (bno.acceleration, bno.gyro, bno.magnetic,
           bno.raw_acceleration, bno.raw_gyro, bno.raw_magnetic,
           bno.linear_acceleration, bno.game_quaternion,
           bno.quaternion, bno.geomagnetic_quaternion, bno.stability_classification)

# Set up counting variables, set time
startTime = currentTime = backupTime = time()
numSeconds = numMinutes * 60
readingNum = fileNum = backupCount = 0

# Choose a filename that is not already taken by incrementing numbers until one is found
while os.path.exists('export' + str(fileNum) + '.csv'):
    fileNum = fileNum + 1
fileName = 'export' + str(fileNum) + '.csv'
saveFile = open(fileName, 'w', newline='')
saveCSV = csv.writer(saveFile)

# CSV first row header
saveCSV.writerow(["Reading Number", "Time", "BMP Pressure",
                  "BMP Temperature", "BMP Altitude",
                  "ICM Accel X", "ICM Accel Y", "ICM Accel Z",
                  "ICM Gyro X", "ICM Gyro Y", "ICM Gyro Z",
                  "BNO Accel X", "BNO Accel Y", "BNO Accel Z",
                  "BNO Gyro X", "BNO Gyro Y", "BNO Gyro Z",
                  "BNO Mag X", "BNO Mag Y", "BNO Mag Z",
                  "BNO Raw Accel X", "BNO Raw Accel Y", "BNO Raw Accel Z",
                  "BNO Raw Gyro X", "BNO Raw Gyro Y", "BNO Raw Gyro Z",
                  "BNO Raw Mag X", "BNO Raw Mag Y", "BNO Raw Mag Z",
                  "BNO Linear Accel X", "BNO Linear Accel Y", "BNO Linear Accel Z",
                  "BNO Game X", "BNO Game Y", "BNO Game Z",
                  "BNO Q X", "BNO Q Y", "BNO Q Z",
                  "BNO Mag Q X", "BNO Mag Q Y", "BNO Mag Q Z",
                  "BNO Stability"])

# data collection while loop
# loops for a certain amount of time
while currentTime < startTime + numSeconds:

    # update tuples and current time
    currentBMP = (bmp.pressure, bmp.temperature, bmp.altitude)
    currentICM = (icm.acceleration, icm.gyro)
    currentBNO = (bno.acceleration, bno.gyro, bno.magnetic,
                  bno.raw_acceleration, bno.raw_gyro, bno.raw_magnetic,
                  bno.linear_acceleration, bno.game_quaternion,
                  bno.quaternion, bno.geomagnetic_quaternion, bno.stability_classification)
    currentTime = time()

    if currentICM != lastICM or currentBMP != lastBMP or currentBNO != lastBNO:
        # update reading number for CSV
        readingNum = readingNum + 1

        # update last sensor data readings for next comparison
        lastBMP = currentBMP
        lastICM = currentICM
        lastBNO = currentBNO

        # write CSV to file
        saveCSV.writerow([readingNum, currentTime,
                          currentBMP[0], currentBMP[1], currentBMP[2],
                          currentICM[0][0], currentICM[0][1], currentICM[0][2],
                          currentICM[1][0], currentICM[1][1], currentICM[1][2],
                          currentBNO[0][0], currentBNO[0][1], currentBNO[0][2],
                          currentBNO[1][0], currentBNO[1][1], currentBNO[1][2],
                          currentBNO[2][0], currentBNO[2][1], currentBNO[2][2],
                          currentBNO[3][0], currentBNO[3][1], currentBNO[3][2],
                          currentBNO[4][0], currentBNO[4][1], currentBNO[4][2],
                          currentBNO[5][0], currentBNO[5][1], currentBNO[5][2],
                          currentBNO[6][0], currentBNO[6][1], currentBNO[6][2],
                          currentBNO[7][0], currentBNO[7][1], currentBNO[7][2],
                          currentBNO[8][0], currentBNO[8][1], currentBNO[8][2],
                          currentBNO[9][0], currentBNO[9][1], currentBNO[9][2],
                          currentBNO[10]])
        # Backup data to another .csv file every 5 seconds
        # can be used with a different storage medium in the future
    if currentTime >= backupTime:
        shutil.copyfile(fileName, fileName + "." + str(backupCount))  # if space is an issue delete old backups
        backupTime = currentTime + 5
        backupCount = backupCount + 1
saveFile.close()

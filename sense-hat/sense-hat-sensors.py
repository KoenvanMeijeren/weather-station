from sense_hat import SenseHat
from time import sleep

sense = SenseHat()

delay = 5
try:
    while True:
        temperature = round(sense.get_temperature(), 1)
        print("Temperature: %sC" % temperature)
        
        humidity = sense.get_humidity()
        print("Humidity: %s" % humidity)
        
        pressure = sense.get_pressure()
        print("Pressure: %s Millibars" % pressure)
        
        orientation_rad = sense.get_orientation_radians()
        print("p: {pitch}, r: {roll}, y: {yaw}".format(**orientation_rad))
        
        orientation = sense.get_orientation_degrees()
        print("p: {pitch}, r: {roll}, y: {yaw}".format(**orientation))
        
        orientation = sense.get_orientation()
        print("p: {pitch}, r: {roll}, y: {yaw}".format(**orientation))
        
        north = sense.get_compass()
        print("North: %s" % north)
        
        gyro_only = sense.get_gyroscope()
        print("p: {pitch}, r: {roll}, y: {yaw}".format(**gyro_only))
        
        accel_only = sense.get_accelerometer()
        print("p: {pitch}, r: {roll}, y: {yaw}".format(**accel_only))
        
        
        
        sleep(delay)
except KeyboardInterrupt:
    pass

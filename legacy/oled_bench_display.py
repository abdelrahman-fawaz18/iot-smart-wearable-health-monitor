#ECE Grad Project
#Smart Wearable Monitoring and Diagnosing eHealth System

#This code is designed to extract sensor data from
#MLX90614 Temp sensor and MPU6050 Inertial Measurement Unit

#Connections
#Vcc-->2 (Top left)
#Gnd-->6
#SCL-->5
#SDA-->3

from smbus import SMBus
from mlx90614 import MLX90614
from mpu6050 import mpu6050
import time
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import PIL

bus = SMBus(1)
sensor = MLX90614(bus, address=0x5A)
mpu = mpu6050(0x68)

RST = None
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
# Initialize library.
disp.begin()
disp.clear()
disp.display()

# Create blank image for drawing.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

font = ImageFont.load_default()

while True:
    #Print on shell
    print()
    accel_data = mpu.get_accel_data()
    print("Acc X : "+str(accel_data['x']))
    print("Acc Y : "+str(accel_data['y']))
    print("Acc Z : "+str(accel_data['z']))
    print()
    gyro_data = mpu.get_gyro_data()
    print("Gyro X : "+str(gyro_data['x']))
    print("Gyro Y : "+str(gyro_data['y']))
    print("Gyro Z : "+str(gyro_data['z']))
    print()
    print("Temp(MPU) : "+str(mpu.get_temp()))
    print("-------------------------------")
    print("Ambient Temperature: ", sensor.get_ambient())
    print("Obj Temperature: ", sensor.get_object_1())
    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.text((x, top),     "Ambient: " + str(round(sensor.get_ambient(), 2)) ,  font=font, fill=255)
    draw.text((x, top+8),   "Object:  " + str(round(sensor.get_object_1(), 2)),  font=font, fill=255)
    draw.text((x, top+16),  "Acc: x" + str(round(accel_data['x'], 1)) + " y" + str(round(accel_data['y'], 1)) + " z"+ str(round(accel_data['z'], 1)),  font=font, fill=255)
    draw.text((x, top+24),  "Gyr: x" + str(round(gyro_data['x'], 1)) + " y" + str(round(gyro_data['y'], 1)) + " z"+ str(round(gyro_data['z'], 1)),  font=font, fill=255)


    # Display image.
    disp.image(image)
    disp.display()
    time.sleep(.1)

bus.close()

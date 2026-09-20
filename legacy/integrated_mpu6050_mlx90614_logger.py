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
from datetime import datetime
from statistics import mean
import time
import csv

#Initializing objects
bus = SMBus(1) #I2C bus for MLX90614
sensor = MLX90614(bus, address=0x5A)
mpu = mpu6050(0x68)

#Initialize csv file
with open('j.csv', mode='w') as test_file:
    test_writer = csv.writer(test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #Write column titles to new csv row
    test_writer.writerow(['Time',\
                          'Acc-X', 'Acc-Y', 'Acc-Z',\
                          'Gyro-X', 'Gyro-Y', 'Gyro-Z',\
                          'Ambient Temp', 'Object Temp'])    
    
    Gyro_x_Buffer = [0,0,0]; Gyro_y_Buffer = [0,0,0]; Gyro_z_Buffer = [0,0,0];
    Acc_x_Buffer = [0,0,0]; Acc_y_Buffer = [0,0,0]; Acc_z_Buffer = [0,0,0];
    Ambient_Buffer = [0,0,0]; Object_Buffer = [0,0,0];
    
    while True:
        #Obtain sensor readings
        accel_data = mpu.get_accel_data()
        gyro_data = mpu.get_gyro_data()
        ambient_temp = sensor.get_ambient()
        object_temp = sensor.get_object_1()
        
        #Pop oldest reading
        Gyro_x_Buffer.pop(0); Gyro_y_Buffer.pop(0); Gyro_z_Buffer.pop(0);
        Acc_x_Buffer.pop(0); Acc_y_Buffer.pop(0); Acc_z_Buffer.pop(0);
        Ambient_Buffer.pop(0); Object_Buffer.pop(0);
        
        #Append latest reading
        Gyro_x_Buffer.append(gyro_data['x'])
        Gyro_y_Buffer.append(gyro_data['y'])
        Gyro_z_Buffer.append(gyro_data['z'])
        Acc_x_Buffer.append(accel_data['x'])
        Acc_y_Buffer.append(accel_data['y'])
        Acc_z_Buffer.append(accel_data['z'])
        Ambient_Buffer.append(ambient_temp)
        Object_Buffer.append(object_temp)
        
        #Calculate the mean of the lastest 3 readings
        Gyro_x = mean(Gyro_x_Buffer); Gyro_y = mean(Gyro_y_Buffer); Gyro_z = mean(Gyro_z_Buffer);
        Acc_x  = mean(Acc_x_Buffer);  Acc_y  = mean(Acc_y_Buffer);  Acc_z  = mean(Acc_z_Buffer);
        Amb_temp = mean(Ambient_Buffer); Obj_temp = mean(Object_Buffer)
        
        #Write sensor readings to new csv row
        test_writer.writerow([str(datetime.now()),\
                              str(Acc_x), str(Acc_y), str(Acc_z),\
                              str(Gyro_x), str(Gyro_y), str(Gyro_z),\
                              Amb_temp, Obj_temp])
            
        #Print readings on shell
        print()
        print("Acc X : "+str(accel_data['x']))
        print("Acc Y : "+str(accel_data['y']))
        print("Acc Z : "+str(accel_data['z']))
        print()
        print("Gyro X : "+str(gyro_data['x']))
        print("Gyro Y : "+str(gyro_data['y']))
        print("Gyro Z : "+str(gyro_data['z']))
        print()
        print("-------------------------------")
        print("Ambient Temperature: ", sensor.get_ambient())
        print("Obj Temperature: ", sensor.get_object_1())
        time.sleep(.02) #1/5 of the original value

bus.close()

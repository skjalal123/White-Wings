import os     
import time   
time.sleep(1) 
import pigpio 
os.system('sudo pigpio')

max_value = 2000
min_value = 700
print ("For first time launch, select calibrate")
print ("Type the exact word for the function you want")
print ("calibrate OR control OR stop")
class Motor:
    def __init__(self,ESC1=26,ESC2=19,ESC3=13,ESC4=6):
        pi = pigpio.pi()
        self.pi = pi
        self.ESC1 = ESC1
        self.ESC2 = ESC2
        self.ESC3 = ESC3
        self.ESC4 = ESC4
        pi.set_servo_pulsewidth(ESC1, 0) 
        pi.set_servo_pulsewidth(ESC2, 0)
        pi.set_servo_pulsewidth(ESC3, 0)
        pi.set_servo_pulsewidth(ESC4, 0)
        
    def calibrate(self):
        self.pi.set_servo_pulsewidth(self.ESC1, 0) 
        self.pi.set_servo_pulsewidth(self.ESC2, 0)
        self.pi.set_servo_pulsewidth(self.ESC3, 0)
        self.pi.set_servo_pulsewidth(self.ESC4, 0)
        print("Disconnect the battery and press Enter")
        inp = raw_input()
        if inp == '':
            self.pi.set_servo_pulsewidth(self.ESC1, max_value)
            self.pi.set_servo_pulsewidth(self.ESC2, max_value)
            self.pi.set_servo_pulsewidth(self.ESC3, max_value)
            self.pi.set_servo_pulsewidth(self.ESC4, max_value)
            print("Connect the battery NOW.. you will here two beeps, then wait for a gradual falling tone then press Enter")
            inp = raw_input()
            if inp == '':            
                self.pi.set_servo_pulsewidth(self.ESC1, min_value)
                self.pi.set_servo_pulsewidth(self.ESC2, min_value)
                self.pi.set_servo_pulsewidth(self.ESC3, min_value)
                self.pi.set_servo_pulsewidth(self.ESC4, min_value)
                print ("Wierd eh! Special tone")
                time.sleep(3)
                print ("Wait for it ....")
                time.sleep (2)
                print ("Im working on it, DONT WORRY JUST WAIT.....")
                self.pi.set_servo_pulsewidth(self.ESC1, 0) 
                self.pi.set_servo_pulsewidth(self.ESC2, 0)
                self.pi.set_servo_pulsewidth(self.ESC3, 0)
                self.pi.set_servo_pulsewidth(self.ESC4, 0)
                time.sleep(2)
                print ("Arming ESC now...")
                self.pi.set_servo_pulsewidth(self.ESC1, min_value)
                self.pi.set_servo_pulsewidth(self.ESC2, min_value)
                self.pi.set_servo_pulsewidth(self.ESC3, min_value)
                self.pi.set_servo_pulsewidth(self.ESC4, min_value)
                time.sleep(1)
                print ("Calibration complete... Now It ready to Fly")
            
    def control(self): 
        print ("I'm Starting the motor, I hope its calibrated and armed, if not restart by giving 'x'")
        time.sleep(1)
        speed = 700
        print ("Controls - a to decrease speed & d to increase speed OR q to decrease a lot of speed & e to increase a lot of speed")
        while True:            
            self.pi.set_servo_pulsewidth(self.ESC1, speed)
            self.pi.set_servo_pulsewidth(self.ESC2, speed)
            self.pi.set_servo_pulsewidth(self.ESC3, speed)
            self.pi.set_servo_pulsewidth(self.ESC4, speed)
            inp = raw_input()
        
            if inp == "q":
                speed -= 100
                print ("speed = %d" % speed)
            elif inp == "e":    
                speed += 100
                print ("speed = %d" % speed)
            elif inp == "d":
                speed += 10
                print ("speed = %d" % speed)
            elif inp == "a":
                speed -= 10
                print ("speed = %d" % speed)
            elif inp == "stop":
                self.stop()
                break	
            else:
                print ("WHAT DID I SAID!! Press a,q,d or e")
            
    def stop(self):
        self.pi.set_servo_pulsewidth(self.ESC1, 0) 
        self.pi.set_servo_pulsewidth(self.ESC2, 0)
        self.pi.set_servo_pulsewidth(self.ESC3, 0)
        self.pi.set_servo_pulsewidth(self.ESC4, 0)
        self.pi.stop()

inp = raw_input()
M = Motor()
if inp == "calibrate":
    M.calibrate()
elif inp == "control":
    M.control()
elif inp == "stop":
    M.stop()
else :
    print ("Thank You for not following the things I'm saying... now you gotta restart the program STUPID!!")

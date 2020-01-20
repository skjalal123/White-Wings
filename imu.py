import smbus
import time
import math
import sys
power_mgmt_1 = 0x6b

power_mgmt_2 = 0x6c

bus = smbus.SMBus(1)

address = 0x68

bus.write_byte_data(address, power_mgmt_1, 0)


class MPU9250:
	address = 0x68

	def __init__(self,gyro_x_reg,gyro_y_reg,gyro_z_reg,acc_x_reg,acc_y_reg,acc_z_reg):
		self.gyro_x_reg = gyro_x_reg
		self.gyro_y_reg = gyro_y_reg
		self.acc_x_reg = acc_x_reg
		self.acc_y_reg = acc_y_reg
		self.acc_z_reg = acc_z_reg
		self.gyro_z_reg = gyro_z_reg
		pre_time = 0
		self.pre_time = pre_time
		Xangle = 0
		self.Xangle = Xangle
		Yangle = 0
		self.Yangle = Yangle
		X = 0
		self.X = X
		Y = 0
		self.Y = Y
		self.configMPU9250()
	def configMPU9250(self):
		bus.write_byte_data(self.address, 0x6b, 0x00)
		bus.write_byte_data(self.address, 0x6b, 0x01)
		time.sleep(0.1)
		bus.write_byte_data(self.address, 0x1A, 0x03)
		bus.write_byte_data(self.address, 0x19, 0x04)
		bus.write_byte_data(self.address, 0x1B, 0x02<<3)
		bus.write_byte_data(self.address, 0x1C, 0x02<<3)
		bus.write_byte_data(self.address, 0x1D, 0x03)
		bus.write_byte_data(self.address, 0x37, 0x02)
		
	def read_byte(self,reg):
		return bus.read_byte_data(self.address, self.reg)

	def read_word(self,reg):

		self.reg = reg

		h = bus.read_byte_data(self.address, reg)

		l = bus.read_byte_data(self.address, reg+1)

		value = (h << 8) + l

		return value

	def read_word_2c(self,reg):

		self.reg = reg

		val = self.read_word(reg)

		if (val >= 0x8000):

			return -((65535 - val) + 1)
		else:
			return val



	def dist(self,a,b):
		self.a = a
		self.b = b
		return math.sqrt((a*a)+(b*b))



	def Acc_rotation(self):

		x = self.read_word_2c(self.acc_x_reg)/4096.0

		y = self.read_word_2c(self.acc_y_reg)/4096.0

		z = self.read_word_2c(self.acc_z_reg)/4096.0
		
		x_radians = math.atan2(x, self.dist(y,z))
		y_radians = math.atan2(y, self.dist(x,z))
	
		val_x = -math.degrees(x_radians)
		val = math.degrees(y_radians)
		
		return {'x':round(val_x , 3), 'y':round(val_y,3)}

	def Gyro_ang_rotation(self):

		x = self.read_word_2c(self.gyro_x_reg)/32.8
		y = self.read_word_2c(self.gyro_y_reg)/32.8
		z = self.read_word_2c(self.gyro_z_reg)/32.8
		
		return {'x':round(x,3),'y':round(y,3),'z':round(z,3)}
	
	def Gyro_rotaion(self):
		temp = time.time()
		curr_time = time.time() - temp
		dt = curr_time - self.pre_time
		dt_Xangle = self.Gyro_ang_rotation()['x'] * dt
		dt_Xangle = self.Gyro_ang_rotation()['y'] * dt
		Xangle = self.Xangle - dt_Xangle
		Yangle = self.Yangle - dt_Yangle
		self.pre_time = curr_time
		return {'x':Xangle, 'y':Yangle}
		
	def Gyro_mean(self):
		gyro_x_error = 0
		gyro_y_error = 0
		if self.gyro_error == 0
			global gyro_x_mean
			global gyro_y_mean
			for i in range(200):
				gyro_x_error = gyro_x_error + self.Gyro_rotation()['x']
				gyro_y_error = gyro_y_error + self.Gyro_rotation()['y']
				if(i==199):
					gyro_x_mean = gyro_x_error / 200
					gyro_y_mean = gyro_y_mean / 200
					self.gyro_error = 1
		return {'x':gyro_x_mean,'y':gyro_y_mean}
	def Acc_mean(self):
		Acc_x_error = 0
		Acc_y_error = 0
		if self.Acc_error == 0
			global Acc_x_mean
			global Acc_y_mean
			for i in range(200):
				Acc_x_error = Acc_x_error + self.Acc_rotation()['x']
				Acc_y_error = Acc_y_error + self.Acc_rotation()['y']
				if(i==199):
					Acc_x_mean = Acc_x_error / 200
					Acc_y_mean = Acc_y_mean / 200
					self.Acc_error = 1
		return {'x':Acc_x_mean,'y':Acc_y_mean}
	
	def Acc_angle(self,x_angle = 0,y_angle = 0):
		self.x_angle = x_angle
		self.y_angle = y_angle
		x_angle = self.Acc_rotation()['x'] - self.Acc_mean()['x']
		y_angle = self.Acc_rotation()['y'] - self.Acc_mean()['y']
		return {'x':x_angle,'y':y_angle}
		
	def Gyro_angle(self,x_angle = 0,y_angle = 0):
		self.x_angle = x_angle
		self.y_angle = y_angle
		x_angle = self.Gyro_rotation()['x'] - self.Gyro_mean()['x']
		y_angle = self.Gyro_rotation()['y'] - self.Gyro_mean()['y']
		return {'x':x_angle,'y':y_angle}
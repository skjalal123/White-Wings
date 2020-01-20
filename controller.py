import imu
import time
try:
	import matplotlib.pyplot as plt
except:
	print('Not Found')
gyro_x_reg = 0x43
gyro_y_reg = 0x45
gyro_z_reg = 0x47
acc_x_reg = 0x3B
acc_y_reg = 0x3D
acc_z_reg = 0x3F

temp = imu.MPU9250(gyro_x_reg,gyro_y_reg,gyro_z_reg,acc_x_reg,acc_y_reg,acc_z_reg)
X_angle = 0
Y_angle = 0
X = []
Y = []
for a in range(200):
	X_angle = temp.Acc_x_rotation()
	Y_angle = temp.Acc_y_rotation()
	if (a==199):
		X_angle = X_angle/200
		Y_angle = Y_angle/200
	X.append(a)
	Y.append(Y_angle)
plt.plot(X,Y)
print('X_angle')
print(X_angle)
print('Y_angle')
print(Y_angle)
plt.show()

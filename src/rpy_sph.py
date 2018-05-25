import math 
import numpy as np

def sph2cart(az, inc, r):
	az = math.radians(az)
	inc = math.radians(inc)

	x = r*math.sin(inc)*math.cos(az) 
	y = r*math.sin(inc)*math.sin(az)
	z = r*math.cos(inc)

	return np.array([x, y, z])

def orientation_transformation(pitch, yaw, roll, input_vector): 
	# Clockwise rotations about axes

	pitch = math.radians(pitch) 
	yaw = math.radians(yaw)
	roll = math.radians(roll)

	pitchTransform = [[math.cos(pitch), 0, -math.sin(pitch)], [0, 1, 0], [math.sin(pitch), 0, math.cos(pitch)]]
	yawTransform = [[math.cos(yaw), -math.sin(yaw), 0], [math.sin(yaw), math.cos(yaw), 0], [0, 0 , 1]]
	rollTransform = [[1, 0, 0], [0, math.cos(roll), -math.sin(roll)], [0, math.sin(roll), math.cos(roll)]]

	matrixTransform = np.matmul(pitchTransform, yawTransform)
	matrixTransform = np.matmul(matrixTransform, rollTransform)

	return np.matmul(matrixTransform, input_vector) 

def findAngle(vector):
	normal = [0, 0, 1] # Normal of plane
	sin_angle = (np.dot(vector, normal))/(np.linalg.norm(vector) * np.linalg.norm(normal)) 
	return math.degrees(math.asin(sin_angle))

az = 0
inc = 90 
r = 1 

array_pitch = 35.9
array_yaw = 157
array_roll = 0

speaker_pitch = -array_pitch # Array pitch => Opposite of Speaker pitch 
speaker_yaw = -array_yaw 
speaker_roll = -array_roll

plane_normal = [0, 0, 1]

vector = sph2cart(az,inc,r) # Take the cartesian position of the speaker in space as a vector 

new_vector = orientation_transformation(speaker_pitch, speaker_yaw, speaker_roll, vector) # Rotation of camera array mapped to corresponding rotation of speaker vector instead 
# Instead of taking the orientation of the array, take the corresponding orientation of the speaker vector instead 
# Note that must do pitch, then yaw, then roll in that order since I defined the matrix that way 
# This is because the plane changes with each rotation in any of the axes 
# However, when i'm doing the pitch, yaw and roll of the array, relatively I should keep the array in the reference plane and do the orientations with reference to the same plane. 
# i.e pitch up, but when i do azimuth I rotate about the original z axis still, not about the tilted z axis! 


# for array_yaw in range(0, 360, 10):
# 	print('For array_yaw of' + str(array_yaw))
# 	speaker_yaw = -array_yaw 
# 	new_vector = pitch_transformation(speaker_pitch, speaker_yaw, vector)
# 	print(findAngle(new_vector))

print(findAngle(new_vector))


#print(pitch_transformation(pitch, vector))

# def dir_wrt_rotated_axes(az, inc, r): 
# 	x, y, z = sph2cart(az, inc, r)

# Note that trigo functions convert between an angle and the ratio of two sides of a triangle 
# Cos, Sin and Tan take an angle in radians as input and returns the ratio 
# aCos, aSin, aTan take the ratio as input and return an angle in radians 
# Only convert the angles, never the ratios 
# https://en.wikipedia.org/wiki/Spherical_coordinate_system
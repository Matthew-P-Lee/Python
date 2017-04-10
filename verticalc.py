import math

#speed, distance, time calculations	
class Verticalc(object):

	grade = 0.0
	distance = 0.0
	speed = 0.0
	time = 0.0

	def __init__(self, grade,distance,speed,time):
		self.grade = grade
		self.distance = distance
		self.speed = speed
		self.time = time
		
	def getVerticalFeet(self):
		vert = ((float(grade)/100) * float(distance)) 
		vertFeet = float(vert) * 5280
		return vertFeet
		
	def getDistance(self):
		return float(speed/60.0) * float(time)

 #   def __str__(self):
  #      return
  
#calculate vertical gain from an angle and average speed - treadmill calculator
grade = input("Enter the average angle of the climb (in degrees): ")
distance = input("Enter the distance of the climb (in miles): ")
speed = input ("Enter your average pace (in mph): ")
time = input ("Enter your total time at " + str(grade) + "% grade (in minutes): ")

vc = Verticalc(grade,distance,speed,time)

#vertical feet gained
print "%s vertical feet at %s%% grade" % (str(vc.getVerticalFeet()), vc.grade)

#distance given time / speed
print "%s miles travelled at %s mph for %s minutes" % (str(vc.getDistance()),str(vc.speed),str(vc.time))

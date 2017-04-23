'''
SkullCam FaceTracker 2017

This is a heavily modified version of an openCV sample demonstrating
Canny edge detection. It no longer does Canny edge detection.

Usage:
  faceTrack 2017-ubuntu.py [no args]

'''



import cv2
import numpy as np
import time
import video
import sys
import serial


# hardcoded video resolution
CAM_X = 352
CAM_Y = 292
# 640 480

# hardcoded video source
skullCam = 0

# hardcoded serial port for arduino communication
ser = serial.Serial('/dev/ttyACM0', 9600)	# ubuntu
#ser = serial.Serial('COM3', 9600)	# windows

# improve tracking
goodPoints = list()

# direction to move
whichWay = list()

def detect(img, cascade_fn='haarcascade_frontalface_alt.xml',
	scaleFactor=1.3, minNeighbors=4, minSize=(20, 20),
	flags=cv2.cv.CV_HAAR_SCALE_IMAGE):
	
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	gray = cv2.equalizeHist(gray)
	
	cascade = cv2.CascadeClassifier(cascade_fn)
	
	# the actual detection function
	rect = cascade.detectMultiScale(gray, scaleFactor=scaleFactor, minNeighbors=minNeighbors, minSize=minSize, flags=flags)
	
	faces = list()
	trackPoints = list()
	
	for x1, y1, x2, y2 in rect:
		faces.append([y1, y2, x1, x2])
		
		# if there's a face, add it to the list
		if len(faces) == 1:
			goodPoints.append([y1, y2, x1, x2])
	
	# if we've seen a face for the last 3 frames...
	# ACTUALLY it's been modified for 2 instead of 3
	if len(goodPoints) >= 2:
		# get the positions
		data1 = goodPoints[0]
		data2 = goodPoints[1]
		#data3 = goodPoints[2]
		
		# calculate our average position values
		#avgX = (data1[2] + data2[2] + data3[2]) / 3
		#avgY = (data1[0] + data2[0] + data3[0]) / 3
		#avgW = (data1[3] + data2[3] + data3[3]) / 3
		#avgH = (data1[1] + data2[1] + data3[1]) / 3
		# two instead of three
		avgX = (data1[2] + data2[2]) / 2
		avgY = (data1[0] + data2[0]) / 2
		avgW = (data1[3] + data2[3]) / 2
		avgH = (data1[1] + data2[1]) / 2
		
		# draw a rectangle
		cv2.rectangle(img, (avgX, avgY), (avgX+avgW, avgY+avgH), (0, 0, 255), 3)
		
		# note the center point of the averaged face position
		tpX = avgX + (avgW / 2)
		tpY = avgY + (avgH / 2)
		trackPoints.append([tpX, tpY])
		
		# draw a little circle there
		cv2.circle(img, (tpX, tpY), 5, (0, 255, 0), 3)
		
		# keep the list fresh!
		pop1 = goodPoints.pop(0)
	
	return faces, img, trackPoints

def get_direction(midX, midY, trackX, trackY):
	# which way to look?
	
	attnThreshold = 30
	xBig = False
	yBig = False
	answer = 'X'
	
	# calculate the difference between the center and the given position
	diffX = midX - trackX
	diffY = midY - trackY
	absX = abs(diffX)
	absY = abs(diffY)
	
	# is the difference big enough to worry about?
	if absX > attnThreshold or absY > attnThreshold:
		if absX > absY:
			xBig = True
		elif absY > absX:
			yBig = True
	
	if xBig:
		if diffX < 0:
			# cam look right
			answer = 'R'
		elif diffX > 0:
			# cam look left
			answer = 'L'
	
	if yBig:
		if diffY < 0:
			# cam look down
			answer = 'D'
		elif diffY > 0:
			# cam look up
			answer = 'U'
	
	return answer

if __name__ == '__main__':
	print __doc__
    
	def nothing(*arg):
		pass
	
	# startup calculations
	midX = (CAM_X / 2)
	midY = (CAM_Y / 2)

	# create window
	cv2.namedWindow('camFaces')
    
	#set up video capture
	skullCapture = video.create_capture(skullCam)
    
	while True:
		# get video frame
		print 'capture frame'
		flagL, skullImg = skullCapture.read()
		
		if(flagL):
			# detect faces
			print 'detect faces'
			#if(flagL):
			faces, imgFaces, trackingPoints = detect(skullImg)
			print 'found: ' + str(len(faces))
			
			# show detected faces
			print 'show detected faces'
			cv2.imshow('camFaces', imgFaces)
			#for face in faces:
			#	print face
			for tPts in trackingPoints:
				print tPts
			
			# determine a looky direction
			print 'where to look?'
			goto1 = ''
			for tPts in trackingPoints:
				goto1 = get_direction(midX, midY, tPts[0], tPts[1])
				print goto1
			
			# comm w/ arduino
			goto2 = ''
			if(len(trackingPoints) >= 1):
				ptX = trackingPoints[(len(trackingPoints) - 1)]
				goto2 = get_direction(midX, midY, ptX[0], ptX[1])
				print goto2
				ser.write(goto2)
			
        	# detect keypresses
		ch = cv2.waitKey(5)
		if ch == 27:
			# exit on 'escape' key
			break
		
	cv2.destroyAllWindows() 			


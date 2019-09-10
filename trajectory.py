import cv2
import numpy as np
import os

# Get the file name in absolute path
# Separate the dir name for later use
# Open the video for reading and save its fps
file = input("Type the path to the file with the extension: ")
file = os.path.abspath(file)
dir = os.path.dirname(file) + "/"
vin = cv2.VideoCapture(file)
fps = vin.get(5)

# Set all the specifications for the blob detector
# Most important are the circularity and the area
params = cv2.SimpleBlobDetector_Params()
params.minThreshold = 0;
params.maxThreshold = 255;
params.filterByCircularity = True
params.minCircularity = 0.7
params.filterByArea = True
params.minArea = 300
params.filterByConvexity = True
params.minConvexity = 0.1
params.filterByInertia = True
params.minInertiaRatio = 0.01
detector = cv2.SimpleBlobDetector_create(params)

num_points = 0 # number of times we found the ball
count = 0 # number of frames we've gone through, 0-indexed
start = 0 # can be changed so we don't start at the beginning of the video
success = True

fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
vin.set(1, start)
parabolaX = []
parabolaY = []
parabola = np.array([]) # will hold the result from numpy's polyfit()

# while there are images to be read
while success:
	success,image = vin.read()
	# if an image is read
	if success:
		# separate background and foreground, then save the image
		# then invert the colors and save it again
		fgmask = fgbg.apply(image)
		cv2.imwrite(dir + "back%d.jpg" % count, fgmask)
		fgmask = cv2.bitwise_not(fgmask)
		cv2.imwrite(dir + "back_inv%d.jpg" % count, fgmask)

		# detect blobs in the current inverted foreground image
		keypoints = detector.detect(fgmask)
		# if there is only one keypoint, that means we found only the bball
		# also in this implementation, we've chosen to use just the first 7 times
		#	we find the ball
		if len(keypoints) is 1 and num_points < 7:
			parabolaX.append(keypoints[0].pt[0])
			parabolaY.append(keypoints[0].pt[1])
			parabola = np.polyfit(parabolaX, parabolaY, 2)
			num_points += 1

		# create a new image with the circle where the ball is
		# save the new image
		new_im = cv2.drawKeypoints(image, keypoints, 
			np.array([]), (0,255,0), 4)
		cv2.imwrite(dir + "circles%d.jpg" % count, new_im)
		count += 1
	
out_points = [] # points on the predicted curve
in_points = [] # points we have already found

# this makes sure that our parabola can span any direction the shooter 
#	is shooting
begin = 0
if 1000-int(parabolaX[0]) < int(parabolaX[0]):
	begin = 1000-int(parabolaX[0])
else:
	begin = int(parabolaX[0])

# plot a point on our predicted curve every 5 pixels
for num in range(begin, 1000, 5):
	a = num*num*parabola[0]
	b = num*parabola[1]
	c = parabola[2]
	point = cv2.KeyPoint(num, a+b+c, 3)
	out_points.append(point)
# plot the points we found from tracking the ball
for i in range(len(parabolaX)):
	point = cv2.KeyPoint(parabolaX[i], parabolaY[i], 3)
	in_points.append(point)

count = 0 # number of frames we've gone through, 0-indexed
start = 0 # can be changed so we don't start at the beginning of the video
success = True
vin.set(1, start) 

# while there are images to be read
while success:
  success,image = vin.read()
  # if an image is read
  if success:
  	  # plot the predicted curve in red, the known points in green, and save the
  	  # 	resulting image
	  new_im = cv2.drawKeypoints(image, out_points, np.array([]), (0,0,255), 4)
	  new_im = cv2.drawKeypoints(new_im, in_points, np.array([]), (0,255,0), 4)
	  cv2.imwrite(dir + "predicted%d.jpg" % count, new_im)
	  count += 1

vin.release()

# we'll use ffmpeg to turn the .jpg's into an .mp4
# there are a lot of compatibility issues here, so if there is an issue with the 
# 	actual production of a video, this is the first place to look
cmd1 = "ffmpeg -framerate "
cmd1 = cmd1 + str(fps)

# saving the four output videos
cmd = cmd1 + " -i " + dir + "back%1d.jpg -pix_fmt yuv420p " + dir + "back.mp4"
os.system(cmd)
cmd = cmd1 + " -i " + dir + "back_inv%1d.jpg -pix_fmt yuv420p " + dir + "back_inv.mp4"
os.system(cmd)
cmd = cmd1 + " -i " + dir + "circles%1d.jpg -pix_fmt yuv420p " + dir + "circles.mp4"
os.system(cmd)
cmd = cmd1 + " -i " + dir + "predicted%1d.jpg -pix_fmt yuv420p " + dir + "predicted.mp4"
os.system(cmd)

# deleting all the .jpg's we made in the process
os.system("rm " + dir + "*.jpg")
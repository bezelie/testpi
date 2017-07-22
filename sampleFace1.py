# -*- coding: utf-8 -*-
# Bezelie Sample Code : Face Recognition Test
import picamera
import picamera.array
import cv2
import bezelie

cascade_path =  "/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml"
cascade = cv2.CascadeClassifier(cascade_path)

# Initializing
count = 0

# Get Started
bezelie.initPCA9685()
bezelie.moveCenter()

# Main Loop
with picamera.PiCamera() as camera:                         # Open Pi-Camera as camera
  with picamera.array.PiRGBArray(camera) as stream:         # Open Video Stream from Pi-Camera as stream
    camera.resolution = (320, 240)                          # Display Resolution
    camera.hflip = True                                     # Vertical Flip 
    camera.vflip = True                                     # Horizontal Flip

    while True:
      camera.capture(stream, 'bgr', use_video_port=True)    # Capture the Video Stream
      gray = cv2.cvtColor(stream.array, cv2.COLOR_BGR2GRAY) # Convert BGR to Grayscale
      facerect = cascade.detectMultiScale(gray,             # Find face from gray
        scaleFactor=1.5,                                    # 1.1 - 1.9 :the bigger the quicker & less acurate 
        minNeighbors=2,                                     # 3 - 6 : the smaller the more easy to detect
        minSize=(60,60),                                  # Minimam face size 
        maxSize=(200,200))                                  # Maximam face size

      if len(facerect) > 0:
        bezelie.moveHead (20)
        for rect in facerect:
          cv2.rectangle(stream.array,                       # Draw a red rectangle at face place 
            tuple(rect[0:2]),                               # Upper Left
            tuple(rect[0:2]+rect[2:4]),                     # Lower Right
            (0,0,255), thickness=2)                         # Color and thickness

	x = rect[0]
	y = rect[1]
	width = rect[2]
	height = rect[3]
#	dst1 = stream.array[y:y+height, x:x+width]           # Face trimming
	dst1 = gray[y:y+height, x:x+width]           # Face trimming
        dst2 = cv2.resize(dst1,(384,int(384*height/width)))    # Resize into 384width
        cv2.rectangle(dst2,(0,0),(383,383),(0,0,0), thickness=2)  # Color and thickness
        (ret, binary) = cv2.threshold(dst2, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

	new_image_path = '/home/pi/bezelie/testpi/img/' + 'face-'+str(count)+'.jpg'
        count = count + 1
	cv2.imwrite(new_image_path, binary)                    # Creating a jpg file

#      cv2.imshow('frame', stream.array)                     # Display the stream
      dst = cv2.resize(stream.array,(640,480))
      cv2.imshow('frame',dst)
      bezelie.moveHead (0)

      if cv2.waitKey(1) & 0xFF == ord('q'):                 # Quit operation
        break

      stream.seek(0)                                        # Reset the stream
      stream.truncate()

    cv2.destroyAllWindows()

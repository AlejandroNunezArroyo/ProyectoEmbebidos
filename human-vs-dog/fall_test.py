#import os
#os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"   # see issue #152
#os.environ["CUDA_VISIBLE_DEVICES"] = ""

import sys, time 
import numpy as np
import cv2
import tensorflow as tf 
from tensorflow import keras 
from tensorflow.keras.models import load_model
from tensorflow.keras.optimizers import RMSprop

model = load_model('model_humandog.h5')

#prev_img=cv2.imread('/home/ubuntu/tensorrt/URFD_images/Falls/fall_fall-02/frame0039.jpg')
#curr_img=cv2.imread('/home/ubuntu/tensorrt/URFD_images/Falls/fall_fall-02/frame0040.jpg')


cap = cv2.VideoCapture('304x304_human-dog.mp4')
#cap = cv2.VideoCapture(0)
ret, frame = cap.read()
prev_img=frame
prev_img_res=cv2.resize(prev_img,(300,300))
prev_img_c=cv2.cvtColor(prev_img_res, cv2.COLOR_BGR2GRAY)
kernel = np.ones((15,15),np.float32)/225.0
counter=0
acc=0.0
while(True):
        
    ret, frame = cap.read()

    curr_img_res=cv2.resize(frame,(300,300))
    curr_img_res=cv2.cvtColor(curr_img_res, cv2.COLOR_BGR2RGB)
    pp = cv2.cvtColor(curr_img_res, cv2.COLOR_RGB2BGR)
    # vert = vert.astype('uint8')
    
    # smoothed = cv2.filter2D(vert,-1,kernel)

    # back = cv2.cvtColor(smoothed,cv2.COLOR_GRAY2RGB)

    #fall = np.expand_dims(back ,axis=0)
    fall = np.expand_dims(curr_img_res ,axis=0)
    start_time = time.time()
    fall_norm = fall/255.0
    preds = model.predict(fall_norm)
	
    #acc=acc+(time.time()-start_time)
    if preds[0][0] > 0.5:
        print("Human",preds," FPS: ", 1.0/(time.time()-start_time), counter)
    else:
        print("Dog",preds," FPS: ", 1.0/(time.time()-start_time), counter)

    cv2.imshow("frame", pp)
    cv2.waitKey(1)
    # prev_img_c=curr_img_c
    # print(preds," FPS: ", 1.0/(time.time()-start_time))
    acc=acc+1.0/(time.time()-start_time)
    counter=counter+1
    if counter>=5000:
        print('average FPS:',acc/counter)
        break
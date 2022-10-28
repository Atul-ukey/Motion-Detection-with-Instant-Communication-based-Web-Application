from django.shortcuts import render,HttpResponse
import cv2
import pywhatkit as what
import time
import win32api
from sys import exit
#import numpy as np
from datetime import datetime

# Create your views here.
def home(request):
    try:
        if request.method == 'POST':
            print('we are using post request')
            IP = request.POST.get('IP')
            whats = request.POST.get('whats')
            camera = IP
            camera = camera + '/video'
            number = whats
            #camera = "http://26.149.203.27:8080/video"
            cap = cv2.VideoCapture(0)
            cap.open(camera)
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            output = cv2.VideoWriter('C:\\Apps\\output.avi',fourcc, 20.0,(int(cap.get(3)),int(cap.get(4))))
            #out = cv2.VideoWriter('C:\\Apps\\out.avi',fourcc, 20.0,(int(cap.get(3)),int(cap.get(4))))
            #output = cv2.VideoWriter('C:\\Apps\\output.avi',fourcc, 20.0,(int(cap.get(3)),int(cap.get(4))))
            rat,frame = cap.read()
            myuse = frame
            #set the image adddress.
            cv2.imwrite("C:\\Apps\\frame\\imgN.jpg",myuse)
            background = cv2.imread("C:\\Apps\\frame\\imgN.jpg")
            background = cv2.cvtColor(background,cv2.COLOR_BGR2GRAY)
            background = cv2.GaussianBlur(background,(21,21),0)
            print(cap)
            temp = 0
            pre = 0
            while True:
                
                status,frame = cap.read()
                gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                gray = cv2.GaussianBlur(gray,(21,21),0)
                diff = cv2.absdiff(background,gray)
                thresh = cv2.threshold(diff,30,225,cv2.THRESH_BINARY)[1]
                thresh = cv2.dilate(thresh,None,iterations=2)
                
                
                cnts,res = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
                for contour in cnts:
                    if cv2.contourArea(contour)<100000:
                        continue
                    (x,y,w,h) = cv2.boundingRect(contour)
                    x = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,225,0),3)
                    tt = frame
                    if background != frame:
                        font = cv2.FONT_HERSHEY_PLAIN
                        cv2.putText(x, str(datetime.now()), (20, 40), font, 2, (0, 0, 255), 2, cv2.LINE_AA)
                        #set the image adddress till framex.
                        cv2.imwrite("C:\\Apps\\frame\\framex%d.jpg"%temp,x)
                        output.write(x)
                        #set the image adddress till framex.
                        image = 'C:\\Apps\\frame\\framex%d.jpg'%temp
                        if pre<3:   
                            what.sendwhats_image(number,image,"Hey, Someone is There",12,True,12)
                            pre = pre+1
                cv2.imshow("RoboSecurity",frame)
                print("temp:",temp)
                temp +=1
                key = cv2.waitKey(1)
                if key == ord("s"):
                    break
                elif key == ord("e"):
                    exit()
            cap.release()  
            output.release()
            cv2.destroyAllWindows()
    except:
        pass
    return render(request,'home/index.html')



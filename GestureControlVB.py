import cv2
import numpy as np

import utility
import screen_brightness_control as sbc

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

cam=cv2.VideoCapture(0)

detector=utility.hand_Detector(detect_conf=0.7)
width,height=640,480
cam.set(3,width)
cam.set(4,height)

brightness=0
vol=0
vol_bar=0
vol_per=0



devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

CurrVol=volume.GetVolumeRange()

min_vol=CurrVol[0]
max_vol=CurrVol[1]

while True:
    success,img=cam.read()
    img = cv2.flip(img, 1)
    img=detector.find_hands(img)
    landmark,boundary=detector.find_Pos(img,draw=False,Print=False,boundary_box=True)
    if len(landmark)!=0:
        #print(landmark)
        x1,y1=landmark[4][1],landmark[4][2]
        x2,y2=landmark[8][1],landmark[8][2]
        x3,y3=landmark[12][1],landmark[12][2]

        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        if x1>x2:
            if x3>x2:
                area = (boundary[0] - boundary[2]) * (boundary[1] - boundary[3]) // 100
                #print(area)
                if 290 < area < 1000:

                    cv2.circle(img, (x1, y1), 12, (255, 0, 0), cv2.FILLED)
                    cv2.circle(img, (x2, y2), 12, (255, 0, 0), cv2.FILLED)

                    cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

                    length = np.sqrt(np.square(x2 - x1) + np.square(y2 - y1))

                    # linear interpolation

                    vol_bar = np.interp(length, [25, 240], [400, 160])
                    vol_per = np.interp(length, [25, 240], [1, 100])

                    if landmark[16][2] < landmark[14][2]:
                        finger = 1
                    else:
                        finger = 0

                    if finger == 0:
                        volume.SetMasterVolumeLevelScalar((10 * round(vol_per / 10)) / 100, None)

                    cv2.rectangle(img, (50, 160), (75, 400), (255, 22, 0), 3)
                    cv2.rectangle(img, (50, int(vol_bar)), (75, 400), (0, 255, 0), cv2.FILLED)

                    cv2.putText(img, f'{int(10 * round(vol_per / 10))}%', (40, 450), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 1,
                                (0, 25, 255), 3)
                elif area<290:
                    cv2.putText(img,"BRING CLOSER!!!",(400,50),cv2.FONT_HERSHEY_PLAIN,1.5,(0,0,255),2)
                else:
                    cv2.putText(img, "PUT AWAY!!!", (400, 50), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 255), 2)


            else:
                #print(x1,x2)
                area = (boundary[0] - boundary[2]) * (boundary[1] - boundary[3]) // 100
                #print(area)
                if 290 < area < 1000:
                    cv2.circle(img,(x1,y1),5,(255,0,0),cv2.FILLED)
                    cv2.circle(img,(x2,y2),5,(255,0,0),cv2.FILLED)
                    cv2.line(img,(x1,y1),(x2,y2),(255,0,0),2)

                    cv2.circle(img,(cx,cy),4,(255,0,255),cv2.FILLED)
                    length=np.sqrt(np.square(x2-x1)+np.square(y2-y1))
                    #print(int(length))


                    bright_bar=np.interp(length,[25,240],[400,160])
                    bright_per=np.interp(length,[25,240],[0,100])
                    #print(int(length), brightness)
                    if landmark[20][2] < landmark[18][2]:
                        finger = 1
                    else:
                        finger = 0

                    if finger == 0:
                        sbc.set_brightness(int(10*round(bright_per/10)))

                    cv2.rectangle(img,(550,160),(575,400),(255,0,0),2)
                    cv2.rectangle(img, (550, int(bright_bar)), (575, 400), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img,f'Brightness: {int(10*round(bright_per/10))}%',(440,450),cv2.FONT_HERSHEY_PLAIN,1.5,(0,0,255),2)

                elif area < 290:
                    cv2.putText(img, "BRING CLOSER!!!", (400, 50), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 255), 2)
                else:
                    cv2.putText(img, "PUT AWAY!!!", (400, 50), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 255), 2)
        else:
            if x2>x3:
                area = (boundary[0] - boundary[2]) * (boundary[1] - boundary[3]) // 100
                #print(area)
                if 290 < area < 1000:
                    #print(x1,x2)
                    cv2.circle(img,(x1,y1),5,(255,0,0),cv2.FILLED)
                    cv2.circle(img,(x2,y2),5,(255,0,0),cv2.FILLED)
                    cv2.line(img,(x1,y1),(x2,y2),(255,0,0),2)

                    cv2.circle(img,(cx,cy),4,(255,0,255),cv2.FILLED)
                    length=np.sqrt(np.square(x2-x1)+np.square(y2-y1))
                    #print(int(length))


                    bright_bar = np.interp(length, [25, 240], [400, 160])
                    bright_per = np.interp(length, [25, 240], [0, 100])
                    #print(int(length), brightness)
                    if landmark[20][2] < landmark[18][2]:
                        finger = 1
                    else:
                        finger = 0

                    if finger == 0:
                        sbc.set_brightness(int(10*round(bright_per/10)))
                    cv2.rectangle(img, (550, 160), (575, 400), (255, 0, 0), 2)
                    cv2.rectangle(img, (550, int(bright_bar)), (575, 400), (0, 255, 0), cv2.FILLED)


                    cv2.putText(img,f'Brightness: {int(10*round(bright_per/10))}%',(435,450),cv2.FONT_HERSHEY_PLAIN,1.5,(0,0,255),2)

                elif area < 290:
                    cv2.putText(img, "BRING CLOSER!!!", (400, 50), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 255), 2)
                else:
                    cv2.putText(img, "PUT AWAY!!!", (400, 50), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 255), 2)
            else:

                area = (boundary[0] - boundary[2]) * (boundary[1] - boundary[3]) // 100
                print(area)
                if 290 < area < 1000:

                    cv2.circle(img, (x1, y1), 12, (255, 0, 0), cv2.FILLED)
                    cv2.circle(img, (x2, y2), 12, (255, 0, 0), cv2.FILLED)

                    cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

                    length = np.sqrt(np.square(x2 - x1) + np.square(y2 - y1))

                    # linear interpolation

                    vol_bar = np.interp(length, [25, 240], [400, 160])
                    vol_per = np.interp(length, [25, 240], [1, 100])

                    if landmark[16][2] < landmark[14][2]:
                        finger = 1
                    else:
                        finger = 0

                    if finger == 0:
                        volume.SetMasterVolumeLevelScalar((10 * round(vol_per / 10)) / 100, None)

                    cv2.rectangle(img, (50, 160), (75, 400), (255, 22, 0), 3)
                    cv2.rectangle(img, (50, int(vol_bar)), (75, 400), (0, 255, 0), cv2.FILLED)

                    cv2.putText(img, f'{int(10 * round(vol_per / 10))}%', (40, 450), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 1,
                                (0, 25, 255), 3)
                elif area < 290:
                    cv2.putText(img, "BRING CLOSER!!!", (400, 50), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 255), 2)
                else:
                    cv2.putText(img, "PUT AWAY!!!", (400, 50), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 255), 2)

    cv2.imshow("Image",img)
    cv2.waitKey(1)




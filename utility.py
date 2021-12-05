import cv2
import mediapipe

class hand_Detector():
    def __init__(self,max_num=2,detect_conf=0.5,track_conf=0.5):

        self.max_Hand=max_num
        self.D_confidence=detect_conf
        self.T_confidence=track_conf


        self.hands=mediapipe.solutions.hands.Hands(False,self.max_Hand,self.D_confidence,self.T_confidence)
        self.Draw=mediapipe.solutions.drawing_utils

    def find_hands(self,img):
        imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.result=self.hands.process(imgRGB)

        return img

    def find_Pos(self,img,handNo=0,draw=True,Print=True,boundary_box=False):

        boundary=[]
        land_mark=[]
        if self.result.multi_hand_landmarks!=None:
            hand_indicator=self.result.multi_hand_landmarks[handNo]
            abscissa = []
            ordinate = []
            for index, j in enumerate(hand_indicator.landmark):
                height,width,_ = img.shape
                cx,cy = int(j.x * width), int(j.y * height)
                abscissa.append(cx)
                ordinate.append(cy)
                land_mark.append([index,cx,cy])

                if Print:
                    print(index, cx, cy)
                if draw:
                    cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)

            abscissa_min,abscissa_max=min(abscissa),max(abscissa)
            ordinate_min,ordinate_max=min(ordinate),max(ordinate)

            boundary=abscissa_min,ordinate_min,abscissa_max,ordinate_max
            if boundary_box==True:
                cv2.rectangle(img,(abscissa_min-25,ordinate_min-25),(abscissa_max+25,ordinate_max+25),(0,255,255),2)

        return land_mark,boundary




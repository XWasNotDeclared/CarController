import cv2
import mediapipe as mp
import time
import numpy as np
from HandTrackingModule import handDectector
from pynput.keyboard import Key, Controller

keyboard=Controller()
# def angle(x1,x2,y1,y2):
#     vector1 = np.array([x1,y1])
#     vector2 = np.array([x2,y2])

#     angle_radians = np.arctan2(np.cross(vector1,vector2),np.dot(vector1,vector2))
#     angle_degrees = np.degrees(angle_radians)

#     return angle_degrees
def pressKeyControl(keyboard,lineAngle,LeftThumpUp,RightThumpUp):
    if RightThumpUp:
        keyboard.release('w')
        keyboard.press('s')
    else:
        keyboard.press('w')
        keyboard.release('s')
    if LeftThumpUp:
        keyboard.press(Key.space)
    else:
        keyboard.release(Key.space)

    if (lineAngle<80):
        keyboard.press('d')
    else:
        keyboard.release('d')

    if (lineAngle>100):
        keyboard.press('a')
    else:
        keyboard.release('a')




def isThumbUp(Hand):
    if Hand[4][2] < Hand[3][2]-20:
        return True
    return False

def angle(x1, y1, x2, y2):
    dot_product = x1 * x2 + y1 * y2
    magnitude1 = np.sqrt(x1**2 + y1**2)
    magnitude2 = np.sqrt(x2**2 + y2**2)

    cos_theta = dot_product / (magnitude1 * magnitude2)
    angle_radians = np.arccos(np.clip(cos_theta, -1.0, 1.0))
    angle_degrees = np.degrees(angle_radians)

    return angle_degrees



def main():
    pTime=0
    cTime=0
    cap = cv2.VideoCapture(0)
    Detector=handDectector()
    while True:
        success , img = cap.read()
        img = cv2.flip(img,1)
        img=Detector.findHands(img)
        HandOne=Detector.findPositions(img,handNo=0)
        HandTwo=Detector.findPositions(img,handNo=1)
       
        if len(HandOne)!=0 and len(HandTwo)!=0:
            
            if HandOne[0][1]>HandTwo[0][1]:
                HandOne,HandTwo=HandTwo,HandOne
            cv2.line(img,(HandOne[0][1],HandOne[0][2]),(HandTwo[0][1],HandTwo[0][2]),(255,255,255),2) 
            vectorHandx= HandTwo[0][1]-HandOne[0][1]
            vectorHandy= HandTwo[0][2]-HandOne[0][2]

            lineAngle=angle(vectorHandx,vectorHandy,0,1 )
           # print(lineAngle)
            print(isThumbUp(HandOne)," ",isThumbUp(HandTwo))
            pressKeyControl(keyboard,lineAngle,isThumbUp(HandOne),isThumbUp(HandTwo))
        else:
            keyboard.release('w')


        

        
        cTime = time.time()
        fps=1/(cTime-pTime)
        pTime=cTime
        cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_ITALIC,2,(255,0,255),3)
        cv2.imshow("img",img)
        if cv2.waitKey(1) & 0xFF== ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
        




if __name__=='__main__':
    main()
import cv2
import mediapipe as mp
import time

class handDectector():
    def __init__(self,mode=False,maxHands=2,modelC=1,detectionCon=0.5,trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.modelC = modelC
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxHands,self.modelC,self.detectionCon,self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
    def findHands(self,img,draw=True):
        imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw==True:
                    self.mpDraw.draw_landmarks(img,handLms,self.mpHands.HAND_CONNECTIONS)
        return img
    def findPositions(self,img,handNo,isOneHand=False):
        lmList = []
        if self.results.multi_hand_landmarks:
            if len(self.results.multi_hand_landmarks)>=handNo+1:
                myHand = self.results.multi_hand_landmarks[handNo]
                for id, lm in enumerate(myHand.landmark):
                    h,w,c = img.shape
                    cx,cy = int(lm.x*w), int(lm.y*h)
                    lmList.append([id,cx,cy])
                    #cv2.circle(img,(cx,cy),abs(int(lm.z*100)),(255,125,0),3)
        return lmList
def main():
    pTime=0
    cTime=0
    cap = cv2.VideoCapture(0)
    Detector=handDectector()
    while True:
        success , img = cap.read()
        img = cv2.flip(img,1)
        img=Detector.findHands(img)
        lmList=Detector.findPositions(img,handNo=1)
        if len(lmList)!=0:
            print(lmList[4])
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
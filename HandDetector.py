import cv2
import mediapipe as mp

class HandDetector():
    def __init__(self,mode=False,
               maxHands=2,
               modelComplexity=1,
               detectionCon=0.5,
               trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplexity = modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxHands,self.modelComplexity,self.detectionCon,self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
    def findHands(self,img,draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img
    def findPosition(self,img,handNo=0,draw = True):
        lmList = []

        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                height, width, channel = img.shape
                cx, cy = int(lm.x * width), int(lm.y * height)
                lmList.append([id,cx,cy])
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        return lmList
    def fingersUp(self,lmList):
        fingersIds = [4,8,12,16,20]
        fingers = []
        if len(lmList):

            if lmList[fingersIds[0]][1] > lmList[fingersIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            for i in range(1, 5):

                if lmList[fingersIds[i]][2] < lmList[fingersIds[i] - 1][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
        return fingers




# def main():
#     cap = cv2.VideoCapture(0)
#     handDetector = HandDetector()
#     while True:
#         success,img = cap.read()
#         img = handDetector.findHands(img)
#         lis = handDetector.findPosition(img)
#         if len(lis) != 0:
#            print(lis[4])
#         cv2.imshow("Image", img)
#         cv2.waitKey(1)

# if __name__ == "__main__":
#     main()
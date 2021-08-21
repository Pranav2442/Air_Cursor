import math  
import pyautogui,mediapipe as mp,cv2 as cv,numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume



previous_locx,previous_locy=0,0
current_locx,current_locy=0,0
factor=8
framer=100

width_S, height_S = 640, 480
cap = cv.VideoCapture(0)
cap.set(3,width_S)
cap.set(4,height_S)
cap.set(5,120)


class Detect_Hands():
    def __init__(self, status=False, maxHands=2, detection_confidence=0.5, tracking_confidence=0.5):
        self.status = status
        self.maxHands = maxHands
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.status, self.maxHands,
                                        self.detection_confidence, self.tracking_confidence)
        self.mpDraw = mp.solutions.drawing_utils

    
    
    def trackPos(self, frame, handNo=0, draw=True, color =  (255, 0, 255), z_axis=False):

        landmarks_list = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = frame.shape
                if z_axis == False:
                   cx, cy = int(lm.x * w), int(lm.y * h)
                   landmarks_list.append([id, cx, cy])
                elif z_axis:
                    cx, cy, cz = int(lm.x * w), int(lm.y * h), round(lm.z,3)
                    landmarks_list.append([id, cx, cy, cz])

                if draw:
                    cv.circle(frame, (cx, cy),5,color, cv.FILLED)

        return landmarks_list

    
    
    
    
    def track_hands(self, frame, draw=True):
        framergb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(framergb)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(frame, hand_landmarks,
                                               self.mpHands.HAND_CONNECTIONS)
        return frame

    

def main():
    cap = cv.VideoCapture(0)
    detector = Detect_Hands(maxHands=1)
    while True:
        ret, frame = cap.read()
        frame=cv.flip(frame,1)
        frame = detector.track_hands(frame)
        landmarks_list = detector.trackPos(frame,z_axis=True,draw=False)
        if len(landmarks_list) != 0:
            print(landmarks_list[4])
        cv.imshow("img", frame)
        if cv.waitKey(1) ==27:
            break




detector = Detect_Hands(maxHands=1, detection_confidence=0.85, tracking_confidence=0.8)
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()   


status = ''
stat = 0
upper_points = [4, 8, 12, 16, 20]



min_volume = volRange[0]
max_volume = volRange[1]
height_min = 50
height_max = 200
vol = 0
volBar = 400
volpercentage = 0



pyautogui.FAILSAFE = False
while (cap.isOpened()):
    fingers=[]
    ret,frame = cap.read()
    frame=cv.flip(frame,1)
    frame = detector.track_hands(frame)
    landmarks_list = detector.trackPos(frame, draw=False)

    if len(landmarks_list)!=0:
        if landmarks_list[upper_points[0]][1] > landmarks_list[upper_points[0 -1]][1]:
            if landmarks_list[upper_points[0]][1] >= landmarks_list[upper_points[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
        elif landmarks_list[upper_points[0]][1] < landmarks_list[upper_points[0 -1]][1]:
            if landmarks_list[upper_points[0]][1] <= landmarks_list[upper_points[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

        for i in range(1,5):
            if landmarks_list[upper_points[i]][2] < landmarks_list[upper_points[i] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)


      
        if (fingers == [0,0,0,0,0]) & (stat == 0 ):
            status='None'
        elif (fingers == [0, 1, 1, 1, 0] ) & (stat == 0 ):
            status = 'Scroll'
            stat = 1
        elif (fingers == [1, 1, 0, 0, 0] ) & (stat == 0 ):
             status = 'VolumeBar'
             stat = 1
        elif (fingers == [1 ,1 , 1, 1, 1] ) & (stat == 0 ):
             status = 'Cursor'
             stat = 1


    
    if status == 'VolumeBar':
        stat = 1
        putText(status)
        if len(landmarks_list) != 0:
            if fingers[-1] == 1:
                stat = 0
                status = 'None'
                print(status)

            else:

                 
                    x1, y1 = landmarks_list[4][1], landmarks_list[4][2]
                    x2, y2 = landmarks_list[8][1], landmarks_list[8][2]
                    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                    cv.circle(frame, (x1, y1), 10, (0,215,255), cv.FILLED)
                    cv.circle(frame, (x2, y2), 10, (0,215,255), cv.FILLED)
                    cv.line(frame, (x1, y1), (x2, y2), (0,215,255), 3)
                    cv.circle(frame, (cx, cy), 8, (0,215,255), cv.FILLED)

                    length = math.hypot(x2 - x1, y2 - y1)
                    

                    
                    
                    vol = np.interp(length, [height_min, height_max], [min_volume, max_volume])
                    volBar = np.interp(vol, [min_volume, max_volume], [400, 150])
                    volpercentage = np.interp(vol, [min_volume, max_volume], [0, 100])
                    print(vol)
                    volfinal = int(vol)
                    
                
                    volume.SetMasterVolumeLevel(volfinal, None)
                    if length < 40:
                        cv.circle(frame, (cx, cy), 11, (0, 0, 255), cv.FILLED)

                    cv.rectangle(frame, (30, 150), (55, 400), (0, 255, 0), 3)
                    cv.rectangle(frame, (30, int(volBar)), (55, 400), (0, 255, 0), cv.FILLED)
                    cv.putText(frame, f"{int(volpercentage)}%", (25, 430), cv.FONT_HERSHEY_COMPLEX, 0.9, (220, 210, 0), 3)

    
    
    
    
    if status == 'Cursor':
        stat = 1
        
        putText(status)
        cv.rectangle(frame, (framer, framer), (width_S-framer, height_S-framer), (255, 255, 255), 3)

        if fingers[1:] == [0,0,0,0]: 
            stat = 0
            status ='None'
            print(status)
        else:
            if len(landmarks_list) != 0:
                x1, y1 = landmarks_list[8][1], landmarks_list[8][2]
                x2,y2=landmarks_list[12][1:]
                w, h = pyautogui.size()
                x3 = int(np.interp(x1, [framer, width_S-framer], [0, w]))
                y3 = int(np.interp(y1, [framer,height_S-framer], [0, h ]))
                cv.circle(frame, (landmarks_list[8][1], landmarks_list[8][2]), 7, (255, 255, 255), cv.FILLED)
                

                x4,y4=int((x1+x2)/2),int((y1+y2)/2)
                x5,y5=landmarks_list[12][1],landmarks_list[12][2]
                lengthx=math.hypot(x5-x2,y5-y2)
                if fingers[1]==1 and fingers[0]==1:
                    current_locx=previous_locx+(x3-previous_locx)/factor
                    current_locy=previous_locy+(y3-previous_locy)/factor
                    pyautogui.moveTo(2*current_locx,2*current_locy)
                    previous_locx,previous_locy=current_locx,current_locy
                if fingers[0]==0 :
                    # if lengthx<10:
                        cv.circle(frame, (landmarks_list[4][1],landmarks_list[4][2]), 10, (0, 0, 255), cv.FILLED)  # thumb
                        pyautogui.click()

    if status=='Scroll':
        stat=1
        putText(status)
        
        if len(landmarks_list)!=0:
            if fingers==[0,1,1,1,0]:
            # up
                putText(status = 'Up', loc=(190, 40), color = (0, 0, 255))
                pyautogui.scroll(100)

            if fingers == [0,1,1,1,1]:
                # down
                putText(status = 'Down', loc =  (190, 40), color = (0, 0, 255))
                pyautogui.scroll(-100)
            elif fingers == [0, 0, 0, 0, 0]:
                stat = 0
                status = 'None'

    cv.imshow('Air Window',frame)

    if cv.waitKey(1) ==27:
        break

    def putText(status,loc = (10, 40), color = (255,0, 255)):
        cv.putText(frame, str(status), loc, cv.FONT_HERSHEY_DUPLEX,2, color, 2)
        
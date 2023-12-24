import mediapipe as mp
import cv2, math, random
cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1000) 
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

color = (0,0,255)

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands()

top_left = (20,20)
bottom_right = (220,220)


def calculate_distance(x1, y1, x2, y2):
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance
while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    imgRGB = cv2.flip(imgRGB, 1)
    results = hands.process(imgRGB)

    img = cv2.resize(img, (0,0), fx=2, fy=1.5)
    img = cv2.flip(img, 1)

    if results.multi_hand_landmarks:
        for handLM in results.multi_hand_landmarks:
            index_fingure = None
            thumb_fingure = None
            middle_fingure = None
            for id,lm in enumerate(handLM.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                if id == 4:
                    cx, cy = int(lm.x*w), int(lm.y*h)
                    cv2.circle(center=(cx,cy), img=img, color=(0,0,255), radius=15, thickness=-1)
                    thumb_fingure = (cx, cy)
                if id == 8:
                    cv2.circle(center=(cx,cy), img=img, color=(0,0,255), radius=20, thickness=-1)
                    index_fingure = (cx,cy)
                if id==12:
                    cv2.circle(center=(cx,cy), img=img, color=(0,0,255), radius=20, thickness=-1)
                    middle_fingure = (cx,cy)
                if index_fingure and thumb_fingure:
                    res = calculate_distance(index_fingure[0],index_fingure[1],thumb_fingure[0],thumb_fingure[1])
                    if top_left[0]<index_fingure[0]<bottom_right[0] and top_left[1]<index_fingure[1]<bottom_right[1]:
                        if res < 50:
                            top_left = (index_fingure[0]-100, index_fingure[1]-100)
                            bottom_right = (index_fingure[0]+100, index_fingure[1]+100)
                if index_fingure and middle_fingure:
                    res2 = calculate_distance(index_fingure[0],index_fingure[1],middle_fingure[0],middle_fingure[1])
                    if res2<30:
                        color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))

            mp_draw.draw_landmarks(img, handLM, mp_hands.HAND_CONNECTIONS)
            
    
    rect = cv2.rectangle(pt1=top_left,pt2=bottom_right, img=img, color=color, thickness=-1)

    cv2.imshow("frame", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
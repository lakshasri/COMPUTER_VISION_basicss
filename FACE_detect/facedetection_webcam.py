import cv2
import mediapipe as mp
import time

cap=cv2.VideoCapture(0)#open webcam
pTime=0

mpFaceDetection=mp.solutions.face_detection
mpDraw=mp.solutions.drawing_utils
faceDetection=mpFaceDetection.FaceDetection(0.75)

while True:
    success,img=cap.read()
    if not success:
        break

    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results=faceDetection.process(imgRGB)

    if results.detections:
        for detection in results.detections:
            bboxC=detection.location_data.relative_bounding_box
            ih,iw,_=img.shape
            bbox=(int(bboxC.xmin*iw),int(bboxC.ymin*ih),
                  int(bboxC.width*iw),int(bboxC.height*ih))
            cv2.rectangle(img,bbox,(255,0,255),2)
            cv2.putText(img,f'{int(detection.score[0]*100)}%',
                        (bbox[0],bbox[1]-10),cv2.FONT_HERSHEY_PLAIN,
                        2,(255,0,255),2)

    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,f'FPS:{int(fps)}',(20,70),cv2.FONT_HERSHEY_PLAIN,
                3,(0,255,0),2)
    
    cv2.imshow("Webcam Face Detection",img)
    if cv2.waitKey(1)&0xFF==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
from gpiozero import DistanceSensor, Robot, OutputDevice, Motor
from bluedot import BlueDot
import cv2, math
from time import sleep

# Variables
eyes = DistanceSensor(23, 24, max_distance=1, threshold_distance=0.2)
car = Robot(left=(4, 14), right=(17,18))
castorWheel = Motor(18)
eyes.when_activated = car.backward(speed=0.5)
eyes.when_deactivated = car.stop()

class RoboCar():
    def spin(self):
        car.right(0.25)
        car.sleep(2)
        car.stop()
    def square(self):
        for i in range(4):
            car.forward()
            sleep(10)
            car.right()
            sleep(1)
    def move(self, pos):
        if pos.top:
            car.forward(pos.distance)
        elif pos.bottom:
            car.backward(pos.distance)
        elif pos.left:
            car.left(pos.distance)
        elif pos.right:
            car.right(pos.distance)
    def SprayFire(self):
        water_pump.on()
        sleep(30)
        water_pump.off()

water_pump = OutputDevice(18)

water_pump.on()
sleep(10)
water_pump.off()

path = "/Users/trivikram/Downloads/Fire-Detection-using-HAAR-Cascade-Classifier-in-OpenCV-main/cascade.xml"
cameraNo = 0
objectName = 'FIRE'
frameWidth = 640
frameHeight = 480
color = (255, 0, 255)
safeDistance = 100
desiredAngle = 45

cap = cv2.VideoCapture(cameraNo)
if not cap.isOpened():
    raise IOError("Cannot open webcam")

cap.set(3, frameWidth)
cap.set(4, frameHeight)

def empty(a):
    pass

# CREATE TRACKBAR; PURELY FOR TESTING PURPOSES
cv2.namedWindow("TRACKBAR")
cv2.resizeWindow("TRACKBAR", frameWidth, frameHeight+100 )
cv2.createTrackbar("Scale", " TRACKBAR", 400, 1000, empty)
cv2.createTrackbar("Neig", "TRACKBAR", 8, 20, empty)
cv2.createTrackbar("Min Area", "TRACKBAR", 0, 100000, empty)

cascade = cv2.CascadeClassifier(path)

waterpump = OutputDevice(17)
def moveTowardsFire(x, y):
    center_x = frameWidth/ 2
    angle = (x - center_x) * desiredAngle / frameWidth
    car.forward(speed=0.5)
    castorWheel.stop()

def Extinguish_fire():
    waterpump.on()
    sleep(30)
    waterpump.off()
    print('Fire Extinguished. You are now safe.')

while True:
    cameraBrightness = cv2.getTrackbarPos("Brightness", "TRACKBAR")
    cap.set(10, cameraBrightness)
    success, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    scaleVal = 1 + (cv2.getTrackbarPos("Scale", "TRACKBAR") / 1000)
    neig = cv2.getTrackbarPos("Neig", "TRACKBAR")

    objects = cascade.detectMultiScale(gray)

    for (x, y, w, h) in objects:
        area = w*h
        minArea = cv2.getTrackbarPos("Min Area", "TRACKBAR")
        if area > minArea:
            cv2.rectangle(img, (x, y), (x+w, y+h), color, 3)
            cv2.putText(img, objectName, (x, y-5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, color, 2)
            roi_color = img[y:y+h, x:x+w]

            Extinguish_fire()  # Call function to extinguish fire when detected

    cv2.imshow("TRACKBAR", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

distance_sensor = DistanceSensor.distance - 100
distance_point = 5.0

angle_rad = math.acos(distance_point / distance_sensor)
angle_deg = math.degrees(angle_rad)

distance_fire = math.sqrt(distance_sensor**2 - distance_point**2)

print('Angle: {} degrees'.format(angle_deg))
print('Distance to Fire: {} units'.format(distance_fire))

while True:
    print('I am currently', eyes.distance, 'm away from the nearest object')
    sleep(1)

cap.release()
cv2.destroyAllWindows()




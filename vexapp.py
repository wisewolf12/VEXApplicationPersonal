from gpiozero import DistanceSensor, Robot, Motor
from bluedot import BlueDot
import cv2, math
from time import sleep

# Variables
eyes = DistanceSensor(20, 26, max_distance=5, threshold_distance=0.2)
car = Robot(left=(17, 18), right=(22,23))
castorWheel = Motor(forward=6, backward=12)
eyes.when_activated = car.backward(speed=0.5)
eyes.when_deactivated = car.stop()

a = 0.5

path = "C:/Users/trivikram/Downloads/Fire-Detection-using-HAAR-Cascade-Classifier-in-OpenCV-main/cascade.xml"
#cameraNo = 0
# objectName = 'FIRE'
framewidth = 640
frameheight = 480
# color = (255, 0, 255)
safeDistance = 100
desiredAngle = 45

def empty(self):
    pass

cap = cv2.VideoCapture(0)
water_pump = Motor(forward=16, backward=19)
class CarControl():
        
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
    def control_water_pump(self, direction, duration):
        if direction == "forward":
            water_pump.forward()
        elif direction == "backward":
            water_pump.backward()

            sleep(duration)
            water_pump.stop()
    def extinguishfire(self):
        water_pump.forward()
        sleep(5)
        water_pump.stop()
    def get_angle(self, a, c):
        cos_angle = (a**2 + c**2 - a**2) / (2*a*c)
        angle_rad = math.acos(cos_angle)
        angle_deg = math.degrees(angle_rad)
        return angle_deg
    

    def move_to_fire(self, angle):
        
        turn_duration = angle/90
        turn_duration = min(turn_duration, 1.0)
        
        move_duration = 1.0
        car.forward()
        sleep(move_duration)
        car.stop()
      
    def forward(self):
        car.left()
        sleep(5)
        car.stop()
    def backward(self):
        car.right()
        sleep(5)
        car.stop()
    def left(self):
        car.left()
        sleep(2)
        car.stop()
    def right(self):
        car.right()
        sleep(2)
        car.stop()
    def stop(self):
        car.stop()

    def detect_fire(self):
#         cc = CarControl()
        print('in detect fire main loop')
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
                raise IOError('Cannot open webcam')
                return
            
        blurred = None
        
        while True:
            
                
            ret, frame = cap.read()
                
            if not ret:
                print('failed to read frame')
                break
                    
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            blurred = cv2.GaussianBlur(gray, (15, 15), 0)
            
            _, threshold = cv2.threshold(blurred, 220, 255, cv2.THRESH_BINARY)
            
            blurred = cv2.GaussianBlur(gray, (15, 15), 0)
            
            contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                 
            if len(contours) > 0:
                print('Fire detected')
                fire_detected = True
                print('after detected')
                c = eyes.distance
                print('after distance')
                angle = cc.get_angle(a, c)
                print('after get angle')
                cc.move_to_fire(angle)
                print('after movement')
                cc.extinguishfire()
                print('after extinguished')
                #print('water pump'+ water_pump.is_active)
#                 cv2.imshow('Live footage', frame)        
            cv2.imshow('Live footage', frame)
            
            if cv2.waitKey(1) & 255 == ord('q'):
                break
                
    cap.release()
    cv2.destroyAllWindows()        
   

def diagnostic():
    cc.spin
    sleep(5)
    cc.square()
    
              
bd = BlueDot(cols=5, rows=3)
bd.wait_for_connection(timeout=None)
cc=CarControl()
print('before while loop')

while  bd.is_connected:
    
    #print('connection stable')
    
    bd[0,0].visible =   False
    bd[2,0].visible =   False
    bd[3,0].visible =   False
    bd[4,0].visible =   False
    bd[1,1].visible =   False
    bd[0,2].visible =   False
    bd[2,2].visible =   False
#     bd[3,2].visible =   False
#     bd[4,2].visible =   False

    bd[1,0].color = 'gray'
    bd[1,0].square = True
    bd[1,2].color = 'gray'
    bd[1,2].square = True
    bd[0,1].color = 'gray'
    bd[0,1].square = True
    bd[2,1].color = 'gray'
    bd[2,1].square = True
    bd[3,1].circle = True
    bd[3,1].color = 'blue'
    bd[4,1].square = True
    bd[4,1].color = 'red'
    bd[4,2].circle = True
    bd[4,2].color = 'green'
    bd[3,2].square = True
    bd[3,2].color = 'yellow'
    
    bd[1,0].when_pressed = cc.forward
    bd[1,2].when_pressed = cc.backward
    bd[0,1].when_pressed = cc.left
    bd[2,1].when_pressed = cc.right
    bd[4,1].when_pressed = cc.stop
    bd[3,1].when_pressed = cc.detect_fire
    bd[4,2].when_pressed = diagnostic
    bd[3,2].when_pressed = cc.extinguishfire
#end of program

import RPi.GPIO as GPIO
import time

button = 10

def setup():
       GPIO.setmode(GPIO.BOARD)
       GPIO.setup(button, GPIO.IN)
       
def loop():
        while True:
              button_state = GPIO.input(button)
              if  button_state == False:
                  print("Button Pressed…")
                  while GPIO.input(button) == False:
                    time.sleep(0.2)

def endprogram():
    GPIO.cleanup()
    
if __name__ == "__main__":
         setup()
         try:
                 loop()
         except KeyboardInterrupt:
                 print("keyboard interrupt detected")
                 endprogram()
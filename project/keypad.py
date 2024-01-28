import RPi.GPIO as GPIO
import time

row1 = 18
row2 = 23
row3 = 24
row4 = 25
col1 = 12
col2 = 16
col3 = 20
col4 = 21
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(row1, GPIO.OUT)
GPIO.setup(row2, GPIO.OUT)
GPIO.setup(row3, GPIO.OUT)
GPIO.setup(row4, GPIO.OUT)
GPIO.setup(col1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(col2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(col3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(col4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

enteredPassword = ""
def readLine(line, characters):
    global enteredPassword
    GPIO.output(line, GPIO.HIGH)
    if(GPIO.input(col1) == 1):
        enteredPassword += characters[0]
    if(GPIO.input(col2) == 1):
        enteredPassword += characters[1]
    if(GPIO.input(col3) == 1):
        enteredPassword += characters[2]
    if(GPIO.input(col4) == 1):
        enteredPassword += characters[3]
    print(enteredPassword)
    GPIO.output(line, GPIO.LOW)

try:
    while True:
        readLine(row1, ["1","2","3","A"])
        readLine(row2, ["4","5","6","B"])
        readLine(row3, ["7","8","9","C"])
        readLine(row4, ["*","0","#","D"])
        time.sleep(0.25)
except KeyboardInterrupt:
    print("\nApplication stopped!")
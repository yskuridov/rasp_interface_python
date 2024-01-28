from gpiozero import DistanceSensor
from time import sleep

distanceSensor = DistanceSensor(6, 5)

while True:
    print(distanceSensor.distance)
    sleep(1)
from gpiozero import Button
from picamera import PiCamera
from time import sleep

print("hello")

btn = Button(10)
camera = PiCamera()
camera.start_preview(alpha=192)
print("smile")
btn.wait_for_press()
print("pressed")

camera.capture("path")
camera.stop_preview()
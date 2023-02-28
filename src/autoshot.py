from time import sleep
from ahk import AHK

ahk = AHK()
# press Alt+Shift+S every 20 seconds

while True:
    ahk.send_input("{Alt down}{Shift down}{S down}")
    sleep(0.1)
    ahk.send_input("{Alt up}{Shift up}{S up}")
    sleep(19.9)
    # with keyboard.pressed(Key.ctrl, Key.shift, Key.alt):
    #     keyboard.press("3")
    #     keyboard.release("3")
    # sleep(10)


from pad4pi import rpi_gpio
from gpiozero import TonalBuzzer, Button
from gpiozero.tones import Tone
import time

KEYPAD = [
        ["1", "2", "3", "A"],
        ["4", "5", "6", "B"],
        ["7", "8", "9", "C"],
        ["*", "0", "#", "D"]
]

ROW_PINS = [4, 14, 15, 17]
COL_PINS = [18,27,22,23]
buzzer = TonalBuzzer(16)
door_switch = Button(12)

factory = rpi_gpio.KeypadFactory()
keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)

class Doorbell:

    def __init__(self):
        self.password = ""
        self.can_open = False
        self.is_door_open = False

    def process(self):
        if not door_switch.is_pressed and not self.can_open:
            self.buzz()

        if self.can_open:
            print('You can open the door now')
            time.sleep(10)
            print('Locked!')
            self.can_open = False

    def buzz(self):
        buzzer.play(Tone("A4"))
        time.sleep(2)
        buzzer.stop()


    def handleKeyPress(self, key):
        if not self.can_open:
            self.password += key
            buzzer.play(Tone("C4"))
            time.sleep(0.1)
            buzzer.stop()
            if len(self.password) == 4:
                print(f'password: {self.password}')
                self.checkpassword()
                self.password = ""

    def checkpassword(self):
        if self.password == '1234':
            self.can_open = True;
            print("yay! password accepted")
        else:
            print("bummer, wrong password")


doorbell = Doorbell()
keypad.registerKeyPressHandler(doorbell.handleKeyPress)



try:
    while(True):
        time.sleep(0.2)
        doorbell.process()
except e:
    print(e)
    keypad.cleanup()





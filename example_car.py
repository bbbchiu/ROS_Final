from cars import CAR
import time
import keyboard
import random

stop = False
def press_fn(_):
    global stop
    stop = True

keyboard.on_press_key("q",press_fn)

c = CAR('TOM',1)

c.get_connect()

c.ModifyConfig('Create')
c.set_tag_val()
#c.update_data('ATag2',41)
#c.c.ModifyConfig('Delete')
while True:
    if(stop):
        break
    
    a = random.randint(38,45)
    b = random.randint(50,80)
    print(a,b)
    c.send_farm_temperature(1,a)
    c.send_farm_humidity(1,b)
    time.sleep(15)

c.get_disconnect()
from server import SERVER
import time
import keyboard
import random

stop = False
def press_fn(_):
    global stop
    stop = True

keyboard.on_press_key("q",press_fn)

s = SERVER('Apple',1)

s.get_connect()

s.ModifyConfig('Create')
s.set_tag_val()
#s.update_data('ATag1',10)
#c.c.ModifyConfig('Delete')
while True:
    if(stop):
        break
    
    #a = random.randint(38,45)
    #b = random.randint(50,80)
    #print(a,b)
    #c.update_data('ATag1',a)
    #c.update_data('ATag2',b)
    #time.sleep(15)

s.get_disconnect()
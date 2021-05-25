# 檔案
* cars.py: 車子的library檔
* server.py: 農場的library檔
* example檔: 測試檔

## library

import:
	from cars import CAR
	from server import SERVER

create object:
	c = CAR(name,id)
	(id = 1, device = 'Device1')
	s = SERVER(name,id)
	(id = 1, device = "Device1")

connect to datahub:
	c.get_connect()
	s.get_connect()

disconnect to datahub:
	c.get_disconnect()
	s.get_disconeect()

create new device:
	c.ModifyConfig('Create')
	/* it'll create a new device based on your id */
	/* the tags info is in cars.py -> info_Init -> tagId,tagDes */

set default_value:
	c.set_tag_val()
	/* do it after create new device, it'll set default value to tags */
	/* the tags info is in cars.py -> info_Init -> tagId,default_tag_val */

delete device:
	c.ModifyConfig('Delete')
	/* it'll delete tags info in device */
	/* the tags info is in cars.py -> info_Init -> tagId,tagDes,default_tag_val */

update data to car:
	c.update_data(id,Tag,Value)
	c.update_data(id,Tag,Value,'car')

update data to farm:
	c.update_data(id,Tag,Value,'farm')


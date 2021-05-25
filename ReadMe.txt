import:
	from cars import CAR

create object:
	c = CAR(id)
	(id = 1, car = Device1)

connect to datahub:
	c.get_connect()

disconnect to datahub:
	c.get_disconnect()

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
	c.update_data(Tag,Value)
	c.update_data(Tag,Value,'car')

update data to server:
	c.update_data(Tag,Value,'server')


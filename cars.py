import datetime
import time
import random

from wisepaasdatahubedgesdk.EdgeAgent import EdgeAgent
import wisepaasdatahubedgesdk.Common.Constants as constant
from wisepaasdatahubedgesdk.Model.Edge import EdgeAgentOptions, MQTTOptions, DCCSOptions, EdgeData, EdgeTag, EdgeStatus, EdgeDeviceStatus, EdgeConfig, NodeConfig, DeviceConfig, AnalogTagConfig, DiscreteTagConfig, TextTagConfig
from wisepaasdatahubedgesdk.Common.Utils import RepeatedTimer

class CAR():
    def __init__(self,name,id):
        self.CarId = id
        self.name = name
        self.infoInit()
        self.createEdgeAgent()

    def infoInit(self):
        self.DeviceId = 'Device'+str(self.CarId)
        self.DCCS_apiUrl = 'https://api-dccs-ensaas.education.wise-paas.com/'

        self.CarNodeId = ''
        self.Car_DCCS_CreKey = ''
        self.ServerNodeId = ''
        self.Server_DCCS_CreKey = ''

        self.tagId =           ['ATag1'      ,'ATag2'   ,'ATag3'    ,'TTag2'          ,'TTag3']
        self.tagDes =          ['Temperature','Humidity','Farm ID'  ,'Car Name'       ,'Car Travel']
        self.default_tag_val = [0            ,0         ,""         ,str(self.name)   ,'Start']

    def createEdgeAgent(self):
        self.CarOptions = EdgeAgentOptions(
            nodeId = self.CarNodeId,        
            type = constant.EdgeType['Gateway'], 
            deviceId = self.DeviceId,
            heartbeat = 60,
            dataRecover = True,
            connectType = constant.ConnectType['DCCS'],                                                  # 若連線類型是 DCCS, DCCSOptions 為必填
            DCCS = DCCSOptions(
                apiUrl = self.DCCS_apiUrl,
                credentialKey = self.Car_DCCS_CreKey
            )
        )
        
        self.ServerOptions = EdgeAgentOptions(
            nodeId = self.ServerNodeId,        
            type = constant.EdgeType['Gateway'], 
            deviceId = self.DeviceId,
            heartbeat = 60,
            dataRecover = True,
            connectType = constant.ConnectType['DCCS'],                                                  # 若連線類型是 DCCS, DCCSOptions 為必填
            DCCS = DCCSOptions(
                apiUrl = self.DCCS_apiUrl,
                credentialKey = self.Server_DCCS_CreKey
            )
        )

        self.CarEdgeAgent = EdgeAgent( options = self.CarOptions )
        self.CarEdgeAgent.on_connected = self.car_on_connected
        self.CarEdgeAgent.on_disconnected = self.car_on_disconnected
        self.CarEdgeAgent.on_message = self.car_on_message

        self.ServerEdgeAgent = EdgeAgent( options = self.ServerOptions )
        self.ServerEdgeAgent.on_connected = self.server_on_connected
        self.ServerEdgeAgent.on_disconnected = self.server_on_disconnected
        self.ServerEdgeAgent.on_message = self.server_on_message

    def ModifyConfig(self,actions):
        self.config = EdgeConfig()
        self.CarNodeConfig = NodeConfig(nodeType = constant.EdgeType['Gateway'])
        self.config.node = self.CarNodeConfig
        self.CarDeviceConfig = DeviceConfig(
            id = 'Device' + str(self.CarId),
            name = 'Device' + str(self.CarId),
            description = 'Device' + str(self.CarId),
            deviceType = 'Smart Device',
            retentionPolicyName = '')
        for index,i in enumerate(self.tagId):
            if(i.split('Tag')[0] == 'A'):
                analog = AnalogTagConfig(name = i,
                    description = self.tagDes[index],
                    readOnly = False,
                    arraySize = 0,
                    spanHigh = 1000,
                    spanLow = 0,
                    engineerUnit = '',
                    integerDisplayFormat = 4,
                    fractionDisplayFormat = 2)
                self.CarDeviceConfig.analogTagList.append(analog)
            elif(i.split('Tag')[0] == 'D'):
                discrete = DiscreteTagConfig(name = i,
                    description = self.tagDes[index],
                    readOnly = False,
                    arraySize = 0,
                    state0 = '0',
                    state1 = '1',
                    state2 = '',
                    state3 = '',
                    state4 = '',
                    state5 = '',
                    state6 = '',
                    state7 = '')
                self.CarDeviceConfig.discreteTagList.append(discrete)
            elif(i.split('Tag')[0] == 'T'):
                text = TextTagConfig(name = i,
                description = self.tagDes[index],
                readOnly = False,
                arraySize = 0)
                self.CarDeviceConfig.textTagList.append(text)
            else:
                print("error")
        self.config.node.deviceList.append(self.CarDeviceConfig)
        self.CarEdgeAgent.uploadConfig(action = constant.ActionType[actions], edgeConfig = self.config)

    def car_on_connected(self,isConnected):
        print("connected")

    def car_on_disconnected(self,isDisconnect):
        print("disconnected")

    def car_on_message(self,agent, messageReceivedEventArgs):
        type = messageReceivedEventArgs.type
        message = messageReceivedEventArgs.message
        if type == constant.MessageType['WriteValue']:
            for device in message.deviceList:
                print('deviceId: {0}'.format(device.id))
            for tag in device.tagList:
                print('tagName: {0}, Value: {1}'.format(tag.name, str(tag.value)))
            if(device.id == "Device"+str(self.CarId)):
                self.update_data(self.DeviceId,tag.name,tag.value,'car')
        elif type == constant.MessageType['WriteConfig']:
            print('WriteConfig')
        elif type == constant.MessageType['TimeSync']:
        # message format: Model.Edge.TimeSyncCommand
            print(str(message.UTCTime))
        elif type == constant.MessageType['ConfigAck']:
        # message format: Model.Edge.ConfigAck
            print('Upload Config Result: {0}').format(str(message.result))

    def server_on_connected(self):
        print("connected")

    def server_on_disconnected(self):
        print("disconnected")

    def server_on_message(self):
        print("message")

    def get_connect(self):
        print("Start Connecting")
        self.CarEdgeAgent.connect()
        time.sleep(1)
        self.ServerEdgeAgent.connect()
        time.sleep(1)
        print("Finish Connecting")


    def get_disconnect(self):
        print("Start Disconnecting")
        self.CarEdgeAgent.disconnect()
        time.sleep(1)
        self.ServerEdgeAgent.disconnect()
        time.sleep(1)
        print("Finish Disconnecting")

    def update_data(self,id,TagId,data,des='car'):
        print("updating value")
        self.edgeData = EdgeData()
        tagD = EdgeTag(id,TagId,data)
        self.edgeData.tagList.append(tagD)
        self.edgeData.timestamp = datetime.datetime.now()
        if(des == 'car'):
            self.CarEdgeAgent.sendData(data=self.edgeData)
        elif(des == 'farm'):
            self.ServerEdgeAgent.sendData(data=self.edgeData)
        else:
            print("Wrong destination")
    
    def send_farm_temperature(self,id,temperature):
        self.update_data("Device"+str(id),'ATag1',temperature,'farm')

    def send_farm_humidity(self,id,humidity):
        self.update_data("Device"+str(id),'ATag2',humidity,'farm')

    def set_tag_val(self):
        for index,i in enumerate(self.tagId):
            self.update_data(self.DeviceId,self.tagId[index],self.default_tag_val[index],'car')
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json
from datetime import datetime, timedelta
import time
import threading

class messages():

    def __init__(self, lat, long, dateandtime = datetime(2023, 5, 11, 12, 36, 57, 643401), PublishingTopic= "hi", json_msg = {}, brokerip = '192.168.100.12' , frid = 'FR003', ToolID = 'LOC-SELF', sourceid = "FR001#FR") -> None:
        #self.tool = tool
        self.brokerip = brokerip
        self.frid = frid
        self.ToolID = ToolID
        self.PublishingTopic = PublishingTopic
        self.json_msg = json_msg
        self.PublishingTopic= 'fromtool-'+ self.ToolID.lower()
        self.client = mqtt.Client(self.ToolID)
        self.sourceid = sourceid
        self.lat = lat
        self.long = long
        self.dateandtime = dateandtime

    def create_json(self):
       # brokerip= '192.168.100.12' 
        if self.ToolID == 'LOC-SELF':
            #ToolName ='Visual based self-Localization'
            category = "VisualSelfLoc#FRLocation"
            extid = 'LOC-SELF_01'
            devicesourcetype = 'VisualSelfLoc'
            types = 'SelfLocData'
            #self.timediff = 2

        elif self.ToolID == 'LOC-IBL':
            #ToolName ='Inertial-Based Localisation'
            category = "INERTIO#LocationUpdate"
            extid = 'E4_01'
            devicesourcetype = 'InertioLoc'
            types = 'InrLocData'
            # self.dateandtime = self.dateandtime + timedelta(hours = self.timediff)

        elif self.ToolID == 'LOC-GLT':
            #ToolName ='Galileo based Localization'
            category = "GalileoLoc#FRLocation"
            extid = 'LOC-GLT_01'
            devicesourcetype = 'GalileoLoc'
            types = 'GalileoLocData'
            # self.dateandtime = self.dateandtime + timedelta(hours = self.timediff)


        #ToolID ='LOC-SELF'
        #self.PublishingTopic= 'fromtool-'+ self.ToolID.lower()
            
        self.json_msg= {}
        #self.json_msg['toolName'] = ToolName
        self.json_msg['toolID'] = self.ToolID
        self.json_msg['sourceID'] = self.sourceid
        self.json_msg['broadcast'] = True
                
        json_infoprioPayload = {}
        json_infoprioPayload['category'] = category
        self.dateandtime = self.dateandtime
        json_infoprioPayload['startTS'] = self.dateandtime.isoformat() 
        

        # json_location = {}
        # json_location['geometryType'] = 'Point'
        # json_location['coordinatePairs'] = [45.19567392091811, 6.667046347228574]
        # json_data['locationData'] = json_location

        # json_source = {}
        # json_source['extID'] = extid
        # json_source['frID'] = 'FR003'
        # json_source['deviceSourceType'] = devicesourcetype

        # json_indata={}
        # json_indata['type'] = types
        # json_indata['creationTS'] = self.dateandtime

        # json_indata['source'] = json_source

        json_tooldata={}
        json_tooldata['latitude'] = self.lat
        json_tooldata['longitude'] = self.long
        json_tooldata['heading'] = 0
        json_tooldata['altitude'] = 0
        json_tooldata['quality'] = 0
        json_tooldata['qualityHeading'] = 0
        json_tooldata['outdoor'] = True
        json_tooldata['mounting'] = "helmet"
        


        # json_relPos = {}
        # json_relPos['dx'] = 1.23
        # json_relPos['dy'] = 1.23
        # json_relPos['dz'] = 1.23
        # json_relPos['dyaw'] = 1.23
        # json_relPos['dpitch'] = 1.23
        # json_relPos['droll'] = 1.23
        # json_tooldata['rel_pos'] = json_relPos

        #json_indata['toolData'] = [json_tooldata]

        #json_includedData = [json_indata] 
        #json_data['toolPayload'] = json_includedData
        json_infoprioPayload['toolData'] =  [json_tooldata]    
        self.json_msg['infoprioPayload'] = json_infoprioPayload
        self.json_msg = json.dumps(self.json_msg) 
        return self.json_msg, self.dateandtime


    #mqtt_qos = 0
    def publish(self):
        msg_count = 0
        #while True:
        #for i in range(2):
        time.sleep(10)
        msg = f"messages: {msg_count}"
        result = self.client.publish(self.PublishingTopic, self.create_json(), qos = 0)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{self.PublishingTopic}`")
        else:
            print(f"Failed to send message to topic {self.PublishingTopic}")
        msg_count += 1


    def run(self):
        #client = mqtt.Client(self.ToolID)
        self.client.connect(self.brokerip)
        #self.client.loop_start()
        self.publish()
        #self.client.loop_stop()

    def publish_message(self):
        # Create a new MQTT client
        client = mqtt.Client(self.ToolID)

        # Connect to the MQTT broker
        client.connect('192.168.100.12')

        # Publish the message to the specified topic
        client.publish(self.PublishingTopic, self.create_json()[0])

        # Disconnect from the MQTT broker
        client.disconnect()

    def threads(self, lat, long, visual_timediff, inertio_timediff, galileo_timediff):
        lat = [0,1,2]
        long = [0,1,2]
        mqtt_visual = []
        mqtt_inertio = []
        mqtt_galileo = []
        mess_visual = []
        mess_inertio = []
        mess_galileo = []
        date_visual = self.dateandtime
        date_inertio = self.dateandtime
        date_galileo = self.dateandtime
        #dateandtime = datetime(2023, 5, 11, 12, 36, 57, 643401)
        # d = datetime(2023, 5, 11, 12, 36, 57, 643401)
        # t_visual = timedelta(seconds = 10)
        # t_inertio = timedelta(seconds = 20)
        # t_galileo = timedelta(seconds = 30)
        for i in range(len(lat)):
        # timediff = 0
        # dateandtime = dateandtime + timedelta(hours = timediff)

            # d_galileo = d + t_galileo
            mqtt_visual.append(messages(ToolID = 'LOC-SELF', lat = lat[i], long = long[i],  dateandtime = date_visual))
            mess_visual.append([(mqtt_visual[i].PublishingTopic, mqtt_visual[i].create_json())])
            #self.dateandtime = self.dateandtime + timedelta(seconds = self.timediff)
            mqtt_inertio.append(messages(ToolID = 'LOC-IBL', lat = lat[i], long = long[i],  dateandtime = date_inertio))
            mess_inertio.append([(mqtt_inertio[i].PublishingTopic, mqtt_inertio[i].create_json())])
            #self.dateandtime = self.dateandtime + timedelta(seconds = self.timediff)
            mqtt_galileo.append(messages(ToolID = 'LOC-GLT', lat = lat[i], long = long[i],  dateandtime = date_galileo))
            mess_galileo.append([(mqtt_galileo[i].PublishingTopic, mqtt_galileo[i].create_json())])
            date_visual = date_visual + timedelta(seconds = visual_timediff)
            date_inertio = date_inertio + timedelta(seconds = inertio_timediff)
            date_galileo  = date_galileo + timedelta(seconds = galileo_timediff)
            #self.dateandtime = self.dateandtime + timedelta(seconds = self.timediff)



        # Define your messages and topics
            # mess = [
            #     (mqtt_visual[i].PublishingTopic, mqtt_visual[i].create_json()),
            #     (mqtt_inertio[i].PublishingTopic, mqtt_inertio[i].create_json()),
            #     (mqtt_galileo[i].PublishingTopic, mqtt_galileo[i].create_json())
            # ]
            
            
            
        #mqttc.run()
        #mqttc1.run()

        # Publish messages using multiple threads
            threads_visual = []
            threads_inertio = []
            threads_galileo = []
            
        for i in range(len(lat)):
            for topic, message in mess_visual[i]:
                t_visual = threading.Thread(target=mqtt_visual[i].publish_message(), args=(topic, message))
                #time.sleep(10)

            for topic, message in mess_inertio[i]:
                t_inertio = threading.Thread(target=mqtt_inertio[i].publish_message(), args=(topic, message))
                #time.sleep(10)

            for topic, message in mess_galileo[i]:
                t_galileo = threading.Thread(target=mqtt_galileo[i].publish_message(), args=(topic, message))
                #time.sleep(10)

                threads_visual.append(t_visual)
                threads_inertio.append(t_inertio)
                threads_galileo.append(t_galileo)
        t_visual.start()
        t_inertio.start()
        t_galileo.start()

            # Wait for all threads to complete
            # for t in threads:
            #     t.join()

            # All messages published
        print("All messages published.")
        #return self.timediff

th = messages(dateandtime = datetime(2023, 5, 11, 12, 36, 57, 643401), lat = 1, long = 1)
th.threads(lat = [0,1,2], long = [0,1,2], visual_timediff=1, inertio_timediff=2, galileo_timediff=3)
            # if __name__ == '__main__':
            #     run()

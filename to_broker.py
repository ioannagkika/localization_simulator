import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json
from datetime import datetime, timedelta
import time
import threading
import numpy as np

class messages():

    def __init__(self, lat = 1, long = 1, dateandtime = datetime(2023, 5, 11, 12, 36, 57, 643401), 
                 PublishingTopic= "hi", json_msg = {}, brokerip = '192.168.100.12' , frid = 'FR003', ToolID = 'LOC-SELF', 
                 sourceid = "FR001#FR", quality = None, quality_heading = None, outdoor = None, mounting = "helmet") -> None:
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
        self.quality = quality
        self.quality_heading = quality_heading
        self.outdoor = outdoor
        self.mounting = mounting
    

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
        json_tooldata['quality'] = self.quality
        json_tooldata['qualityHeading'] = self.quality_heading
        json_tooldata['outdoor'] = self.outdoor
        json_tooldata['mounting'] = self.mounting
        


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
        return self.json_msg #, self.dateandtime


    # #mqtt_qos = 0
    # def publish(self):
    #     msg_count = 0
    #     #while True:
    #     #for i in range(2):
    #     time.sleep(10)
    #     msg = f"messages: {msg_count}"
    #     result = self.client.publish(self.PublishingTopic, self.create_json(), qos = 0)
    #     # result: [0, 1]
    #     status = result[0]
    #     if status == 0:
    #         print(f"Send `{msg}` to topic `{self.PublishingTopic}`")
    #     else:
    #         print(f"Failed to send message to topic {self.PublishingTopic}")
    #     msg_count += 1


    # def run(self):
    #     #client = mqtt.Client(self.ToolID)
    #     self.client.connect(self.brokerip)
    #     #self.client.loop_start()
    #     self.publish()
    #     #self.client.loop_stop()

    # def publish_message(self):
    #     # Create a new MQTT client
    #     client = mqtt.Client(self.ToolID)

    #     # Connect to the MQTT broker
    #     client.connect('192.168.100.12')

    #     # Publish the message to the specified topic
    #     client.publish(self.PublishingTopic, self.create_json()[0])

    #     # Disconnect from the MQTT broker
    #     client.disconnect()

    def threads_visual(self, visual_latitude, visual_longitude, visual_timediff, sourceid, brokerip):
        mqtt_visual = []
        mess_visual = []
        date_visual = self.dateandtime
        for i in range(len(visual_latitude)):
            mqtt_visual.append(messages(ToolID = 'LOC-SELF', lat = visual_latitude[i], long = visual_longitude[i],  
                                        dateandtime = date_visual, sourceid = sourceid, brokerip=brokerip))
            mess_visual.append([(mqtt_visual[i].create_json())])
            date_visual = date_visual + timedelta(seconds = visual_timediff)
            # threads_visual = []
        mess_visual = (mqtt_visual[0].PublishingTopic, mess_visual, visual_timediff)
        # for i in range((len(visual_latitude))):
        #     for topic, message in mess_visual[i]:
        #         t_visual = threading.Thread(target=mqtt_visual[i].publish_message(), args=(topic, message))
        #         time.sleep(visual_timediff)
        #         # threads_visual.append(t_visual)
        return mess_visual
        #t_visual.start()
        
        

########################################################################################

    def threads_inertio(self, inertio_latitude, inertio_longitude, inertio_timediff, sourceid, brokerip):
        mqtt_inertio = []
        mess_inertio = []
        date_inertio = self.dateandtime
        for i in range(len(inertio_latitude)):
            mqtt_inertio.append(messages(ToolID = 'LOC-IBL', lat = inertio_latitude[i], long = inertio_longitude[i],  
                                         dateandtime = date_inertio, sourceid=sourceid, brokerip = brokerip,
                                         quality=1.23456, mounting=None))
            mess_inertio.append([(mqtt_inertio[i].create_json())])
            date_inertio = date_inertio + timedelta(seconds = inertio_timediff)
            # threads_inertio = []
        mess_inertio = (mqtt_inertio[0].PublishingTopic, mess_inertio, inertio_timediff)
        # for i in range((len(inertio_latitude))):
        #     for topic, message in mess_inertio[i]:
        #         t_inertio = threading.Thread(target=mqtt_inertio[i].publish_message(), args=(topic, message))
        #         time.sleep(inertio_timediff)
        #         # threads_inertio.append(t_inertio)
        return mess_inertio
        #t_visual.start()
        #t_inertio.start()
########################################################################################

    def threads_galileo(self, galileo_latitude, galileo_longitude, galileo_timediff, sourceid, brokerip):
        mqtt_galileo = []
        mess_galileo = []
        date_galileo = self.dateandtime
        for i in range(len(galileo_latitude)):
            mqtt_galileo.append(messages(ToolID = 'LOC-GLT', lat = galileo_latitude[i], long = galileo_longitude[i],  
                                         dateandtime = date_galileo, sourceid=sourceid, brokerip = brokerip,
                                         quality=1.23456, quality_heading = 0, outdoor=True))
            mess_galileo.append([(mqtt_galileo[i].create_json())])
            date_galileo = date_galileo + timedelta(seconds = galileo_timediff)
            # threads_galileo = []
        mess_galileo = (mqtt_galileo[0].PublishingTopic, mess_galileo, galileo_timediff)
        # for i in range((len(galileo_latitude))):
        #     for topic, message in mess_galileo[i]:
        #         t_galileo = threading.Thread(target=mqtt_galileo[i].publish_message(), args=(topic, message))
        #         time.sleep(galileo_timediff)
        #         # threads_galileo.append(t_galileo)
        return mess_galileo
        #t_galileo.start()

  

    #def publish_message(self, topic, message):
    #    # Create a new MQTT client
    #    client = mqtt.Client(self.ToolID)
    #
    #    # Connect to the MQTT broker
    #    client.connect(self.brokerip)
    #
    #    # Publish the message to the specified topic
    #    client.publish(topic, message[0], qos= 0)
    #
    #    # Disconnect from the MQTT broker
    #    client.disconnect()

    def publish_messages_with_delay(self, topic, message_list, delay, progress):
        client = mqtt.Client(topic)
        client.connect(self.brokerip)
    
        for index in range(len(message_list)):
            message = message_list[index][0]
            progress[topic] = float(index+1) / len(message_list)
            t_begin = datetime.now()
            # Edo mporeis na antikatastiseis tin ora pou eixe me tin t_begin
            client.publish(topic, message, qos= 0)
            time.sleep(delay - (datetime.now()-t_begin).seconds)

        client.disconnect()

    # Publish messages with delays using multiple timers
    def otinanai(self, messages, progress_button, windowclass):
        print("Begun sending messages!")

        progress = {}

        for topic, message_list, delay in messages:
            timer = threading.Timer(0, self.publish_messages_with_delay, args=(topic, message_list, delay, progress))
            timer.start()

        min_progress = 0.0
        while min_progress < 1.0:
            progress_list = list(progress.values())
            min_progress = np.min(progress_list) if len(progress_list) > 0 else 0

            progress_button.configure(text= str(int(min_progress * 100)) + "%")
            windowclass.update()

            #callback(min_progress)
            # self.progress_button = customtkinter.CTkLabel(master=self.frame_left, width = 20, height = 20, text=broker_messages.min_progress)
            # self.progress_button.grid(pady=(10, 0), padx=(5, 5), row=13, column=0)
            #print(str(self.min_progress * 100) + "%")
            # update to GUI element
        print("All messages published!")



        # Wait for all timers to complete
        # for timer in timers:
        #     timer.join()

        # All messages published


# broker_messages = messages()
# broker_messages.otinanai()




            # Wait for all threads to complete
            # for t in threads:
            #     t.join()

            # All messages published
        #print("All messages published.")
        #return self.timediff


            # if __name__ == '__main__':
            #     run()
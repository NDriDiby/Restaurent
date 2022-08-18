import json
from channels.generic.websocket import WebsocketConsumer
  
class SendOrderToKitchen(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.send(text_data=json.dumps({
            'type':'connection established',
            'message':'you are now connected!'
        }))
        
  
    def disconnect(self, close_code):
        self.close()
        
  
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
        print('Client Message:',message)
        
        self.send(text_data=json.dumps({
            'type':'send order',
            'message': message
        }))
        
        
        
  
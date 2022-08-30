import json
from asgiref.sync import async_to_sync
from asgiref.sync import sync_to_async
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from . models import Order
from datetime import datetime,timedelta,time
from django.utils import timezone
from channels.db import database_sync_to_async

today = timezone.localtime(timezone.now()).date()
  
class SendOrderToKitchen(WebsocketConsumer):
    def connect(self):
        
        self.room_group_name = 'uncompleted-order'
        
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
       
        self.accept()
        
         # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': self.room_group_name 
        }))
        
  
    def disconnect(self, close_code):
         # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        
  
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
        
        # Message from client
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {  'type': 'order_status',
                'message': message,
            }
        )
        print('Client said:',text_data_json)
        
        
        
        
        
    #  Send message to client
   
    def order_status(self, event):
        message = event['message']
        
       
        
        #Uncompleted Order
        uncompleted_order =  Order.objects.filter(status='Sent',date_ordered__date = today).order_by('date_ordered')
        
        current_time = datetime.strftime(datetime.today().now(),'%H:%M')
        current_time= datetime.strptime(current_time,'%H:%M')
        
        uncompleted = list()
        for order in range(0,len(uncompleted_order)):
            
            order_date = datetime.strftime(uncompleted_order[order].date_ordered,'%H:%M')
            #order_date= datetime.strptime(order_date,'%H:%M')
            
            #time_since = current_time - order_date
            data = {
                'order_id':uncompleted_order[order].id,
                'order_table':uncompleted_order[order].table,
                'order_name':uncompleted_order[order].customer.full_name(),
                'order_date':order_date,
                'transaction_id':uncompleted_order[order].transaction_id,
                'order_item':[],
                'side_orderitem':[],
            }
            
            # data['order_date'] = datetime.strftime(data['order_date'],'%H:%M')
        #    datetime.strftime(uncompleted_order[order].date_ordered,'%H:%M')
            # print('DateOrdered:',current_time)
            # print('DateOrdered_since:',time_since)
            # print(order_date)
            
            #ORDER ITEM
            all_orderitem = uncompleted_order[order].orderitem_set.all()
            for orderitem in range(0,len(all_orderitem)):
                if data['order_id'] == all_orderitem[orderitem].order.id:
                    orderItem = {
                    'order_id':all_orderitem[orderitem].order.id,
                        'orderItem_id':all_orderitem[orderitem].id,
                    'order':all_orderitem[orderitem].customer.user.first_name +" "+ all_orderitem[orderitem].customer.user.last_name,
                        'item':all_orderitem[orderitem].item.name,
                        'quantity':all_orderitem[orderitem].quantity,
                    }
                    
                    if all_orderitem[orderitem].ingredient:
                        orderItem['ingredient'] = all_orderitem[orderitem].ingredient
                        
                    if all_orderitem[orderitem].accompagnememt:
                        for accomp in all_orderitem[orderitem].accompagnememt.all():
                            
                            orderItem['accompagnement'] = list(all_orderitem[orderitem].accompagnememt.values_list('name',flat=True))
                            
                    if all_orderitem[orderitem].supplement:
                        for sup in all_orderitem[orderitem].supplement.all():
                            orderItem['supplement'] = list(all_orderitem[orderitem].supplement.values_list('name',flat=True))
                            
                        
                    data['order_item'].append(orderItem)
            
            # SIDE ORDER ITEM
            if uncompleted_order[order].sideorderitem_set.all():
                all_side = uncompleted_order[order].sideorderitem_set.all()
                for side in range(0,len(all_side)):
                    if data['order_id'] == all_side[side].order.id:
                        my_side = {
                            'order_id':all_side[side].order.id,
                            'name':all_side[side].item.name,
                            'quantity':all_side[side].quantity,
                        }
                
                        data['side_orderitem'].append(my_side)
                        
            
            uncompleted.append(data)
            
       
        # Send message to Client
        self.send(text_data=json.dumps({
            'message': message,
            'type':'order_sent',
            'uncompleted_order': list(uncompleted)
        }))
        
        
        
  
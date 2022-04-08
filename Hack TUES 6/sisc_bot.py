import os
from fbchat import log, Client
from fbchat.models import *
 
FB_SEND = True
FB_USER = 'sisc.elsys@gmail.com'
FB_PASS = '******'

class EchoBot(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        self.markAsDelivered(thread_id, message_object.uid)
        self.markAsRead(thread_id)
 
        log.info("{} from {} in {}".format(message_object, thread_id, thread_type.name))
 
        msgText=message_object.text
        
        if(msgText.upper() == "START"):
            reply="Starting the programme..."
            os.system("systemctl start sisc.service")
        elif(msgText.upper()=="STOP"):
            reply="Stopping the programme..."
            os.system("systemctl stop sisc.service")
        elif(msgText.upper()=="HELP"):
            reply="Commands:\nStart\n\t-start the progamme\nStop\n\t-stop the programme"
        else:
            reply="Invalid command. Type 'Help' for more information."
        
        if author_id != self.uid:
            self.send(Message(text=reply), thread_id=thread_id, thread_type=thread_type)

client = EchoBot(FB_USER, FB_PASS)
client.listen()

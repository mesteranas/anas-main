from threading import Thread
from plyer import notification
from settings import app
def SendNotification1(title,text,time):
	notification.notify(title=title,message=text,app_name=app.name, timeout=time)
def SendNotification(title,text,time):
	Thread(target=SendNotification1,args=[title,text,time]).start()
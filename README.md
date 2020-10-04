









*SISC*

**S**ystem **I**nteligent **S**ecurity **C**amera


Used information:
            
            
https://gilberttanner.com/blog/yolo-object-detection-with-opencv

https://fbchat.readthedocs.io/en/latest/index.html

https://github.com/punkjj/FB-AutoReply


To run the services, do:
1. Copy to /lib/systemd/system/sisc.service
2. Type the commands: 
> systemctl enable sisc.service
> systemctl start sisc.service
                      
                      
Useful commands:
1. Super user + pass (su)
2. systemctl start sisc_bot.service
3. systemctl status sisc_bot.service (to watch the actions)
4. systemctl enable sisc_bot.service (to start the service with the Raspberry Pi)
5. systemctl disable sisc_bot.service (to NOT start the service with the Raspberry Pi)
6. systemctl stop sisc_bot.service
7. python3 sisc.py **MAIN COMMAND FOR STARTING THE PROGRAMME**

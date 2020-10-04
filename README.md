









*SISC*
            **S**ystem **I**nteligent **S**ecurity **C**amera
            Used information:
https://gilberttanner.com/blog/yolo-object-detection-with-opencv
https://fbchat.readthedocs.io/en/latest/index.html
https://github.com/punkjj/FB-AutoReply

*To run the services, do:
> Copy to /lib/systemd/system/sisc.service
> Type the commands: systemctl enable sisc.service
                      systemctl start sisc.service
*Useful commands:
> Super user + pass (su)
> systemctl start sisc_bot.service
> systemctl status sisc_bot.service (to watch the actions)
> systemctl enable sisc_bot.service (to start the service with the Raspberry Pi)
> systemctl disable sisc_bot.service (to NOT start the service with the Raspberry Pi)
> systemctl stop sisc_bot.service
> python3 sisc.py **MAIN COMMAND FOR STARTING THE PROGRAMME**

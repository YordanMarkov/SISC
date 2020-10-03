https://gilberttanner.com/blog/yolo-object-detection-with-opencv
https://fbchat.readthedocs.io/en/latest/index.html

copy to /lib/systemd/system/sisc.service
systemctl enable sisc.service
systemctl start sisc.service

# run sisc with nice because of the slow processing
sudo nice -n -20 python3 sisc.py

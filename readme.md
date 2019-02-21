# Ecomed

## Environment
1.	install tensorflow   
	```pip3 install tensorflow```
2.	install opencv  
	```pip3 install python_opencv```
3.	install some dependicies for opencv, according to [this](https://github.com/amymcgovern/pyparrot/issues/34) link.  
4. 	install some lacked libraries according to the terminal link
5.	install the library of `models` with git
	there is no models after the update of tensorflow, which lead us cannot import label_map_util
6.	install `protobuf` can use it to compile `models`, according to this [link](https://github.com/EdjeElectronics/TensorFlow-Object-Detection-on-the-Raspberry-Pi/blob/master/README.md)
7. 	download the pretrained model `ssdlite_mobilenet_v2_coco_2018_05_09.tar.gz` from the above link
8.	modify the version of the modules like numpy  
```pip3 install numpy==1.15.4```

## Establish
* The `camera_control.py` needs to be put into `/home/pi/Ecomed/object_detection`
* The other scripts can be put into `/home/pi/Ecomed`

## Run the Demo
1. Use the following command to log into our raspberry pi  
```ssh pi@10.19.109.82```  
password: ecomed

2. Go to the following directory  
```cd Ecomed/object_detection```

3. Use the following command to run the script  
```xvfb-run python3 camera_control.py```

## Data Collection
* In order to collect the data, just run the script of `data_collection.py`, if you use ssh to connect the pi, use the following command  
```xvfb-run python3 data_collection.py``` 
* In order to see the image you collect, type the command of   
```python -m SimpleHTTPServer``` on your pi, 
then you can open your brower and type `10.19.109.82:8000` to see the images

## Deploy the model to raspberry pi
In order to use tensorflow-lite
```
rm -rf  /home/pi/.local/lib/python3.5/site-packages/tensorflow
sudo pip3 uninstall tensorflow
git clone https://github.com/PINTO0309/Tensorflow-bin.git
cd Tensorflow-bin
sudo pip3 install tensorflow-1.11.0-cp35-cp35m-linux_armv7l.whl
```
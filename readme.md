# Ecomed

## Environment
* install tensorflow  
~~`pip3 install tensorflow`~~
	* In order to use the tensorflow-lite in raspberry pi, we need to install a specific version of tensorflow
```
rm -rf  /home/pi/.local/lib/python3.5/site-packages/tensorflow  
sudo pip3 uninstall tensorflow  
git clone https://github.com/PINTO0309/Tensorflow-bin.git
cd Tensorflow-bin
sudo pip3 install tensorflow-1.11.0-cp35-cp35m-linux_armv7l.whl  
```
	* In order to use the tensorflow-lite in raspberry pi, we need to install a specific version of tensorflow  
```
	rm -rf  /home/pi/.local/lib/python3.5/site-packages/tensorflow  
	sudo pip3 uninstall tensorflow  
	git clone https://github.com/PINTO0309/Tensorflow-bin.git
	cd Tensorflow-bin
	sudo pip3 install tensorflow-1.11.0-cp35-cp35m-linux_armv7l.whl  
```
* install opencv  
```pip3 install python_opencv```
* install some dependicies for opencv, according to [this](https://github.com/amymcgovern/pyparrot/issues/34) link 
* install some lacked libraries according to the terminal showing
* install the library of `models` with git
	* install `protobuf` can use it to compile `models`, according to this [link](https://github.com/EdjeElectronics/TensorFlow-Object-Detection-on-the-Raspberry-Pi/blob/master/README.md)
	* install `models` with git
* download the pretrained model `ssdlite_mobilenet_v2_coco_2018_05_09.tar.gz` from the above link
* modify the version of the modules like numpy  
```pip3 install numpy==1.15.4```

## Connect to the Pi
1. Use the following command to log into our raspberry pi  
`ssh pi@10.19.109.82`  
password: `ecomed`
2. Go to the following directory  
```cd Ecomed```
3. When you connect to the Pi from remote machine, you need to add `xvfb-run` before the command because some script contains image showing code, however there is no screen connecting to it.

## Data Collection
* In order to collect the data, just run the script of `data_collection.py`, if you use ssh to connect the pi, use the following command  
```xvfb-run python3 data_collection.py```

* In order to see the image you collect, type the command of
```python -m SimpleHTTPServer``` on your pi, 
then you can open your brower and type `10.19.109.82:8000` to see the folders

## Model Training
* We use the MobileNetV2 model to train the data, and we can get a about 0.98 accuracy on the validation dataset, then we saved the model as a `.h5` file
* We then use tensorflow-lite to transfer the model to a `.tflite` model
* We use the MobileNetV2 model to train the data, and we can get a about 0.98 accuracy on the validation dataset, then we saved the model as a .h5 file
* We then use tensorflow-lite to transfer the model to a .tflite model
* Copy that model file to the Pi

## Run the Demo
Just run the script of `main.py`. However, we haven't finished the detecting code in real machine, so we need to go to the folder `~/Ecomed/object_detection` and run the following script
```xvfb-run python3 camera_control.py```


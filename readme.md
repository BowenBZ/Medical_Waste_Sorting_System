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
`ssh pi@10.19.2.71`  
password: `ecomed`
2. Go to the following directory  
```cd Ecomed```
3. When you connect to the Pi from remote machine, you need to add `xvfb-run` before the command because some script contains image showing code, however there is no screen connecting to it.

## Data Collection
* In order to collect the data, just run the script of `data_collection.py` in the folder of `Ecomed`
	* if you use ssh to connect the pi, use the following command
	```xvfb-run <-a> python3 data_collection.py```
	* the scene will let you input the name of the categories first, you can use a new name or a preexisted name
	* when the window show the images of the scene, if you press `s`, you can save one image into the disk
	* when you want to quit, just press `q` or use `ctrl+c`
	* when you press `r`, you can delete the image one by one

* In order to see the image you collect, type the command of
```python -m SimpleHTTPServer``` on your pi, 
then you can open your brower and type `10.19.2.71:8000` to see the folders

## Model Training
### Model Structure
* We use MobileNet model to do the transfer learning. 
	* Load the pretrained MobileNet model
	* Add several new layers
* Optimizer uses `tf.train.GradientDescentOptimizer(0.001)`
* Batch Size of data is `24`
* Epoch is around `60`

### Model Transfer
* Save model 
	* We use the command `tf.contrib.saved_model.save_keras_model()` to save the model after the epoches stops
	* We encountered some problem when using the method of callbacks to save model. Because 
		* when we use `tf.keras.SGD` to be the optimizer, we cannot load the saved file later. The command line said we should use `tf.train.optimizer` to be the optimizer
		* when we use `tf.train.GradientDescentOptimizer` to be the optimizer, the command line said we cannot save the optimizer...
* Load model
	* We use the command `tf.contrib.saved_model.load_keras_model()` to load model
* Transfer model
	* We have a `.h5` file at the beginning
	* We use tensorflow-lite to transfer the model to a `.tflite` model
	* Copy that model file to the Pi

## Step Motor
* 48 Steps is one cycle when the step motor is in the full mode.
* 1.6 second is one cycle when the step motor is in the 1/4 mode and the PWM frequency is 500, dutycycle is 128(0.5 up and 0.5 down)

## Run the Demo
Just run the script of `main.py`. However, we haven't finished the detecting code in real machine, so we need to go to the folder `~/Ecomed/object_detection` and run the following script
```xvfb-run python3 camera_control.py```

## Reference
[1] [Step motro](https://www.rototron.info/raspberry-pi-stepper-motor-tutorial/)
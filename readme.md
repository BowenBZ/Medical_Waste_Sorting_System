# Ecomed
This is the code for the project Ecomed. Our team want to design an automatic sorting garbage can which can classify different kinds of medical waste. The system is running in the Raspberry Pi.
![bin](https://drive.google.com/uc?id=1ce8hs5vJlcS4FhH1EZBe9S4C-XYOIA_e)

For now, we can classify 4 different conditions. Background, pharmaceutical, sharps and trace_chemo.
![waste](https://drive.google.com/uc?id=1nffkzQaLITJcL3fCN74owO1DK0tvwjDl)

## Environment in Raspberry PI
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
* install opencv  
```pip3 install opencv_python```
* install some dependicies for opencv, according to [this](https://github.com/amymcgovern/pyparrot/issues/34) link 
* install some lacked libraries according to the terminal showing


## Software - Deep Learning Model
### Data Collection
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


### Model Structure
* We use MobileNet model to do the transfer learning. 
	* Load the MobileNet model with weights pretrained on ImageNet dataset
	* Add several new layers  

The model structure is as follows:
![model](https://drive.google.com/uc?id=1btF4N7jDOC1FwZG9lP1EgORACcuVd75H)

* Optimizer uses `tf.train.GradientDescentOptimizer(0.001)`
* Batch Size of data is `6`
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
	* We use the following commands in tensorflow-lite to transfer the model to a `.tflite` model
	```
	converter = tf.contrib.lite.TFLiteConverter.from_saved_model(model_path)
	tflite_model = converter.convert()
	open(tflite_model_path, "wb").write(tflite_model)
	```
	* Copy that model file to the Pi

## Hardware
![overview](https://drive.google.com/uc?id=1jYNp0b0qVclo1yoNszAvLSC2zM0j5qFy)

### Raspberry Pi - 3B+
We used `Raspberry Pi 3b+` to do our project. In order to connect to the Pi
1. Use the following command to log into our raspberry pi  
`ssh pi@10.19.2.71`  
password: `ecomed`
Note: the ip of the raspberry pi was set to a static ip, so the ip won't change. There is a small bug which lead the raspberry pi cannot surf on the Internet, but you can still use `scp`, `ssh` commands to log into the raspberry pi
2. Go to the following directory  
```cd Ecomed```
3. When you connect to the Pi from remote machine, you need to add `xvfb-run` before the command because some script contains image showing code, however there is no screen connecting to it.

### Pi Camera - 5MP OV5647
We used the Pi Camera with wide angle of 175 degree and night vision `5MP OV5647`

### Step Motor - 17HS4401A
* 48 Steps is one cycle when the step motor is in the full mode.
* 1.6 second is one cycle when the step motor is in the 1/4 mode and the PWM frequency is 500, dutycycle is 128(0.5 up and 0.5 down)

### Servo Motor - LD 27MG
* The servo motor needs a PWM with the frequency of 50Hz because the servo motor is controled by the PWM every 20 ms.   
* If the pulse for high is 0.5 ms (duty cycle: 2.5%), the servo angle will be 0;
* If the pulse for high is 2.5 ms (duty cycle: 12.5%), the servo angle will be 270.

## Run the Demo
* Connect the circuit and charge the Raspberry Pi
* Type command ```sudo pigpiod```
* Go to the folder `Ecomed` with command `cd Ecomed`
* Use command `xvfb-run python3 main.py` to run the processing

## Reference
[1] [Step motor](https://www.rototron.info/raspberry-pi-stepper-motor-tutorial/)

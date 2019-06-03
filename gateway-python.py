#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import bluetooth
import os
import time
import signal

#BLE Comunication
bd_addr ="00:21:13:05:E1:45"
port = 1
sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM )
sock.connect((bd_addr,port))

#Handler Funtion
def Send_Code(code):
	sock.send(code)
	time.sleep(.02)
def Get_Lux():
	for i in range(5):
			Send_Code("e")
			lux=str(sock.recv(1024))
			time.sleep(.1)
	return lux[2:8]
def Change_PWM(inc_or_dec,dest):
	if inc_or_dec=="1":
		for i in range(255):
			Send_Code("c")
			value=Get_Lux()
			if value>dest:
				return
	elif inc_or_dec=="0":
		for i in range(255):
			Send_Code("d")
			value=Get_Lux()
			if value<dest:
				return
		client.publish("tranglc","Alex: Ánh sáng bên ngoài quá cao. Bạn hãy đóng bớt của sổ đi nhé!")
def Setting_Mode(min_lux,mid_lux,max_lux):
	value=Get_Lux()
	if value<min_lux:
		Change_PWM("1",mid_lux)
	elif value>max_lux:
		Change_PWM("0",mid_lux)
def LED_Handler(mode):
	if mode=="b'dosang'":
		kill_process()
		value=Get_Lux()
		client.publish("tranglc","Độ sáng hiện tại: "+value)
	elif mode=="b'tat'":
		kill_process()
		sock.send("a")
		client.publish("tranglc","Đã tắt")
	elif mode=="b'bat'":
		kill_process()
		sock.send("b")
		client.publish("tranglc","Đã bật với độ sáng lớn nhất")
	elif mode=="b'docsach'":
		kill_process()
		child_process("000350","000375","000400")
		client.publish("tranglc","Alex: Mọi thứ đã sẵn sàng. Đọc sách thôi nào :3")
	elif mode=="b'xemphim'":
		kill_process()
		child_process("000150","000175","000200") 
		client.publish("tranglc","Alex: Mọi thứ đã sẵn sàng. Xem phim thôi nào :3")
	elif mode=="b'giaitri'":
		kill_process()
		child_process("000250","000275","000300") 
		client.publish("tranglc","Alex: Mọi thứ đã sẵn sàng. Giải trí thôi nào :3")
	elif mode=="b'ngu'":
		kill_process()
		child_process("000050","000075","000100")
		client.publish("tranglc","Alex: Mọi thứ đã sẵn sàng. Chúc bạn ngủ ngon :3")		

#Child process
with open("log.txt",'w') as log:
	log.write('-1')
	log.close()
def child_process(min_lux,mid_lux,max_lux):
	try:
	    pid = os.fork()
	except OSError:
	    exit("Could not create a child process")
	if pid == 0:
		with open("log.txt",'w') as log:
				log.write(str(os.getpid()))
				log.close()
		while True:
			Setting_Mode(min_lux,mid_lux,max_lux)
def kill_process():
	with open("log.txt",'r') as data:
		id_process=int(data.read())
		data.close()
	print(id_process)
	if int(id_process)>int('0'):
		print(id_process)
		os.kill(id_process,signal.SIGTERM)	
# Callbacks
def on_connect(client,userdata,flags,rc):
	print("Connected with Code:" + str(rc))
	# Subscribe Topic
	client.subscribe("tranglc/#",qos=0)

def on_message(client,userdata,msg):
	message=str(msg.payload)
	print(message)
	LED_Handler(message)
# This is the Publisher

client = mqtt.Client()
client.on_connect=on_connect
client.on_message=on_message

client.connect("m16.cloudmqtt.com",12615,60)
client.username_pw_set("qnqbhzyl","agzedLO5Jdqo")

client.loop_forever()
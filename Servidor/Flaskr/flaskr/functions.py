import os
import servidorConf as sc
import time
import threading
import subprocess
import shutil

def empaquetar():
	tamLog = os.path.getsize(sc.logDir)
	print "Tamanio log "+ str(tamLog)
	if tamLog > 1000000:
		os.system('tar czvf Log/log.tar.gz '+sc.logDir)
		print "Empaquetado"
		os.system('rm '+ sc.logDir)
		 
def send(message,ser):
	response=""
	if message != 'G' and message != 'V':
		response = "&#"
	if message == 'G':
		response=="&G"
	if sc.board==1:
		message='&'+message+'#'
		ser.write(message)
		t2 = threading.Timer(0.5, alarma)
	        t2.daemon=True
	        t2.start()
	        sArduino =str(ser.readline())
	        sArduino = sArduino[0:-2]
	        if response in sArduino:
	                with open(sc.logDir, 'a') as file_:
	                        file_.write(message+" "+sArduino+" "+time.strftime("%H:%M:%S")+" "+ time.strftime("%d/%m/%Y") + "\n")
	                        file_.close()
	
	                t2.cancel()


def cameraServer():
	os.chdir(sc.mjpgDir)
        print('Video streaming starting on pid ',  os.getpid())
        os.system('./mjpg_streamer -i "./input_uvc.so -d /dev/video0 -r 320x240" -o "./output_http.so -w ./www" ')	
	#os.system('./mjpg_streamer -i "./input_uvc.so -d /dev/video0 -r 160x120 -y" -o "./output_http.so -w ./www"')
	#os.system('./mjpg_streamer -i "./input_uvc.so -r 320x240 -y" -o "./output_http.so -w ./www"')

def checkRoutine(ser):
	send('G',ser)
	t = threading.Timer(5.0, checkRoutine, [ser])
	t.daemon = True
	t.start()

        
	

def test(ser):     
	ser.write("&G#")
	t2 = threading.Timer(0.5, alarma)
	t2.daemon=True
	t2.start()	
	sArduino =str(ser.readline())
	sArduino = sArduino[1:-3]
	if 'GLS' in sArduino:
		with open('log.txt', 'a') as file_:
    			file_.write(sArduino+" "+time.strftime("%H:%M:%S") + "\n")
			file_.close()
					
		t2.cancel()
	
def alarma():
	with open(sc.logDir, 'a') as file_:
        	file_.write("Alarma"+" "+time.strftime("%H:%M:%S") + "\n")
        	file_.close()
	
	



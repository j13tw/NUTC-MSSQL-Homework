#!/usr/bin/python3.6
import pymssql
import requests
import json
import os, sys
import socket
import time
from decimal import getcontext, Decimal

ups_Life_A = ''
serialName_A = ''
systemMode_A = 0
inputLine_A = 0
inputFreq_A = 0
inputVolt_A = 0
outputLine_A = 0
outputFreq_A = 0
outputVolt_A = 0
outputWatt_A = 0
outputAmp_A = 0
outputPercent_A = 0
batteryHealth_A = ''
batteryStatus_A = ''
batteryCharge_Mode_A = ''
batteryRemain_Min_A = ''
batteryRemain_Sec_A = ''
batteryVolt_A = 0
batteryTemp_A = 0
batteryRemain_Percent_A = 0
lastBattery_Year_A = 0
lastBattery_Mon_A = 0
lastBattery_Day_A = 0
nextBattery_Year_A = 0
nextBattery_Mon_A = 0
nextBattery_Day_A = 0
ups_Life_B = ''
serialName_B = ''
systemMode_B = 0
inputLine_B = 0
inputFreq_B = 0
inputVolt_B = 0
outputLine_B = 0
outputFreq_B = 0
outputVolt_B = 0
outputWatt_B = 0
outputAmp_B = 0
outputPercent_B = 0
batteryHealth_B = ''
batteryStatus_B = ''
batteryCharge_Mode_B = ''
batteryRemain_Min_B = ''
batteryRemain_Sec_B = ''
batteryVolt_B = 0
batteryTemp_B = 0
batteryRemain_Percent_B = 0
lastBattery_Year_B = 0
lastBattery_Mon_B = 0
lastBattery_Day_B = 0
nextBattery_Year_B = 0
nextBattery_Mon_B = 0
nextBattery_Day_B = 0
hostname = '10.0.0.197'					#chang to your service IP
port = '5000'							#chang to your service Port

while(True) :
	localOS = os.system('uname 2>&1 >/var/tmp/os.txt')
	if(localOS == 0):
		response = os.system('ping -c 1 ' + hostname + ' 2>&1 >/var/tmp/ping.txt')
	#	os.system('clear')
	else:
		response = os.system('ping -n 1 ' + hostname + ' 2>&1 >ping.txt')
	#	os.system('cls')
	if response == 0:						# check network sevice & server is on
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		result = sock.connect_ex((hostname, int(port)))
		if result == 0:
			sock.close()
			releaseTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			print ('Data Relaod : ', releaseTime)
			distance = 'http://' + hostname + ':' + port
			r = requests.get(distance)
			value = r.content.decode('utf-8')	# get return json value
			key = json.loads(value)
	#		print (json.dumps(key , sort_keys=True, indent=4, separators=(',', ': ')))	# show on the all split json format
	#		change the json key to local temp value
			ups_Life_A = key['ups_Life_A']
			serialName_A = key['connect_A']
			status_A = key['battery_A']['status']
			batteryHealth_A = status_A['batteryHealth_A']
			batteryStatus_A = status_A['batteryStatus_A']
			batteryCharge_Mode_A = status_A['batteryCharge_Mode_A']
			batteryRemain_Min_A = status_A['batteryRemain_Min_A']
			batteryRemain_Sec_A = status_A['batteryRemain_Sec_A']
			batteryVolt_A = status_A['batteryVolt_A']
			batteryTemp_A = status_A['batteryTemp_A']
			batteryRemain_Percent_A = status_A['batteryRemain_Percent_A']
			lastBattery_A = key['battery_A']['lastChange']
			nextBattery_A = key['battery_A']['nextChange']
			inputStatus_A = key['input_A']
			outputStatus_A = key['output_A']
			inputLine_A = inputStatus_A['inputLine_A']
			inputFreq_A = inputStatus_A['inputFreq_A']
			inputVolt_A = inputStatus_A['inputVolt_A']
			systemMode_A = outputStatus_A['systemMode_A']
			outputLine_A = outputStatus_A['outputLine_A']
			outputFreq_A = outputStatus_A['outputFreq_A']
			outputVolt_A = outputStatus_A['outputVolt_A']
			outputAmp_A = outputStatus_A['outputAmp_A']
			outputWatt_A = outputStatus_A['outputWatt_A']
			outputPercent_A = outputStatus_A['outputPercent_A']
			lastBattery_Year_A = lastBattery_A['lastBattery_Year_A']
			lastBattery_Mon_A = lastBattery_A['lastBattery_Mon_A']
			lastBattery_Day_A = lastBattery_A['lastBattery_Day_A']
			nextBattery_Year_A = nextBattery_A['nextBattery_Year_A']
			nextBattery_Mon_A = nextBattery_A['nextBattery_Mon_A']
			nextBattery_Day_A = nextBattery_A['nextBattery_Day_A']
			ups_Life_B = key['ups_Life_B']
			serialName_B = key['connect_B']
			status_B = key['battery_B']['status']
			batteryHealth_B = status_B['batteryHealth_B']
			batteryStatus_B = status_B['batteryStatus_B']
			batteryCharge_Mode_B = status_B['batteryCharge_Mode_B']
			batteryRemain_Min_B = status_B['batteryRemain_Min_B']
			batteryRemain_Sec_B = status_B['batteryRemain_Sec_B']
			batteryVolt_B = status_B['batteryVolt_B']
			batteryTemp_B = status_B['batteryTemp_B']
			batteryRemain_Percent_B = status_B['batteryRemain_Percent_B']
			lastBattery_B = key['battery_B']['lastChange']
			nextBattery_B = key['battery_B']['nextChange']
			inputStatus_B = key['input_B']
			outputStatus_B = key['output_B']
			inputLine_B = inputStatus_B['inputLine_B']
			inputFreq_B = inputStatus_B['inputFreq_B']
			inputVolt_B = inputStatus_B['inputVolt_B']
			systemMode_B = outputStatus_B['systemMode_B']
			outputLine_B = outputStatus_B['outputLine_B']
			outputFreq_B = outputStatus_B['outputFreq_B']
			outputVolt_B = outputStatus_B['outputVolt_B']
			outputAmp_B = outputStatus_B['outputAmp_B']
			outputWatt_B = outputStatus_B['outputWatt_B']
			outputPercent_B = outputStatus_B['outputPercent_B']
			lastBattery_Year_B = lastBattery_B['lastBattery_Year_B']
			lastBattery_Mon_B = lastBattery_B['lastBattery_Mon_B']
			lastBattery_Day_B = lastBattery_B['lastBattery_Day_B']
			nextBattery_Year_B = nextBattery_B['nextBattery_Year_B']
			nextBattery_Mon_B = nextBattery_B['nextBattery_Mon_B']
			nextBattery_Day_B = nextBattery_B['nextBattery_Day_B']
	#####################################################################################################################################
			conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
			cursor = conn.cursor()
			print(cursor)

			tmp = 'INSERT INTO dbo.ups_in (uId, iFreq, iVolt, iLine, iTime) VALUES (' + "'U001' , " + inputFreq_A  + ", " + inputVolt_A + ", " +  inputLine_A + ", '" + str(releaseTime) + "')"
	#		print(tmp)
			cursor.execute(tmp)
			tmp = 'INSERT INTO dbo.ups_in (uId, iFreq, iVolt, iLine, iTime) VALUES (' + "'U002' , " + inputFreq_B  + ", " + inputVolt_B + ", " +  inputLine_B + ", '" + str(releaseTime) + "')"
	#		print(tmp)
			cursor.execute(tmp)
			tmp = 'INSERT INTO dbo.ups_out (uId, oFreq, oVolt, oLine, oTime, oMode, oWatt, oLoad, oAmp) VALUES (' + "'U001' , " + outputFreq_A  + ", " + inputVolt_A + ", " +  inputLine_A + ", '" + str(releaseTime) + "', '" + systemMode_A + "', " + outputWatt_A + ", " + outputPercent_A + ", " + outputAmp_A + ")"
	#		print(tmp)
			cursor.execute(tmp)
			tmp = 'INSERT INTO dbo.ups_out (uId, oFreq, oVolt, oLine, oTime, oMode, oWatt, oLoad, oAmp) VALUES (' + "'U002' , " + outputFreq_B  + ", " + inputVolt_B + ", " +  inputLine_B + ", '" + str(releaseTime) + "', '" + systemMode_B + "', " + outputWatt_B + ", " + outputPercent_B + ", " + outputAmp_B + ")"
	#		print(tmp)
			cursor.execute(tmp)
			ChangeDate_A = str(lastBattery_Year_A) + '-' + str(lastBattery_Mon_A) + '-' + str(lastBattery_Day_A)
			ReplaceDate_A = str(nextBattery_Year_A) + '-' + str(nextBattery_Mon_A) + '-' + str(nextBattery_Day_A)
			tmp = 'INSERT INTO dbo.ups_battery (uId, bLevel, bVolt, bStatus, bTime, bMode, bChangeDate, bReplaceDate, bHealth, bTemp) VALUES (' + "'U001' , " + batteryRemain_Percent_A  + ", " + batteryVolt_A  + ", '" +  batteryStatus_A + "', '" + str(releaseTime) + "', '" + batteryCharge_Mode_A + "', '" + ChangeDate_A + "', '" + ReplaceDate_A + "', '" + batteryHealth_A + "', " +  batteryTemp_A + ")"
	#		print(tmp)
			cursor.execute(tmp)
			ChangeDate_B = str(lastBattery_Year_B) + '-' + str(lastBattery_Mon_B) + '-' + str(lastBattery_Day_B)
			ReplaceDate_B = str(nextBattery_Year_B) + '-' + str(nextBattery_Mon_B) + '-' + str(nextBattery_Day_B)
			tmp = 'INSERT INTO dbo.ups_battery (uId, bLevel, bVolt, bStatus, bTime, bMode, bChangeDate, bReplaceDate, bHealth, bTemp) VALUES (' + "'U002' , " + batteryRemain_Percent_B  + ", " + batteryVolt_B  + ", '" +  batteryStatus_B + "', '" + str(releaseTime) + "', '" + batteryCharge_Mode_B + "', '" + ChangeDate_B + "', '" + ReplaceDate_B + "', '" + batteryHealth_B + "', " +  batteryTemp_B + ")"
	#		print(tmp)
			cursor.execute(tmp)
			conn.commit()
			conn.close()
			time.sleep(8)
	#####################################################################################################################################
		else:
		   	print ('http://' + hostname +':' + port + ' Service Port Found !')
		   	sys.exit(1)   
	else:
	  	print ('http://', hostname, ' Server IP Not Found !')
	  	sys.exit(1)

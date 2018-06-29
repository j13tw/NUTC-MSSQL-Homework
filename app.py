#!/usr/bin/python
import pymssql
import requests
import json
import os, sys
from datetime import datetime, timedelta	
from flask import Flask, request, url_for, redirect, jsonify
from flask import render_template

app = Flask(__name__)

def find_ups(user_id):
	conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
	cursor = conn.cursor()
	cursor.execute("SELECT uId FROM ups WHERE mId = '" + user_id + "'")
	upsList = cursor.fetchall()
	cursor.close()
	return upsList

def auto_load(ups_id):
	systemTime = datetime.now()
	systemTime_A = systemTime.strftime("%Y-%m-%d %H:%M:%S")
	systemTime_tmp = systemTime_A + " (SYSTEM)"
	systemTime_A = systemTime_A + '.000'
#	print(systemTime_A)
	systemTime_B = (systemTime + timedelta(seconds=-60)).strftime("%Y-%m-%d %H:%M:%S")
	systemTime_B = systemTime_B + '.000'
#	print(systemTime_B)
	conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
	cursor = conn.cursor()
	tmp = "SELECT ups_status_in.uid, ups_status_in.iTime, iFreq, iLine, iVolt, oFreq, oLine, oMode, oAmp, oVolt, oWatt, oLoad, bStatus, bMode, bHealth, bLevel, bChangeDate, bReplaceDate, bVolt, bTemp, uIP, uName, uDistance, uNumber FROM ups_in as ups_status_in INNER JOIN ups_battery on ups_status_in.uId = ups_battery.uId and ups_battery.bTime = ups_status_in.iTime INNER JOIN ups_out on ups_status_in.uId = ups_out.uId and ups_status_in.iTime = ups_out.oTime INNER JOIN ups on ups_status_in.uId = ups.uId WHERE ups_status_in.iTime > '" + systemTime_B +  "' and ups_status_in.iTime < '" + systemTime_A + "' and ups_status_in.uId = '" + ups_id + "' ORDER BY ups_status_in.iTime DESC"
#	print(tmp)
	cursor.execute(tmp)
	dataList = cursor.fetchall()
	conn.commit()
	cursor.close()
#	print("UPS-DATA : " + str(dataList))
	try:
		temp = dataList[0]
		list(temp)
	#	print(temp)
	#	print('-------------------------')
	#	print(temp[0])
	#	print(temp[1])
	#	print(temp[2])
	#	print(temp[4])
	#	print(temp[5])
	#	print(temp[6])
	#	print(temp[7])
	#	print(temp[8])
	#	print(temp[10])
	#	print(temp[11])
	#	print(temp[12])
	#	print(temp[13])
	#	print(temp[14])
	#	print(temp[15])
	#	print(temp[16])
	#	print(temp[17])
	#	print(temp[18])
	#	print(temp[19])
	#	print(temp[20])
	#	print(temp[21])
	#	print(temp[22])
	#	print(temp[23])
	#	print('-------------------------')
		msg = ''
		ups_id = temp[0]
		releaseTime = temp[1]
		inputFreq = temp[2]
		inputLine = temp[3]
		inputVolt = temp[4]
		outputFreq = temp[5]
		outputLine = temp[6]
		systemMode = temp[7]
		outputAmp = round(temp[8], 4)
		outputVolt = temp[9]
		outputWatt = temp[10]
		outputPercent = temp[11]
		batteryStatus = temp[12]
		batteryCharge_Mode = temp[13]
		batteryHealth = temp[14]
		batteryRemain_Percent = temp[15]
		batteryVolt = temp[15]
		lastBattery = temp[16]
		nextBattery = temp[17]
		batteryVolt = temp[18]
		batteryTemp = temp[19]
		ups_ip = temp[20]
		ups_name = temp[21]
		ups_locate = temp[22]
		ups_number = temp[23]
	except:
		msg = '請確認 UPS 是否存在與掛載'
		conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
		cursor = conn.cursor()
		tmp = "SELECT uId, uIP, uName, uNumber, uDistance FROM ups WHERE uId = '" + ups_id + "'"
	#	print(tmp)
		cursor.execute(tmp)
		dataList = cursor.fetchall()
		conn.commit()
		cursor.close()
		try:
			temp = list(dataList[0])
			ups_id = temp[0]
			ups_ip = temp[1]
			ups_name = temp[2]
			ups_locate = temp[3]
			ups_number = temp[4]
		except:
			ups_id = ups_id
			ups_ip = 'NULL'
			ups_name = 'NULL'
			ups_locate = 'NULL'
			ups_number = 'NULL'
		releaseTime = systemTime_tmp
		inputFreq = 0
		inputLine = 0
		inputVolt = 0
		outputFreq = 0
		outputLine = 0
		systemMode = 'NULL'
		outputAmp = 0.0
		outputVolt = 0
		outputWatt = 0
		outputPercent = 0
		batteryStatus = 'NULL'
		batteryCharge_Mode = 'NULL'
		batteryHealth = 'NULL'
		batteryRemain_Percent = 0
		batteryVolt = 0
		lastBattery = 'NULL'
		nextBattery = 'NULL'
		batteryVolt = 0
		batteryTemp = 0
	return (msg, ups_id, releaseTime, inputFreq, inputLine, inputVolt, outputFreq, outputLine, systemMode, outputAmp, outputVolt, outputWatt, outputPercent, batteryStatus, batteryCharge_Mode, batteryHealth, batteryRemain_Percent, lastBattery, nextBattery, batteryVolt, batteryTemp, ups_ip, ups_name, ups_locate, ups_number)

@app.route('/')
def root():
	login_check = url_for('login')
	return redirect(login_check)

@app.route('/ups/<ups_id>', methods=['POST', 'GET'])
def ups_index(ups_id):
	if request.method == 'GET':
		conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
		cursor = conn.cursor()
		temp = "SELECT uId FROM ups"
	#	print(temp)
		cursor.execute(temp)
		upsList = cursor.fetchall()
		conn.commit()
		cursor.close()
		for x in range(0, len(upsList)):
			tmp = ''
			for y in list(str(upsList[x]).split("'")[1]):
				if y != ' ':
				#	print('/' + y + '/')
					tmp = tmp + y
				else:
					break
			if tmp == ups_id:
				conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
				cursor = conn.cursor()
				temp = "SELECT mId FROM ups WHERE uId = '" + ups_id + "'"
			#	print(temp)
				cursor.execute(temp)
				memberList = cursor.fetchall()
				conn.commit()
				cursor.close()
				tmp = ''
				for x in list(str(memberList[0]).split("'")[1]):
					if x != ' ':
					#	print('/' + x + '/')
						tmp = tmp + x
					else:
						break
				user_id = tmp
				conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
				cursor = conn.cursor()
				temp = "SELECT mIP FROM member WHERE mId = '" + tmp + "'"
			#	print(temp)
				cursor.execute(temp)
				ipList = cursor.fetchall()
				conn.commit()
				cursor.close()
				tmp = ''
				for y in list(str(ipList[0]).split("'")[1]):
					if y != ' ':
					#	print('/' + y + '/')
						tmp = tmp + y
					else:
						break
				if tmp == request.remote_addr:
				#	print('-------------------------')
				#	print(auto_load(ups_id))
				#	print('-------------------------')
					temp = auto_load(ups_id)
					list(temp)
					msg = temp[0]
					ups_id = temp[1]
					releaseTime = temp[2]
					inputFreq = temp[3]
					inputLine = temp[4]
					inputVolt = temp[5]
					outputFreq = temp[6]
					outputLine = temp[7]
					systemMode = temp[8]
					outputAmp = temp[9]
					outputVolt = temp[10]
					outputWatt = temp[11]
					outputPercent = temp[12]
					batteryStatus = temp[13]
					batteryCharge_Mode = temp[14]
					batteryHealth = temp[15]
					batteryRemain_Percent = temp[16]
					batteryVolt = temp[16]
					lastBattery = temp[17]
					nextBattery = temp[18]
					batteryVolt = temp[19]
					batteryTemp = temp[20]
					ups_ip = temp[21]
					ups_name = temp[22]
					ups_locate = temp[23]
					ups_number = temp[24]
					return render_template('./upsLogin/upsLogin.html', \
								msg = msg, \
								upsList = find_ups(user_id), \
								ups_number = ups_number, \
								ups_locate = ups_locate, \
								ups_name = ups_name, \
								user_id = user_id, \
								ups_id = ups_id, \
								ups_ip = ups_ip, \
								releaseTime = releaseTime, \
								inputVolt = inputVolt, \
								inputFreq = inputFreq, \
								inputLine = inputLine, \
								systemMode = str(systemMode), \
								outputLine = outputLine, \
								outputVolt = outputVolt, \
								outputAmp = outputAmp, \
								outputPercent = outputPercent, \
								outputWatt = outputWatt, \
								outputFreq = outputFreq, \
								batteryHealth = batteryHealth, \
								batteryStatus = batteryStatus, \
								batteryCharge_Mode = batteryCharge_Mode, \
								batteryVolt = batteryVolt, \
								batteryTemp = batteryTemp, \
								batteryRemain_Percent = batteryRemain_Percent, \
								lastBattery = lastBattery, \
								nextBattery = nextBattery
								)
				else:
					print('USER NOT LOGIN !')
					print('-------------------------------')
					return redirect('/login')
			if x == len(upsList) - 1:
				print('UPS NOT ON UPS LIST !')
				print('-------------------------------')
				return redirect('/login')
	else:
		conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
		cursor = conn.cursor()
		temp = "SELECT uId FROM ups"
	#	print(temp)
		cursor.execute(temp)
		upsList = cursor.fetchall()
		conn.close()
		for x in range(0, len(upsList)):
		#	print(str(upsList[x]))
			tmp = ''
			for y in list(str(upsList[x]).split("'")[1]):
				if y != ' ':
				#	print('/' + y + '/')
					tmp = tmp + y
				else:
					break
			if tmp == ups_id:	
			#	print(tmp)
				conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
				cursor = conn.cursor()
				cursor.execute("SELECT mId FROM ups WHERE uId = '" + ups_id + "'")
				memberList = cursor.fetchall()
				conn.close()
				tmp = ''
				for y in list(str(memberList[0]).split("'")[1]):
					if y != ' ':
					#	print('/' + y + '/')
						tmp = tmp + y
					else:
						break
				conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
				cursor = conn.cursor()
				temp = "UPDATE member SET mIP = '0.0.0.0' WHERE mId = '" + tmp + "'"
			#	print(temp)
				cursor.execute(temp)
				conn.commit()
				cursor.close()
				return redirect('/login')

@app.route('/now/<user_id>/<ups_id>', methods=['POST', 'GET'])
def index(user_id, ups_id):
	if request.method == 'GET':
		conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
		cursor = conn.cursor()
		temp = "SELECT mId FROM member"
	#	print(temp)
		cursor.execute(temp)
		memberList = cursor.fetchall()
		conn.commit()
		cursor.close()
		tmp = ''
		for x in range(0, len(memberList)):
			tmp = ''
			for y in list(str(memberList[x]).split("'")[1]):
				if y != ' ':
				#	print('/' + y + '/')
					tmp = tmp + y
				else:
					break
			if tmp == user_id:
				conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
				cursor = conn.cursor()
				temp = "SELECT mIP FROM member WHERE mId = '" + user_id + "'"
			#	print(temp)
				cursor.execute(temp)
				ipList = cursor.fetchall()
				conn.commit()
				cursor.close()
				tmp = ''
				for z in list(str(ipList[0]).split("'")[1]):
					if z != ' ':
					#	print('/' + z + '/')
						tmp = tmp + z
					else:
						break
				if tmp == request.remote_addr:
				#	print('-------------------------')
				#	print(auto_load(ups_id))
				#	print('-------------------------')
					temp = auto_load(ups_id)
					list(temp)
					msg = temp[0]
					ups_id = temp[1]
					releaseTime = temp[2]
					inputFreq = temp[3]
					inputLine = temp[4]
					inputVolt = temp[5]
					outputFreq = temp[6]
					outputLine = temp[7]
					systemMode = temp[8]
					outputAmp = temp[9]
					outputVolt = temp[10]
					outputWatt = temp[11]
					outputPercent = temp[12]
					batteryStatus = temp[13]
					batteryCharge_Mode = temp[14]
					batteryHealth = temp[15]
					batteryRemain_Percent = temp[16]
					batteryVolt = temp[16]
					lastBattery = temp[17]
					nextBattery = temp[18]
					batteryVolt = temp[19]
					batteryTemp = temp[20]
					ups_ip = temp[21]
					ups_name = temp[22]
					ups_locate = temp[23]
					ups_number = temp[24]
					return render_template('./userLogin.html', \
								msg = msg, \
								upsList = find_ups(user_id), \
								ups_number = ups_number, \
								ups_locate = ups_locate, \
								ups_name = ups_name, \
								user_id = user_id, \
								ups_id = ups_id, \
								ups_ip = ups_ip, \
								releaseTime = releaseTime, \
								inputVolt = inputVolt, \
								inputFreq = inputFreq, \
								inputLine = inputLine, \
								systemMode = str(systemMode), \
								outputLine = outputLine, \
								outputVolt = outputVolt, \
								outputAmp = round(outputAmp, 4), \
								outputPercent = outputPercent, \
								outputWatt = outputWatt, \
								outputFreq = outputFreq, \
								batteryHealth = batteryHealth, \
								batteryStatus = batteryStatus, \
								batteryCharge_Mode = batteryCharge_Mode, \
								batteryVolt = batteryVolt, \
								batteryTemp = batteryTemp, \
								batteryRemain_Percent = batteryRemain_Percent, \
								lastBattery = lastBattery, \
								nextBattery = nextBattery
								)
				else:
					print('USER NOT LOGIN !')
					print('-------------------------------')
					return redirect('/login')
			if x == len(memberList) - 1:
				print('USER NOT ON Member List !')
				print('-------------------------------')
				return redirect('/login')
	else:
		ups_id_tmp = ups_id
		print("UPS TMP : " + ups_id_tmp)
		ups_id = request.form.get('ups_id')
		if ups_id != None and ups_id != '':
			Search = url_for('index', ups_id = ups_id, user_id = user_id)
			return redirect(Search)
		elif ups_id == '':
			Search = url_for('index', ups_id = ups_id_tmp, user_id = user_id)
			return redirect(Search)
		else:	
			conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
			cursor = conn.cursor()
			temp = "UPDATE member SET mIP = '0.0.0.0' WHERE mId = '" + user_id + "'"
		#	print(temp)
			cursor.execute(temp)
			conn.commit()
			cursor.close()
			return redirect('/login')

@app.route('/login/', methods=['GET', 'POST'])
def login():
	print('-------------------------------')
	print("Login Client IP : " + request.remote_addr)
	if request.method == 'GET':
		return render_template('login.html')
	else:
		errorCode_A = errorCode_B = 0
		error = ''
		print(request.form)
		user_id = request.form.get('user_id')
		if user_id == None:
			errorCode_A = 1
		else:
			for x in list(user_id):
				if x == ' ':
					errorCode_A = 1
		if user_id != None and user_id != '' and errorCode_A != 1 and len(user_id) <= 10 and len(user_id) >= 4:
			conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
			cursor = conn.cursor()
			cursor.execute("SELECT mId FROM member")
			memberList = cursor.fetchall()
			conn.close()
			tmp = ''
		#	print(memberList)
			for x in range(0, len(memberList)):
				tmp = ''
				for y in list(str(memberList[x]).split("'")[1]):
					if y != ' ':
					#	print('/' + y + '/')
						tmp = tmp + y
					else:
						break
				if tmp == user_id:
					print(user_id)
					user_pwd = request.form.get('user_pwd')
					for x in list(user_pwd):
						if x == ' ':
							errorCode_A = 1
							break
					if user_pwd != '' and errorCode_A != 1:
						conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
						cursor = conn.cursor()
						temp = "SELECT mPassword FROM member WHERE mId = '" + tmp + "'"
					#	print(temp)
						cursor.execute(temp)
						checkPassword = cursor.fetchall()
					#	print(checkPassword)
						cursor.close()
						checkMember = 0
						password = ''
						for z in list(str(checkPassword[0]).split("'")[1]):
							if z != ' ':
							#	print('/' + z + '/')
								password = password + z
							else:
								break
						if user_pwd == password:
							conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
							cursor = conn.cursor()
							temp = "UPDATE member SET mIP = '" + request.remote_addr + "' WHERE mId = '" + user_id + "'"
							print(temp)
							cursor.execute(temp)
							conn.commit()
							cursor.close()
							conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
							cursor = conn.cursor()
							tmp = "SELECT uId FROM ups WHERE mId = '" + user_id + "'"
						#	print(tmp)
							cursor.execute(tmp)
							upsList = cursor.fetchall()
							conn.commit()
							cursor.close()
						#	print("UPS-LIST : " + str(upsList))
							try:
								ups_id = list(upsList[0])[0]
							except:
								ups_id = 'NULL'
						#	print(ups_id)
							login_ok = url_for('index', user_id = user_id, ups_id = ups_id)
							return redirect(login_ok)
						else:
							print('user_pwd Error !')
							errorCode_A = 1
					else:
						print('user_pwd Error !')
						errorCode_A = 1
				if x == len(memberList) - 1 and errorCode_A != 1:
					print('user_id Error !')
					errorCode_A = 1
		else:
			print('user_block input Error !')
			errorCode_A = 1
		print("errorCode_A = " + str(errorCode_A))
		ups_id = request.form.get('ups_id')
		if ups_id == None:
			errorCode_B = 1
		else:
			for x in list(ups_id):
				if x == ' ':
					errorCode_B = 1
		if ups_id != None and ups_id != '' and errorCode_B != 1 and len(ups_id) <= 10 and len(ups_id) >= 4:
			print('Key in ups_id = ' + ups_id)
			conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
			cursor = conn.cursor()
			temp = "SELECT uId FROM ups"
		#	print(temp)
			cursor.execute(temp)
			upsList = cursor.fetchall()
			conn.close()
			for x in range(0, len(upsList)):
			#	print(str(upsList[x]))
				tmp = ''
				for y in list(str(upsList[x]).split("'")[1]):
					if y != ' ':
					#	print('/' + y + '/')
						tmp = tmp + y
					else:
						break
				if tmp == ups_id:	
				#	print(tmp)
					conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
					cursor = conn.cursor()
					cursor.execute("SELECT mId FROM ups WHERE uId = '" + ups_id + "'")
					memberList = cursor.fetchall()
					conn.close()
					tmp = ''
					for y in list(str(memberList[0]).split("'")[1]):
						if y != ' ':
						#	print('/' + y + '/')
							tmp = tmp + y
						else:
							break
					ups_pwd = request.form.get('ups_pwd')
					for x in list(ups_pwd):
						if x == ' ':
							errorCode_B = 1
							break
					if ups_pwd != '' and errorCode_B != 1:
						conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
						cursor = conn.cursor()
						temp = "SELECT mPassword FROM member WHERE mId = '" + tmp + "'"
					#	print(temp)
						cursor.execute(temp)
						checkPassword = cursor.fetchall()
					#	print(checkPassword)
						cursor.close()
						checkMember = 0
						password = ''
						for z in list(str(checkPassword[0]).split("'")[1]):
							if z != ' ':
							#	print('/' + z + '/')
								password = password + z
							else:
								break
					#	print(password)
						if ups_pwd == password:
							print('-------------------------------')
							conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
							cursor = conn.cursor()
							temp = "UPDATE member SET mIP = '" + request.remote_addr + "' WHERE mId = '" + tmp + "'"
							print(temp)
							cursor.execute(temp)
							conn.commit()
							cursor.close()
							login_ok = url_for('ups_index', ups_id = ups_id)
							return redirect(login_ok)
						else:
							errorCode_B = 1
				if x == len(upsList):
					print('ups_id Error !')
					errorCode_B = 1
		else:
			print('ups_block input Error !')
			errorCode_B = 1
		print("errorCode_B = " + str(errorCode_B))
		if errorCode_A == 1 or errorCode_B == 1:
			print('user / ups Error !')
			print('-------------------------------')
			error = '請確認輸入的資料 !'
			return render_template('login.html', error = error)

@app.route('/user_signup', methods=['GET', 'POST'])
def user_signup():
	print('-------------------------------')
	print("User Regist Client IP : " + request.remote_addr)
	errorCode = 0
	if request.method == 'GET':	
		print('-------------------------------')
		error = ''
		return render_template('userSignup.html', error = error)
	else:
		print('-------------------------------')
	#	print (request.form)
		user_id = request.form.get('user_id')
		for x in list(user_id):
			if x == ' ':
				errorCode = 1
		if user_id != '' and errorCode == 0 and len(user_id) <= 10 and len(user_id) >= 4:
			print("user_id : " + user_id)
			user_pwd = request.form.get('user_pwd')
			countLower = countUpper = countNumber = 0
			for x in list(user_pwd):
				if x == ' ':
					errorCode = 1
				elif ord(x) >= 97 and ord(x) <= 122:
					countLower = countLower + 1
				elif ord(x) >= 65 and ord(x) <= 90:
					countUpper = countUpper + 1
				elif ord(x) >= 48 and ord(x) <= 57:
					countNumber = countNumber + 1
			if user_pwd != '' and len(user_pwd) > 8 and len(user_pwd) <= 30 and countLower > 0 or countUpper > 0 or countNumber > 0 and errorCode == 0:
				print("user_pwd : " + user_pwd)
				user_name = request.form.get('user_name')
				for x in list(user_name):
					if x == ' ':
						errorCode = 1
				if user_name != '' and errorCode == 0 and len(user_name) > 4 and len(user_name) <= 30:
					print("user_name : " + user_name)
					user_phone = request.form.get('user_phone')
					tmp = user_phone.split('-')
					if user_phone != '' and len(user_phone) == 12 and int(tmp[0]) <= 999 and int(tmp[1]) <= 999 and int(tmp[2]) <= 999:
						user_mail = request.form.get('user_mail')
						tmp = user_mail.split('@')
						if user_phone != '' and tmp[0] != '' and tmp[1] != '':	
							user_rule = request.form.get('user_rule')
							if user_rule != None:
								user_collect = request.form.get('user_collect')
								if user_collect != None:
									user_collect=1
								else:
									user_collect=0
								print("user_collect : " + str(user_collect))
								conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
								cursor = conn.cursor()
								cursor.execute('SELECT mId FROM member')
								memberList = cursor.fetchall()
								cursor.close()
								for x in range(0, len(memberList)):
								#	print(str(memberList[x]))
									tmp = ''
									for y in list(str(memberList[x]).split("'")[1]):
										if y != ' ':
										#	print('/' + y + '/')
											tmp = tmp + y
										else:
											break
									if tmp == user_id:
										errorCode = 1
								#	print(tmp)
								if errorCode == 0:
									cursor = conn.cursor()
									addMember = "INSERT INTO dbo.member (mId, mPassword, mName, mEmail, mPhone, mCollect) VALUES ('" + user_id + "' , '" + user_pwd + "', '" + user_name + "', '" +  user_mail + "', '" + user_phone + "', " + str(user_collect) +")"
								#	print(addMember)
									cursor.execute(addMember)
									conn.commit()
									conn.close()
									print("DB Incert : OK !")
									print('-------------------------------')
									login_check = url_for('login')
									return redirect(login_check)
								else:
									print("DB Incert : NO !")
									print('-------------------------------')
									error = '此帳號ID被使用，請進行更改'
									return render_template('userSignup.html', error = error)
							else:
								print('user_acess Error !')
								print('-------------------------------')
								error = '請確認已閱讀管理者條文'
								return render_template('userSignup.html', error = error)
						else:
							print('user_mail Error !')
							print('-------------------------------')
							error = '請確認輸入的電子郵件'
							return render_template('userSignup.html', error = error)
					else:
						print('user_phone Error !')
						print('-------------------------------')
						error = '請確認輸入的電話號碼'
						return render_template('userSignup.html', error = error)
				else:
					print('user_name Error !')
					print('-------------------------------')
					error = '請確認輸入的姓名'
					return render_template('userSignup.html', error = error)	
			else:
				print('user_pwd Error !')
				print('-------------------------------')
				error = '請確認輸入的密碼'
				return render_template('userSignup.html', error = error)	
		else:
			print('user_id Error !')
			print('-------------------------------')
			error = '請確認輸入的帳號'
			return render_template('userSignup.html', error = error)

@app.route('/ups_signup/<user_id>', methods=['GET', 'POST'])
def ups_signup(user_id):
	print('-------------------------------')
	print("UPS Regist Client IP : " + request.remote_addr)
	errorCode = 0
	if request.method == 'GET':	
		print('-------------------------------')
		error = ''
		conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
		cursor = conn.cursor()
		temp = "SELECT mId FROM member"
	#	print(temp)
		cursor.execute(temp)
		memberList = cursor.fetchall()
		conn.commit()
		cursor.close()
		tmp = ''
		for x in range(0, len(memberList)):
			tmp = ''
			for y in list(str(memberList[x]).split("'")[1]):
				if y != ' ':
				#	print('/' + y + '/')
					tmp = tmp + y
				else:
					break
			if tmp == user_id:
				conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
				cursor = conn.cursor()
				temp = "SELECT mIP FROM member WHERE mId = '" + user_id + "'"
			#	print(temp)
				cursor.execute(temp)
				ipList = cursor.fetchall()
				conn.commit()
				cursor.close()
				tmp = ''
				for z in list(str(ipList[0]).split("'")[1]):
					if z != ' ':
					#	print('/' + z + '/')
						tmp = tmp + z
					else:
						break
				if tmp == request.remote_addr:		
					print('Login IP :' + tmp)
					try:
						ups_id = list(find_ups(user_id)[0])[0]
					except:
						ups_id = 'NULL'
					return render_template('upsSignup.html', user_id = user_id, ups_id = ups_id)
				else:
					print('USER NOT ON Member List !')
					print('-------------------------------')
					return redirect('/login')
			if x == len(memberList) - 1:
				print('USER NOT LOGIN !')
				print('-------------------------------')
				return redirect('/login')
	else:
		print('-------------------------------')
		print (request.form)
		ups_id = request.form.get('ups_id')
		for x in list(ups_id):
			if x == ' ':
				errorCode = 1
		if ups_id != '' and errorCode == 0 and len(ups_id) <= 10 and len(ups_id) >= 4:
			print("ups_id : " + ups_id)
			conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
			cursor = conn.cursor()
			cursor.execute('SELECT uId FROM ups')
			upsList = cursor.fetchall()
			cursor.close()
			for x in range(0, len(upsList)):
			#	print(str(upsList[x]))
				tmp = ''
				for y in list(str(upsList[x]).split("'")[1]):
					if y != ' ':
					#	print('/' + y + '/')
						tmp = tmp + y
					else:
						break
				if tmp == ups_id:
					errorCode = 1
			#	print(tmp)
			if errorCode != 1:
				print("user_id : " + user_id)
				conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
				cursor = conn.cursor()
				cursor.execute('SELECT mId FROM member')
				memberList = cursor.fetchall()
				cursor.close()
				checkMember = 0
				for x in range(0, len(memberList)):
				#	print(str(memberList[x]))
					tmp = ''
					for y in list(str(memberList[x]).split("'")[1]):
						if y != ' ':
						#	print('/' + y + '/')
							tmp = tmp + y
						else:
							break
					if tmp == user_id:
						user_pwd = request.form.get('user_pwd')
						for x in list(user_pwd):
							if x == ' ':
								errorCode = 1
								break
						if user_pwd != '' and errorCode != 1:
							conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
							cursor = conn.cursor()
							temp = "SELECT mPassword FROM member WHERE mId = '" + tmp + "'"
						#	print(temp)
							cursor.execute(temp)
							checkPassword = cursor.fetchall()
							print(checkPassword)
							cursor.close()
							password = ''
							for z in list(str(checkPassword[0]).split("'")[1]):
								if z != ' ':
								#	print('/' + z + '/')
									password = password + z
								else:
									break
							if user_pwd == password:
								print("password : PASS !")
								ups_name = request.form.get('ups_name')
								for x in list(ups_name):
									if x == ' ':
										errorCode = 1
										break
								if ups_name != '' and errorCode != 1:
									ups_ip = request.form.get('ups_ip')
									try:
										ip = ups_ip.split(":")[0].split('.')
										port = int(ups_ip.split(":")[1])
									except:
										errorCode = 1
								#	print("IP : " + ip[0] + "." + ip[1] + "." + ip[2] + "." + ip[3])
								#	print("PORT : " + str(port))
									if ups_ip != '' and errorCode!= 1 and len(ip) == 4 and int(ip[0]) <= 254 and int(ip[1]) <= 254 and int(ip[2]) <= 254 and int(ip[3]) <= 254 and port <= 30080:
										print("ups_ip : " + ups_ip)
										ups_create = request.form.get('ups_create')
										if (ups_create != 'None'):
											ups_model = request.form.get('ups_model')
											print('ups_model : ' + ups_model)
											if (ups_model != 'None'):
												ups_unit = request.form.get('ups_unit')
												print('ups_unit : ' + ups_unit)
												ups_number = request.form.get('ups_number')
												if (ups_number != ''):
													print('ups_number : ' + ups_number)
													ups_locate = request.form.get('ups_locate')
													if (ups_locate != ''):
														print('ups_locate : ' + ups_locate)
														ups_rule = request.form.get('ups_rule')
														if ups_rule != None:
															ups_collect = request.form.get('ups_collect')
															if ups_collect != None:
																ups_collect=1
															else:
																ups_collect=0
															print("ups_collect : " + str(ups_collect))
															cursor = conn.cursor()
															addUPS = "INSERT INTO dbo.ups (uId, mId, uName, uIP, uFactory, uModel, uUnit, uNumber, uDistance, uCollect) VALUES ('" + ups_id + "' , '" + user_id + "', '" + ups_name + "', '" + ups_ip + "', '" +  ups_create + "', '" + ups_model + "', '" + ups_unit + "', '" + ups_number + "', '" + ups_locate +  "', " + str(ups_collect) + ")"
														#	print(addUPS)
															cursor.execute(addUPS)
															conn.commit()
															conn.close()
															print("DB Incert : OK !")
															print('-------------------------------')
															error = '設備添加成功 !'
															try:
																ups_id = list(find_ups(user_id)[0])[0]
															except:
																ups_id = 'NULL'
															return render_template('upsSignup.html', error = error, user_id = user_id, ups_id = ups_id)
														else:
															print('ups_acess Error !')
															print('-------------------------------')
															error = '請確認已閱讀UPS設備託管條文'
															try:
																ups_id = list(find_ups(user_id)[0])[0]
															except:
																ups_id = 'NULL'
															return render_template('upsSignup.html', error = error, user_id = user_id, ups_id = ups_id)
													else:
														print('ups_locate Error !')
														print('-------------------------------')
														error = '請填寫設備的放置區域或備註信息'
														try:
															ups_id = list(find_ups(user_id)[0])[0]
														except:
															ups_id = 'NULL'
														return render_template('upsSignup.html', error = error, user_id = user_id, ups_id = ups_id)
												else:
													print('ups_number Error !')
													print('-------------------------------')
													error = '請確認設備的識別編號'
													try:
														ups_id = list(find_ups(user_id)[0])[0]
													except:
														ups_id = 'NULL'
													return render_template('upsSignup.html', error = error, user_id = user_id, ups_id = ups_id)	
											else:
												print('ups_model Error !')
												print('-------------------------------')
												error = '請確認設備的所屬系列'
												try:
													ups_id = list(find_ups(user_id)[0])[0]
												except:
													ups_id = 'NULL'
											return render_template('upsSignup.html', error = error, user_id = user_id, ups_id = ups_id)	
										else:
											print('ups_create Error !')
											print('-------------------------------')
											error = '請確認設備的生產廠區'
											try:
												ups_id = list(find_ups(user_id)[0])[0]
											except:
												ups_id = 'NULL'
											return render_template('upsSignup.html', error = error, user_id = user_id, ups_id = ups_id)	
									else:
										print('ups_ip Error !')
										print('-------------------------------')
										error = '請確認設備的託管 IP'
										try:
											ups_id = list(find_ups(user_id)[0])[0]
										except:
											ups_id = 'NULL'
										return render_template('upsSignup.html', error = error, user_id = user_id, ups_id = ups_id)	
								else:
									print('ups_name Error !')
									print('-------------------------------')
									error = '請確認輸入的託管 設備名稱'
									return render_template('upsSignup.html', error = error, user_id = user_id, ups_id = ups_id)
							else:
								errorCode = 1
								print('ups_pwd Error !')
								print('-------------------------------')
								error = '請確認輸入的管理者資料'
								try:
									ups_id = list(find_ups(user_id)[0])[0]
								except:
									ups_id = 'NULL'
								return render_template('upsSignup.html', error = error, user_id = user_id, ups_id = ups_id)
						else:
							errorCode = 1
							print('ups_pwd Error !')
							print('-------------------------------')
							error = '請確認輸入的管理者資料'
							try:
								ups_id = list(find_ups(user_id)[0])[0]
							except:
								ups_id = 'NULL'
							return render_template('upsSignup.html', error = error, user_id = user_id, ups_id = ups_id)
					if x == len(memberList) - 1 and errorCode != 1:
						print('ups_id Error !')
						print('-------------------------------')
						error = '請確認輸入的管理者資料'
						try:
							ups_id = list(find_ups(user_id)[0])[0]
						except:
							ups_id = 'NULL'
						return render_template('upsSignup.html', error = error, user_id = user_id, ups_id = ups_id)
			else:
				print('user_id Error !')
				print('-------------------------------')
				error = 'UPS 編號已被使用'
				try:
					ups_id = list(find_ups(user_id)[0])[0]
				except:
					ups_id = 'NULL'
				return render_template('upsSignup.html', error = error, user_id = user_id, ups_id = ups_id)			
		else:
			print('user_id Error !')
			print('-------------------------------')
			error = '請確認輸入的 UPS 編號'
			try:
				ups_id = list(find_ups(user_id)[0])[0]
			except:
				ups_id = 'NULL'
			return render_template('upsSignup.html', error = error, user_id = user_id, ups_id = ups_id)

@app.route('/user_replace/<user_id>', methods=['GET', 'POST'])
def user_replace(user_id):
	print('-------------------------------')
	print("USER Replace Client IP : " + request.remote_addr)
	errorCode = 0
	if request.method == 'GET':	
		print('-------------------------------')
		error = ''
		conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
		cursor = conn.cursor()
		temp = "SELECT mId FROM member"
	#	print(temp)
		cursor.execute(temp)
		memberList = cursor.fetchall()
		conn.commit()
		cursor.close()
		tmp = ''
		for x in range(0, len(memberList)):
			tmp = ''
			for y in list(str(memberList[x]).split("'")[1]):
				if y != ' ':
				#	print('/' + y + '/')
					tmp = tmp + y
				else:
					break
			if tmp == user_id:
				conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
				cursor = conn.cursor()
				temp = "SELECT mIP FROM member WHERE mId = '" + user_id + "'"
			#	print(temp)
				cursor.execute(temp)
				ipList = cursor.fetchall()
				conn.commit()
				cursor.close()
				tmp = ''
				for z in list(str(ipList[0]).split("'")[1]):
					if z != ' ':
					#	print('/' + z + '/')
						tmp = tmp + z
					else:
						break
				if tmp == request.remote_addr:		
					print('Login IP :' + tmp)
					try:
						ups_id = list(find_ups(user_id)[0])[0]
					except:
						ups_id = 'NULL'
					return render_template('userReplace.html', error = error, user_id = user_id, ups_id = ups_id)
				else:
					print('USER NOT LOGIN !')
					print('-------------------------------')
					return redirect('/login')
			if x == len(memberList) - 1:
				print('USER NOT ON Member List !')
				print('-------------------------------')
				return redirect('/login')

	else:
		print('-------------------------------')
	#	print (request.form)
		print("user_id : " + user_id)
		print('-------------------------------')
		conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
		cursor = conn.cursor()
		cursor.execute("SELECT mId FROM member")
		memberList = cursor.fetchall()
		conn.close()
		error = "已更改 : "
		for x in range(0, len(memberList)-1):
			tmp = ''
			for y in list(str(memberList[x]).split("'")[1]):
				if y != ' ':
				#	print('/' + y + '/')
					tmp = tmp + y
				else:
					break
		#	print("tmp : " + tmp)
			if tmp == user_id:
				user_pwd = request.form.get('user_pwd')
				for x in list(user_pwd):
					if x == ' ':
						errorCode = 1
						break
				if user_pwd != '' and errorCode != 1:
					conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
					cursor = conn.cursor()
					temp = "SELECT mPassword FROM member WHERE mId = '" + user_id + "'"
				#	print(temp)
					cursor.execute(temp)
					checkPassword = cursor.fetchall()
				#	print(checkPassword)
					cursor.close()
					checkMember = 0
					password = ''
					for z in list(str(checkPassword[0]).split("'")[1]):
						if z != ' ':
						#	print('/' + z + '/')
							password = password + z
						else:
							break
				#	print(password)
					if user_pwd == password:
						user_new_pwd_A = request.form.get('user_new_pwd_A')
						user_new_pwd_B = request.form.get('user_new_pwd_B')
						for x in list(user_new_pwd_A):
							if x == ' ':
								errorCode = 1
								break
						for x in list(user_new_pwd_B):
							if x == ' ':
								errorCode = 1
								break
						if user_new_pwd_A == user_new_pwd_B and user_new_pwd_A != '' and user_new_pwd_B != '' and errorCode != 1 and len(user_new_pwd_A) >= 8:
							conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
							cursor = conn.cursor()
							temp = "UPDATE member SET mPassword = '" + user_new_pwd_A + "' WHERE mId = '" + user_id + "'"
						#	print(temp)
							cursor.execute(temp)
							conn.commit()
							conn.close()
							error = error + "密碼 / "
						elif user_new_pwd_A == '' and user_new_pwd_B == '':
							print('user_password Not Change !')
							print('-------------------------------')
						else:
							print('user_password check Error !')
							print('-------------------------------')
							error = " 請驗證更新輸入的密碼"
							try:
								ups_id = list(find_ups(user_id)[0])[0]
							except:
								ups_id = 'NULL'
							return render_template('userReplace.html', error = error, user_id = user_id, ups_id = ups_id)
						user_name = request.form.get('user_name')
						for x in list(user_name):
							if x == ' ':
								errorCode = 1
								break
						if user_name != '' and errorCode != 1:
							print("user_name : " + user_name)
							conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
							cursor = conn.cursor()
						#	temp = "UPDATE member SET mName = '" + user_name + "' WHERE mId = '" + user_id + "'"
							print(temp)
							cursor.execute(temp)
							conn.commit()
							cursor.close()
							error = error + "姓名 / "
						else:
							print('user_name Not Change !')
							print('-------------------------------')
						user_phone = request.form.get('user_phone')
						for x in list(user_phone):
							if x == ' ':
								errorCode = 1
								break
						if user_phone != '' and errorCode != 1:
							try:
								tmp = user_phone.split("-")
							except:
								errorCode = 1
							if errorCode != 1 and int(tmp[0]) <= 999 and int(tmp[1]) <= 999 and int(tmp[2]) <= 999:
								print("user_phone : " + user_phone)
								conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
								cursor = conn.cursor()
								temp = "UPDATE member SET mPhone = '" + user_phone + "' WHERE mId = '" + user_id + "'"
								print(temp)
								cursor.execute(temp)
								conn.commit()
								cursor.close()
								error = error + "電話 / "
							else:
								print('user_phone check Error !')
								print('-------------------------------')
								error = error + " 請驗證更新輸入的電話號碼"
								try:
									ups_id = list(find_ups(user_id)[0])[0]
								except:
									ups_id = 'NULL'
								return render_template('userReplace.html', error = error, user_id = user_id, ups_id = ups_id)
						else:
							print('user_phone Not Change !')
							print('-------------------------------')
						
						user_mail = request.form.get('user_mail')
						for x in list(user_mail):
							if x == ' ':
								errorCode = 1
								break
						if user_mail != '' and errorCode != 1:
							try:
								tmp = user_mail.split('@')
							except:
								errorCode = 1
							if errorCode != 1 and tmp[0] != '' and tmp[1] != '':
								conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
								cursor = conn.cursor()
								temp = "UPDATE member SET mEmail = '" + user_mail + "' WHERE mId = '" + user_id + "'"
							#	print(temp)
								cursor.execute(temp)
								conn.commit()
								cursor.close()
								error = error + "電子信箱 / "
							else:
								print('user_mail check Error !')
								print('-------------------------------')
								error = error + " 請驗證更新輸入的電子信箱"
								try:
									ups_id = list(find_ups(user_id)[0])[0]
								except:
									ups_id = 'NULL'
								return render_template('userReplace.html', error = error, user_id = user_id, ups_id = ups_id)
						else:
							print('user_mail Not Change !')
							print('-------------------------------')
						user_collect = request.form.get('user_collect')
						if user_collect != None:
							user_collect=1
							error = error + "參與資料收集 / "
						else:
							user_collect=0
							error = error + "取消資料收集 / "
						print("user_collect : " + str(user_collect))
						conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
						cursor = conn.cursor()
						temp = "UPDATE member SET mCollect = '" + str(user_collect) + "' WHERE mId = '" + user_id + "'"
					#	print(temp)
						cursor.execute(temp)
						conn.commit()
						cursor.close()
						print('-------------------------------')
						print('驗證成功')
						print('-------------------------------')
						error = error + '驗證成功'
						try:
							ups_id = list(find_ups(user_id)[0])[0]
						except:
							ups_id = 'NULL'
						return render_template('userReplace.html', error = error, user_id = user_id, ups_id = ups_id)	
					else:
						errorCode = 1
				else:
					errorCode = 1		
			if x == len(memberList) - 1:
				errorCode = 1	
		if (errorCode == 1):
			print('user_Data Error !')
			print('-------------------------------')
			error = '請確認輸入的設備資料'
			try:
				ups_id = list(find_ups(user_id)[0])[0]
			except:
				ups_id = 'NULL'
			return render_template('userReplace.html', error = error, user_id = user_id, ups_id = ups_id)

@app.route('/ups_replace/<user_id>', methods=['GET', 'POST'])
def ups_replace(user_id):
	print('-------------------------------')
	print("UPS Replace Client IP : " + request.remote_addr)
	errorCode = 0
	if request.method == 'GET':	
		print('-------------------------------')
		error = ''
		conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
		cursor = conn.cursor()
		temp = "SELECT mId FROM member"
		cursor.execute(temp)
		memberList = cursor.fetchall()
		print(memberList)
		conn.commit()
		cursor.close()
		tmp = ''
		for x in range(0, len(memberList)):
			tmp = ''
			for y in list(str(memberList[x]).split("'")[1]):
				if y != ' ':
				#	print('/' + y + '/')
					tmp = tmp + y
				else:
					break
			print(tmp)
			if tmp == user_id:
				conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
				cursor = conn.cursor()
				temp = "SELECT mIP FROM member WHERE mId = '" + user_id + "'"
			#	print(temp)
				cursor.execute(temp)
				ipList = cursor.fetchall()
				conn.commit()
				cursor.close()
				tmp = ''
				for z in list(str(ipList[0]).split("'")[1]):
					if z != ' ':
					#	print('/' + z + '/')
						tmp = tmp + z
					else:
						break
				if tmp == request.remote_addr:			
					print('Login IP :' + tmp)
					try:
						ups_id = list(find_ups(user_id)[0])[0]
					except:
						ups_id = 'NULL'
					return render_template('upsReplace.html', msg = find_ups(user_id), user_id = user_id, ups_id = ups_id)
				else:
					print('USER NOT LOGIN !')
					print('-------------------------------')
					return redirect('/login')
			if x == len(memberList) - 1:
				print('USER NOT ON Member List !')
				print('-------------------------------')
				return redirect('/login')
	else:
		print('-------------------------------')
	#	print (request.form)
		error = "已更改 : "
		ups_id = request.form.get('ups_id')
		for x in list(ups_id):
			if x == ' ':
				errorCode = 1
				break
		if ups_id != '' and errorCode == 0 and len(ups_id) <= 10 and len(ups_id) >= 4:
			print("ups_id : " + ups_id)
			print('-------------------------------')
			conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
			cursor = conn.cursor()
			cursor.execute('SELECT uId FROM ups')
			upsList = cursor.fetchall()
			cursor.close()
			for x in range(0, len(upsList)):
			#	print(str(upsList[x]))
				tmp = ''
				for y in list(str(upsList[x]).split("'")[1]):
					if y != ' ':
					#	print('/' + y + '/')
						tmp = tmp + y
					else:
						break
				if tmp == ups_id:	
				#	print(tmp)
					print("user_id : " + user_id)
					conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
					cursor = conn.cursor()
					cursor.execute("SELECT mId FROM ups WHERE uId = '" + ups_id + "'")
					memberList = cursor.fetchall()
					conn.close()
					tmp = ''
					for y in list(str(memberList[0]).split("'")[1]):
						if y != ' ':
						#	print('/' + y + '/')
							tmp = tmp + y
						else:
							break
					if tmp == user_id:
						user_pwd = request.form.get('user_pwd')
						for x in list(user_pwd):
							if x == ' ':
								errorCode = 1
								break
						if user_pwd != '' and errorCode != 1:
							conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
							cursor = conn.cursor()
							temp = "SELECT mPassword FROM member WHERE mId = '" + tmp + "'"
						#	print(temp)
							cursor.execute(temp)
							checkPassword = cursor.fetchall()
						#	print(checkPassword)
							cursor.close()
							checkMember = 0
							password = ''
							for z in list(str(checkPassword[0]).split("'")[1]):
								if z != ' ':
								#	print('/' + z + '/')
									password = password + z
								else:
									break
						#	print(password)
							if user_pwd == password:
								print('-------------------------------')
								ups_name = request.form.get('ups_name')
								for x in list(ups_name):
									if x == ' ':
										errorCode = 1
										break
								if ups_name != '' and errorCode != 1:
									conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
									cursor = conn.cursor()
									temp = "UPDATE ups SET uName = '" + ups_name + "' WHERE uId = '" + ups_id +"' AND mId = '" + user_id + "'"
								#	print(temp)
									cursor.execute(temp)
									conn.commit()
									cursor.close()
									error = error + "設備名稱 / "
								else:
									print('ups_name Not Change !')
									print('-------------------------------')
								ups_ip = request.form.get('ups_ip')
								for x in list(ups_ip):
									if x == ' ':
										errorCode = 1
										break
								if ups_ip != '' and errorCode != 1:
									try:
										ip = ups_ip.split(":")[0].split('.')
										port = int(ups_ip.split(":")[1])
									except:
										errorCode = 1
								#	print("IP : " + ip[0] + "." + ip[1] + "." + ip[2] + "." + ip[3])
								#	print("PORT : " + str(port))
									if ups_ip != '' and errorCode != 1 and len(ip) == 4 and int(ip[0]) <= 254 and int(ip[1]) <= 254 and int(ip[2]) <= 254 and int(ip[3]) <= 254 and port <= 30080:
										print("ups_ip : " + ups_ip)
										conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
										cursor = conn.cursor()
										temp = "UPDATE ups SET uIP = '" + ups_ip + "' WHERE uId = '" + ups_id +"' AND mId = '" + user_id + "'"
									#	print(temp)
										cursor.execute(temp)
										conn.commit()
										conn.close()
										error = error + "託管IP / "
									else:
										print('ups_ip Error !')
										print('-------------------------------')
										error = error + '請確認輸入的託管 IP'
										try:
											ups_id = list(find_ups(user_id)[0])[0]
										except:
											ups_id = 'NULL'
										return render_template('upsReplace.html', error = error, msg = find_ups(user_id), user_id = user_id, ups_id = ups_id)
								else:
									print('ups_ip Not Change !')
									print('-------------------------------')
								ups_create = request.form.get('ups_create')
								if ups_create != 'None':
									print("ups_creat : " + ups_create)
									conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
									cursor = conn.cursor()
									temp = "UPDATE ups SET uFactory = '" + ups_create + "' WHERE uId = '" + ups_id +"' AND mId = '" + user_id + "'"
								#	print(temp)
									cursor.execute(temp)
									conn.commit()
									cursor.close()
									error = error + "生產廠區 / "
								else:
									print('ups_create Not Change !')
									print('-------------------------------')
								ups_model = request.form.get('ups_model')
								if ups_model != 'None':
									print("ups_model : " + ups_model)
									ups_unit = request.form.get('ups_unit')
									conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
									cursor = conn.cursor()
									temp = "UPDATE ups SET uModel = '" + ups_model + "', uUnit = '" + ups_unit + "' WHERE uId = '" + ups_id +"' AND mId = '" + user_id + "'"
								#	print(temp)
									cursor.execute(temp)
									conn.commit()
									cursor.close()
									error = error + "設備系列&容量 / "
								else:
									print('ups_model Not Change !')
									print('-------------------------------')
								ups_locate = request.form.get('ups_locate')
								for x in list(ups_locate):
									if x == ' ':
										errorCode = 1
										break
								if ups_locate != '' and errorCode != 1:
									conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
									cursor = conn.cursor()
									temp = "UPDATE ups SET uDistance = '" + ups_locate + "' WHERE uId = '" + ups_id +"' AND mId = '" + user_id + "'"
								#	print(temp)
									cursor.execute(temp)
									conn.commit()
									cursor.close()
									error = error + "設備地點 / "
								else:
									print('ups_locate Not Change !')
									print('-------------------------------')
								ups_collect = request.form.get('ups_collect')
								if ups_collect != None:
									ups_collect=1
									error = error + "參與資料收集 / "
								else:
									ups_collect=0
									error = error + "取消資料收集 / "
								print("ups_collect : " + str(ups_collect))
								print('-------------------------------')
								conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
								cursor = conn.cursor()
								temp = "UPDATE ups SET uCollect = '" + str(ups_collect) + "' WHERE uId = '" + ups_id +"' AND mId = '" + user_id + "'"
							#	print(temp)
								cursor.execute(temp)
								conn.commit()
								cursor.close()
								print('驗證成功')
								print('-------------------------------')
								error = error + '驗證成功'
								try:
									ups_id = list(find_ups(user_id)[0])[0]
								except:
									ups_id = 'NULL'
								return render_template('upsReplace.html', msg = find_ups(user_id), error = error, user_id = user_id, ups_id = ups_id)	
							else:
								errorCode = 1
						else:
							errorCode = 1
					else:
						errorCode = 1
				if x == len(upsList) - 1:
					errorCode = 1		
		else:
			errorCode = 1				
		if (errorCode == 1):
			print('ups_id Error !')
			print('-------------------------------')
			error = '請確認輸入的設備資料'
			try:
				ups_id = list(find_ups(user_id)[0])[0]
			except:
				ups_id = 'NULL'
			return render_template('upsReplace.html', msg = find_ups(user_id), error = error, user_id = user_id, ups_id = ups_id)			

@app.route('/ups_delete/<user_id>', methods=['GET', 'POST'])
def ups_delete(user_id):
	print('-------------------------------')
	print("UPS Delete Client IP : " + request.remote_addr)
	errorCode = 0
	if request.method == 'GET':	
		print('-------------------------------')
		error = ''
		conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
		cursor = conn.cursor()
		temp = "SELECT mId FROM member"
		cursor.execute(temp)
		memberList = cursor.fetchall()
		print(memberList)
		conn.commit()
		cursor.close()
		tmp = ''
		for x in range(0, len(memberList)):
			tmp = ''
			for y in list(str(memberList[x]).split("'")[1]):
				if y != ' ':
				#	print('/' + y + '/')
					tmp = tmp + y
				else:
					break
			print(tmp)
			if tmp == user_id:
				conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
				cursor = conn.cursor()
				temp = "SELECT mIP FROM member WHERE mId = '" + user_id + "'"
			#	print(temp)
				cursor.execute(temp)
				ipList = cursor.fetchall()
				conn.commit()
				cursor.close()
				tmp = ''
				for z in list(str(ipList[0]).split("'")[1]):
					if z != ' ':
					#	print('/' + z + '/')
						tmp = tmp + z
					else:
						break
				if tmp == request.remote_addr:			
					print('Login IP :' + tmp)
					try:
						ups_id = list(find_ups(user_id)[0])[0]
					except:
						ups_id = 'NULL'
					return render_template('upsDelete.html', msg = find_ups(user_id), user_id = user_id, ups_id = ups_id)
				else:
					print('USER NOT ON Member List !')
					print('-------------------------------')
					return redirect('/login')
			if x == len(memberList) - 1:
				print('USER NOT LOGIN !')
				print('-------------------------------')
				return redirect('/login')
	else:
		print('-------------------------------')
	#	print (request.form)
		ups_id = request.form.get('ups_id')
		for x in list(ups_id):
			if x == ' ':
				errorCode = 1
			break
		if ups_id != '' and errorCode == 0 and len(ups_id) <= 10 and len(ups_id) >= 4:
			print("ups_id : " + ups_id)
			conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
			cursor = conn.cursor()
			cursor.execute('SELECT uId FROM ups')
			upsList = cursor.fetchall()
			cursor.close()
			for x in range(0, len(upsList)):
			#	print(str(upsList[x]))
				tmp = ''
				for y in list(str(upsList[x]).split("'")[1]):
					if y != ' ':
					#	print('/' + y + '/')
						tmp = tmp + y
					else:
						break
				if tmp == ups_id:	
					print("user_id : " + user_id)
					conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
					cursor = conn.cursor()
					cursor.execute("SELECT mId FROM ups WHERE uId = '" + ups_id + "'")
					memberList = cursor.fetchall()
					conn.close()
					tmp = ''
					for y in list(str(memberList[0]).split("'")[1]):
						if y != ' ':
						#	print('/' + y + '/')
							tmp = tmp + y
						else:
							break
					if tmp == user_id:
						user_pwd = request.form.get('user_pwd')
						for x in list(user_pwd):
							if x == ' ':
								errorCode = 1
								break
						if user_pwd != '' and errorCode != 1:
							conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
							cursor = conn.cursor()
							temp = "SELECT mPassword FROM member WHERE mId = '" + tmp + "'"
						#	print(temp)
							cursor.execute(temp)
							checkPassword = cursor.fetchall()
							print(checkPassword)
							cursor.close()
							checkMember = 0
							password = ''
							for z in list(str(checkPassword[0]).split("'")[1]):
								if z != ' ':
								#	print('/' + z + '/')
									password = password + z
								else:
									break
							if user_pwd == password:
								print("password : PASS !")
								conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
								cursor = conn.cursor()
								temp = "DELETE FROM ups WHERE uId = '" + ups_id + "'"
							#	print(temp)
								cursor.execute(temp)
								temp = "DELETE FROM ups_in WHERE uId = '" + ups_id + "'"
							#	print(temp)
								cursor.execute(temp)
								temp = "DELETE FROM ups_out WHERE uId = '" + ups_id + "'"
							#	print(temp)
								cursor.execute(temp)
								temp = "DELETE FROM ups_battery WHERE uId = '" + ups_id + "'"
							#	print(temp)
								cursor.execute(temp)
								conn.commit()
								ups_id_delete = ups_id
								cursor.close()
								try:
									ups_id = list(find_ups(user_id)[0])[0]
								except:
									ups_id = 'NULL'
								error = 'UPS 設備' + ups_id_delete + '刪除成功'
								return render_template('upsDelete.html', user_id = user_id, error = error, msg = find_ups(user_id), ups_id = ups_id)
						else:
							errorCode = 1
					else:
						errorCode = 1
				if x == len(upsList) - 1 and errorCode != 1:
						print('ups_id Error !')
						errorCode = 1
		else:
			errorCode = 1
		if errorCode == 1:
			print("Delete Data Error !")
			print('-------------------------------')
			error = "請確認輸入資料"
			try:
				ups_id = list(find_ups(user_id)[0])[0]
			except:
				ups_id = 'NULL'
			return render_template('upsDelete.html', user_id = user_id, error = error, msg = find_ups(user_id), ups_id = ups_id)

def get_avg(date, ups_id):
	temp = "SELECT ups_in.uid, AVG(iFreq) AS avg_iFreq, AVG(iVolt) AS avg_iVolt, AVG(oFreq) AS avg_oFreq ,AVG(oAmp) AS avg_oAmp, AVG(oVolt) AS avg_oVolt, AVG(oWatt) AS avg_oWatt, AVG(oLoad) AS avg_oLoad, AVG(bLevel) AS avg_bLevel, AVG(bVolt) AS avg_bVolt, AVG(bTemp) AS avg_bTemp, uIP, uName, uDistance, uNumber FROM ups_in INNER JOIN ups_battery on ups_in.uId = ups_battery.uId and ups_battery.bTime = ups_in.iTime INNER JOIN ups_out on ups_in.uId = ups_out.uId and ups_in.iTime = ups_out.oTime INNER JOIN ups on ups_in.uId = ups.uId WHERE DATENAME(WEEKDAY, iTime) = '" + date + "' and ups_in.uId = '" + ups_id + "' GROUP BY ups_in.uId, ups_out.oLine, uIP, uName, uDistance, uNumber"
#	temp = "SELECT ups_in.uid, iTime, AVG(iFreq) AS avg_iFreq, AVG(iVolt) AS avg_iVolt, AVG(oFreq) AS avg_oFreq ,AVG(oAmp) AS avg_oAmp, AVG(oVolt) AS avg_oVolt, AVG(oWatt) AS avg_oWatt, AVG(oLoad) AS avg_oLoad, AVG(bLevel) AS avg_bLevel, AVG(bVolt) AS avg_bVolt, AVG(bTemp) AS avg_bTemp, uIP, uName, uDistance, uNumber FROM ups_in INNER JOIN ups_battery on ups_in.uId = ups_battery.uId and ups_battery.bTime = ups_in.iTime INNER JOIN ups_out on ups_in.uId = ups_out.uId and ups_in.iTime = ups_out.oTime INNER JOIN ups on ups_in.uId = ups.uId WHERE DATENAME(WEEKDAY, iTime) = 'Monday' AND ups_in.uId = 'U001' GROUP BY ups_in.uId, ups_out.oLine, uIP, uName, uDistance, uNumber, iTime;"
	conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
	cursor = conn.cursor()
	cursor.execute(temp)
	dataList = cursor.fetchall()
	conn.commit()
	cursor.close()
	return dataList

def get_avg_array(ups_id):
	msg = ''
	avg_iFreq = [0, 0, 0, 0, 0, 0, 0]
	avg_iVolt = [0, 0, 0, 0, 0, 0, 0]
	avg_oFreq = [0, 0, 0, 0, 0, 0, 0]
	avg_oAmp = [0, 0, 0, 0, 0, 0, 0]
	avg_oVolt = [0, 0, 0, 0, 0, 0, 0]
	avg_oWatt = [0, 0, 0, 0, 0, 0, 0]
	avg_oLoad = [0, 0, 0, 0, 0, 0, 0]
	avg_bLevel = [0, 0, 0, 0, 0, 0, 0]
	avg_bVolt = [0, 0, 0, 0, 0, 0, 0]
	avg_bTemp = [0, 0, 0, 0, 0, 0, 0]
#	print(get_avg('Monday', 'U001')[0])
#	print(get_avg('Tuesday', 'U001')[0])
	try:
		tmp = list(get_avg('Monday', ups_id)[0])
		print(tmp)
		avg_iFreq[0] = round(tmp[1], 4)
		avg_iVolt[0] = round(tmp[2], 4)
		avg_oFreq[0] = round(tmp[3], 4)
		avg_oAmp[0] = round(tmp[4], 4)
		avg_oVolt[0] = round(tmp[5], 4)
		avg_oWatt[0] = round(tmp[6], 4)
		avg_oLoad[0] = tmp[7]
		avg_bLevel[0] = tmp[8]
		avg_bVolt[0] = round(tmp[9], 4)
		avg_bTemp[0] = tmp[10]
		ups_name = tmp[12]
		ups_locate = tmp[13]
		print(avg_oVolt[0])
		print(avg_iVolt[0])
		tmp = list(get_avg('Tuesday', ups_id)[0])
		avg_iFreq[1] = round(tmp[1], 4)
		avg_iVolt[1] = round(tmp[2], 4)
		avg_oFreq[1] = round(tmp[3], 4)
		avg_oAmp[1] = round(tmp[4], 4)
		avg_oVolt[1] = round(tmp[5], 4)
		avg_oWatt[1] = round(tmp[6], 4)
		avg_oLoad[1] = tmp[7]
		avg_bLevel[1] = tmp[8]
		avg_bVolt[1] = round(tmp[9], 4)
		avg_bTemp[1] = tmp[10]
		tmp = list(get_avg('Wednesday', ups_id)[0])
		avg_iFreq[2] = round(tmp[1], 4)
		avg_iVolt[2] = round(tmp[2], 4)
		avg_oFreq[2] = round(tmp[3], 4)
		avg_oAmp[2] = round(tmp[4], 4)
		avg_oVolt[2] = round(tmp[5], 4)
		avg_oWatt[2] = round(tmp[6], 4)
		avg_oLoad[2] = tmp[7]
		avg_bLevel[2] = tmp[8]
		avg_bVolt[2] = round(tmp[9], 4)
		avg_bTemp[2] = tmp[10]
		tmp = list(get_avg('ThursDay', ups_id)[0])
		avg_iFreq[3] = round(tmp[1], 4)
		avg_iVolt[3] = round(tmp[2], 4)
		avg_oFreq[3] = round(tmp[3], 4)
		avg_oAmp[3] = round(tmp[4], 4)
		avg_oVolt[3] = round(tmp[5], 4)
		avg_oWatt[3] = round(tmp[6], 4)
		avg_oLoad[3] = tmp[7]
		avg_bLevel[3] = tmp[8]
		avg_bVolt[3] = round(tmp[9], 4)
		avg_bTemp[3] = tmp[10]
		tmp = list(get_avg('Friday', ups_id)[0])
		avg_iFreq[4] = round(tmp[1], 4)
		avg_iVolt[4] = round(tmp[2], 4)
		avg_oFreq[4] = round(tmp[3], 4)
		avg_oAmp[4] = round(tmp[4], 4)
		avg_oVolt[4] = round(tmp[5], 4)
		avg_oWatt[4] = round(tmp[6], 4)
		avg_oLoad[4] = tmp[7]
		avg_bLevel[4] = tmp[8]
		avg_bVolt[4] = round(tmp[9], 4)
		avg_bTemp[4] = tmp[10]
		tmp = list(get_avg('Saturday', ups_id)[0])
		avg_iFreq[5] = round(tmp[1], 4)
		avg_iVolt[5] = round(tmp[2], 4)
		avg_oFreq[5] = round(tmp[3], 4)
		avg_oAmp[5] = round(tmp[4], 4)
		avg_oVolt[5] = round(tmp[5], 4)
		avg_oWatt[5] = round(tmp[6], 4)
		avg_oLoad[5] = tmp[7]
		avg_bLevel[5] = tmp[8]
		avg_bVolt[5] = round(tmp[9], 4)
		avg_bTemp[5] = tmp[10]
		tmp = list(get_avg('Sunday', ups_id)[0])
		avg_iFreq[6] = round(tmp[1], 4)
		avg_iVolt[6] = round(tmp[2], 4)
		avg_oFreq[6] = round(tmp[3], 4)
		avg_oAmp[6] = round(tmp[4], 4)
		avg_oVolt[6] = round(tmp[5], 4)
		avg_oWatt[6] = round(tmp[6], 4)
		avg_oLoad[6] = tmp[7]
		avg_bLevel[6] = tmp[8]
		avg_bVolt[6] = round(tmp[9], 4)
		avg_bTemp[6] = tmp[10]
	except:
		msg = '請確認 UPS 是否存在與掛載'
		conn = pymssql.connect(server="163.17.136.65", user="1410432021", password="H124906356a", database="1410432021")
		cursor = conn.cursor()
		tmp = "SELECT uId, uIP, uName, uNumber, uDistance FROM ups WHERE uId = '" + ups_id + "'"
	#	print(tmp)
		cursor.execute(tmp)
		dataList = cursor.fetchall()
		conn.commit()
		cursor.close()
		try:
			temp = list(dataList[0])
			ups_id = temp[0]
			ups_ip = temp[1]
			ups_name = temp[2]
			ups_locate = temp[3]
			ups_number = temp[4]
		except:
			ups_id = ups_id
			ups_ip = 'NULL'
			ups_name = 'NULL'
			ups_locate = 'NULL'
			ups_number = 'NULL'
#	print(avg_iFreq)
#	print(avg_iVolt)
#	print(avg_oFreq)
#	print(avg_oVolt)
#	print(avg_oAmp)
#	print(avg_iFreq)
#	print(avg_oWatt)
#	print(avg_oLoad)
#	print(avg_bLevel)
#	print(avg_bVolt)
#	print(avg_bTemp)
	return  avg_iFreq, avg_oVolt, avg_bLevel, avg_bTemp, avg_bVolt, avg_iVolt, avg_oAmp, avg_oLoad, avg_oFreq, avg_oWatt, ups_name, ups_locate, ups_name, ups_locate, ups_id, msg	

@app.route('/history/<ups_id>', methods=['GET'])
def history_tmp(ups_id):
	temp = get_avg_array(ups_id)
	avg_iFreq = temp[0]
	avg_iVolt = temp[5]
	avg_oFreq = temp[8]
	avg_oAmp = temp[6]
	avg_oVolt = temp[1]
	avg_oWatt = temp[9]
	avg_oLoad = temp[7]
	avg_bLevel = temp[2]
	avg_bVolt = temp[4]
	avg_bTemp = temp[3]
	ups_name = temp[10]
	ups_locate = temp[11]
	msg = temp[15]
	print(avg_iFreq)
	print(avg_iVolt)
	print(avg_oFreq)
	print(avg_oVolt)
	print(avg_oAmp)
	print(avg_iFreq)
	print(avg_oWatt)
	print(avg_oLoad)
	print(avg_bLevel)
	print(avg_bVolt)
	print(avg_bTemp)
	return render_template('/history/upsHistory.html', msg = msg, ups_id = ups_id, avg_iFreq = avg_iFreq, avg_oVolt = avg_oVolt, avg_bLevel = avg_bLevel, avg_bTemp = avg_bTemp, avg_bVolt = avg_bVolt, avg_iVolt = avg_iVolt, avg_oAmp = avg_oAmp, avg_oLoad = avg_oLoad, avg_oFreq = avg_oFreq, avg_oWatt = avg_oWatt, ups_name = ups_name, ups_locate = ups_locate)

@app.route('/history/<user_id>/<ups_id>', methods=['POST', 'GET'])
def history(user_id, ups_id):
	if request.method == 'GET':
		temp = get_avg_array(ups_id)
		avg_iFreq = temp[0]
		avg_iVolt = temp[5]
		avg_oFreq = temp[8]
		avg_oAmp = temp[6]
		avg_oVolt = temp[1]
		avg_oWatt = temp[9]
		avg_oLoad = temp[7]
		avg_bLevel = temp[2]
		avg_bVolt = temp[4]
		avg_bTemp = temp[3]
		ups_name = temp[10]
		ups_locate = temp[11]
		msg = temp[15]
		print(avg_iFreq)
		print(avg_iVolt)
		print(avg_oFreq)
		print(avg_oVolt)
		print(avg_oAmp)
		print(avg_iFreq)
		print(avg_oWatt)
		print(avg_oLoad)
		print(avg_bLevel)
		print(avg_bVolt)
		print(avg_bTemp)
		return render_template('/history/userHistory.html', user_id = user_id, msg = msg ,upsList = find_ups(user_id) ,ups_id = ups_id, avg_iFreq = avg_iFreq, avg_oVolt = avg_oVolt, avg_bLevel = avg_bLevel, avg_bTemp = avg_bTemp, avg_bVolt = avg_bVolt, avg_iVolt = avg_iVolt, avg_oAmp = avg_oAmp, avg_oLoad = avg_oLoad, avg_oFreq = avg_oFreq, avg_oWatt = avg_oWatt, ups_name = ups_name, ups_locate = ups_locate)
	else:
		ups_id_tmp = ups_id
		print("UPS TMP : " + ups_id_tmp)
		ups_id = request.form.get('ups_id')
		if ups_id != None and ups_id != '':
			Search = url_for('history', ups_id = ups_id, user_id = user_id)
			return redirect(Search)
		elif ups_id == '':
			Search = url_for('history', ups_id = ups_id_tmp, user_id = user_id)
			return redirect(Search)
		else:	
			Search = url_for('history', ups_id = ups_id_tmp, user_id = user_id)
			return redirect(Search)


if __name__ == '__main__':
#	app.run(debug = True)
	app.run(host = '0.0.0.0', port = 3000, debug = True)
	
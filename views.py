#!/usr/bin/env python
#coding=utf-8

import sys,os,time
import defines,utils
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

#ok
def setChinese():
	session["lang"]="cn"
	return redirect(request.referrer)
#ok
def setEnglish():
	session["lang"]="en"
	return redirect(request.referrer)
#ok
def index():
	contents=utils.genContent()
	contents["user"]=g.user
	if "lang" not in session:
		session["lang"]="en"
	if utils.validLogin([1,2,3,4,5,6,7,8,9]):
		return render_template("%s/index.html" % session["lang"],info=contents)
	else:
		return render_template("%s/index.html" % session["lang"],info={})
#ok
def config():
	contents=utils.genContent()
	contents["user"]=g.user
	if "lang" not in session:
		session["lang"]="en"
	if utils.validLogin([9]):
		return render_template("%s/config.html" % session["lang"],info=contents)
	else:
		return render_template("%s/index.html" % session["lang"],info={})		
#ok
def servers():
	contents=utils.genContent()
	contents["user"]=g.user
	if "lang" not in session:
		session["lang"]="en"
	if utils.validLogin([9]):
		contents["servers"]=utils.queryServers()
		return render_template("%s/servers.html" % session["lang"],info=contents)
	else:
		return render_template("%s/index.html" % session["lang"],info={})
#ok
def ajax(action,id):
	contents=utils.genContent()
	contents["user"]=g.user
	if "lang" not in session:
		session["lang"]="en"
	if utils.validLogin([9]):
		if action=='serverdetail':
			contents["server"]=utils.queryServer(id)
			return render_template("%s/ajax_serverdetail.html" % session["lang"],info=contents)
#ok
def virtualHosts():
	contents=utils.genContent()
	contents["user"]=g.user
	if "lang" not in session:
		session["lang"]="en"
	if utils.validLogin([9]):
		contents["vhosts"]=utils.queryVhosts()
		contents["hosts"]=utils.queryServer4Template()
		contents["apps"]=utils.queryApps4Template()
		contents["vhosts"]=utils.queryVhosts()
		return render_template("%s/virtualhosts.html" % session["lang"],info=contents)
	else:
		return render_template("%s/index.html" % session["lang"],info={})
	
def system():
	utils.validLogin()
	contents=utils.genContent()
	contents["user"]=g.user
	contents["zone_title"]="System"
	return render_template("system.html",info=contents)

def newServer():
	utils.validLogin()
	contents=utils.genContent()
	contents["user"]=g.user
	contents["zone_title"]="New Server"
	return render_template("newserver.html",info=contents)

def newAdmin():
	utils.validLogin()
	contents=utils.genContent()
	contents["user"]=g.user
	contents["zone_title"]="New Admin"
	return render_template("newadmin.html",info=contents)

def newReseller():
	utils.validLogin()
	contents=utils.genContent()
	contents["user"]=g.user
	contents["zone_title"]="New Reseller"
	return render_template("newreseller.html",info=contents)

def newCustomer():
	utils.validLogin()
	contents=utils.genContent()
	contents["user"]=g.user
	contents["zone_title"]="New Customer"
	return render_template("newcustomer.html",info=contents)

def allUsers():
	utils.validLogin()
	contents=utils.genContent()
	contents["user"]=g.user
	contents["zone_title"]="All Users"
	contents["users"]=utils.queryAllUsers()
	return render_template("allusers.html",info=contents)

def editUser(id):
	utils.validLogin()
	contents=utils.genContent()
	contents["user"]=g.user
	contents["zone_title"]="Edit User"
	contents["user"]=utils.queryUser4Edit(id)
	return render_template("edituser.html",info=contents)
	
def addVhost():
	utils.validLogin()
	contents=utils.genContent()
	contents["user"]=g.user
	contents["zone_title"]="Add Virtual Host"
	contents["users"]=utils.queryUsers4Select()
	contents["hosts"]=utils.queryHosts4Select()
	contents["apps"]=utils.queryApps4Select()
	return render_template("addvhost.html", info=contents)
	
def post_addvhost():
	utils.validLogin()
	if request.method=="POST":
		subdomain = request.form['subdomain']
		maindomain = request.form['maindomain']
		hostid=request.form["hostid"]
		if (subdomain.strip()=='') or (maindomain.strip()==''):
			flash("Please eneter the Sub Domain and Main Domain")
			return redirect("/addvhost")
		if utils.subdomainExists(subdomain,maindomain):
			flash("The Sub Domain exists. Please re-enter.")
			return redirect("/addvhost")
		if (hostid=="-1"):
			flash("Please select the Host parked on.")
			return redirect("/addvhost")
		domainalias = request.form['domainalias']
		userid=request.form['userid']
		hostid=request.form['hostid']
		appid=request.form['appid']
		adminuser=request.form['adminuser']
		adminpwd=request.form['adminpwd']
		createdate=time.strftime('%Y%m%d',time.localtime(time.time()))
		expiredate=request.form["expiredate"]
		if expiredate.strip()=='':
			expiredate="0"
		utils.addVhost(subdomain,maindomain,domainalias,userid,hostid,appid,adminuser,adminpwd,createdate,expiredate)
		return redirect('/virtualhosts')
		
def applications():
	utils.validLogin()
	contents=utils.genContent()
	contents["user"]=g.user
	contents["zone_title"]="Applications"
	return render_template("applications.html",info=contents)

def profile():
	utils.validLogin()
	contents=utils.genContent()
	contents["user"]=g.user
	contents["zone_title"]="Profile"
	return render_template("profile.html",info=contents)

def editServer(id):
	utils.validLogin()
	contents=utils.genContent()
	contents["user"]=g.user
	contents["zone_title"]="Edit Server"
	contents["server"]=utils.queryServer(id)
	return render_template("editserver.html",info=contents)

def enableServer(id):
	utils.validLogin()
	utils.setServer("senabled",1,id)
	return redirect("/servers") 

def disableServer(id):
	utils.validLogin()
	utils.setServer("senabled",0,id)
	return redirect("/servers") 

def removeServer(id):
	utils.validLogin()
	utils.removeServer(id)
	return redirect("/servers") 

def post_newserver():
	utils.validLogin()
	if request.method=="POST":
		if ('servername' in request.form) and ('serverip' in request.form):
			servername=request.form["servername"]
			serverip=request.form["serverip"]
			serverport=request.form["serverport"]
			if "enabled" in request.form:
				senabled="1"
			else:
				senabled="0"
			if "apache" in request.form:
				sapache="1"
			else:
				sapache="0"
			if "mysql" in request.form:
				smysql="1"
			else:
				smysql="0"
			utils.insertServer(servername,serverip,serverport,senabled,sapache,smysql)
			return redirect('/servers')
		else:
			flash('Please enter Server Name and IP Address.')
			return recirect('/newserver')
	else:
		return redirect("/newserver")

def post_updateserver():
	utils.validLogin()
	if request.method=="POST":
		if ('servername' in request.form) and ('serverip' in request.form) and ('id' in request.form):
			servername=request.form["servername"]
			serverip=request.form["serverip"]
			serverport=request.form["serverport"]
			if "enabled" in request.form:
				senabled="1"
			else:
				senabled="0"
			if "apache" in request.form:
				sapache="1"
			else:
				sapache="0"
			if "mysql" in request.form:
				smysql="1"
			else:
				smysql="0"
			id=request.form["id"]
			utils.updateServer(servername,serverip,serverport,senabled,sapache,smysql,id)
			return redirect('/servers')
		else:
			flash('Please enter Server Name and IP Address.')
			return recirect('/editserver/%s' % request.form["id"])
	else:
		return redirect("/newserver")

def post_newadmin():
	utils.validLogin()
	if request.method=="POST":
		if ('uname' in request.form) and ('upwd' in request.form):
			uname=request.form['uname']
			upwd=request.form['upwd']
			if (uname.strip()=='') or (upwd.strip()==''):
				flash("Please enter the Name and Password.")
				return redirect('/newadmin')
			ucompany=request.form['ucompany']
			uemail=request.form['uemail']
			ucontact=request.form['ucontact']
			urefcode=request.form['urefcode']
			if not utils.userExists(uname):
				ugroup="9"
				uenabled="1"
				uparent="-1"
				utils.insertUser(uparent,uname,upwd,ucompany,uemail,ucontact,urefcode,ugroup,uenabled)
				return redirect('/allusers')
			else:
				flash("Username exists. Please re-enter.")
				return redirect('/newadmin')
	else:
		return redirect('/newadmin')

def post_updateUser():
	utils.validLogin()
	if request.method=='POST':
		id=request.form['id']
		uname = request.form['uname']
		ucompany = request.form['ucompany']
		uemail = request.form['uemail']
		ucontact = request.form['ucontact']
		urefcode= request.form['urefcode']
		if uname.strip()=='':
			flash('Please enter the Name.')
			return redirect('/edituser/%s' % id)
		else:
			utils.updateUser(id,uname,ucompany,uemail,ucontact,urefcode)
			return redirect('/allusers') 
	else:
		return redirect('/allusers')
		
def post_updateUpwd():
	utils.validLogin()
	if request.method=="POST":
		id=request.form["id"]
		upwd=request.form["upwd"]
		if upwd.strip()=="":
			flash("Please eneter the Password.")
			return redirect("/edituser/%s" % id)
		else:
			utils.updateUpwd(id,upwd)
			return redirect("/allusers")
	else:
		return redirect("/allusers")

def enableUser(id):
	utils.validLogin()
	utils.setUser('uenabled',"1",id)
	return redirect('/allusers')

def disableUser(id):
	utils.validLogin()
	utils.setUser('uenabled',"0",id)
	return redirect('/allusers')

def removeUser(id):
	utils.validLogin()
	utils.removeUser(id)
	return redirect("/allusers")

def callServer(action,id):
	return utils.callServer(action,id)
	
def login():
	if request.method=="POST":
		username=request.form["username"].strip()
		password=request.form["password"].strip()
		if (username == "" ) and (password ==""):
			flash("Please enter the username and password.")
			return redirect("/")
		else:
			r=utils.checkLogin(username,password)
			if r==-1:
				flash("Wrong username or password. Please re-enter.")
			else:
				session["uid"]=r
			return redirect("/")
def logout():
	del(session["uid"])
	g.user=None
	return redirect('/')

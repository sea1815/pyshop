#!/usr/bin/env python
#coding=utf-8

import sys,os
import ConfigParser
import MySQLdb
import httplib, urllib
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import defines,views,utils
 
reload(sys)  
sys.setdefaultencoding('utf8')

current_path = sys.path[0]

#读取设置文件config.ini，初始化defines里的全局变量
fconfig = "%s/%s" % (current_path,defines.CONFIG_FILE)
if os.path.exists(fconfig):
	cf = ConfigParser.ConfigParser()
	cf.read(fconfig)
	defines.DB_HOST = cf.get("db","host")
	defines.DB_USER = cf.get("db","user")
	defines.DB_PWD	= cf.get("db","pwd")
	defines.DB_NAME = cf.get("db","name")

app = Flask(__name__)
app.secret_key = "asd9922kjasdo99090luiemnmmbhhs"

@app.before_request
def before_request():
	g.db = utils.connect_db()
	g.user = None
	if 'uid' in session:
		g.user = utils.queryUser(session['uid'])
		if g.user["uenabled"]!=1:
			g.user=None
		
@app.after_request
def after_request(response):
	g.db.close()
	return response

app.add_url_rule('/', view_func=views.index)
app.add_url_rule('/cn', view_func=views.setChinese)
app.add_url_rule('/en', view_func=views.setEnglish)
app.add_url_rule('/config', view_func=views.config)
app.add_url_rule('/servers', view_func=views.servers)
app.add_url_rule('/virtualhosts', view_func=views.virtualHosts)

app.add_url_rule('/ajax/<string:action>/<int:id>', view_func=views.ajax)

app.add_url_rule('/login', view_func=views.login,methods=['POST'])
app.add_url_rule('/logout', view_func=views.logout)

'''app.add_url_rule('/system', view_func=views.system)
app.add_url_rule('/newserver', view_func=views.newServer)
app.add_url_rule('/servers', view_func=views.servers)
app.add_url_rule('/newadmin', view_func=views.newAdmin)
app.add_url_rule('/newreseller', view_func=views.newReseller)
app.add_url_rule('/newcustomer', view_func=views.newCustomer)
app.add_url_rule('/allusers', view_func=views.allUsers)
app.add_url_rule('/addvhost', view_func=views.addVhost)
app.add_url_rule('/virtualhosts', view_func=views.virtualHosts)
app.add_url_rule('/applications', view_func=views.applications)
app.add_url_rule('/profile', view_func=views.profile)
app.add_url_rule('/editserver/<int:id>',view_func=views.editServer)
app.add_url_rule('/enableserver/<int:id>',view_func=views.enableServer)
app.add_url_rule('/disableserver/<int:id>',view_func=views.disableServer)
app.add_url_rule('/removeserver/<int:id>',view_func=views.removeServer)
app.add_url_rule('/edituser/<int:id>',view_func=views.editUser)
app.add_url_rule('/enableuser/<int:id>',view_func=views.enableUser)
app.add_url_rule('/disableuser/<int:id>',view_func=views.disableUser)
app.add_url_rule('/removeuser/<int:id>',view_func=views.removeUser)

app.add_url_rule('/post_newserver',view_func=views.post_newserver,methods=['POST'])
app.add_url_rule('/post_updateserver',view_func=views.post_updateserver,methods=['POST'])
app.add_url_rule('/post_newadmin',view_func=views.post_newadmin,methods=['POST'])
app.add_url_rule('/post_updateuser',view_func=views.post_updateUser,methods=['POST'])
app.add_url_rule('/post_updateupwd',view_func=views.post_updateUpwd,methods=['POST'])
app.add_url_rule('/post_addvhost',view_func=views.post_addvhost,methods=['POST'])

app.add_url_rule('/call/<int:action>/<int:id>',view_func=views.callServer,methods=["GET"])
'''

if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0',port=8000)

'''
Created on 2012/11/3

@author: arbiter
'''
import webapp2
import drives
import json
import os
import jinja2
import fileman
from google.appengine.ext import db
from google.appengine.api import users

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env= jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                              autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
        
    def render_str(self, template,**params):
        t = jinja_env.get_template(template)
        return t.render(params)
    
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))
        
class userdb(db.Model):
    user_account = db.UserProperty(required = True)
    cloud_type = db.StringProperty(required=True,
                           choices=set(["dropbox", "googledrive", "skydrive", "box"]))
    access_token_key = db.StringProperty()
    access_token_secret = db.StringProperty()
    uid = db.StringProperty()
    refresh_token = db.StringProperty()
    email = db.EmailProperty()

class contactdb(db.Model):
    user_account = db.UserProperty(required = True)
    email = db.EmailProperty()
    message = db.StringProperty()

class contactUs(Handler):
    def get(self):
        self.render('contact.html')
    def post(self):
        user=users.get_current_user()
        email = self.request.get('email')
        message = self.request.get('message')
        if email and message:
            tmpdb = contactdb(user_account = user,
                              message = message,
                              email = email
                              )
            tmpdb.put()
            self.render('thankSub.html')

class MainPage(Handler):
    def get(self):
        providers = {
                        'Google'   : 'https://www.google.com/accounts/o8/id',
                        'Yahoo'    : 'yahoo.com',
                        'MySpace'  : 'myspace.com',
                        'AOL'      : 'aol.com',
                        'MyOpenID' : 'myopenid.com'
                        # add more here
                    }
        html = """
                <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
                <html xmlns="http://www.w3.org/1999/xhtml">
                    <head>
                        <title>MultiClouds Project</title>
                        <link rel="stylesheet" type="text/css" href="css/index.css">
                    </head>
                    <body>
                            <div id="upperdiv"></div>
                            <div id='content'>
                                <div id='welcome'>Welcome to MultiClouds</div>
                                <img id='logo' src="/images/logo2.jpg" alt="Logo" height="300" width="300">
                                <div id='loginban'>Please Login with your accounts!</div>
                                <div id='urls'>%s</div>
                            </div>
                            <div id="lowerdiv">
                                <a id='help' href="http://multiclouds.appspot.com/introduction/intro.html">Help Page</a>
                            </div>
                    </body>
                    
                </html>"""
        user = users.get_current_user()
        if user:  # signed in already
            self.redirect("/user")
        else:     # let user choose authenticator
            out=''
            for name, uri in providers.items():
                out+='<a href="%s"><img id="%slogo" src="/images/%s.jpg" alt="%s" height="25" width="70"></a>&nbsp' % (users.create_login_url(federated_identity=uri), name, name, name)
            self.response.out.write(html % out)

s=drives.skyDrive()
class AddSkyDrive(Handler):
    def get(self):
        code = self.request.get('code')
        if not code:
            self.redirect(s.get_auth_url())
        else:
            s.get_access_token(code=code)
            self.redirect("/user/skydriveinfo")
            
class skyDriveInfo(Handler):
    def get(self):
        json_user_info = s.get_user_info()
        user=users.get_current_user()
        q = db.GqlQuery("SELECT * FROM userdb WHERE user_account=:1 AND email=:2 AND cloud_type=:3 AND uid=:4"
                        ,user,json_user_info['emails']['account'],"skydrive",json_user_info['id'])
        if q.get()==None:
            dbtmp = userdb(user_account = user,
                       cloud_type = "skydrive",
                       refresh_token = s.refresh_token,
                       email = json_user_info['emails']['account'],
                       uid = json_user_info['id']
                    )
            dbtmp.put()
        self.render('thankSub.html')

g=drives.gdrive()
class AddGoogleDrive(Handler):
    def get(self):
        code = self.request.get('code')
        if not code:
            self.redirect(g.get_auth_url())
        else:
            g.get_access_token(code=code)
            self.redirect("/user/gdriveinfo")
        
class gDriveInfo(Handler):
    def get(self):
        try:
            user=users.get_current_user()
            json_user_info = g.get_user_info()
            q = db.GqlQuery("SELECT * FROM userdb WHERE user_account=:1 AND email=:2 AND cloud_type=:3",user,json_user_info['email'],"googledrive")
            if q.get()==None:
                dbtmp = userdb(user_account = user,
                           cloud_type = "googledrive",
                           refresh_token = g.refresh_token,
                           email = json_user_info['email']
                        )
                dbtmp.put()
        except:
            self.response.out.write('Notworking')
        self.render('thankSub.html')

d=drives.dropbox()
class AddDropbox(Handler):
    def get(self):
        user = users.get_current_user()
        uid = self.request.get("uid")
        oauth_token = self.request.get("oauth_token")
        not_approved = self.request.get("not_approved")
        if not_approved:
            self.response.out.write("You have to let me access to use this app")
        elif uid and oauth_token:
            q = db.GqlQuery("SELECT * FROM userdb WHERE uid=:1 AND user_account=:2 AND cloud_type=:3",uid,user,"dropbox")
            if q.get()==None:
                d.get_access_token()
                email = d.get_account_info()
                email = email['email']
                dbtmp = userdb(user_account = user,
                           cloud_type = "dropbox",
                           access_token_key = d.access_token.key,
                           access_token_secret = d.access_token.secret,
                           email=email,
                           uid = uid,
                        )
                dbtmp.put()
        else:
            self.redirect(d.get_dropbox_auth_url(self.request.uri))
        self.render('thankSub.html')

b=drives.box()
class AddBox(Handler): 
    def get(self):
        auth_token = self.request.get('auth_token')
        ticket = self.request.get('ticket')
        if not (auth_token and ticket):
            self.redirect(b.get_auth_url())
        else:
            b.input_auth_token(auth_token)
            self.redirect("/user/boxinfo")
            
class boxInfo(Handler):
    def get(self):
        user=users.get_current_user()
        json_user_info = b.get_account_info()
        q = db.GqlQuery("SELECT * FROM userdb WHERE user_account=:1 AND email=:2 AND uid=:3 AND cloud_type=:4",
                        user,json_user_info['login'],json_user_info['id'],"box")
        if q.get()==None:
            dbtmp = userdb(user_account = user,
                       cloud_type = "box",
                       access_token_key = b.auth_token,
                       email = json_user_info['login'],
                       uid = json_user_info['id']
                    )
            dbtmp.put()
        self.render('thankSub.html')
        
class AuthPage(Handler):
    def get(self):
        self.redirect("/adddropbox")
        
class getAllInfo(Handler):
    def get(self):
        query = "SELECT * FROM userdb WHERE user_account=:1"
        q = db.GqlQuery(query,users.get_current_user())
        al = []
        tmp = ''
        for i in q:
            if i.cloud_type == 'dropbox':
                td=drives.dropbox(access_token = i.access_token_key,
                                  access_token_secret = i.access_token_secret)
                try:
                    tmp = td.get_all_data()
                    tmp['cloudtype']='dropbox'
                except:
                    pass
                
            elif i.cloud_type == 'googledrive':
                tg=drives.gdrive(refresh_token=i.refresh_token)
                try:
                    tmp = tg.get_all_metadata(maxResults='10')
                    tmp['cloudtype']='googledrive'
                except:
                    pass

            elif i.cloud_type == 'skydrive':
                ts=drives.skyDrive(refresh_token=i.refresh_token)
                try:
                    tmp = ts.get_all_metadata()
                    tmp['cloudtype']='skydrive'
                except:
                    pass
                    
            elif i.cloud_type == 'box':
                tb=drives.box(auth_token = i.access_token_key)
                try:
                    tmp = tb.get_all_data()
                    tmp['cloudtype']='box'
                except:
                    pass
            al.append(tmp);
        self.response.out.write(fileman.get(json.dumps(al)))
                
class userPage(Handler):   
    def get(self):
        html="""
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <title>MultiClouds Project</title>
        <style>
            body {
                background-color: #c9ff96;
            }
            #menu
            {
                float : left;
                width : 180px;
                height: 300px;
                padding-left: 40px;
                line-height: 50px;
                font-size: 30px;
            }
            #menu p
            {
                font-weight: bold;
                color : blue;
                border-bottom : 1px dotted;
                text-decoration : none;
                background: lightgreen;
            }
            tr {
                text-align: center;
            }
            th
            {
                width:250px
            }
            </style>
            </head>
            <body>
                <div id="menu">
                    <p>&nbspB&nbspo&nbspx&nbsp.&nbspc&nbspo&nbspm&nbsp </p>
                    <p>&nbsp&nbsp&nbspDrop&nbspBox&nbsp&nbsp&nbsp </p>
                    <p>Google Drive&nbsp </p>
                    <p>&nbsp&nbsp&nbspSky&nbsp&nbsp Drive&nbsp&nbsp</p>
                </div>
                <p><br/></p>
                <p>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
                &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
                <input type="button" onClick="parent.location='http://multiclouds.appspot.com/user/addbox'" value="Extend Box">
                &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
                &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
                <input type="button" onClick="parent.location='http://multiclouds.appspot.com/user/adddropbox'" value="Extend Dropbox">
                &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
                &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
                <input type="button" onClick="parent.location='http://multiclouds.appspot.com/user/addgdrive'" value="Extend Google Drive">
                &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
                &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
                <input type="button" onClick="parent.location='http://multiclouds.appspot.com/user/addskydrive'" value="Extend SkyDrive">
                &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
                &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
                <input type="button" onClick="parent.location='http://multiclouds.appspot.com/user/getallinfo'" value="List All Data Info">
                <br/>
                </p><br/>
                <table>
                <tr>
                  <th class='title'>Box</th>
                  <th class='title'>DropBox</th>
                  <th class='title'>GoogleDrive</th>
                  <th class='title'>SkyDrive</th>
                </tr>
                %s
              </table>
                <br><br><br><br><br><br><br>
                &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
                &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
                &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
                &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
                &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
                &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
                <a href="http://multiclouds.appspot.com/user/contactus" style="font-size: 25px; border: 1px outset green; color: green; text-shadow: 3px 3px lightgreen;" >Contact Us</a>
                &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
                <a href="%s" style="font-size: 25px; border: 1px outset green; color: green; text-shadow: 3px 3px lightgreen;">Log Out</a>
            </body>
        </html>
        """
        query = "SELECT * FROM userdb WHERE user_account=:1"
        q = db.GqlQuery(query,users.get_current_user())
        dic={"box":[],"dropbox":[],"googledrive":[],"skydrive":[]}
        if q:
            for i in q:
                for j in dic.keys():
                    if i.cloud_type == j:
                        if i.email:
                            dic[j].append(i.email)
                            break
            out=""
            m=0
            for j in dic.items():
                m=max(m,len(j[1]))
            for i in range(0,m):
                out+="<tr>"
                for j in dic.items():
                    out+="<td>"
                    if len(j[1])>i:
                        out+=j[1][i]
                    out+="</td>"
                out+="</tr>"
        urls=''
        urls += "<a href=%s>Add Dropbox</a>" % (self.request.uri+"/adddropbox")
        urls += "<a href=%s>Add GoogleDrive</a>" % (self.request.uri+"/addgdrive")
        urls += "<a href=%s>Add SkyDrive</a>" % (self.request.uri+"/addskydrive")
        urls += "<a href=%s>Add Box</a>" % (self.request.uri+"/addbox")
        urls += "<a href=%s>All Info</a>" % (self.request.uri+"/getallinfo")
        urls += "<a href=%s>Contact Us</a>" % (self.request.uri+"/contactus")
        html=html%(out,users.create_logout_url("http://multiclouds.appspot.com"))
        self.response.out.write(html)


app = webapp2.WSGIApplication([('/', MainPage),
                              ('/auth', AuthPage),
                              ('/user/adddropbox', AddDropbox),
                              ('/user/addgdrive', AddGoogleDrive),
                              ('/user/addskydrive', AddSkyDrive),
                              ('/user/addbox', AddBox),
                              ('/user', userPage),
                              ('/user/getallinfo', getAllInfo),
                              ('/user/gdriveinfo',gDriveInfo),
                              ('/user/skydriveinfo',skyDriveInfo),
                              ('/user/boxinfo',boxInfo),
                              ('/user/contactus',contactUs)],
                              debug=True)
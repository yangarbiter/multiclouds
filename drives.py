import oauth_helper
import urllib2
import urllib
import json
import unicodedata
from xml.dom import minidom
class auth(object):
    def http_request(self, url, headers={}, data={}, dataappend=""):
        req = urllib2.Request(url)
        for i in headers.items():
            req.add_header(i[0], i[1])
        if dataappend or data:
            data=urllib.urlencode(data)+dataappend
            req.add_data(data)
        return urllib2.urlopen(req).read()
    
class box(auth):
    def __init__(self, auth_token = ''):
        self.api_key = ' '
        self.auth_token = auth_token
        self.ticket = ''
    
    def get_ticket(self):
        url = 'https://www.box.com/api/1.0/rest?action=get_ticket&api_key='+self.api_key
        r = self.http_request(url)
        tmp = minidom.parseString(r)
        self.ticket=tmp.getElementsByTagName('ticket')[0].childNodes[0].nodeValue
        return self.ticket
    
    def get_auth_url(self):
        url = 'https://www.box.com/api/1.0/auth/'+unicodedata.normalize('NFKD', self.get_ticket()).encode('ascii','ignore')
        return url

    def get_auth_token(self):
        if not self.auth_token :
            url = 'https://www.box.com/api/1.0/rest?action=get_auth_token&api_key='+self.api_key
            url += '&ticket='+self.ticket
            r = self.http_request(url)
            tmp = minidom.parseString(r)
            self.auth_token = tmp.getElementsByTagName('auth_token')[0].childNodes[0].nodeValue
        return self.auth_token
        
    def get_account_info(self):
        if self.auth_token=='':
            self.get_auth_token()
        header = {'Authorization':'BoxAuth api_key=%s&auth_token=%s' % (self.api_key,self.auth_token)}
        r = self.http_request("https://api.box.com/2.0/users/me", headers=header)
        return json.loads(r)
    
    def input_auth_token(self,auth_token):
        self.auth_token=auth_token
    
    def get_data(self, folder_id):
        header = {'Authorization':'BoxAuth api_key=%s&auth_token=%s' % (self.api_key,self.auth_token)}
        url = 'https://api.box.com/2.0/folders/%s/items' % folder_id
        r = self.http_request(url, headers=header)
        tmp = json.loads(r)
        for i in tmp["entries"]:
            if i['type'] == 'folder':
                i['child'] = self.get_data(i['id'])
        return tmp
        
    def get_all_data(self):
        self.data = self.get_data('0')
        return self.data
    
class skyDrive(auth):
    def __init__(self,refresh_token=''):
        self.CLIENT_ID = ''
        self.CLIENT_SECRET = ''
        self.OAUTH_SCOPE = 'wl.offline_access+wl.emails+wl.skydrive+wl.basic'
        self.REDIRECT_URI = 'http://multiclouds.appspot.com/user/addskydrive'
        self.refresh_token = refresh_token
    def get_auth_url(self):
        url="https://login.live.com/oauth20_authorize.srf?"
        url+="client_id="+self.CLIENT_ID
        url+="&scope="+self.OAUTH_SCOPE
        url+='&response_type=code'
        url+="&redirect_uri="+self.REDIRECT_URI
        return url
    def get_user_info(self):
        access_token=self.get_access_token()
        header={"access_token": access_token}
        url = "https://apis.live.net/v5.0/me?access_token="
        url += access_token
        return json.loads(self.http_request(url,headers=header))
    def get_access_token(self,code=''):
        header={"Content-type": "application/x-www-form-urlencoded"}
        if self.refresh_token=='':
            data={  "client_id" : self.CLIENT_ID,
                    "client_secret" : self.CLIENT_SECRET,
                    "redirect_uri" : self.REDIRECT_URI,
                    "grant_type": "authorization_code",}
            tmp = "&code=%s" % code
            r = self.http_request("https://login.live.com/oauth20_token.srf",
                                  headers=header, data=data, dataappend=tmp)
            r = json.loads(r)
            self.refresh_token=r["refresh_token"]
            return r["access_token"]
        else:
            data={  "client_id" : self.CLIENT_ID,
                   "client_secret" : self.CLIENT_SECRET,
                   "grant_type": "refresh_token",
                   "refresh_token": self.refresh_token}
            r = self.http_request("https://login.live.com/oauth20_token.srf",
                                 headers=header, data=data)
            r = json.loads(r)
            return r['access_token']
    def get_all_metadata(self):
        access_token = self.get_access_token()
        header={"access_token": access_token}
        url = "https://apis.live.net/v5.0/me/skydrive/files?access_token="
        url += access_token
        return json.loads(self.http_request(url,headers=header))
      
class gdrive(auth):
    def __init__(self,refresh_token=''):
        self.CLIENT_ID = ''
        self.CLIENT_SECRET = ''
        self.OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive+https://www.googleapis.com/auth/userinfo.email'
        self.REDIRECT_URI = "http://multiclouds.appspot.com/user/addgdrive"
        self.API_KEY = ''
        self.refresh_token = refresh_token

    def get_auth_url(self):
        url="https://accounts.google.com/o/oauth2/auth?"
        url+="scope=%s&" % self.OAUTH_SCOPE
        url+="redirect_uri=%s&" % self.REDIRECT_URI
        url+="response_type=code&" 
        url+="client_id=%s&" % self.CLIENT_ID
        url+="access_type=offline&approval_prompt=force"
        return url
    
    def get_user_info(self):
        header={"Authorization": "OAuth "+self.get_access_token()}
        url = "https://www.googleapis.com/oauth2/v2/userinfo"
        return json.loads(self.http_request(url,headers=header))
    
    def get_access_token(self,code='',refresh_token=''):
        header={"Content-type": "application/x-www-form-urlencoded"}
        if refresh_token:
            self.refresh_token=refresh_token
        if self.refresh_token=='':
            data={  "client_id" : self.CLIENT_ID,
                    "client_secret" : self.CLIENT_SECRET,
                    "redirect_uri" : self.REDIRECT_URI,
                    "scope":'',
                    "grant_type": "authorization_code"}
            tmp = "&code=%s" % code
            r = self.http_request("https://accounts.google.com/o/oauth2/token",
                                  headers=header, data=data, dataappend=tmp)
            r = json.loads(r)
            self.refresh_token=r["refresh_token"]
            return r["access_token"]
        else:
            data={  "client_id" : self.CLIENT_ID,
                   "client_secret" : self.CLIENT_SECRET,
                   "grant_type": "refresh_token",
                   "refresh_token": self.refresh_token}
            r = self.http_request("https://accounts.google.com/o/oauth2/token",
                                 headers=header, data=data)
            r = json.loads(r)
            return r['access_token']
            
    def get_all_metadata(self,pageToken='',maxResults='5',q=''):
        header={"Authorization": "OAuth "+self.get_access_token()}
        url = "https://www.googleapis.com/drive/v2/files?"
        url +="maxResults="+maxResults
        url +="&fields=items(parents%2Ceditable%2CdownloadUrl%2CfileSize%2Cid%2Ckind%2ClastModifyingUserName%2CmimeType%2CmodifiedDate%2CoriginalFilename%2CthumbnailLink%2Ctitle)%2CnextLink"
        if pageToken != '':
            url += '&pageToken=' + pageToken
        if q != '':
            url += '&q=' + q
        self.url=url
        return json.loads(self.http_request(url,headers=header))
    
class dropbox(auth):
    def __init__(self, access_token = '',access_token_secret = ''):
        self.oauth_token = ''
        self.oauth_token_secret = ''
        self.access_token = oauth_helper.Token(access_token,access_token_secret)
        self.uid = ''
        self.app_info = oauth_helper.AppInfo(self.oauth_token, self.oauth_token_secret)
        self.url_request_token = "https://api.dropbox.com/1/oauth/request_token"
        self.url_oauthorize = "https://www.dropbox.com/1/oauth/authorize?oauth_token="
        self.url_access_token = "https://api.dropbox.com/1/oauth/access_token"
        self.url_account_info="https://api.dropbox.com/1/account/info"
        self.url_delta = "https://api.dropbox.com/1/delta"
        self.data = []

    def input_access_token(self,access_token = '',access_token_secret = ''):
        self.access_token = oauth_helper.Token(access_token,access_token_secret)

    def get_dropbox_auth_url(self ,uri):
        r = self.http_request(self.url_request_token, {"Authorization":oauth_helper.mk_header_no_token(self.app_info)})
        self.request_token = oauth_helper.parse_token(r)
        url = self.url_oauthorize
        url += urllib.quote_plus(self.request_token.key)
        url += "&oauth_callback="+uri
        return url

    def get_access_token(self):  
        r = self.http_request(self.url_access_token, {"Authorization":oauth_helper.mk_header_with_token(self.app_info,self.request_token)})
        self.access_token = oauth_helper.parse_token(r)

    def get_account_info(self):
        #header = {'Authorization':'OAuth oauth_version="1.0", oauth_signature_method="PLAINTEXT",oauth_consumer_key="evis2b04kh9dzxo", oauth_token="ml3y2dh0d9s9e6l",oauth_signature="ff15fqzdqvlz9tx&hk650yuqz0n2evp"'}
        r = self.http_request(self.url_account_info, {"Authorization":oauth_helper.mk_header_with_token(self.app_info,self.access_token)})
        return json.loads(r)

    def get_all_data(self, cursor=''):
        url = self.url_delta + '?cursor=' + cursor
        req = urllib2.Request(url=url,
                              headers={"Authorization":oauth_helper.mk_header_with_token(self.app_info,self.access_token)},
                              data='cursor')
        raw = urllib2.urlopen(req).read()
        return json.loads(raw)

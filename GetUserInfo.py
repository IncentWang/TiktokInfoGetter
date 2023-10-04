from bs4 import BeautifulSoup
import json
import requests

# Use this script only for get influencer info, not follower info (follower info is contained in follower gathering response)
class GetUserInfo:
    def __init__(self, uniqueid: str):
        self.uniqueid = uniqueid
        self.response = {}
        pass

    def getInfo(self):
        response = requests.get("https://www.tiktok.com/@" + self.uniqueid)
        count = 0
        while (BeautifulSoup(response.content, features="html.parser").find(id="SIGI_STATE") == None and count < 5):
            respose = requests.get("https://www.tiktok.com/@" + self.uniqueid)
            count += 1

        if count >= 3:
            raise Exception("Cannot gather user info, unique id: " + self.uniqueid)
        
        allJson = BeautifulSoup(response.content, features="html.parser").find(id="SIGI_STATE")
        
        userModule = json.loads(allJson.text)['UserModule']

        self.response['id'] = userModule['users'][self.uniqueid]['id']
        self.response['secuid'] = userModule['users'][self.uniqueid]['secUid']
        self.response['uniqueid'] = self.uniqueid
        self.response['diggcount'] = userModule['stats'][self.uniqueid]['diggCount']
        self.response['followercount'] = userModule['stats'][self.uniqueid]['followerCount']
        self.response['followingcount'] = userModule['stats'][self.uniqueid]['followingCount']
        self.response['friendcount'] = userModule['stats'][self.uniqueid]['friendCount']
        self.response['heart'] = userModule['stats'][self.uniqueid]['heart']
        self.response['heartcount'] = userModule['stats'][self.uniqueid]['heartCount']
        self.response['videocount'] = userModule['stats'][self.uniqueid]['videoCount']
        self.response['commentsetting'] = userModule['users'][self.uniqueid]['commentSetting']
        self.response['downloadsetting'] = None
        self.response['duetsetting'] = userModule['users'][self.uniqueid]['duetSetting']
        self.response['ftc'] = userModule['users'][self.uniqueid]['ftc']
        self.response['isadvirtual'] = userModule['users'][self.uniqueid]['isADVirtual']
        self.response['nickname'] = userModule['users'][self.uniqueid]['nickname']
        self.response['openfavorite'] = userModule['users'][self.uniqueid]['openFavorite']
        self.response['relation'] = userModule['users'][self.uniqueid]['relation']
        self.response['secretfield'] = userModule['users'][self.uniqueid]['secret']
        self.response['stitchsetting'] = userModule['users'][self.uniqueid]['stitchSetting']
        self.response['ttseller'] = userModule['users'][self.uniqueid]['ttSeller']
        self.response['verified'] = userModule['users'][self.uniqueid]['verified']

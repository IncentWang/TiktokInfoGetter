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
        while (BeautifulSoup(response.content, features="html.parser").find(id="__UNIVERSAL_DATA_FOR_REHYDRATION__") == None and count < 5):
            respose = requests.get("https://www.tiktok.com/@" + self.uniqueid)
            count += 1

        if count >= 5:
            raise Exception("Cannot gather user info, unique id: " + self.uniqueid)
        
        allJson = BeautifulSoup(response.content, features="html.parser").find(id="__UNIVERSAL_DATA_FOR_REHYDRATION__")
        
        userModule = json.loads(allJson.text)['__DEFAULT_SCOPE__']['webapp.user-detail']['userInfo']

        self.response['id'] = userModule['user']['id']
        self.response['secuid'] = userModule['user']['secUid']
        self.response['uniqueid'] = userModule['user']['uniqueId']
        self.response['diggcount'] = userModule['stats']['diggCount']
        self.response['followercount'] = userModule['stats']['followerCount']
        self.response['followingcount'] = userModule['stats']['followingCount']
        self.response['friendcount'] = userModule['stats']['friendCount']
        self.response['heart'] = userModule['stats']['heart']
        self.response['heartcount'] = userModule['stats']['heartCount']
        self.response['videocount'] = userModule['stats']['videoCount']
        self.response['commentsetting'] = userModule['user']['commentSetting']
        self.response['downloadsetting'] = None
        self.response['duetsetting'] = userModule['user']['duetSetting']
        self.response['ftc'] = userModule['user']['ftc']
        self.response['isadvirtual'] = userModule['user']['isADVirtual']
        self.response['nickname'] = userModule['user']['nickname']
        self.response['openfavorite'] = userModule['user']['openFavorite']
        self.response['relation'] = userModule['user']['relation']
        self.response['secretfield'] = userModule['user']['secret']
        self.response['stitchsetting'] = userModule['user']['stitchSetting']
        self.response['ttseller'] = userModule['user']['ttSeller']
        self.response['verified'] = userModule['user']['verified']

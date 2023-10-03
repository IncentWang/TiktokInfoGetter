import requests
from seleniumwire import webdriver
import time
import sys
import threading
from datetime import datetime
import os

TARGET = "https://www.tiktok.com/api/user/list/"
DEPTH_LIMIT = 1
SEND_REQUEST_LIMIT = 10
FOLDER_NAME = ""

def mergeDict(a: dict, b:dict):
    temp = {}
    temp.update(a)
    temp.update(b)
    return temp

class TiktokFollowInfo(threading.Thread): 
    def __init__(self, url:str, **kwargs):
        threading.Thread.__init__(self)
        self.allresponses = []
        self.queryParams = {}
        self.getFollowing = False
        self.secUid = ""
        self.url = url
        self.sendCount = 0
        self.depth_limit = DEPTH_LIMIT
        self.send_request_limit = SEND_REQUEST_LIMIT
        self.folder_name = "temp"

        if 'depthLimit' in kwargs:
            self.depth_limit = kwargs['depthLimit']
        if 'sendRequestLimit' in kwargs:
            self.send_request_limit = kwargs['sendRequestLimit']
        if 'folderName' in kwargs:
            self.folder_name = kwargs['folderName']

        for i in url.split('?', 2)[1].split('&'):
            j = i.split('=')
            self.queryParams[j[0]] = j[1]
        self.queryParams['minCursor'] = 0
        self.queryParams['maxCursor'] = 0
        self.secUid = self.queryParams['secUid']
        if kwargs['getFollowing'] == 'true':
            if 'secUid' in kwargs:
                self.queryParams['secUid'] = kwargs['secUid']
                self.queryParams['scene'] = 21
                self.secUid = self.queryParams['secUid']
                self.getFollowing = True
            else:
                # throw param exception here
                pass
        else:
            self.queryParams['scene'] = 67
            self.getFollowing = False
        print(f"[{datetime.now()}][INFO] [{self.queryParams['secUid'][-7:]}] A new thread of getting data is initialized. secUid: {self.queryParams['secUid']}, getFollowing status: {kwargs['getFollowing']}")
    
    def run(self):
        self.getInfo()
    
    def getInfo(self):
        count = 1
        print(f"[{datetime.now()}][INFO][{self.queryParams['secUid'][-7:]}] Sending number {count} request, maxCursor = {self.queryParams['maxCursor']}, minCursor = {self.queryParams['minCursor']}")
        response = requests.get(TARGET, params = self.queryParams)
        while response.status_code == 200:
            currentJson = response.json()
            if currentJson['status_code'] != 0:
                break
            if 'maxCursor' not in currentJson:
                break
            if currentJson['maxCursor'] == -1 and currentJson['minCursor'] == -1:
                break
            for i in range(len(currentJson['userList'])):
                currentJson['userList'][i]['user']['start_time'] = currentJson['minCursor']
                currentJson['userList'][i]['user']['end_time'] = currentJson['maxCursor']
                self.allresponses.append(currentJson['userList'][i])
            self.queryParams['minCursor'] = currentJson['minCursor']
            self.queryParams['maxCursor'] = currentJson['maxCursor']
            count += 1

            print(f"[{datetime.now()}][INFO][{self.queryParams['secUid'][-7:]}] Sending number {count} request, maxCursor = {self.queryParams['maxCursor']}, minCursor = {self.queryParams['minCursor']}")
            self.sendCount += 1
            if self.sendCount > self.send_request_limit:
                break

            response = requests.get(TARGET, params = self.queryParams)
        self.cleanData()
        return self

    def cleanData(self):
        if len(self.allresponses) == 0:
            return
        # pre-process the dict
        for i in range(len(self.allresponses)):
            del self.allresponses[i]['user']['signature']
            del self.allresponses[i]['user']['nickname']
            del self.allresponses[i]['user']['avatarLarger']
            del self.allresponses[i]['user']['avatarThumb']
            del self.allresponses[i]['user']['avatarMedium']
            self.allresponses[i] = mergeDict(self.allresponses[i]['stats'], self.allresponses[i]['user'])

        print(f"[{datetime.now()}][INFO][{self.queryParams['secUid'][-7:]}] Writing to .csv file...")
        if self.getFollowing:
            self.writeToCsv(self.secUid + '_Following')
        else:
            self.writeToCsv(self.secUid + '_Follower')
    
    def writeToCsv(self, name:str):
        if not os.path.exists(self.folder_name):
            os.mkdir(self.folder_name)
        f = open(self.folder_name + "/" + name + '.csv', 'w')
        f.write(','.join(self.allresponses[0].keys()))
        f.write('\n')
        for i in self.allresponses:
            f.write(','.join(str(x) for x in i.values()))
            f.write('\n')
        f.close()

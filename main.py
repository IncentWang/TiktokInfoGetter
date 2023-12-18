from TiktokFollowInfo import TiktokFollowInfo
from GetUserInfo import GetUserInfo
import sys
import time
import shutil
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
import json
from urllib.parse import urlencode
import argparse

if __name__ == '__main__':
    '''
    Usage: main.py unique id Depth_limit send_request_limit Folder_name
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("uniqueid", help="Unique id of influencer you want to find follower information")
    parser.add_argument("foldername", help="Folder name the program will use to store data.")
    parser.add_argument("--depth", type=int, help="depth of searching, 1 means only get followers info, 2 means get followers info and their following info")
    parser.add_argument("--requestlimit", type=int, help="Max count of sending requests, one request will fetch 30 records.")
    parser.add_argument("--d", help="Contain this flag to store results to database")

    args = parser.parse_args()

    DEPTH_LIMIT = 1
    SEND_REQUEST_LIMIT = 10
    DATABASE = False

    FOLDER_NAME = args.foldername
    uniqueid = args.uniqueid

    if args.depth:
        DEPTH_LIMIT = args.depth

    if args.requestlimit:
        SEND_REQUEST_LIMIT = args.requestlimit
    
    if args.d:
        DATABASE = True

    with open("config.json") as f:
        jsonData = json.load(f)
    queryParams = jsonData["QueryParams"]
    parent = GetUserInfo(uniqueid)
    parent.getInfo()
    queryParams['secUid'] = parent.response['secuid']
    count = 0
    threadPoolExecutor = ThreadPoolExecutor(jsonData['MaxThreadCount'])
    url = "https://www.tiktok.com/api/user/list/?" + urlencode(queryParams)
    
    firstRequest = TiktokFollowInfo(url, getFollowing = 'false', depthLimit = DEPTH_LIMIT, sendRequestLimit = SEND_REQUEST_LIMIT, folderName = FOLDER_NAME)
    future = threadPoolExecutor.submit(firstRequest.getInfo)
    threadPool = []
    threadPool.append(future)

    while count < DEPTH_LIMIT:
        allresponses = []
        for i in as_completed(threadPool):
            if count != DEPTH_LIMIT - 1:
                allresponses.append(i.result())
            else:
                threadPool.remove(i)
        threadPool.clear()
        count += 1
        if count >= DEPTH_LIMIT:
            break
        for i in allresponses:
            for j in i.allresponses: 
                temp = TiktokFollowInfo(url, getFollowing = 'true', secUid = j['secUid'], depthLimit = DEPTH_LIMIT, sendRequestLimit = SEND_REQUEST_LIMIT, folderName = FOLDER_NAME)
                future = threadPoolExecutor.submit(temp.getInfo)
                threadPool.append(future)
    # Zip all necessary file into one zip file
    archived = shutil.make_archive(f'{FOLDER_NAME}_archived', 'zip', f'{FOLDER_NAME}/')
    threadPoolExecutor.shutdown()

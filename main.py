from TiktokFollowInfo import TiktokFollowInfo
from GetUserInfo import GetUserInfo
import sys
import time
import shutil
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
import json
from urllib.parse import urlencode

if __name__ == '__main__':
    '''
    Usage: main.py unique id Depth_limit send_request_limit Folder_name
    '''
    DEPTH_LIMIT = 0
    SEND_REQUEST_LIMIT = 10
    FOLDER_NAME = ""

    if len(sys.argv) < 3:
        raise ValueError("Argv count is not correct. Please try again.")
    if len(sys.argv) == 3:
        DEPTH_LIMIT = 0
        SEND_REQUEST_LIMIT = 10
        FOLDER_NAME = sys.argv[2]
    if len(sys.argv) == 4:
        FOLDER_NAME = sys.argv[2]
        DEPTH_LIMIT = int(sys.argv[3])
        SEND_REQUEST_LIMIT = 10
    if len(sys.argv) == 5:
        FOLDER_NAME = sys.argv[2]
        DEPTH_LIMIT = int(sys.argv[3])
        SEND_REQUEST_LIMIT = int(sys.argv[4])
    
    uniqueid = sys.argv[1]
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
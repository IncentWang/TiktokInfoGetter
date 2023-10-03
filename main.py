from TiktokFollowInfo import TiktokFollowInfo
import sys
import time
import shutil
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
import json

if __name__ == '__main__':
    '''
    Usage: main.py "url for the first request" unix timestamp MAX_DEPTH REQUEST_SEND_LIMIT
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
    
    url = sys.argv[1]
    count = 0
    with open("config.json") as config:
        configFile = json.load(config)
    threadPoolExecutor = ThreadPoolExecutor(configFile["MaxThreadCount"])
    Parent = TiktokFollowInfo(url, getFollowing = 'false', depthLimit = DEPTH_LIMIT, sendRequestLimit = SEND_REQUEST_LIMIT, folderName = FOLDER_NAME)
    future = threadPoolExecutor.submit(Parent.getInfo)
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
    threadPoolExecutor.close()

    # Zip all necessary file into one zip file
    archived = shutil.make_archive(f'{FOLDER_NAME}_archived', 'zip', f'{FOLDER_NAME}/')
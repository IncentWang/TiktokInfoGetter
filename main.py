from TiktokFollowInfo import TiktokFollowInfo
import sys

if __name__ == '__main__':
    '''
    Usage: main.py "url for the first request" MAX_DEPTH REQUEST_SEND_LIMIT
    '''

    if len(sys.argv) < 2:
        raise ValueError("Argv count is not correct. Please try again.")
    if len(sys.argv) == 2:
        TiktokFollowInfo.DEPTH_LIMIT = 0
        TiktokFollowInfo.SEND_REQUEST_LIMIT = 10
    if len(sys.argv) == 3:
        TiktokFollowInfo.DEPTH_LIMIT = int(sys.argv[2])
        TiktokFollowInfo.SEND_REQUEST_LIMIT = 10
    if len(sys.argv) == 4:
        TiktokFollowInfo.DEPTH_LIMIT = int(sys.argv[2])
        TiktokFollowInfo.SEND_REQUEST_LIMIT = int(sys.argv[3])
    
    url = sys.argv[1]
    count = 0
    threadPool = []
    Parent = TiktokFollowInfo(url, getFollowing = 'false')
    threadPool.append(Parent)

    while count < TiktokFollowInfo.DEPTH_LIMIT:
        for i in threadPool:
            i.start()
        for i in threadPool:
            i.join()
        newPool = []
        count += 1
        if count >= TiktokFollowInfo.DEPTH_LIMIT:
            break

        for i in threadPool:
            for j in i.allresponses:
                temp = TiktokFollowInfo(url, getFollowing = 'true', secUid = j['secUid'])
                newPool.append(temp)
        threadPool = newPool
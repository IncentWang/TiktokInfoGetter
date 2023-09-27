from TiktokFollowInfo import TiktokFollowInfo

def lambda_handler(event, context):
    depth = 1
    request_count = 10
    if 'url' not in event:
        raise ValueError("No Avaliable Url Avaliable!")
    if 'MAX_DEPTH' not in event:
        depth = 1
        TiktokFollowInfo.MAX_DEPTH = depth
    else:
        depth = event['MAX_DEPTH']
        TiktokFollowInfo.MAX_DEPTH = depth
    
    if 'REQUEST_SEND_LIMIT' not in event:
        request_count = 10
        TiktokFollowInfo.REQUEST_SEND_LIMIT = request_count
    else:
        request_count = event['REQUEST_SEND_LIMIT']
        TiktokFollowInfo.REQUEST_SEND_LIMIT = request_count
    
    count = 0
    url = event['url']
    threadPool = []
    Parent = TiktokFollowInfo(url, getFollowing = 'false')
    threadPool.append(Parent)

    while count < request_count:
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

# Tiktok Info Getter

## What is this?
Tiktok Info Getter is a open-source tiktok info gather script. In current version, it can get up to ~5000 followers full information of one creator or ~5000 following user full information of any "public profile".
This script will need users' own login identification to access info. However, in current version, it cannot handle "login" flow automatically due to the reCAPTCHA methods Tiktok are currently using.

## Usage
### Quick Start
Use one of following:

`node index.js`

This will start a simple server (only one static html file) in localhost:8081 for user to put all needeed parameters into a webform and run the python file. If all params are passed correctly, browers will download dataset in .zip file automatically. To run this, you will need to write `config.json` before execute this command.

or

`"PythonPathOfTiktokVirtualEnvironment" main.py "uniqueID" "FOLDER_NAME" "DEPTH" "SEND_REQUEST_COUNT"`

This will call python script directly with four parameters: uniqueID, FOLDER_NAME, DEPTH, and SEND_REQUEST_COUNT. The DEPTH and SEND_REQUEST_COUNT is optional parameters and the first two parameters are needed to run this script correctly.

### Parameters
In current Version, to run the script correctly, we will need four parameters: uniqueID, FOLDER_NAME, DEPTH, and REQUEST_SEND_COUNT.

#### FOLDER_NAME
I recommand to use Unix Timestamp of the starting time of the task as the FOLDER_NAME. At the end of task, our script will generate a `FOLDER_NAME_archived.zip` file to download or access. For further scructure of generated file, please see more detailed information below.

#### DEPTH
In current version, the script only supports two depth: 1 or 2. DEPTH == 1 means script will only get followers info of the creator. DEPTH == 2 means script will get followers info AND all followers' following info.
> Warning: the generate file will be large if DEPTH == 2 and REQUEST_SEND_COUNT is high
>
> Warning: In currnt version there is no bound-check method in the script, if DEPTH > 2, script will hit meaningless task forever and generate tons of trash data

#### SEND_REQUEST_COUNT
This parameter defines how many requests will be done in "one search". One search means search all followers of one creator OR search all followings of one public profile. Each request means return 30 new data. For example, if we set SEND_REQUEST_COUNT = 10, for each search we will be able to get up to ~300 data. This parameter is useful when we want to minimize the data set and save computing resources.

#### Some Limitations
Due to the Tiktok-end limitation, this script only be able to get up to ~5000 followers information or following information of one certain user.

The running time and dataset of this script may be very large if we put DEPTH to 2 and SEND_REQUEST_COUNT to int.maxvalue. We are building database infrastructure for handling large amount of data.

## Project Structure
Structure of this project for current version is just like this:
```
/root
|-- /node_modules
|---- "All nodejs needed package"
|-- public
|---- /getinfo.html
|-- TiktokFollowInfo.py
|-- main.py
|-- lambda_function.py (deprecated)
|-- index.js
|-- env.yml
|-- config.json (NOT INCLUDE IN REPOSITORY, you will need to write one, see instructions below)
```
Useful files are "TiktokFollowInfo.py", "main.py", "config.json", and "env.yml".

### TiktokFollowInfo.py
Contains main algorithm to send and parse request and response from tiktok server and generate final .csv file.

### main.py
The entry point of the program.

### config.json
This file is not in git repository, but it is needed to start `index.js`. 

We need those field to make sure info getter is working properly:

`Pyhonpath` : Python exectuable in `tiktok` conda environment.

`MaxThreadCount` : Max concurrent thread count. To save CPU and RAM resource, we recommend to set it as `NumofCPUs + 4` according to python official document. One thread may cause `20 MB` ram usage, if info getter crashed when running, it may caused by memory limit excceed.

`QueryParams` : This is the original url query string dictionary we need to use. We found one url can be reused up to unlimited times, and this is how we done the automatically generation of url using uniqueID. However, for the tiktok signature, X-bogus, and tiktok login logic, we have not find a solution yet. So you need to get one url for all further using manually. The method we use to find URL is at below.

Here is the sample of the QueryParams:
```json
    "QueryParams" : {
        "WebIdLastTime":"some_value",
        "aid":"1988",
        "app_language":"en",
        "app_name":"tiktok_web",
        "browser_language":"en-US",
        "browser_name":"Mozilla",
        "browser_online":"true",
        "browser_platform":"Win32",
        "browser_version":"5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "channel":"tiktok_web",
        "cookie_enabled":"true",
        "count":"30",
        "device_id":"some_value",
        "device_platform":"web_pc",
        "focus_state":"false",
        "from_page":"user",
        "history_len":"3",
        "is_fullscreen":"false",
        "is_page_visible":"true",
        "maxCursor":"some_value",
        "minCursor":"some_value",
        "os":"windows",
        "priority_region":"US",
        "referer":"",
        "region":"US",
        "scene":"67",
        "screen_height":"1440",
        "screen_width":"2560",
        "secUid":"some_value",
        "tz_name":"America/Los_Angeles",
        "webcast_language":"en",
        "msToken":"some_value",
        "X-Bogus":"some_value",
        "_signature":"some_value"
    }
```

#### How to get URL?
First, you need to find the homepage of the account you want to get follower information manually.

For example, in this example, we want to get follower information of [@Symposia.live.game](https://www.tiktok.com/@symposia.live.game).

You should be in this webpage for further actions:

![Tiktok account info page](/ReadmeSrc/InfoPage.png)

Then in Chrome, press F12 to open DevTools:

![Account Info with DevTool](/ReadmeSrc/InfoPageWithDevTool.png)

Then switch to Network tab:
![DevTool Network Tab](/ReadmeSrc/NetworkTab.png)

Apply Search Filter with keyword `WebIdLastTime`:
![WebIdLastTime Filter](/ReadmeSrc/WebIdLastTime.png)

Then click Followers Button:
![Click Followers Button](/ReadmeSrc/ClickFollowersButton.png)

At this point, you may see 0 or more web request in devtool, don't worry. Then scroll down the pop-up followers window to make Ajax send a new request:
![Scroll Down Pop-up Window until new request appears](/ReadmeSrc/FutherInstruction.png)

Then click the new request and select "Headers" tab, you will see the url we will use:
![See URL](/ReadmeSrc/SeeUrl.png)

Then parse the query string in this URL and add it into our `config.json` file, we are ready-to-go!

### env.yml
Conda virtual environment config file. use `Conda env create -f env.yml` to create `tiktok` conda virtual envionment.

## Contribution
All contribution are welcomed including fixing typo in the doc file, debugging, and/or add new features. Just start a pull request!

## Ending
If this script/ repo helps you to get info from tiktok, and you want to share how you use this script to me, please feel free to send me an email about that! (wwhincent@gmail.com) I am really glad to hear how other people use this script!


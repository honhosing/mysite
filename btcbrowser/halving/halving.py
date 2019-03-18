import time

blockheight = 567608
blocktarget = 210000*3
blockspace = blocktarget - blockheight
timespace = blockspace * 10 * 60
blocktimestamp_now = 1552897401
firsthalvingtimestamp = 1354116278
secondhalvingtimestamp = 1468082773
thirdhalvingtimestamp = 1590332601
print(thirdhalvingtimestamp)
print(timespace)


blocktime = '2016-07-10 00:46:13'
blocktimestamp = time.strptime(blocktime, "%Y-%m-%d %H:%M:%S")
blocktimestamp = int(time.mktime(blocktimestamp))
print(blocktimestamp)
print(time.strftime("%Y-%m-%d %H:%M:%S GM+8", time.localtime(firsthalvingtimestamp)))
print(time.strftime("%Y-%m-%d %H:%M:%S GM+8", time.localtime(secondhalvingtimestamp)))
print(time.strftime("%Y-%m-%d %H:%M:%S GM+8", time.localtime(thirdhalvingtimestamp)))

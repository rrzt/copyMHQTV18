#coding=utf-8
#!/usr/bin/python
import sys
sys.path.append('..') 
from base.spider import Spider
import json
import time
import base64
import requests

class Spider(Spider):  # 元类 默认的元类 type
	def getName(self):
		return "哔哩"
	def init(self,extend=""):
		print("============{0}============".format(extend))
		pass
	def isVideoFormat(self,url):
		pass
	def manualVideoCheck(self):
		pass
	def homeContent(self,filter):
		result = {}
		cateManual = {
			        "粤语": "粤语歌曲超清",
        "2022年热榜": "2022年热们歌曲",
        "经典老歌": "经典老歌",
        "古风歌曲": "古风歌曲",
        "闽南语歌曲": "闽南语歌曲",
        "DJ": "DJ歌曲",
        "网红翻唱": "网红翻唱歌曲",
        "音乐": "音乐 4k",
        "A阿黛尔": "阿黛尔演唱会超清超清",
        "Blackpink": "blackpink演唱会超清",
        "Beyond": "beyond演唱会超清",
        "B坂井泉水": "坂井泉水演唱会超清",
        "B宝丽金": "宝丽金演唱会超清",
        "B布兰妮": "布兰妮演唱会超清",
        "C陈瑞": "陈瑞演唱会超清",
        "C陈奕迅": "陈奕迅演唱会超清",
        "C崔健": "催件演唱会超清",
        "Coldplay": "coldplay演唱会超清",
        "C陈慧娴": "陈慧娴演唱会超清",
        "C陈百强": "陈百强演唱会超清",
        "C陈淑桦": "陈淑桦演唱会超清",
        "C陈慧琳": "陈慧琳演唱会超清",
        "D邓丽君": "邓丽君演唱会超清",
        "D邓紫棋": "邓紫棋演唱会超清",
        "D刀郎": "刀郎演唱会超清",
        "D达明一派": "刘以达歌曲",
        "F费玉清": "费玉清演唱会超清",
        "G谷村新司": "谷村新司演唱会超清",
        "G郭富城": "郭富城演唱会超清",
        "G邰正宵": "邰正宵演唱会超清",
        "G关淑怡": "关淑怡演唱会超清",
        "H黄凯芹": "黄凯芹演唱会超清",
        "H黑豹乐队": "H黑豹乐队",
        "J降央卓玛": "降央卓玛演唱会超清",
        "J江慧": "江慧歌曲",
        "J吉永小百合": "吉永小百合歌曲",
        "J金庸": "金庸影视歌曲",
        "L刘德华": "刘德华演唱会超清",
        "Lady Gaga": "Lady Gaga演唱会超清",
        "L龙飘飘": "龙飘飘演唱会超清",
        "L罗百吉": "罗百吉演唱会超清",
        "L罗大佑": "罗大佑演唱会超清",
        "L林志炫": "林志炫演唱会超清",
        "L林忆莲": "林忆莲演唱会超清",
        "L李知恩": "李知恩演唱会超清",
        "L梁静茹": "梁静茹演唱会超清",
        "L冷漠": "冷漠演唱会超清",
        "L李克勤": "李克勤演唱会超清",
        "L林子祥": "林子祥演唱会超清",
        "L黎明": "黎明演唱会超清",
        "L刘若英": "刘若英演唱会超清",
        "MC Hotdog": "MC Hotdog演唱会超清",
        "M莫文蔚": "莫文蔚演唱会超清",
        "M孟庭苇": "孟庭苇演唱会超清",
        "M麦当娜": "麦当娜演唱会超清",
        "M迈克杰克逊": "迈克杰克逊演唱会超清",
        "N雅尼紫禁城": "雅尼紫禁城演唱会超清",
        "P潘越云": "潘越云演唱会超清",
        "P潘美辰": "潘美辰演唱会超清",
        "Q齐秦": "齐秦演唱会超清",
        "Q祁美云": "祁美云演唱会超清",
        "R任贤齐": "任贤齐演唱会超清",
        "S苏慧伦": "苏慧伦演唱会超清",
        "T唐朝乐队": "唐朝乐队",
        "T童安格": "童安格演唱会超清",
        "TFBOYS": "TFBOYS演唱会超清",
        "T太极乐队": "太极乐队演唱会超清",
        "T唐朝摇滚": "唐朝摇滚演唱会超清",
        "T谭咏麟": "谭咏麟演唱会超清",
        "W王琪": "王琪歌曲",
        "W伍珂玥": "伍珂玥演唱会超清",
        "W王杰": "王杰演唱会超清",
        "W伍佰": "伍佰演唱会超清",
        "W温兆伦": "温兆伦演唱会超清",
        "W王菲": "王菲演唱会超清",
        "X熊天平": "熊天平演唱会超清",
        "X徐小凤": "徐小凤演唱会超清",
        "X席琳迪翁": "席琳迪翁演唱会超清",
        "X许嵩": "黄许嵩演唱会超清",
        "X许美静": "许美静演唱会超清",
        "X许冠杰": "许冠杰演唱会超清",
        "X小虎队": "小虎队演唱会超清",
        "X许巍": "许巍演唱会超清",
        "Y叶启田": "叶启田演唱会超清",
        "Y叶玉卿": "叶玉卿演唱会超清",
        "Y杨千嬅": "杨千嬅演唱会超清",
        "Z左麟右李": "左麟右李演唱会超清",
        "Z赵传": "赵传演唱会超清",
        "Z周华健": "周华健演唱会超清",
        "Z周启生": "周启生演唱会超清",
        "Z张信哲": "张信哲演唱会超清",
        "Z周慧敏": "周慧敏演唱会超清",
        "Z张碧晨": "张碧晨演唱会超清",
        "Z中岛美雪": "中岛美雪演唱会超清",
        "Z张学友": "张学友演唱会超清",
        "Z猪哥亮": "猪哥亮歌曲",
        "Z周杰伦": "周杰伦演唱会超清",
        "Z周深": "周深演唱会超清",
        "Z张蔷": "张蔷演唱会超清",
        "Z张帝": "张帝演唱会超清",
        "Z张国荣": "张国荣演唱会超清",
        "Z郑钧": "郑钧演唱会超清",
        "Z张楚": "张楚演唱会超清",
        "Z张真": "张真演唱会超清",
        "Z赵传": "赵传演唱会超清",
        "Z周传雄": "周传雄演唱会超清"
		}
		classes = []
		for k in cateManual:
			classes.append({
				'type_name':k,
				'type_id':cateManual[k]
			})
		result['class'] = classes
		if(filter):
			result['filters'] = self.config['filter']
		return result
	def homeVideoContent(self):
		result = {
			'list':[]
		}
		return result
	cookies = ''
	def getCookie(self):
		cookies_str = self.fetch("https://agit.ai/138001380000/MHQTV/raw/branch/master/bbcookie.txt").text
		cookies_dic = dict([co.strip().split('=') for co in cookies_str.split(';')])
		rsp = requests.session()
		cookies_jar = requests.utils.cookiejar_from_dict(cookies_dic)
		rsp.cookies = cookies_jar
		content = self.fetch("http://api.bilibili.com/x/web-interface/nav", cookies=rsp.cookies)
		res = json.loads(content.text)
		if res["code"] == 0:
			self.cookies = rsp.cookies
		else:
			rsp = self.fetch("https://www.bilibili.com/")
			self.cookies = rsp.cookies
		return rsp.cookies
		
	def categoryContent(self,tid,pg,filter,extend):		
		result = {}
		url = 'https://api.bilibili.com/x/web-interface/search/type?search_type=video&keyword={0}&duration=4&page={1}'.format(tid,pg)
		if len(self.cookies) <= 0:
			self.getCookie()
		rsp = self.fetch(url,cookies=self.cookies)
		content = rsp.text
		jo = json.loads(content)
		if jo['code'] != 0:			
			rspRetry = self.fetch(url,cookies=self.getCookie())
			content = rspRetry.text		
		jo = json.loads(content)
		videos = []
		vodList = jo['data']['result']
		for vod in vodList:
			aid = str(vod['aid']).strip()
			title = vod['title'].strip().replace("<em class=\"keyword\">","").replace("</em>","")
			img = 'https:' + vod['pic'].strip()
			remark = str(vod['duration']).strip()
			videos.append({
				"vod_id":aid,
				"vod_name":title,
				"vod_pic":img,
				"vod_remarks":remark
			})
		result['list'] = videos
		result['page'] = pg
		result['pagecount'] = 9999
		result['limit'] = 90
		result['total'] = 999999
		return result
	def cleanSpace(self,str):
		return str.replace('\n','').replace('\t','').replace('\r','').replace(' ','')
	def detailContent(self,array):
		aid = array[0]
		url = "https://api.bilibili.com/x/web-interface/view?aid={0}".format(aid)

		rsp = self.fetch(url,headers=self.header)
		jRoot = json.loads(rsp.text)
		jo = jRoot['data']
		title = jo['title'].replace("<em class=\"keyword\">","").replace("</em>","")
		pic = jo['pic']
		desc = jo['desc']
		typeName = jo['tname']
		vod = {
			"vod_id":aid,
			"vod_name":title,
			"vod_pic":pic,
			"type_name":typeName,
			"vod_year":"",
			"vod_area":"",
			"vod_remarks":"",
			"vod_actor":"",
			"vod_director":"",
			"vod_content":desc
		}
		ja = jo['pages']
		playUrl = ''
		for tmpJo in ja:
			cid = tmpJo['cid']
			part = tmpJo['part']
			playUrl = playUrl + '{0}${1}_{2}#'.format(part,aid,cid)

		vod['vod_play_from'] = 'B站'
		vod['vod_play_url'] = playUrl

		result = {
			'list':[
				vod
			]
		}
		return result
	def searchContent(self,key,quick):
		result = {
			'list':[]
		}
		return result
	def playerContent(self,flag,id,vipFlags):
		# https://www.555dianying.cc/vodplay/static/js/playerconfig.js
		result = {}

		ids = id.split("_")
		url = 'https://api.bilibili.com:443/x/player/playurl?avid={0}&cid=%20%20{1}&qn=112'.format(ids[0],ids[1])
		rsp = self.fetch(url)
		jRoot = json.loads(rsp.text)
		jo = jRoot['data']
		ja = jo['durl']
		
		maxSize = -1
		position = -1
		for i in range(len(ja)):
			tmpJo = ja[i]
			if maxSize < int(tmpJo['size']):
				maxSize = int(tmpJo['size'])
				position = i

		url = ''
		if len(ja) > 0:
			if position == -1:
				position = 0
			url = ja[position]['url']

		result["parse"] = 0
		result["playUrl"] = ''
		result["url"] = url
		result["header"] = {
			"Referer":"https://www.bilibili.com",
			"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
		}
		result["contentType"] = 'video/x-flv'
		return result

	config = {
		"player": {},
		"filter": {}
	}
	header = {}

	def localProxy(self,param):
		return [200, "video/MP2T", action, ""]
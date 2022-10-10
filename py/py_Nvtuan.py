#coding=utf-8
#!/usr/bin/python
import sys
sys.path.append('..') 
from base.spider import Spider
import json
import time
import base64

class Spider(Spider):  # 元类 默认的元类 type
	def getName(self):
		return "女团组合热舞"
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
			"中国女团":"中国女团 4K"，
"日本女团":"日本女团 4K"，
"韩国女团":"韩国女团 4K",
"SNH48":"SNH48 MV 合集",
"S.H.E":"S.H.E MV 合集",
"Twins":"Twins MV 合集",
"火箭少女101":"火箭少女101 MV 合集",
"BY2":"BY2 MV 合集",
"S.I.N.G":"S.I.N.G MV 合集",
"3unshine":"3unshine MV 合集",
"蜜蜂少女队":"蜜蜂少女队 MV 合集",
"七朵组合":"七朵组合 MV 合集",
"GNZ48":"GNZ48 MV 合集",
"TWICE":"TWICE MV 合集",
"4MINUTE":"4MINUTE MV 合集",
"EXID":"EXID MV 合集",
"KARA":"KARA MV 合集",
"TARA":"TARA MV 合集",
"BLACKPINK":"BLACKPINK MV 合集",
"LOONA":"LOONA MV 合集",
"ITZY":"ITZY MV 合集",
"Red Velvet":"Red Velvet MV 合集",
"Everglow":"Everglow MV 合集",
"Mamamoo":"Mamamoo MV 合集",
"少女时代":"少女时代 MV 合集",
"S.E.S":"S.E.S MV 合集",
"FIN.K.L":"FIN.K.L MV 合集",
"2NE1":"2NE1 MV 合集",
"Wonder Girls":"Wonder Girls MV 合集",
"IZ*ONE":"IZ*ONE MV 合集",
"Sistar":"Sistar MV 合集",
"Apink":"Apink MV 合集",
"AOA":"AOA MV 合集",
"GFRIEND":"GFRIEND MV 合集",
"f(x)":"f(x) MV 合集",
"(G)I-DLE":"(G)I-DLE MV 合集",
"Itzy":"Itzy MV 合集",
"Oh! GG":"Oh! GG MV 合集",
"GirlCrush":"GirlCrush MV 合集",
"AKB48":"AKB48 MV 合集",
"SKE48":"SKE48 MV 合集",
"NMB48":"NMB48 MV 合集",
"JKT48":"JKT48 MV 合集",
"HKT48":"HKT48 MV 合集",
"AKB48 Team TP":"AKB48 Team TP MV 合集",
"Perfume":"Perfume MV 合集",
"桃色幸运草Z":"桃色幸运草Z MV 合集",
"乃木坂46乃":"乃木坂46乃 MV 合集",
"樱坂46":"樱坂46 MV 合集",
"日向坂46":"日向坂46 MV 合集",
"E-girls":"E-girls MV 合集",
"NiziU":"NiziU MV 合集",
"BiSH":"BiSH MV 合集",
"早安少女组":"早安少女组 MV 合集"
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
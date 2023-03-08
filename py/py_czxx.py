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
        return "初中"
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
            "7年级地理":"7年级地理",
       "7年级生物":"7年级生物",
       "7年级物理":"7年级物理",
       "7年级化学":"7年级化学",
       "8年级语文":"8年级语文",
       "8年级数学":"8年级数学",
       "8年级英语":"8年级英语",
       "8年级历史":"8年级历史",
       "8年级地理":"8年级地理",
       "8年级生物":"8年级生物",   
       "8年级物理":"8年级物理",
       "8年级化学":"8年级化学",
       "9年级语文":"9年级语文",
       "9年级数学":"9年级数学",
       "9年级英语":"9年级英语",
       "9年级历史":"9年级历史",
       "9年级地理":"9年级地理",
       "9年级生物":"9年级生物",
       "9年级物理":"9年级物理",
       "9年级化学":"9年级化学"
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
        import requests
        import http.cookies
        # 这里填cookie
        raw_cookie_line = "buvid3=93456A95-EBF2-D2E9-8E7E-BF4CAEE28EBF15630infoc; b_nut=1678187414; buvid4=FECB5AD9-8C05-D3E6-2CA4-04D8F11C81E315630-123030719-/UB6HDpRwO7Y8xPozjrudA%3D%3D; bsource=search_baidu; _uuid=68786BC5-E3C10-1011D-277F-21E8E581086C481391infoc; buvid_fp_plain=undefined; fingerprint=dae430368fff18fc48ba52945bee0873; buvid_fp=dae430368fff18fc48ba52945bee0873; SESSDATA=31d18870%2C1693740532%2C4c963%2A31; bili_jct=4e7176ba803644d029a992524cf2b9d2; DedeUserID=1634385901; DedeUserID__ckMd5=a66f7f7df57f3a5a; sid=5yxkn9i3; b_lsid=DF626619_186BFF1D8CD; rpdid=|(l|JYkkY|0J'uY~)kl~ll~"
        simple_cookie = http.cookies.SimpleCookie(raw_cookie_line)
        cookie_jar = requests.cookies.RequestsCookieJar()
        cookie_jar.update(simple_cookie)
        return cookie_jar
    def get_dynamic(self,pg):
        result = {}
        
        url= 'https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/all?timezone_offset=-480&type=all&page={0}'.format(pg)
        
        rsp = self.fetch(url,cookies=self.getCookie())
        content = rsp.text
        jo = json.loads(content)
        if jo['code'] == 0:
            videos = []
            vodList = jo['data']['items']
            for vod in vodList:
                if vod['type'] == 'DYNAMIC_TYPE_AV':
                    ivod = vod['modules']['module_dynamic']['major']['archive']
                    aid = str(ivod['aid']).strip()
                    title = ivod['title'].strip().replace("<em class=\"keyword\">","").replace("</em>","")
                    img =  ivod['cover'].strip()
                    remark = str(ivod['duration_text']).strip()
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

    def get_hot(self,pg):
        result = {}
        url= 'https://api.bilibili.com/x/web-interface/popular?ps=20&pn={0}'.format(pg)
        rsp = self.fetch(url,cookies=self.getCookie())
        content = rsp.text
        jo = json.loads(content)
        if jo['code'] == 0:
            videos = []
            vodList = jo['data']['list']
            for vod in vodList:
                aid = str(vod['aid']).strip()
                title = vod['title'].strip().replace("<em class=\"keyword\">","").replace("</em>","")
                img =  vod['pic'].strip()
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
    def get_rank(self):
        result = {}
        url= 'https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all'
        rsp = self.fetch(url,cookies=self.getCookie())
        content = rsp.text
        jo = json.loads(content)
        if jo['code'] == 0:
            videos = []
            vodList = jo['data']['list']
            for vod in vodList:
                aid = str(vod['aid']).strip()
                title = vod['title'].strip().replace("<em class=\"keyword\">","").replace("</em>","")
                img =  vod['pic'].strip()
                remark = str(vod['duration']).strip()
                videos.append({
                    "vod_id":aid,
                    "vod_name":title,
                    "vod_pic":img,
                    "vod_remarks":remark
                })
            result['list'] = videos
            result['page'] = 1
            result['pagecount'] = 1
            result['limit'] = 90
            result['total'] = 999999
        return result
    def categoryContent(self,tid,pg,filter,extend):	
        result = {}
        if tid == "热门":
            return self.get_hot(pg=pg)
        if tid == "排行榜" :
            return self.get_rank()
        if tid == '动态':
            return self.get_dynamic(pg=pg)
        url = 'https://api.bilibili.com/x/web-interface/search/type?search_type=video&keyword={0}&page={1}'.format(tid,pg)
        if len(self.cookies) <= 0:
            self.getCookie()
        rsp = self.fetch(url,cookies=self.getCookie())
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
            title = tid + ":" + vod['title'].strip().replace("<em class=\"keyword\">","").replace("</em>","")
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

        rsp = self.fetch(url,headers=self.header,cookies=self.getCookie())
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
            "vod_area":"bilidanmu",
            "vod_remarks":"",
            "vod_actor":jo['owner']['name'],
            "vod_director":jo['owner']['name'],
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
        search = self.categoryContent(tid=key,pg=1,filter=None,extend=None)
        result = {
            'list':search['list']
        }
        return result
    def playerContent(self,flag,id,vipFlags):
        # https://www.555dianying.cc/vodplay/static/js/playerconfig.js
        result = {}

        ids = id.split("_")
        url = 'https://api.bilibili.com:443/x/player/playurl?avid={0}&cid=%20%20{1}&qn=112'.format(ids[0],ids[1])
        rsp = self.fetch(url,cookies=self.getCookie())
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

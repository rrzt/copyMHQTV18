# coding=utf-8
# !/usr/bin/python
import sys
from base.spider import Spider
import json
import threading
import requests
from requests import session
import time

sys.path.append('..')


class Spider(Spider):
    def getDependence(self):
        return ['py_bilibili']

    def getName(self):
        return "哔哩影视"

    def init(self, extend=""):
        #self.bilibili = extend[0]
        #print("============{0}============".format(extend))
        pass

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    # 主页
    def homeContent(self, filter):
        result = {}
        cateManual = {
            "番剧": "1",
            "国创": "4",
            "电影": "2",
            "电视剧": "5",
            "纪录片": "3",
            "综艺": "7",
            "全部": "全部",
            # "追番追剧": "追番追剧",
            "时间表": "时间表",
            # ————————以下可自定义关键字，结果以搜索方式展示————————
            # "奥特曼": "奥特曼"

        }
        classes = []
        for k in cateManual:
            classes.append({
                'type_name': k,
                'type_id': cateManual[k]
            })
        result['class'] = classes
        if filter:
            result['filters'] = self.config['filter']
        return result

    # 用户cookies
    cookies = ''
    userid = ''
    csrf = ''

    def getCookie(self):
        # self.cookies = self.bilibili.getCookie()
        # self.userid = self.bilibili.userid
        # self.csrf = self.bilibili.csrf
        # return self.cookies
        # 单用此文件，请注释掉上面4行，取消以下注释，在下方raw_cookie_line后的双引号内填写cookies/外链
        import http.cookies
        raw_cookie_line = ""
        if raw_cookie_line.startswith('http'):
            raw_cookie_line = self.fetch(raw_cookie_line).text
        simple_cookie = http.cookies.SimpleCookie(raw_cookie_line)
        cookie_jar = requests.cookies.RequestsCookieJar()
        cookie_jar.update(simple_cookie)
        rsp = session()
        rsp.cookies = cookie_jar
        content = self.fetch("https://api.bilibili.com/x/web-interface/nav", cookies=rsp.cookies)
        res = json.loads(content.text)
        if res["code"] == 0:
            self.cookies = rsp.cookies
            self.userid = res["data"].get('mid')
            self.csrf = rsp.cookies['bili_jct']
        return cookie_jar


    # 格式化图片，默认16:9的webp格式，降低内存占用
    def format_img(self, img):
        img += "@640w_360h_1c_100q.webp"  # 格式，[jpg/png/gif]@{width}w_{high}h_{is_cut}c_{quality}q.{format}
        return img

    # 将没有page_size参数的页面分页
    def pagination(self, array, pg):
        page_size = 10      # 默认单页视频数量为10，可自定义
        max_number = page_size * int(pg)
        min_number = max_number - page_size
        return array[min_number:max_number]

    # 记录观看历史
    def post_history(self, aid, cid):
        url = 'https://api.bilibili.com/x/v2/history/report?aid={0}&cid={1}&csrf={2}'.format(aid, cid, self.csrf)
        requests.post(url=url, cookies=self.cookies)

    # 将超过10000的数字换成成以万和亿为单位
    def zh(self, num):
        if int(num) >= 100000000:
            p = round(float(num) / float(100000000), 1)
            p = str(p) + '亿'
        else:
            if int(num) >= 10000:
                p = round(float(num) / float(10000), 1)
                p = str(p) + '万'
            else:
                p = str(num)
        return p

    def homeVideoContent(self):
        result = {}
        videos = self.get_rank(1, 1)['list'][0:2]
        for i in [4, 2, 5, 3, 7]:
            videos += self.get_rank2(i, 1)['list'][0:2]
        result['list'] = videos
        return result

    def get_rank(self, tid, pg):
        result = {}
        url = 'https://api.bilibili.com/pgc/web/rank/list?season_type={0}&day=3'.format(tid)
        rsp = self.fetch(url, cookies=self.cookies)
        content = rsp.text
        jo = json.loads(content)
        if jo['code'] == 0:
            videos = []
            vodList = jo['result']['list']
            vodList = self.pagination(vodList, pg)
            for vod in vodList:
                aid = str(vod['season_id']).strip()
                title = vod['title'].strip()
                img = vod['cover'].strip()
                remark = vod['new_ep']['index_show']
                videos.append({
                    "vod_id": 'ss' + aid,
                    "vod_name": title,
                    "vod_pic": self.format_img(img),
                    "vod_remarks": remark
                })
            result['list'] = videos
            result['page'] = pg
            result['pagecount'] = 9999
            result['limit'] = 90
            result['total'] = 999999
        return result

    def get_rank2(self, tid, pg):
        result = {}
        url = 'https://api.bilibili.com/pgc/season/rank/web/list?season_type={0}&day=3'.format(tid)
        rsp = self.fetch(url, cookies=self.cookies)
        content = rsp.text
        jo = json.loads(content)
        if jo['code'] == 0:
            videos = []
            vodList = jo['data']['list']
            vodList = self.pagination(vodList, pg)
            for vod in vodList:
                aid = str(vod['season_id']).strip()
                title = vod['title'].strip()
                img = vod['ss_horizontal_cover'].strip()
                remark = vod['new_ep']['index_show']
                videos.append({
                    "vod_id": aid,
                    "vod_name": title,
                    "vod_pic": self.format_img(img),
                    "vod_remarks": remark
                })
            result['list'] = videos
            result['page'] = pg
            result['pagecount'] = 9999
            result['limit'] = 90
            result['total'] = 999999
        return result

    def get_zhui(self, pg, mode):
        result = {}
        if len(self.cookies) <= 0:
            self.getCookie()
        url = 'https://api.bilibili.com/x/space/bangumi/follow/list?type={2}&follow_status=0&pn={1}&ps=10&vmid={0}'.format(
            self.userid, pg, mode)
        rsp = self.fetch(url, cookies=self.cookies)
        content = rsp.text
        jo = json.loads(content)
        videos = []
        vodList = jo['data']['list']
        for vod in vodList:
            aid = str(vod['season_id']).strip()
            title = vod['title']
            img = vod['cover'].strip()
            remark = vod['new_ep']['index_show'].strip()
            videos.append({
                "vod_id": aid,
                "vod_name": title,
                "vod_pic": self.format_img(img),
                "vod_remarks": remark
            })
        result['list'] = videos
        result['page'] = pg
        result['pagecount'] = 9999
        result['limit'] = 90
        result['total'] = 999999
        return result

    def get_all(self, tid, pg, order, season_status):
        result = {}
        if len(self.cookies) <= 0:
            self.getCookie()
        url = 'https://api.bilibili.com/pgc/season/index/result?order={2}&pagesize=10&type=1&season_type={0}&page={1}&season_status={3}'.format(
            tid, pg, order, season_status)
        rsp = self.fetch(url, cookies=self.cookies)
        content = rsp.text
        jo = json.loads(content)
        videos = []
        vodList = jo['data']['list']
        for vod in vodList:
            aid = str(vod['season_id']).strip()
            title = vod['title']
            img = vod['cover'].strip()
            remark = vod['index_show'].strip()
            videos.append({
                "vod_id": aid,
                "vod_name": title,
                "vod_pic": self.format_img(img),
                "vod_remarks": remark
            })
        result['list'] = videos
        result['page'] = pg
        result['pagecount'] = 9999
        result['limit'] = 90
        result['total'] = 999999
        return result

    def get_timeline(self, tid, pg):
        result = {}
        url = 'https://api.bilibili.com/pgc/web/timeline/v2?season_type={0}&day_before=2&day_after=4'.format(tid)
        rsp = self.fetch(url, cookies=self.cookies)
        content = rsp.text
        jo = json.loads(content)
        if jo['code'] == 0:
            videos1 = []
            vodList = jo['result']['latest']
            for vod in vodList:
                aid = str(vod['season_id']).strip()
                title = vod['title'].strip()
                img = vod['cover'].strip()
                remark = vod['pub_index'] + '　' + vod['follows'].replace('系列', '')
                videos1.append({
                    "vod_id": aid,
                    "vod_name": title,
                    "vod_pic": self.format_img(img),
                    "vod_remarks": remark
                })
            videos2 = []
            for i in range(0, 7):
                vodList = jo['result']['timeline'][i]['episodes']
                for vod in vodList:
                    if str(vod['published']) == "0":
                        aid = str(vod['season_id']).strip()
                        title = str(vod['title']).strip()
                        img = str(vod['cover']).strip()
                        date = str(time.strftime("%m-%d %H:%M", time.localtime(vod['pub_ts'])))
                        remark = date + "   " + vod['pub_index']
                        videos2.append({
                            "vod_id": aid,
                            "vod_name": title,
                            "vod_pic": self.format_img(img),
                            "vod_remarks": remark
                        })
            result['list'] = self.pagination(videos2 + videos1, pg)
            result['page'] = pg
            result['pagecount'] = 9999
            result['limit'] = 90
            result['total'] = 999999
        return result

    def categoryContent(self, tid, pg, filter, extend):
        if len(self.cookies) <= 0:
            self.getCookie()
        if tid == "1":
            return self.get_rank(tid=tid, pg=pg)
        elif tid in {"2", "3", "4", "5", "7"}:
            return self.get_rank2(tid=tid, pg=pg)
        elif tid == "全部":
            tid = '1'
            order = '2'
            season_status = '-1'
            if 'tid' in extend:
                tid = extend['tid']
            if 'order' in extend:
                order = extend['order']
            if 'season_status' in extend:
                season_status = extend['season_status']
            return self.get_all(tid, pg, order, season_status)
        elif tid == "追番追剧":
            mode = '1'
            if 'mode' in extend:
                mode = extend['mode']
            return self.get_zhui(pg, mode)
        elif tid == "时间表":
            tid = '1'
            if 'tid' in extend:
                tid = extend['tid']
            return self.get_timeline(tid, pg)
        else:
            result = self.searchContent(key=tid, quick="false")
        return result

    def cleanSpace(self, str):
        return str.replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '')

    con = threading.Condition()

    def get_season(self, n, nList, fromList, urlList, season_id, season_title):
        url = 'https://api.bilibili.com/pgc/view/web/season?season_id={0}'.format(season_id)
        try:
            rsp = self.fetch(url, headers=self.header, cookies=self.cookies)
            season = json.loads(rsp.text)
        except:
            with self.con:
                nList.remove(n)
                self.con.notify_all()
            return
        episode = season['result']['episodes']
        if len(episode) == 0:
            with self.con:
                nList.remove(n)
                self.con.notify_all()
            return
        playUrl = ''
        for tmpJo in episode:
            aid = tmpJo['aid']
            cid = tmpJo['cid']
            part = tmpJo['title'].replace("#", "﹟").replace("$", "﹩")
            if tmpJo['badge'] != '':
                part += ' 【' + tmpJo['badge'] + '】'
            part += tmpJo['long_title'].replace("#", "﹟").replace("$", "﹩")
            playUrl += '{0}${1}_{2}_bangumi#'.format(part, aid, cid)
        with self.con:
            while True:
                if n == nList[0]:
                    fromList.append(season_title)
                    urlList.append(playUrl)
                    nList.remove(n)
                    self.con.notify_all()
                    break
                else:
                    self.con.wait()

    def detailContent(self, array):
        aid = array[0]
        if 'ep' in aid:
            aid = 'ep_id=' + aid.replace('ep', '')
        elif 'ss' in aid:
            aid = 'season_id=' + aid.replace('ss', '')
        else:
            aid = 'season_id=' + aid
        url = "https://api.bilibili.com/pgc/view/web/season?{0}".format(aid)
        rsp = self.fetch(url, headers=self.header, cookies=self.cookies)
        jRoot = json.loads(rsp.text)
        jo = jRoot['result']
        id = jo['season_id']
        title = jo['title']
        s_title = jo['season_title']
        img = jo['cover']
        typeName = jo['share_sub_title']
        date = jo['publish']['pub_time'][0:4]
        dec = jo['evaluate']
        remark = jo['new_ep']['desc']
        stat = jo['stat']
        status = "弹幕: " + self.zh(stat['danmakus']) + "　点赞: " + self.zh(stat['likes']) + "　投币: " + self.zh(
            stat['coins']) + "　追番追剧: " + self.zh(stat['favorites'])
        if 'rating' in jo:
            score = "评分: " + str(jo['rating']['score']) + '　' + jo['subtitle']
        else:
            score = "暂无评分" + '　' + jo['subtitle']
        vod = {
            "vod_id": id,
            "vod_name": title,
            "vod_pic": self.format_img(img),
            "type_name": typeName,
            "vod_year": date,
            "vod_area": "bilidanmu",
            "vod_remarks": remark,
            "vod_actor": status,
            "vod_director": score,
            "vod_content": dec
        }
        playUrl = ''
        for tmpJo in jo['episodes']:
            aid = tmpJo['aid']
            cid = tmpJo['cid']
            part = tmpJo['title'].replace("#", "﹟").replace("$", "﹩")
            if tmpJo['badge'] != '':
                part += '【' + tmpJo['badge'] + '】'
            part += tmpJo['long_title'].replace("#", "﹟").replace("$", "﹩")
            playUrl += '{0}${1}_{2}#'.format(part, aid, cid)

        fromList = []
        urlList = []
        if playUrl != '':
            fromList.append(s_title)
            urlList.append(playUrl)
        nList = []
        if len(jo['seasons']) > 1:
            n = 0
            for season in jo['seasons']:
                season_id = season['season_id']
                season_title = season['season_title']
                if season_id == id and len(fromList) > 0:
                    isHere = fromList.index(s_title)
                    fromList[isHere] = season_title
                    continue
                n += 1
                nList.append(n)
                t = threading.Thread(target=self.get_season, args=(n, nList, fromList, urlList, season_id, season_title))
                t.start()

        while True:
            _count = threading.active_count()
            # 计算线程数，不出结果就调大，结果少了就调小
            if _count <= 2:
                break

        vod['vod_play_from'] = '$$$'.join(fromList)
        vod['vod_play_url'] = '$$$'.join(urlList)

        result = {'list': [vod]}
        return result

    def searchContent(self, key, quick):
        if len(self.cookies) <= 0:
            self.getCookie()
        url1 = 'https://api.bilibili.com/x/web-interface/search/type?search_type=media_bangumi&keyword={0}'.format(
            key)  # 番剧搜索
        rsp1 = self.fetch(url1, cookies=self.cookies)
        content1 = rsp1.text
        jo1 = json.loads(content1)
        rs1 = jo1['data']
        url2 = 'https://api.bilibili.com/x/web-interface/search/type?search_type=media_ft&keyword={0}'.format(
            key)  # 影视搜索
        rsp2 = self.fetch(url2, cookies=self.cookies)
        content2 = rsp2.text
        jo2 = json.loads(content2)
        rs2 = jo2['data']
        videos = []
        if rs1['numResults'] == 0:
            vodList = jo2['data']['result']
        elif rs2['numResults'] == 0:
            vodList = jo1['data']['result']
        else:
            vodList = jo1['data']['result'] + jo2['data']['result']
        for vod in vodList:
            aid = str(vod['season_id']).strip()
            title = key + '➢' + vod['title'].strip().replace("<em class=\"keyword\">", "").replace("</em>", "")
            img = vod['cover'].strip()
            remark = vod['index_show']
            videos.append({
                "vod_id": aid,
                "vod_name": title,
                "vod_pic": self.format_img(img),
                "vod_remarks": remark
            })
        result = {
            'list': videos
        }
        return result

    def playerContent(self, flag, id, vipFlags):
        if len(self.cookies) <= 0:
            self.getCookie()
        result = {}
        url = ''
        ids = id.split("_")
        if len(ids) < 2:
            return result
        elif len(ids) >= 2:
            aid = ids[0]
            cid = ids[1]
            url = 'https://api.bilibili.com/pgc/player/web/playurl?aid={0}&cid={1}&qn=116'.format(aid, cid)
            self.post_history(aid, cid)  # 回传播放历史记录
        rsp = self.fetch(url, cookies=self.cookies, headers=self.header)
        jRoot = json.loads(rsp.text)
        if jRoot['code'] != 0:
            return {}
        jo = jRoot['result']
        ja = jo['durl']
        maxSize = -1
        position = -1
        for i in range(len(ja)):
            tmpJo = ja[i]
            if maxSize < int(tmpJo['size']):
                maxSize = int(tmpJo['size'])
                position = i
        if len(ja) > 0:
            if position == -1:
                position = 0
            url = ja[position]['url']
        result["parse"] = 0
        result["playUrl"] = ''
        result["url"] = url
        result["header"] = {
            "Referer": "https://www.bilibili.com",
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
        }
        result["contentType"] = 'video/x-flv'
        return result

    config = {
        "player": {},
        "filter": {
            "全部": [{"key": "tid", "name": "分类",
                    "value": [{"n": "番剧", "v": "1"}, {"n": "国创", "v": "4"}, {"n": "电影", "v": "2"},
                              {"n": "电视剧", "v": "5"}, {"n": "记录片", "v": "3"}, {"n": "综艺", "v": "7"}]},
                   {"key": "order", "name": "排序",
                    "value": [{"n": "播放数量", "v": "2"}, {"n": "更新时间", "v": "0"}, {"n": "最高评分", "v": "4"},
                              {"n": "弹幕数量", "v": "1"}, {"n": "追看人数", "v": "3"}, {"n": "开播时间", "v": "5"},
                              {"n": "上映时间", "v": "6"}, ]},
                   {"key": "season_status", "name": "付费",
                    "value": [{"n": "全部", "v": "-1"}, {"n": "免费", "v": "1"},
                              {"n": "付费", "v": "2%2C6"}, {"n": "大会员", "v": "4%2C6"}, ]}, ],
            "追番追剧": [{"key": "mode", "name": "分类",
                      "value": [{"n": "追番", "v": "1"}, {"n": "追剧", "v": "2"}, ]}, ],
            "时间表": [{"key": "tid", "name": "分类",
                     "value": [{"n": "番剧", "v": "1"}, {"n": "国创", "v": "4"}, ]}, ],

        }
    }

    header = {
        "Referer": "https://www.bilibili.com",
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }

    def localProxy(self, param):
        return [200, "video/MP2T", action, ""]

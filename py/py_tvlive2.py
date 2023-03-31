# coding=utf-8
# !/usr/bin/python
import re
import sys

sys.path.append('..')
from base.spider import Spider

class Spider(Spider):  # 元类 默认的元类 type
    def getName(self):
        return "电视直播"

    def init(self, extend=""):
        print("============{0}============".format(extend))
        pass
    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def homeContent(self, filter):
        result = {}
        cateManual = {
            "电视直播": "https://agit.ai/138001380000/MHQTV/raw/branch/master/TV/18c.txt"
        }
        classes = []
        for k in cateManual:
            classes.append({
                'type_name': k,
                'type_id': cateManual[k]
            })
        result['class'] = classes
        if (filter):
            result['filters'] = self.config['filter']
        return result

    def homeVideoContent(self):
        tid = self.homeContent(False)['class'][0]['type_id']
        result = self.categoryContent(tid, 1)
        return result

    def categoryContent(self, tid, pg, filter=False, extend=''):
        result = {}
        videos = []
        rsp = self.fetch(tid, headers=self.header)
        if '#EXTM3U' in rsp.text:
            txt_str = self.m3utotxt(rsp.text)
        else:
            txt_str = self.cleanText(rsp.text)
        infoList = txt_str.strip('\n').split('\n')
        groupposList = []
        i = 0
        for info in infoList:
            if info == '':
                i = i + 1
                continue
            info = info.split(',')
            if info[1].strip() == '#genre#' or i == len(infoList) - 1:
                if i == len(infoList) - 1:
                    i = i + 1
                groupposList.append(i)
                if len(groupposList) == 2:
                    videos.append({
                        "vod_id": '{}@@@{}@@@{}@@@{}'.format(groupposList[0] + 1, groupposList[1] - 1, group, tid),
                        "vod_name": group,
                        "vod_pic": 'https://i.postimg.cc/dty6NDQ1/zhibo.png',
                        "vod_remarks": ''
                    })
                    del (groupposList[0])
                group = info[0].strip()
            i = i + 1
        result['list'] = videos
        result['page'] = 1
        result['pagecount'] = 1
        result['limit'] = len(videos)
        result['total'] = len(videos)
        return result

    def detailContent(self, array):
        ids = array[0].split('@@@')
        url = ids[3]
        title = ids[2]
        end_lint = int(ids[1])
        start_line = int(ids[0])
        rsp = self.fetch(url,headers=self.header)
        if '#EXTM3U' in rsp.text:
            txt_str = self.m3utotxt(rsp.text)
        else:
            txt_str = self.cleanText(rsp.text)
        infoList = txt_str.strip('\n').split('\n')[start_line:end_lint]
        vod = {
            "vod_id": title,
            "vod_name": title,
            "vod_pic": 'https://i.postimg.cc/dty6NDQ1/zhibo.png',
            "vod_tag": '',
            "vod_play_from": title
        }
        purl = ''
        for info in infoList:
            if info == '':
                continue
            purl = purl + '{}${}#'.format(info.split(',')[0], info.split(',')[1])
        vod['vod_play_url'] = purl.strip('#')
        result = {
            'list': [
                vod
            ]
        }
        return result

    def searchContent(self, key, quick):
        result = {
            'list': []
        }
        return result

    def playerContent(self, flag, id, vipFlags):
        result = {}
        result["parse"] = 0
        result["playUrl"] = ''
        result["url"] = id
        return result

    flurl = ''
    config = {
        "player": {},
        "filter": {}
    }
    header = {}

    def m3utotxt(self, m3u_str):
        infos = m3u_str.strip('\n').split('\n')
        txtDict = {}
        txtList = []
        groupList = []
        txt_str = ''
        for info in infos:
            if info.startswith('#EXTINF'):
                infoList = info.split(',')
                channel = infoList[-1]
                infoList = infoList[0].strip().split()
                url = infos[infos.index(info) + 1]
                for iL in infoList:
                    if iL.startswith('group-title'):
                        group = iL.split('=', 1)[1]
                        if group not in groupList:
                            groupList.append(group)
                            locals()[group] = '{},#genre#\n'.format(group)
                        locals()[group] = locals()[group] + '{},{}\n'.format(channel, url)
                    txt_str = txt_str + '{},{}\n'.format(channel, url)
        if len(groupList) != 0:
            txt_str = ''
            for group in groupList:
                txt_str = txt_str + locals()[group]
        return txt_str

    def localProxy(self, param):
        return [200, "video/MP2T", action, ""]
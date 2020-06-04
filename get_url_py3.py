
#-*- coding:utf-8 -*-
import urllib.request as urllib2
import re,sys,os
import json

import requests
import zlib
from io import BytesIO
import gzip

import ssl

#context = ssl._create_unverified_context()
#ssl._create_default_https_context = ssl._create_unverified_context
type_list=[u'偷拍自拍',u'制服诱惑',u'清纯少女',u'辣妹大奶',u'女同专属',u'素人出演',u'角色扮演',u'成人动漫',u'人妻熟女',u'变态另类',u'经典伦理',u'首页',u'全部',u'搜索']
type_dict={
        u'偷拍自拍':'https://92m303r2a84roj2l0234.guoguoapps.com/vod/listing-4-0-0-0-0-0-0-0-0-',
        u'制服诱惑':'https://92m303r2a84roj2l0234.guoguoapps.com/vod/listing-5-0-0-0-0-0-0-0-0-',
        u'清纯少女':'https://92m303r2a84roj2l0234.guoguoapps.com/vod/listing-6-0-0-0-0-0-0-0-0-',
        u'辣妹大奶':'https://92m303r2a84roj2l0234.guoguoapps.com/vod/listing-7-0-0-0-0-0-0-0-0-',
        u'女同专属':'https://92m303r2a84roj2l0234.guoguoapps.com/vod/listing-8-0-0-0-0-0-0-0-0-',
        u'素人出演':'https://92m303r2a84roj2l0234.guoguoapps.com/vod/listing-9-0-0-0-0-0-0-0-0-',
        u'角色扮演':'https://92m303r2a84roj2l0234.guoguoapps.com/vod/listing-10-0-0-0-0-0-0-0-0-',
        u'成人动漫':'https://92m303r2a84roj2l0234.guoguoapps.com/vod/listing-11-0-0-0-0-0-0-0-0-',
        u'人妻熟女':'https://92m303r2a84roj2l0234.guoguoapps.com/vod/listing-12-0-0-0-0-0-0-0-0-',
        u'变态另类':'https://92m303r2a84roj2l0234.guoguoapps.com/vod/listing-13-0-0-0-0-0-0-0-0-',
        u'经典伦理':'https://92m303r2a84roj2l0234.guoguoapps.com/vod/listing-14-0-0-0-0-0-0-0-0-',
        u'全部':'https://92m303r2a84roj2l0234.guoguoapps.com/vod/listing-0-0-0-0-0-0-0-0-0-',
        u'首页':'https://92m303r2a84roj2l0234.guoguoapps.com/index',
        u'搜索':'https://92m303r2a84roj2l0234.guoguoapps.com/search?page=1&wd='
            }


def get_url(url,root,page="0"):
    header = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
    'Sec-Fetch-Dest': 'document',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Accept-Language': 'ja,zh;q=0.9,zh-CN;q=0.8,en;q=0.7',
    'Referer': 'https://92m303r2a84roj2l0234.guoguoapps.com',
        }
    if page=="0":
        pass
    elif page=="14":
        pass
    else:
        url=url+page
    if not os.path.exists("m3u8_file"):
        os.makedirs("m3u8_file")
    if not os.path.exists("m3u8_file/"+root):
        os.makedirs("m3u8_file/"+root) 
        
    #print url
    context = ssl._create_unverified_context()
    
    try:
        
        req = urllib2.Request(url, headers = header)
        response = urllib2.urlopen(req,context=context)
        html = response.read()
    except:
        response = urllib2.urlopen(url,header,context=context)
        html= response.read()
        
    encoding = response.info().get('Content-Encoding')
    """获得压缩信息"""

    #language = response.info().getparam('charset')
    """获取编码信息"""
    if encoding == 'gzip':
        """如果是'gzip'压缩(最常用的方式)"""
        text= BytesIO()
        text.write(html)
        text.seek(0)
        with gzip.GzipFile(fileobj=text, mode='rb') as fo:
            gunzipped_bytes_obj = fo.read()
 
        html = gunzipped_bytes_obj.decode()

        

    if encoding == 'deflate':
        """如果是'deflate'压缩(少数落后网站还在用)"""
        html = zlib.decompress(html, -zlib.MAX_WBITS)

        """如果是'GB2312'编码,需要转为'utf-8'编码"""
        #if language == 'GB2312':
        #html = unicode(html, 'gbk').encode('utf-8')

    
    html=json.loads(html)

    with open("m3u8_file/"+root+"/look.txt","w") as f:
        json.dump(html,f,indent=4,sort_keys=True)#
    
    with open("m3u8_file/"+root+"/index.txt","w") as f:
        json.dump(html,f,sort_keys=True)#indent=4
    return html

def get_m3u8(html_text,root):
    header = {    
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
    'Referer': 'https://92m303r2a84roj2l0234.guoguoapps.com',
        }
    if not os.path.exists("m3u8_file/"+root):
        return
    with open("m3u8_file/"+root+"/index.txt","r") as file:
        text=file.read()
    html_text=(text)
    #re.compile(r'\"coverpic\": \"(https://pic.1024av.cc.*?.[jpg|png])\", (.*?)+\s(.*?)+\"down_url\": \"(/vod/reqdown/\d+)\", (.*?)+\s(.*?)+\"play_url\": \"(/vod/reqplay/\d+)\", (.*?)+\s(.*?)+\"title\": \"(.*?)\"')
    pattern = re.compile(r'\"coverpic\": \"(https://pic.1024av.cc.*?.[jpg|png])\", (.*?)+\s(.*?)+\"down_url\": \"(/vod/reqdown/\d+)\", (.*?)+\s(.*?)+\"play_url\": \"(/vod/reqplay/\d+)\", (.*?)+\s(.*?)+\"title\": \"(.*?)\"')
    vedio_data = (pattern.findall(html_text)) # match默认从开头开始匹配，开头是字母o，所以没有匹配成功



    context = ssl._create_unverified_context()
    print ("start!")


    for it in vedio_data:
        new_list = list(tuple(it))
        del new_list[8]
        del new_list[7]
        del new_list[5]
        del new_list[4]
        del new_list[2]
        del new_list[1]
        
        url_base="https://92m303r2a84roj2l0234.guoguoapps.com"
        url_really=url_base+new_list[-2]
        #print "title: "+new_list[-1].decode('unicode_escape')+ "  " + "http: " + url_really
        
        try:
            req = urllib2.Request(url_really, headers = header)
            response = urllib2.urlopen(req,context=context)
            html = json.loads(response.read())
        except:
            response = urllib2.urlopen(url_really,header,context=context)
            html= json.loads(response.read())
        f=open("m3u8_file/"+root+"/m3u8.txt",'a+')
        try:
            #print (html)
            m3u8=html['data']['httpurl'].replace("?300","")
            print ("title: "+new_list[-1]+ "  " + "http: " + m3u8)
            f.write(new_list[-1].decode('unicode_escape') + "," + m3u8)
            f.write("\n")
        except:
            try:
                m3u8=html['data']['httpurl_preview'].replace("?300","")
                print  (new_list[-1].decode('unicode_escape')+ "," + m3u8)
                f.write(new_list[-1].decode('unicode_escape')+ ","+ m3u8)
                f.write("\n")
            except Exception as e:
                print ("error-> ",e)
        f.close()

    print ("over!")

            



        
try:      
    type_num=int(input("请输入下载类型：\n\
            1偷拍自拍.\n\
            2制服诱惑.\n\
            3清纯少女.\n\
            4辣妹大奶.\n\
            5女同专属.\n\
            6素人出演.\n\
            7角色扮演.\n\
            8成人动漫.\n\
            9人妻熟女.\n\
            10变态另类.\n\
            11经典伦理.\n\
            12首页.\n\
            13全部.\n\
            14搜索.\n "))
    page=int(input(u"请输入下载页数：\n"))
except:
    type_num=input("请输入下载类型：\n\
            1偷拍自拍.\n\
            2制服诱惑.\n\
            3清纯少女.\n\
            4辣妹大奶.\n\
            5女同专属.\n\
            6素人出演.\n\
            7角色扮演.\n\
            8成人动漫.\n\
            9人妻熟女.\n\
            10变态另类.\n\
            11经典伦理.\n\
            12首页.\n\
            13全部.\n\
            14搜索.\n ")
    page=input(u"请输入下载页数：\n")
if type_num==14:
    print("not found！\n")
elif type_num==12:
    url=type_dict[type_list[type_num-1]]
    html=get_url(url,type_list[type_num-1])
    get_m3u8(html,type_list[type_num-1])
else:
    for i in range(1,page+1):
        url=type_dict[type_list[type_num-1]]
        html=get_url(url,type_list[type_num-1],str(i))
        get_m3u8(html,type_list[type_num-1])



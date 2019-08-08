import requests,re

# pc headers user-agent
user_agent_pc = [
    # 谷歌
    'Mozilla/5.0.html (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.html.2171.71 Safari/537.36',
    'Mozilla/5.0.html (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.html.1271.64 Safari/537.11',
    'Mozilla/5.0.html (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.html.648.133 Safari/534.16',
    # 火狐
    'Mozilla/5.0.html (Windows NT 6.1; WOW64; rv:34.0.html) Gecko/20100101 Firefox/34.0.html',
    'Mozilla/5.0.html (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
    # opera
    'Mozilla/5.0.html (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.html.2171.95 Safari/537.36 OPR/26.0.html.1656.60',
    # qq浏览器
    'Mozilla/5.0.html (compatible; MSIE 9.0.html; Windows NT 6.1; WOW64; Trident/5.0.html; SLCC2; .NET CLR 2.0.html.50727; .NET CLR 3.5.30729; .NET CLR 3.0.html.30729; Media Center PC 6.0.html; .NET4.0C; .NET4.0E; QQBrowser/7.0.html.3698.400)',
    # 搜狗浏览器
    'Mozilla/5.0.html (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.html.963.84 Safari/535.11 SE 2.X MetaSr 1.0.html',
    # 360浏览器
    'Mozilla/5.0.html (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.html.1599.101 Safari/537.36',
    'Mozilla/5.0.html (Windows NT 6.1; WOW64; Trident/7.0.html; rv:11.0.html) like Gecko',
    # uc浏览器
    'Mozilla/5.0.html (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.html.2125.122 UBrowser/4.0.html.3214.0.html Safari/537.36',
]

#随机获取一个PC headers user_agent
def get_user_agent_pc():
    return random.choice(user_agent_pc)

#百度网盘转存
#   furl = 分享链接
#   verify = 提取码
#   savepath = 转存到百度网盘指定目录
#   BDUSS = 从百度COOKICES中提取
#   STOKEN = 从百度COOKICES中提取
#   bdstoken = 从百度COOKICES中提取
def bdsave(furl,verify,savepath,BDUSS,STOKEN,bdstoken):
    s = requests.Session()
    s.cookies['BDUSS'] = BDUSS
    s.cookies['STOKEN'] = STOKEN
    surl=furl.split('/')[-1][1:len(furl.split('/')[-1])]
    headers={
        'User-Agent': user_agent_pc(),
        'Referer': 'https://pan.baidu.com/share/init?surl='+surl
    }
    req = s.get(furl,headers=headers)
    req.encoding='utf-8'
    if '侵权、色情、反动、低俗' in req.text:
        return ('此链接分享内容可能因为涉及侵权、色情、反动、低俗等信息，无法访问！')
    else:
        purl='https://pan.baidu.com/api/report/user?channel=chunlei&web=1&app_id=250528&bdstoken='+bdstoken+'&logid=MTU2NTI1MzM3OTY2MDAuMjI4MDU3NjY2NTk5MDkwODg=&clienttype=0'
        data = {'timestamp':'1565244533','action':'web_home'}
        req = s.post(purl,data=data,headers=headers)
        purl = 'https://pan.baidu.com/share/verify?surl='+surl+'&t=1565244999152&channel=chunlei&web=1&app_id=250528&bdstoken='+bdstoken+'&logid=MTU2NTI1MzM3OTY2MDAuMjI4MDU3NjY2NTk5MDkwODg=&clienttype=0'
        data = {'pwd':verify,'vcode':'','vcode_str':''}
        req = s.post(purl,data=data,headers=headers)
        rinfo = re.findall('"errno":[-]{0,1}\d+',req.text)[0].replace('"errno":','')
        if rinfo == '-12':
            return ('验证码错误。')
        else:
            req = s.get(furl,headers=headers)
            req.encoding='utf-8'
            shareid=re.findall('"shareid":\d+',req.text)[0].replace('"shareid":','')
            uk=re.findall('uk=\d+',req.text)[0].replace('uk=','')
            fsidlist = re.findall('"fs_id":\d+', req.text)[0].replace('"fs_id":','')
            app_id = re.findall('"app_id":"\d+"',req.text)[0].replace('"app_id":','').replace('"','')
            #print('shareid:',shareid,'uk:',uk,'fs_id:',fsidlist,'app_id:',app_id)
            purl='https://pan.baidu.com/share/transfer?shareid='+shareid+'&from='+uk+'&channel=chunlei&web=1&app_id='+app_id+'&bdstoken='+bdstoken+'&logid=MTU2NTI1MzM3OTY2MDAuMjI4MDU3NjY2NTk5MDkwODg=&clienttype=0'

            data = {
                'fsidlist':'['+fsidlist+']',
                'path':'/'+savepath
            }
            req =s.post(purl,data=data,headers=headers)
            req.encoding = 'utf-8'
            try:
                zcinfo = re.findall('\[\{"errno":[-]{0,1}\d+',req.text)[0].replace('[{"errno":','')
            except:
                return 'Cookies失效，请更新BDUSS、STOKEN、bdstoken后再试！'
            else:
                info ={
                    "0":"转存成功。",
                    "-1":"由于您分享了违反相关法律法规的文件，分享功能已被禁用，之前分享出去的文件不受影响。",
                    "-2":"用户不存在,请刷新页面后重试。",
                    "-3":"文件不存在,请刷新页面后重试。",
                    "-4":"登录信息有误，请重新登录试试。",
                    "-5":"host_key和user_key无效。",
                    "-6":"请重新登录。",
                    "-7":"该分享已删除或已取消。",
                    "-8":"该分享已经过期。",
                    "-9":"访问密码错误。",
                    "-10":"分享外链已经达到最大上限100000条，不能再次分享。",
                    "-11":"验证cookie无效。",
                    "-14":"对不起，短信分享每天限制20条，你今天已经分享完，请明天再来分享吧！",
                    "-15":"对不起，邮件分享每天限制20封，你今天已经分享完，请明天再来分享吧！",
                    "-16":"对不起，该文件已经限制分享！",
                    "-17":"文件分享超过限制。",
                    "-21":"预置文件无法进行相关操作。",
                    "-30":"文件已存在。",
                    "-31":"文件保存失败。",
                    "-33":"一次支持操作999个，减点试试吧。",
                    "-32":"未知结果。",
                    "-70":"你分享的文件中包含病毒或疑似病毒，为了你和他人的数据安全，换个文件分享吧。",
                    "2":"参数错误。",
                    "3":"未登录或帐号无效。",
                    "4":"存储好像出问题了，请稍候再试。",
                    "108":"文件名有敏感词，优化一下吧。",
                    "110":"分享次数超出限制，可以到“我的分享”中查看已分享的文件链接。",
                    "114":"当前任务不存在，保存失败。",
                    "115":"该文件禁止分享。",
                    "112":'页面已过期，请刷新后重试。',
                    "9100":'你的帐号存在违规行为，已被冻结。',
                    "9200":'你的帐号存在违规行为，已被冻结。',
                    "9300":'你的帐号存在违规行为，该功能暂被冻结。',
                    "9400":'你的帐号异常，需验证后才能使用该功能。',
                    "9500":'你的帐号存在安全风险，已进入保护模式，请修改密码后使用。'}
                return (info[zcinfo])

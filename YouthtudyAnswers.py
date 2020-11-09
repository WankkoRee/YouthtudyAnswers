# -*- coding: utf-8 -*-
#Author:    Wankko Ree
#Time:      2020/11/09 23:06
#Version:   v1.14


import codecs
import smtplib
import sys
import time
import traceback
from email.mime.text import MIMEText
from email.utils import formataddr
import requests
from lxml import html
import re


def getMidString(str, start_str, end_str):
    start = str.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = str.find(end_str, start)
        if end >= 0:
            return str[start:end].strip()

try:
    response = requests.get(
        "http://h5.cyol.com/special/daxuexi/daxuexiall/m.html",
        headers={
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045130 Mobile Safari/537.36 MMWEBID/2526 MicroMessenger/7.0.11.1600(0x27000B32) Process/tools NetType/WIFI Language/zh_CN ABI/arm64",
            "Host": "h5.cyol.com",
            "Accept-Encoding": "gzip, deflate, br"
        }
    )
    response.encoding = 'utf-8'
    lastUrl = re.findall(r"\$\('#[\s\S]*? \.[\s\S]*?'\)\.click\(function\(\){[\s]*location.href='([\s\S]*?)';[\s]*}\);", response.text)[-1]
    print(lastUrl)
    time.sleep(5)
    response = requests.get(
        lastUrl,
        headers={
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045130 Mobile Safari/537.36 MMWEBID/2526 MicroMessenger/7.0.11.1600(0x27000B32) Process/tools NetType/WIFI Language/zh_CN ABI/arm64",
            "Host": "h5.cyol.com",
            "Accept-Encoding": "gzip, deflate, br"
        }
    )
    response.encoding = 'utf-8'
    lastUrl = re.findall(r"\$\('#[\s\S]*? \.[\s\S]*?'\)\.click\(function\(\){[\s]*location.href='([\s\S]*?)';[\s]*}\);", response.text)[-1].replace("index.php", "m.php").replace("index.htm", "m.htm")
    print(lastUrl)
    time.sleep(5)
    response = requests.get(
        lastUrl,
        headers={
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045130 Mobile Safari/537.36 MMWEBID/2526 MicroMessenger/7.0.11.1600(0x27000B32) Process/tools NetType/WIFI Language/zh_CN ABI/arm64",
            "Host": "h5.cyol.com",
            "Accept-Encoding": "gzip, deflate, br"
        }
    )
    response.encoding = 'utf-8'
    title = getMidString(response.text, "var shareDesc = '", "';")
    miniTitle = getMidString(response.text, "var shareTitle = '", "';")
    publishDate = html.fromstring(response.text).xpath("//meta[@name='publishdate']/@content")[0]
    titleImg = html.fromstring(response.text).xpath("//video[@id='Bvideo']/@poster")[0]
    if titleImg[0:4] != "http":
        titleImg = response.url[0:response.url.rfind("/") + 1] + titleImg
    video = html.fromstring(response.text).xpath("//video[@id='Bvideo']/@src")[0]
    shareImg = getMidString(response.text, "var shareImg = '", "';")
    print(miniTitle + "——《" + title + "》[" + publishDate + "]")
    print(titleImg)
    print(video)
    print(shareImg)

    encodejs = getMidString(response.text, "<script>", "</script>")

    answers = {}
    orders = {}

    regex = re.finditer("""<div class=['"](\S+)['"]>\s*(<div class=['"]\S+['"]></div>\s*)*(<div class=['"]\S+ option['"] data-a=['"]\S['"][\s\S]*?></div>\s*)+(<div class=['"]\S+['"]></div>\s*)*</div>""", response.text)
    for i in regex:
        regexS = re.findall("""<div class=['"]\S+ option['"] data-a=['"](\S)['"][\s\S]*?></div>""", i.group())
        base = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        answer = ""
        for j in range(0, len(regexS)):
            if regexS[j] == '1':
                answer += base[j]
        tmpLen = len(answer)
        if tmpLen >= 2: # 多选
            answer = answer[0:int(tmpLen/2)]
        answers[i.groups()[0]] = [answer]
        orders[i.start()] = i.groups()[0]

    regex = re.finditer("""<div class=['"](\S+)['"]>\s*(<div class=['"]\S+['"]></div>\s*)*<div class=['"]\S+_ul['"]>\s*(<div class=['"]\S+_li['"] data=['"]\S+['"] data1=-2></div>\s*)+</div>\s*(<div class=['"]\S+['"]></div>\s*)*</div>""", response.text)
    for i in regex:
        rightAnswer = getMidString(getMidString(response.text, """$(".""" + i.groups()[0] + """_click").on('click',function(){""", "});"), "if(", "){")
        regexS = re.findall("""data1.ary2\[\S\]==(\S)""", rightAnswer)
        base = "①②③④⑤⑥⑦⑧⑨⑩"
        answer = ""
        for j in range(0, len(regexS)):
            answer += base[int(regexS[j])]
        answers[i.groups()[0]] = [answer]
        orders[i.start()] = i.groups()[0]

    regex = re.search("""\(\$,'(\S+)'\)\['removeClass'\]""", response.text)
    questionAfterClass = regex.group(1).replace(".", "").split(",")

    ordersNew = {}
    for i in sorted(orders.keys()):
        ordersNew[i] = orders[i]
    n = len(ordersNew)
    y = len(questionAfterClass)
    x = n - y
    answersString = ""
    for i in range(0, x):
        tmp = "第" + str(i + 1) + "题：" + answers[ordersNew[list(ordersNew.keys())[i]]][0]
        answersString += tmp + "<br />"
        print(tmp)
    for i in range(0, y):
        tmp = "课后第" + str(i + 1) + "题：" + answers[ordersNew[list(ordersNew.keys())[i + x]]][0]
        answersString += tmp + "<br />"
        print(tmp)

    resultHTML = """<!DOCTYPE html>
<html lang="zh">
	<head>
		@include('layouts.header')
		<title>青学Answers - {{ env('APP_NAME') }}</title>
		<meta property="og:img" content="splitshareImg">
	</head>
	<body class="page-body">
	    <p style="display: none;">
            <img src="splitshareImg" />
        </p>
        <div class="page-container">
	        @include('layouts.sidebar')
	        <div class="main-content">
	            <nav class="navbar user-info-navbar" role="navigation">
	                <ul class="user-info-menu left-links list-inline list-unstyled">
	                    <li class="hidden-sm hidden-xs">
	                        <a href="#" data-toggle="sidebar">
	                            <i class="fa fa-bars"></i>
	                        </a>
	                    </li>
	                </ul>
	            </nav>
	            <div class="row">
					<div class="col-sm-4" align="center">
	            		<video poster="splittitleImg" width="320px" controls="controls" src="splitvideo"></video>
	            	</div>
	            	<div class="col-sm-8">
				        <h3 align="center">《splittitle》</h3>
				        <h4 align="right">——splitminiTitle</h4>
				        <h5 align="center">官方编辑日期：splitpublishDate</h5>
				        <strong>splitanswersString</strong>
				        <p>答案仅供参考，反正官方动不动就改动框架，我也莫得办法，只能跟在后面修bug</p>
                        <div class="btn-group" id="fakeTitle">
                            <button type="button" class="btn btn-primary dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                选择伪造的分享标题 <span class="caret"></span>
                            </button>
                            <ul class="dropdown-menu">
                            </ul>
                        </div>
				        <div align="center">
					        Copyright © <kbd>青学Answers</kbd> by <a href="https://www.wkr.moe">Wankko Ree</a> All Rights Reserved.<br />
					        Powered by <kbd>splitPythonVersion</kbd><br />
					        Source Code: <a href="https://github.com/WankkoRee/YouthtudyAnswers">YouthtudyAnswers - Github</a><br />
					        Update Time: <kbd>splitupdateTime</kbd><br />
				        </div>
				    </div>
				</div>
				@include('layouts.footer')
			</div>
		</div>
		<script src="https://jsdec.js.org/js/dec.js"></script>
		<script>
		    function midstr(str, begin, end){
		        var left = str.indexOf(begin) + begin.length;
		        var right = str.indexOf(end, left);
		        return str.substring(left, right);
		    }
		    var encjs = String.raw`splitencodejs`;
		    var decjs = dec_jsjiamiv6_default(encjs);
		    decjs = decjs.substring(0, decjs.lastIndexOf(';'));
		    var shareArr = decjs.match(/sharetitle=(\S+?);/g);
		    for(i in shareArr){
                var exp = shareArr[i];
                var value = midstr(exp, '=', ';');
                var varegex = /_0x(\S+)\['(\S+)'\]/;
                if(varegex.test(value)){
                    var name = midstr(exp, "'", "'");
                    while(decjs.search("'"+name+"':_0x") != -1){
                        name = midstr(decjs, "'"+name+"':_0x", ']');
                        name = midstr(name, "'", "'");
                    }
                    value = midstr(decjs, "'"+name+"':'", "'");
                }else{
                    value = midstr(decjs, "'"+name+"':'", "'");
                }
                $("#fakeTitle>ul").append('<li><a href="#">'+ value + '</a></li>');
            }
		</script>
		<script>
		    $("#fakeTitle>ul>li>a").click(function(){
                $(document).attr("title", $(this).text());
                alert("修改标题成功，尽情分享吧");
            });
		</script>
	</body>
</html>"""
    updateTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    resultHTML = resultHTML.replace("splittitleImg", titleImg).replace("splittitle", title).replace("splitminiTitle", miniTitle).replace("splitpublishDate", publishDate).replace("splitvideo", video).replace("splitanswersString", answersString).replace("splitupdateTime", updateTime).replace("splitPythonVersion", "Python " + str(sys.version_info.major) + "." + str(sys.version_info.minor) + "." + str(sys.version_info.micro)).replace("splitencodejs", encodejs).replace("splitshareImg", shareImg) # 实际上分享封面图并不显示，必须要公众号api才行
    file = codecs.open("YouthtudyAnswers.blade.php", "w", "utf-8")
    file.write(resultHTML)
    file.close()
except TimeoutError as err:
    print("网络异常")
    traceback.print_exc()
except Exception as err:
    print("ERROR!")
    traceback.print_exc()
    smtpObj = smtplib.SMTP_SSL("smtp服务器", 端口号)
    emailAddr = "邮箱"
    emailPswd = "密码"
    emailName = "昵称"
    smtpObj.login(emailAddr, emailPswd)
    message = MIMEText(traceback.format_exc(), 'plain', 'utf-8')
    message['From'] = formataddr([emailName, emailAddr])
    message['To'] = formataddr([emailName, emailAddr])
    message['Subject'] = "青学Answers源码需要更新"
    smtpObj.sendmail(emailAddr, [emailAddr], message.as_string())

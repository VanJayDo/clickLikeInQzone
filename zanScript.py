#!/bin/env python
#coding: utf-8

#Author:Vanjay Do
#Repo URL:https://github.com/VanjayDo/clickLikeInQzone.git

from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import string

#设置所需参数
VALS={
	"ACCOUNT" :"*********",#QQ账号
	"PASSWORD" :"********",#QQ密码
	"NickName" :"********",#QQ昵称
	"AutoReply":"[自动回复]本人空间已交由爬虫进行自动点赞和回复，有问题请直接联系我，谢谢。"#自动回复，根据自己需要修改
}

ZAN="""
	//点赞
	var myAccount=$ACCOUNT;
	var all=document.getElementsByClassName("item qz_like_btn_v3");
	for(var i=0;i<all.length;i++)
	{ 
		if(all[i].getAttribute("data-clicklog")=="like")
		{
			target=all[i].getAttribute("data-unikey");
			if(target.indexOf(myAccount)==-1)//不点自己的说说，需要的话可以去掉该判断条件
			{
				all[i].click();
				if(all[i].getAttribute("data-clicklog")=="like") all[i].click();
				console.log("Just clicked the-> "+target+" <-");//其中target为说说地址，可在浏览器粘贴直接访问
				break;//考虑到js异步的特点，每次只点一条
			}
		}
	}
	"""
REPLY="""
	//函数：对@本人的说说进行查找
	function search(){
		var myNickName="$NickName";
		var myAccount="$ACCOUNT";
		var comment=document.getElementsByClassName("comments-item bor3");
		for(var j=0;j<comment.length;j++)
		{
			var content=comment[j].getElementsByClassName("comments-content");
			var allAt=content[0].getElementsByClassName("nickname name c_tx  q_namecard");
			for(var i=0;i<allAt.length;i++)
			{
				if((allAt[i].innerText).indexOf("@"+myNickName)!=-1&&allAt[i].href.indexOf(myAccount)!=-1)
				{
					if(comment[j].getElementsByClassName("comments-list mod-comments-sub").length==0)
					{
						content[0].getElementsByClassName("act-reply none")[0].click();
						return 1;
					}
				}
			}
		}
		return 0;
	}
	//函数：进行回复
	function reply()
	{
		var autoReply="$AutoReply";
		var box=document.getElementsByClassName("comment-box-wrap")[0];
		box=document.getElementsByClassName("comment-box-wrap")[0];
		if(box!=null)
		{
			box.getElementsByClassName("textinput textarea c_tx2")[0].innerText=autoReply;
			document.getElementsByClassName("btn-post gb_bt  evt_click")[1].click();
			console.log("Just clicked auto-reply");
		}	
	}
	var atMe=0; 
	atMe=search();
	if(atMe==1)
	{
		reply();
	}
	"""

def quit(driver):
	driver.quit()
	exit(0)

def login(driver):
	print ("Logging......")
	driver.get("http://i.qq.com/")
	time.sleep(5)
	driver.switch_to_frame("login_frame")
	time.sleep(3)
	driver.find_element_by_id("switcher_plogin").click()
	time.sleep(3)
	driver.find_element_by_id("u").clear()  
	driver.find_element_by_id("u").send_keys(VALS.get("ACCOUNT"))
	time.sleep(2)
	driver.find_element_by_id("p").clear()
	driver.find_element_by_id("p").send_keys(VALS.get("PASSWORD"))
	# driver.save_screenshot('before-click-login-button.png')#填完用户密码登录之前截图，有需要的取消注释
	time.sleep(2)
	driver.find_element_by_id("login_button").click()
	# driver.save_screenshot('after-click-login-button-butNotLogin.png')#此时应该还没登录上显示“登录中”，截图，有需要的取消注释
	time.sleep(5)
	# driver.save_screenshot('after-click-login-button-shouldHaveLogined.png')#正常网络情况下此时应该已经登录上，显示空间内容界面，截图，有需要的取消注释
	try:
		driver.find_element_by_id('feed_tab_hover')
	except NoSuchElementException:
		print("Login failed,\nplease check your account & password & network,\nor maybe you are limited from loginning.")
		quit(driver)
	else:
		print("Login successfully.")
		return driver
	
if __name__=="__main__":
	dcap = dict(DesiredCapabilities.PHANTOMJS)
	dcap["phantomjs.page.settings.resourceTimeout"] = 15
	dcap["phantomjs.page.settings.loadImages"] = False 
	dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (X11; Linux x86_64; rv:23.0) Gecko/20100101 Firefox/23.0") #伪装ua
	driver = webdriver.PhantomJS(desired_capabilities=dcap)
	# driver.viewportSize={'width':1024,'height':800} #设置截图分辨率，需要截图的取消注释
	# driver.maximize_window()#窗口最大化，需要截图的取消注释
	zanTemp =string.Template(ZAN)
	newZAN=zanTemp.substitute(VALS)
	replyTemp =string.Template(REPLY)
	newREPLY=replyTemp.substitute(VALS)
	couter=0
	while 1:
		try:
			driver.find_element_by_id('feed_tab_hover')
		except NoSuchElementException:
			driver=login(driver)
		else:
			driver.execute_script(newZAN)
			driver.execute_script(newREPLY)
			#driver.save_screenshot("screenshot"+str(couter)+".png")#每次执行自动点赞和回复后进行截图，有需要的取消注释
			#couter++
			log=driver.get_log("browser")
			for i in log:
				if (i["message"].find("clicked")!=-1):
					print(str(i["message"]).encode("utf8"))
			driver.refresh()
			time.sleep(30)
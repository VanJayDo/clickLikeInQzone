#!/bin/env python
#coding: utf-8
__author__="Vanjay Do"

from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
import time

ACCOUNT="******"#改为账号
PASSWORD="*****"#改为密码

ZAN="""
	//点赞
	var myAccount="******";//设置自己的账号
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
		var myNickName="****";//设置直接的qq昵称
		var myAccount="*****";//设置自己的账号
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
		var autoReply="[自动回复]本人空间已交由爬虫进行自动点赞和回复，有问题请直接联系我，谢谢。";
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
	time.sleep(3)
	driver.switch_to_frame("login_frame")
	time.sleep(3)
	driver.find_element_by_id("switcher_plogin").click()
	time.sleep(3)
	driver.find_element_by_id("u").clear()  
	driver.find_element_by_id("u").send_keys(ACCOUNT)
	driver.find_element_by_id("p").clear()
	driver.find_element_by_id("p").send_keys(PASSWORD)
	time.sleep(3)
	driver.find_element_by_id("login_button").click()
	time.sleep(3)
	try:
		driver.find_element_by_id('feed_tab_hover')
	except NoSuchElementException:
		print("Login failed,\nplease check your account & password & network,\nor maybe you are limited from loginning.")
		quit(driver)
	else:
		print("Login successfully.")
		return driver
	
if __name__=="__main__":
	driver = webdriver.PhantomJS()
	while 1:
		try:
			driver.find_element_by_id('feed_tab_hover')
		except NoSuchElementException:
			driver=login(driver)
		else:
			driver.execute_script(ZAN)
			driver.execute_script(REPLY)
			log=driver.get_log("browser")
			for i in log:
				if (i["message"].find("clicked")!=-1):
					print(str(i["message"]).encode("utf8"))
			driver.refresh()
			time.sleep(30)
# -*- coding: utf-8 -*-
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
			}
		}
	}
	"""

REPLY="""
	//下面对@本人的评论进行自动回复
	var myNickName="*****";//设置自己的qq昵称
	
	var autoReply="[自动回复]本人空间已交由爬虫进行自动点赞和回复，有问题请直接联系我，谢谢。";
	var comment=document.getElementsByClassName("comments-item bor3");
	for(var j=0;j<comment.length;j++)
	{
	    var content=comment[j].getElementsByClassName("comments-content");
	    var allAt=content[0].getElementsByClassName("nickname name c_tx  q_namecard");
	    for(var i=0;i<allAt.length;i++)
	    {
	        if((allAt[i].innerText).indexOf("@"+myNickName)!=-1)
	        {
	            if(comment[j].getElementsByClassName("comments-list mod-comments-sub").length==0)
	            {
	                content[0].getElementsByClassName("act-reply none")[0].click();
	                var box=document.getElementsByClassName("comment-box-wrap")[0];
	                box=document.getElementsByClassName("comment-box-wrap")[0];
                	if(box==null)
	                	console.log("click is null");
	       			else
	       			{
                		box.getElementsByClassName("textinput textarea c_tx2")[0].innerText=autoReply;
                		comment[j].getElementsByClassName("btn-post gb_bt  evt_click")[0].click();
                		console.log("Just clicked auto-reply");
	       			}
	            }
	        }
	    }
	}
	"""

def login(driver):
	try:
		print ("Logging......")
		driver.get("http://qzone.qq.com/")
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
	except Exception as e:
		print("Login failed,\nplease check your account & password & network.\n")
		driver.close()
		exit(0)
	else:
		print("Login successfully.")
		return driver

if __name__=="__main__":
	driver = webdriver.PhantomJS()#window下需填入executable_path="浏览器绝对路径"属性	
	while 1:
		a=driver.execute_script("return document.getElementById('feed_tab_hover')")
		if a is None:
			driver=login(driver)
		driver.execute_script(ZAN)
		driver.execute_script(REPLY)
		log=driver.get_log("browser")
		for i in log:
			if (i["message"].find("clicked")!=-1):
				print(str(i["message"]).encode("utf8"))
		driver.refresh()
		time.sleep(30)
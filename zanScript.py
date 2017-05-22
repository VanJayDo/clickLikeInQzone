from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time

ACCOUNT="******"#改为账号
PASSWORD="*****"#改为密码

ZAN="""
	var all=document.getElementsByClassName("item qz_like_btn_v3");
	console.log("Finding unclicked");
	for(var i=0;i<all.length;i++)
	{ 
		if(all[i].getAttribute("data-clicklog")=="like")
		{
			target=all[i].getAttribute("data-unikey");
			all[i].click();
			console.log("Just clicked the-> "+target+" <-");//其中target为说说地址，可在浏览器粘贴直接访问
		}
	}"""

def login(driver):
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
	return driver

if __name__=="__main__":
	driver = webdriver.PhantomJS()#window下需填入executable_path="浏览器绝对路径"属性
	while 1:
		try:
			driver.find_element_by_xpath('//a[@id="feed_tab_hover"]')
		except NoSuchElementException:
			driver=login(driver)
			try:
				driver.find_element_by_xpath('//a[@id="feed_tab_hover"]')
			except NoSuchElementException:
				print("Login failed,\nplease check your account & password & network.\n")
				exit(0)
			else:
				print("Login successfully.")
		driver.execute_script(ZAN)
		log=driver.get_log("browser")
		for i in log:
			if (i["message"].find("click")!=-1):
				print(str(i["message"]).encode("utf8"))
		driver.refresh()
		time.sleep(30)
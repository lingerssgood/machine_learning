#微博自动化运营方略
#首先：微博登录
#1、加关注
#2、写评论
#3、发微博

from selenium import webdriver
import time
browser=webdriver.Chrome()
# 登录微博
def weibo_login(username,password):
     #打开微博登录页
     browser.get('https://passport.weibo.cn/signin/login')
     #隐式等待5秒，5秒内没发现元素则报错
     browser.implicitly_wait(5)
     #在给定的时间内挂起当前线程的执行
     time.sleep(1)
     # 填写登录信息：用户名、密码
     #send_keys:填写文本；clear:清除文本；click:点击操作；submit:提交表单
     browser.find_element_by_id("loginName").send_keys(username)
     browser.find_element_by_id("loginPassword").send_keys(password)
     time.sleep(1)
     # 点击登录
     browser.find_element_by_id("loginAction").click()
     time.sleep(1)
#添加指定用户
def add_follow(uid):
     browser.get('https://m.weibo.com/u/' + str(uid))
     time.sleep(1)
     # browser.find_element_by_id("follow").click()
     follow_button = browser.find_element_by_xpath('//div[@class="m-add-box m-followBtn"]')
     follow_button.click()
     time.sleep(1)
     # 选择分组
     group_button = browser.find_element_by_xpath('//div[@class="m-btn m-btn-white m-btn-text-black"]')
     group_button.click()
     time.sleep(1)
# 给指定某条微博添加内容
def add_comment(weibo_url, content):
     browser.get(weibo_url)
     browser.implicitly_wait(5)
     content_textarea = browser.find_element_by_css_selector("textarea.W_input").clear()
     content_textarea = browser.find_element_by_css_selector("textarea.W_input").send_keys(content)
     time.sleep(2)
     comment_button = browser.find_element_by_css_selector(".W_btn_a").click()
     time.sleep(1)

# 发文字微博
def post_weibo(content):
     # 跳转到用户的首页
     browser.get('https://weibo.com')
     browser.implicitly_wait(5)
     # 点击右上角的发布按钮
     post_button = browser.find_element_by_css_selector("[node-type='publish']").click()
     # 在弹出的文本框中输入内容
     content_textarea = browser.find_element_by_css_selector("textarea.W_input").send_keys(content)
     time.sleep(2)
     # 点击发布按钮
     post_button = browser.find_element_by_css_selector("[node-type='submit']").click()
     time.sleep(1)



if __name__=='__main__':
     # 设置用户名、密码
     username = 'XXXX'
     password = "XXXX"
     weibo_login(username, password)
     # 每天学点心理学UID
     uid = '1890826225'
     add_follow(uid)
     # 给指定的微博写评论
     weibo_url = 'https://weibo.com/1890826225/HjjqSahwl'
     content = 'Gook Luck!好运已上路！'
     # 自动发微博
     content = '每天学点心理学'
     post_weibo(content)
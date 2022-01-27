from selenium import webdriver
import time
browser = webdriver.Chrome()
# browser=webdriver.ie()
# browser=webdriver.firefox()
# ��¼΢��
def weibo_login(username, password):
     # ��΢����¼ҳ
     browser.get('https://passport.weibo.cn/signin/login')
     browser.implicitly_wait(5)
     time.sleep(1)
     # ��д��¼��Ϣ���û���������
     #��λԪ��
     a=browser.find_element_by_id("loginName").send_keys(username)
     print(a)
     browser.find_element_by_id("loginPassword").send_keys(password)
     time.sleep(1)
     # �����¼
     browser.find_element_by_id("loginAction").click()
     time.sleep(1)
     # �����û���������

# ���ָ�����û�
def add_follow(uid):
    browser.get('https://m.weibo.com/u/'+str(uid))
    time.sleep(1)
    #browser.find_element_by_id("follow").click()
    follow_button = browser.find_element_by_xpath('//div[@class="m-add-box m-followBtn"]')
    follow_button.click()
    time.sleep(1)
    # ѡ�����
    group_button = browser.find_element_by_xpath('//div[@class="m-btn m-btn-white m-btn-text-black"]')
    group_button.click()
    time.sleep(1)

# ��ָ��ĳ��΢���������
def add_comment(weibo_url, content):
    browser.get(weibo_url)
    browser.implicitly_wait(5)
    content_textarea = browser.find_element_by_css_selector("textarea.W_input").clear()
    content_textarea = browser.find_element_by_css_selector("textarea.W_input").send_keys(content)
    time.sleep(2)
    comment_button = browser.find_element_by_css_selector(".W_btn_a").click()
    time.sleep(1)

# ������΢��
def post_weibo(content):
    # ��ת���û�����ҳ
    browser.get('https://weibo.com')
    browser.implicitly_wait(5)
    # ������Ͻǵķ�����ť
    post_button = browser.find_element_by_css_selector("[node-type='publish']").click()
    # �ڵ������ı�������������
    content_textarea = browser.find_element_by_css_selector("textarea.W_input").send_keys(content)
    time.sleep(2)
    # ���������ť
    post_button = browser.find_element_by_css_selector("[node-type='submit']").click()
    time.sleep(1)

if __name__=='__main__':
    username = 'XXXX'
    password = "XXXX"
    weibo_login(username, password)
    # ��ָ����΢��д����
    weibo_url = 'https://weibo.com/1890826225/HjjqSahwl'
    # content = 'Gook Luck!��������·��'
    # �Զ���΢��
    content = 'ÿ��ѧ������ѧ'
    post_weibo(content)
    # ÿ��ѧ������ѧUID
    uid = '1890826225'
    add_follow(uid)
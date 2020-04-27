from selenium import webdriver
import random
import time
import json
import os

def voteLaunch(cookiePath):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("http://www.yiban.cn")
    driver.implicitly_wait(5)
    with open(cookiePath, "r") as fp:
        listCookies = json.load(fp)
    for cookie in listCookies:
        driver.add_cookie(cookie)    
    driver.get("http://www.yiban.cn")
    time.sleep(1)
    driver.get("http://www.yiban.cn/my/publishvote")


    with open("question.txt", "r") as fp:
        lines = fp.read()
    questions = lines.split("\n")
    #print(questions)
    for question in questions:
        list = question.split(",")
        title = list[0]
        optionA = list[1]
        optionB = list[2]
        optionC = list[3]

        driver.get("http://www.yiban.cn/my/publishvote")
        driver.implicitly_wait(5)
        title_field = driver.find_element_by_xpath("/html/body/main/div/section/div[1]/div/div[1]/div[1]/input")
        title_field.send_keys(title)
        choice_field = driver.find_element_by_xpath("/html/body/main/div/section/div[1]/div/ul[1]/li[1]/div[1]/input")
        choice_field.send_keys(optionA)

        choice_field = driver.find_element_by_xpath("/html/body/main/div/section/div[1]/div/ul[1]/li[2]/div/input")
        choice_field.send_keys(optionB)

        choice_field = driver.find_element_by_xpath("/html/body/main/div/section/div[1]/div/ul[1]/li[3]/div/input")
        choice_field.send_keys(optionC)

        target = driver.find_element_by_xpath("/html/body/main/div/section/div[1]/div/p[6]/label/div/ins")
        driver.execute_script("arguments[0].scrollIntoView();", target)          #拖动到可见的元素去

        class_button = driver.find_element_by_xpath("/html/body/main/div/section/div[1]/div/div[3]/ul[1]/li[1]/label/div/ins")
        class_button.click()

        select_button = driver.find_element_by_xpath("/html/body/main/div/section/div[1]/div/p[6]/label/div/ins")
        select_button.click()

        publish_button = driver.find_element_by_xpath("/html/body/main/div/section/div[2]/div/div/a")
        publish_button.click()

        try:
            pageTitle = driver.find_element_by_xpath('//*[@id="vote_content"]/div[1]/span')
            time.sleep(3)
            print("新的投票发布成功！")

        except:  #无界面下验证码无意义
            verity_input = driver.find_elements_by_id("pop_captcha_value")
            str1 = input("输入验证码:")
            verity_input[0].send_keys(str1)
            publish_button = driver.find_element_by_xpath("/html/body/section[2]/div/div[2]/a[1]")
            publish_button.click()
            time.sleep(3)
            print("新的投票发布成功！")
    userName = cookiePath.split(".")
    user = userName[0].split("/")[1]
    print("用户" + user + "发布投票完成！")
    driver.quit()
    
def vote(cookiePath):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("http://www.yiban.cn")
    driver.implicitly_wait(5)
    with open(cookiePath, "r") as fp:
        listCookies = json.load(fp)
    for cookie in listCookies:
        driver.add_cookie(cookie) 
    driver.get("http://www.yiban.cn")
    driver.implicitly_wait(5)

    driver.get("https://www.yiban.cn/newgroup/showMorePub/puid/997180/group_id/444262/type/3")

    voteUrls = []
    #投票个数目前为10
    for i in range(1,6):
        votePageTag = driver.find_element_by_xpath('/html/body/main/div/div/div/div[1]/section[2]/ul/li[' + str(i) + ']/div/div[1]/span[1]/a')
        voteUrls.append(votePageTag.get_attribute('href'))
    #print(voteUrls)

    for url in voteUrls:
        #随机数影响选择
        choice = random.randint(1, 3)
        driver.get(url)
        time.sleep(2)
        choiceBtn = driver.find_element_by_xpath('/html/body/main/div/div/div[1]/article/section[2]/div/table['+ str(choice) +']/tbody/tr/td[1]')
        choiceBtn.click()
        time.sleep(1)
        submitBtn = driver.find_element_by_xpath('/html/body/main/div/div/div[1]/article/section[4]/a[1]')
        submitBtn.click()
        time.sleep(4)
        print("投票成功！")

    userName = cookiePath.split(".")
    user = userName[0].split("/")[1]
    print("用户" + user + "投票完成！")
    driver.quit()

    

def voteMain():    
    print("注意：1.由于易班服务器限制，本程序刷分速度保持在较慢的水平，您可以在任何时刻关闭窗口结束进程。")
    print("2.请确保您已经完成了用户账户登陆的操作。")
    input("按任意键开始刷分")
    print("即将开始挂机刷分")
    fileList = os.listdir("userCookie")
    userCookie = []
    for fileName in fileList:
        filePath = "userCookie/" + fileName
        userCookie.append(filePath)
    usersNum = len(userCookie)  #用户数量

    for i in range(0, usersNum):
        try:
            voteLaunch(userCookie[i])   #第i个用户发起投票
            for j in range(0, usersNum):
                try:
                    vote(userCookie[j]) #所有用户参与投票
                except:
                    continue
        except:
            continue
        
    
    
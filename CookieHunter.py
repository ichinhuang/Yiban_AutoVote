from selenium import webdriver
import json
import time

def login(userName, password, driver):
    try:
        driver.get("https://www.yiban.cn/login")
        login_field = driver.find_element_by_id("account-txt")
        login_field.clear()
        login_field.send_keys(userName)
        password_field = driver.find_element_by_id("password-txt")
        password_field.clear()
        password_field.send_keys(password)
        login_button = driver.find_element_by_id("login-btn")
        login_button.click()
        driver.implicitly_wait(5)
        while True:
            try:
                driver.find_element_by_xpath('//*[@id="main-menu"]/li[2]/a')
                isSuccess = 1
                print(userName + "用户登陆成功！")
                break
            except:
                errorText = driver.find_element_by_xpath('//*[@id="login-box"]/p[1]')
                login_field = driver.find_element_by_id("account-txt")
                login_field.clear()
                login_field.send_keys(userName)
                password_field = driver.find_element_by_id("password-txt")
                password_field.clear()
                password_field.send_keys(password)
                verify_field = driver.find_element_by_id("login-captcha")
                verify_field.clear()
                verify_field.click()
                verifyCode = input("用户" + userName + "的验证码:")
                if verifyCode == "r":
                    isSuccess = -1
                    return isSuccess
                if verifyCode == "p":
                    isSuccess == -2
                    return isSuccess
                verify_field.click()  #验证码有时候输不进去，多次点击保证输入率
                verify_field.send_keys(verifyCode)
                login_button = driver.find_element_by_id("login-btn")
                login_button.click()
                driver.implicitly_wait(5)
    except:
        isSuccess = 0
        driver.quit()
    
    cookie = driver.get_cookies()
    jsonCookie = json.dumps(cookie)
    filePath = "userCookie/" + str(userName) + ".txt"
    with open(filePath, "w+") as fp:
        fp.write(jsonCookie)
    return isSuccess

def cookieHunterMain():
    print('注意：1.登陆时将会弹出浏览器窗口，如果出现验证码请按照要求将验证码输入命令行（注意不是浏览器窗口），一般所有账号登陆过一次后就不再需要验证码了。')
    print("2.请在控制台出现“请输入用户xxx的验证码:”提示后再输入验证码，否则可能会出现验证码无法写入对应位置的问题。")
    print("3.如果登陆页面没有响应，请在控制台输入r重置本次操作。")
    print("4.请保证所有用户名密码的准确性。如果该用户账号密码有误，输入p可跳过该用户。")
    input("按任意键开始操作")
    print("即将开始收集用户的Cookie...")
    with open("user.txt", "r") as fp:
        text = fp.read()
    usersList = text.split("\n")
    i = 0
    for user in usersList:
        i = i + 1
        if(i <= 0):
            continue
        driver = webdriver.Chrome()
        userInfo = user.split(",")
        userName = userInfo[0]
        password = userInfo[1]
        while True:
            isSuccess = login(userName, password, driver)
            if isSuccess == 1:
                driver.quit()
                break
            elif isSuccess == -2:  #跳过
                continue
    print("所有用户Cookie收集完毕。")

    

from CookieHunter import cookieHunterMain
from Vote import voteMain

print("易班自动投票 v1.0")
print("1.登陆用户账户")
print("2.开始挂机刷分")
print("3.退出")
print("请选择要使用的功能：", end="")
while True:
    i = eval(input())
    if(i == 1):
        cookieHunterMain()
    elif(i == 2):
        voteMain()
    elif(i == 3):
        exit(0)
    else:
        print("输入有误，请重新输入！")
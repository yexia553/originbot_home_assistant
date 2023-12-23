#!/usr/bin/env python
# -*- coding:utf-8 -*-

# https://www.jianshu.com/p/0d14ae8f081c

# https://blog.csdn.net/wei389083222/article/details/78721074/
# https://blog.csdn.net/weixin_34368949/article/details/85991563
# 验证只能用post方法
# 虽然流密钥的格式像是get类型，但是必须使用POST获取参数。
from flask import Flask, request, Response

app = Flask(__name__)


# 传入url格式为: xx.xx.xx.xx:10078/user/auth?usr=xxx&passWord=xxx
@app.route("/user/auth", methods=["POST"])
def auth():
    # user = request.form["username"]  # 从url后获取的数据
    # password = request.form["password"]
    # print(user, "\t", password)
    # # 此处可改为从数据库获取数据
    # auth_user = "admin"
    # auth_passWord = "Pass1234"
    # if auth_user == user and auth_passWord == password:
    #     return Response(response="success", status=200)  # 返回200状态码
    # else:
    #     return Response(status=500)  # 返回500状态码
    token = request.form["token"]
    if token == "Pass1234":
        return Response(response="success", status=200)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10078, debug=True)

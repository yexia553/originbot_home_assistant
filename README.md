>打算基于古月居的[OriginBot](https://www.originbot.org/)创建一个家庭助理,在这里记录相关信息

# 仓库结构解释
```
.
├── backend # 基于Django开发的后端
├── frontend # 基于Vue开发的前端
├── LICENSE # APACHE 2.0
└── README.md
```

# 后端说明

1. 编译docker image
进入到backend目录，执行`docker build -t originbot_home_assistant:0.0.1 .`,会得到一个originbot_home_assistant:0.0.1的镜像

2. 运行后端容器
第一步编译成功之后，运行`docker run -d -p 8000:8000 originbot_home_assistant:0.0.1`
然后通过浏览器打开http://127.0.0.1:8000/admin, 用admin/Pass1234进行登录，登录成功的话就说明运行正常。

# 前端说明
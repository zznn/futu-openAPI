
# 富途开放平台第三方使用手册

for 第三方开发者

author: july

<!-- MarkdownTOC -->

- [Step1 下载源代码及数据库表](#app-mysql)
- [Step2 配置自己的Appid](#appid-config)
- [Step3 使用docker部署API server](#docker)
    - [服务器支持外部连接（个人主机）](#DaoCloud)
    - [服务器不支持外部连接](#Aliyun)
- [参考API说明文档](#api)
   
<!-- /MarkdownTOC -->

## <a name='app-mysql'></a>下载源代码及数据库表
####下载app及mydata文件夹并放置在用户目录或具有执行权限的路径下，如/home/zhulei/app, /home/zhulei/mydata;

####APP包结构图
- app/
-  ├── CA                              
-  │   ├── client.cer                 
-  │   └── client.key                 
-  ├── conf
-  │   ├── appinfo.ini
-  │   └── log.ini
-  ├── db.py
-  ├── futu_server_api.py
-  ├── log
-  │   └── db.log
-  ├── mainapp.py
-  ├── myutility.py
-  ├── script.sh

####包文件说明

-  CA文件夹存放数字证书及密钥
-  conf文件夹存放配置文件
-  db.py数据库操作
-  futu_server_api.py封装富途开放接口
-  log文件夹存放服务日志
-  mainapp.py主程序
-  myutility工具类程序
-  script.sh程序启动脚本
 
  
## <a name='appid-config'></a>配置自己的Appid
####首先请在CA文件夹中存放生成的证书及私钥，并在conf文件夹中按照如下说明配置appinfo.ini文件。 
####appinfo.ini配置说明
####多个APP请按照如下格式配置在appinfo.ini文件中,请确保配置文件中的证书名与实际证书名一致：

- [app_id]为富途分配的第三方应用ID
- app_secret为富途分配的第三方签名密钥
- client_cer为富途返回的证书
- client_key为第三方自己生成的私钥

####例如
- [1000001]
- app_secret = !UMC+RztTD5De9ZV4sg6H6eUURJdyzlL
- client_cer = ./CA/client.cer
- client_key = ./CA/client.key
- [XXXXXX]
- app_secret = XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
- client_cer = XXXXXXXXXXXXXXXXXXXX
- client_key = XXXXXXXXXXXXXXXXXXXX

## <a name='docker'></a>使用docker部署API server
### <a name='DaoCloud'></a>服务器支持外部连接（个人主机）
####首先注册DaoCloud并按下面的步骤（https://dashboard.daocloud.io/nodes/new）连接自己的主机；
####Step1
![](https://raw.githubusercontent.com/zznn/zhulei-github/master/step1.jpg)
####Step2
![](https://raw.githubusercontent.com/zznn/zhulei-github/master/step2.jpg)
####Step3
![](https://raw.githubusercontent.com/zznn/zhulei-github/master/step3.jpg)
####点击“应用联排”，创建一个新的stack，如图中所示，取名myapp，填写YML文件（说明如下），选择刚刚接入的主机，开始部署，
####Step4
![](https://raw.githubusercontent.com/zznn/zhulei-github/master/%E7%BB%98%E5%9B%BE1.jpg)
####YML文件说明
请按如下说明修改github示例中的YML文件（只需改动图中的三处）：
![](https://raw.githubusercontent.com/zznn/zhulei-github/master/%E7%BB%98%E5%9B%BE2.jpg)

####耐心等待一会，见到如下图所示的“创建成功”即部署成功；
![](https://raw.githubusercontent.com/zznn/zhulei-github/master/mytu3.png)
### <a name='Aliyun'></a>服务器不支持外部连接
####Step1 根据主机系统安装Docker（自行参考Docker官方文档）

####Step2 登录阿里云获取Docker镜像（密码是futu@123456）
    sudo docker login --username=富途证券开放平台 registry.aliyuncs.com
    sudo docker pull registry.aliyuncs.com/futu_openapi/mysql
    sudo docker pull registry.aliyuncs.com/futu_openapi/flask
    
####Step3 运行Docker容器（请依照YML文件说明修改相关路径）
    sudo docker run -v /home/zhulei/mydata/:/var/lib/mysql --name mysql -e MYSQL_ROOT_PASSWORD=123456 -d registry.aliyuncs.com/futu_openapi/mysql
    sudo docker run -d --name web -v /home/zhulei/app/:/app -v /etc/localtime:/etc/localtime -p 8080:8080 --link mysql:futudb registry.aliyuncs.com/futu_openapi/flask ./script.sh


## <a name='api'></a>参考API说明文档
####按照接口说明文档调用相关API，若某个接口调用有问题，请将log文件夹中的日志文件发给富途开放助手。

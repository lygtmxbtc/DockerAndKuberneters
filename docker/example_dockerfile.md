### 构建可以运行后端代码的镜像dockerfile
```txt
FROM ubuntu
MAINTAINER tm
#添加python的安装包
ADD  Python-3.5.0.tar.xz /opt
#添加requirement.txt文件
ADD  requirements.txt /home
#更新apt
RUN  apt-get update && apt-get install -y
#安装依赖
RUN  apt-get install gcc -y && apt-get install make -y \
		&& apt-get install vim -y && apt-get install openssl -y \
		&& apt-get install libssl-dev -y && apt-get install python3-pip -y
RUN  ./opt/Python-3.5.0/configure --prefix=/usr/local/python3.5 \
		&& make && make install
RUN pip3 install -r /home/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

#由于工程代码路径问题，需要到工程目录下运行
WORKDIR /home/deeplink/shentong/backend/

CMD [""]
```
### 构建镜像
```bash
docker build -t 镜像名:版本号 .
```
### 创建容器
```bash
docker run -it -d -p 5080:5080 -v /home/deeplink/shentong/backend/:/home/deeplink/shentong/backend/ 镜像名:版本号 python3 main.py -x
```
### docker -v 对挂载目录没权限 Permission denied解决方案
```bash
临时关闭selinux
setenforce 0
```

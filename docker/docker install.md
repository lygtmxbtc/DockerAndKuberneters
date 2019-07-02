### 安装docker依赖
```bash
yum install -y yum-utils device-mapper-persistent-data lvm2
```
### 设置yum源
```bash
yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
```
### 安装docker
```bash
yum install docker-ce-17.12.0.ce
```
### 启动并加入开机启动
```bash
systemctl start docker
systemctl enable docker
```
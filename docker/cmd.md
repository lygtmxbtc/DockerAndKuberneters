```bash
# 查看本地镜像：
docker images
docker image ls
# 下载镜像：
docker pull <img>[:<version>]
# 创建镜像：
docker build <img>[:<version>]
# 导出镜像：
docker save <img>[:<version>] > <filename>
# 导入镜像：
docker load <filename>
# 删除镜像：
docker rmi <img>[:<version>]
# 命名镜像：
docker tag <img>[:<version>] <new_img>[:<version>]

docker ps
docker ps -a
docker run -it <img>[:<version>] <cmd>
docker run -d  <img>[:<version>] <cmd>
# 删除容器：
docker stop <container-id>
# 删除所有容器：
docker rm $(docker ps -aq)
# 删除停用的容器
docker container prune

# 查看容器控制台输出
docker logs -details <container-id>
# 进入正在运行的容器
docker exec -it <container-id> <cmd>
# 重启容器
docker restart <container-id>
# 查看容器详情
docker inspect <container-id>
# 保存容器到镜像
docker commit <container-id> <img>[:<version>]
# 查看容器占用磁盘
docker system df
```

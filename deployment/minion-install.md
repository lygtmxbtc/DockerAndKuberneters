# minion install

## install
```bash
#! /bin/bash

systemctl stop firewalld
systemctl disable firewalld
setenforce 0
sed -i '/^SELINUX=/c SELINUX=disabled' /etc/sysconfig/selinux

yum -y install flannel kubernetes

```
## config
### 1. kubernetes config
```bash
vim /etc/kubernetes/config
```
```ini
###
# kubernetes system config
#
# The following values are used to configure various aspects of all
# kubernetes services, including
#
#   kube-apiserver.service
#   kube-controller-manager.service
#   kube-scheduler.service
#   kubelet.service
#   kube-proxy.service
# logging to stderr means we get it in the systemd journal
KUBE_LOGTOSTDERR="--logtostderr=true"

# journal message level, 0 is debug
KUBE_LOG_LEVEL="--v=0"

# Should this cluster be allowed to run privileged docker containers
KUBE_ALLOW_PRIV="--allow-privileged=false"

# How the controller-manager, scheduler, and proxy find the apiserver
KUBE_MASTER="--master=http://10.0.0.81:8080"
KUBE_ETCD_SERVERS="--etcd_servers=http://10.0.0.81:2379"
```
### 2. kubernetes kubelet config
```bash
vim /etc/kubernetes/kubelet
```
```ini
###
# kubernetes kubelet (minion) config

# The address for the info server to serve on (set to 0.0.0.0 or "" for all interfaces)
KUBELET_ADDRESS="--address=0.0.0.0"

# The port for the info server to serve on
KUBELET_PORT="--port=10250"

# You may leave this blank to use the actual hostname
# KUBELET_HOSTNAME="--hostname-override=node-1" ???
KUBELET_HOSTNAME="--hostname-override=10.0.0.83"

# location of the api-server
KUBELET_API_SERVER="--api-servers=http://10.0.0.81:8080"

# pod infrastructure container
KUBELET_POD_INFRA_CONTAINER="--pod-infra-container-image=registry.access.redhat.com/rhel7/pod-infrastructure:latest"

# Add your own!
KUBELET_ARGS=""

```
### 3. flanneld config
```bash
vim /etc/sysconfig/flanneld
```
```ini
# Flanneld configuration options  

# etcd url location.  Point this to the server where etcd runs
FLANNEL_ETCD_ENDPOINTS="http://10.0.0.81:2379"

# etcd config key.  This is the configuration key that flannel queries
# For address range assignment
FLANNEL_ETCD_PREFIX="/atomic.io/network"

# Any additional options that you want to pass
FLANNEL_OPTIONS="-iface=enp0s8"

```
## start service
```bash
for service in flanneld kube-proxy kubelet docker
do 
systemctl restart ${service}
systemctl enable ${service}
systemctl status ${service}
done

```
## TIPS:
### 1. error when starting pod: no file redhat-ca.crt
```bash
open /etc/docker/certs.d/registry.access.redhat.com/redhat-ca.crt: no such file or directory
```
```bash
yum install *rhsm* -y
wget http://mirror.centos.org/centos/7/os/x86_64/Packages/python-rhsm-certificates-1.19.10-1.el7_4.x86_64.rpm
rpm2cpio python-rhsm-certificates-1.19.10-1.el7_4.x86_64.rpm | cpio -iv --to-stdout ./etc/rhsm/ca/redhat-uep.pem | tee /etc/rhsm/ca/redhat-uep.pem
docker pull registry.access.redhat.com/rhel7/pod-infrastructure:latest

```

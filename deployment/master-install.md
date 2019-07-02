# master install

## install
```bash
#! /bin/bash

systemctl stop firewalld
systemctl disable firewalld
setenforce 0
sed -i '/^SELINUX=/c SELINUX=disabled' /etc/sysconfig/selinux

yum -y install etcd kubernetes

```
## config
### 1. etcd config
```bash
vim /etc/etcd/etcd.conf
```
```ini
ETCD_NAME=default
ETCD_DATA_DIR="/var/lib/etcd/default.etcd"
ETCD_LISTEN_CLIENT_URLS="http://0.0.0.0:2379"
ETCD_ADVERTISE_CLIENT_URLS="http://localhost:2379"
```
### 2. kubernetes apiserver config
```bash
vim /etc/kubernetes/apiserver
```
```ini
###
# kubernetes system config
#
# The following values are used to configure the kube-apiserver
#

# The address on the local server to listen to.
KUBE_API_ADDRESS="--address=0.0.0.0"

# The port on the local server to listen on.
KUBE_API_PORT="--port=8080"

# Port minions listen on
KUBELET_PORT="--kubelet-port=10250"

# Comma separated list of nodes in the etcd cluster
# KUBE_ETCD_SERVERS="--etcd-servers=http://127.0.0.1:2379" ???
KUBE_ETCD_SERVERS="--etcd-servers=http://10.0.0.81:2379"

# Address range to use for services
KUBE_SERVICE_ADDRESSES="--service-cluster-ip-range=10.254.0.0/16"

# default admission control policies
KUBE_ADMISSION_CONTROL="--admission-control=NamespaceLifecycle,NamespaceExists,LimitRanger,SecurityContextDeny,ResourceQuota"

# Add your own!
KUBE_API_ARGS=""

```
## start service
```bash
for service in etcd kube-apiserver kube-controller-manager kube-scheduler
do 
systemctl restart ${service}
systemctl enable ${service}
systemctl status ${service}
done

```
## setup etcd
```bash
etcdctl set /atomic.io/network/config '{"Network":"10.1.0.0/16"}'
```
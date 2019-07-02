# kubeadm
```bash
kubeadm reset
kubeadm config images list

```
## 1. Master
### auto-script
```bash
#! /bin/bash

systemctl stop firewalld
systemctl disable firewalld
setenforce 0
sed -i '/^SELINUX=/c SELINUX=disabled' /etc/sysconfig/selinux

yum install -y docker
echo '{ "insecure-registries":["172.12.78.69:5000"] }' > /etc/docker/daemon.json
systemctl restart docker
systemctl enable docker
imgs=(
kube-apiserver:v1.12.2
kube-controller-manager:v1.12.2
kube-scheduler:v1.12.2
kube-proxy:v1.12.2
pause:3.1
etcd:3.2.24
coredns:1.2.2
kubernetes-dashboard-amd64:v1.10.0
heapster-amd64:v1.5.4
heapster-grafana-amd64:v5.0.4
heapster-influxdb-amd64:v1.5.2
)

for img in ${imgs[@]}
do
    docker pull 172.12.78.69:5000/${img}
    docker tag 172.12.78.69:5000/${img} k8s.gcr.io/${img}
    docker rmi 172.12.78.69:5000/${img}
done

# yum remove -y kubernetes-client kubernetes-node
kube_repo='
[kubernetes]
name=Kubernetes
baseurl=https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64/
enabled=1
gpgcheck=0
'
echo "${kube_repo}" > /etc/yum.repos.d/kubernetes.repo
yum install -y kubeadm
systemctl enable kubelet

kubeadm init --apiserver-advertise-address=172.12.78.31 --kubernetes-version=v1.12.2 --pod-network-cidr=10.244.0.0/16

mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config


kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/master/src/deploy/recommended/kubernetes-dashboard.yaml

```
### tips
#### pull k8s component image
```bash
imgs=(
kube-apiserver:v1.12.2
kube-controller-manager:v1.12.2
kube-scheduler:v1.12.2
kube-proxy:v1.12.2
pause:3.1
etcd:3.2.24
coredns:1.2.2
kubernetes-dashboard-amd64:v1.10.0
heapster-amd64:v1.5.4
heapster-grafana-amd64:v5.0.4
heapster-influxdb-amd64:v1.5.2
)
repo=registry.cn-hangzhou.aliyuncs.com/google_containers
for img in ${imgs[@]}
do
	docker pull ${repo}/${img}
	docker tag ${repo}/${img} 172.12.78.69:5000/${img}
	docker push 172.12.78.69:5000/${img}
done
```
#### close swap
```bash
swapoff -a
sed -i '/swap/s/^/# /' /etc/fstab
free -m
```
#### iptable bridge
```bash
echo 1 > /proc/sys/net/bridge/bridge-nf-call-iptables
echo net.bridge.bridge-nf-call-iptables = 1 >> /etc/sysctl.conf

```
#### cert
```bash
grep 'client-certificate-data' ~/.kube/config | head -n 1 | awk '{print $2}' | base64 -d > kubecfg.crt
grep 'client-key-data' ~/.kube/config | head -n 1 | awk '{print $2}' | base64 -d > kubecfg.key
openssl pkcs12 -export -clcerts -inkey kubecfg.key -in kubecfg.crt -out kubecfg.p12 -name "kubernetes-client"
```
#### install heapster
```bash
wget https://github.com/kubernetes/heapster/raw/master/deploy/kube-config/influxdb/heapster.yaml
sed -i '/--source=/s/$/?useServiceAccount=true\&kubeletHttps=true\&kubeletPort=10250\&insecure=true/' heapster.yaml
kubectl create -f heapster.yaml
kubectl create -f https://github.com/kubernetes/heapster/raw/master/deploy/kube-config/influxdb/grafana.yaml
kubectl create -f https://github.com/kubernetes/heapster/raw/master/deploy/kube-config/influxdb/influxdb.yaml
wget https://github.com/kubernetes/heapster/raw/master/deploy/kube-config/rbac/heapster-rbac.yaml
sed -i 's/system:heapster/cluster-admin/' heapster-rbac.yaml
kubectl create -f heapster-rbac.yaml
```
## 2. Minion
```bash
hostnamectl set-hostname minion2
kubeadm join 172.12.78.51:6443 --token t9vliy.nmjgrf3oa5em7key --discovery-token-ca-cert-hash sha256:f67d90c4073a3dd40b05b6f64a8dbe0dcae135f02d39ce52df21c2cfb2b2b28d
```
```text
[preflight] running pre-flight checks
	[WARNING RequiredIPVSKernelModulesAvailable]: the IPVS proxier will not be used, because the following required kernel modules are not loaded: [ip_vs ip_vs_rr ip_vs_wrr ip_vs_sh] or no builtin kernel ipvs support: map[nf_conntrack_ipv4:{} ip_vs:{} ip_vs_rr:{} ip_vs_wrr:{} ip_vs_sh:{}]
you can solve this problem with following methods:
 1. Run 'modprobe -- ' to load missing kernel modules;
2. Provide the missing builtin kernel ipvs support

[discovery] Trying to connect to API Server "172.12.78.51:6443"
[discovery] Created cluster-info discovery client, requesting info from "https://172.12.78.51:6443"
[discovery] Requesting info from "https://172.12.78.51:6443" again to validate TLS against the pinned public key
[discovery] Cluster info signature and contents are valid and TLS certificate validates against pinned roots, will use API Server "172.12.78.51:6443"
[discovery] Successfully established connection with API Server "172.12.78.51:6443"
[kubelet] Downloading configuration for the kubelet from the "kubelet-config-1.12" ConfigMap in the kube-system namespace
[kubelet] Writing kubelet configuration to file "/var/lib/kubelet/config.yaml"
[kubelet] Writing kubelet environment file with flags to file "/var/lib/kubelet/kubeadm-flags.env"
[preflight] Activating the kubelet service
[tlsbootstrap] Waiting for the kubelet to perform the TLS Bootstrap...
[patchnode] Uploading the CRI Socket information "/var/run/dockershim.sock" to the Node API object "bd4" as an annotation

This node has joined the cluster:
* Certificate signing request was sent to apiserver and a response was received.
* The Kubelet was informed of the new secure connection details.

Run 'kubectl get nodes' on the master to see this node join the cluster.

```
## misc
```text
Your Kubernetes master has initialized successfully!

To start using your cluster, you need to run the following as a regular user:

  mkdir -p $HOME/.kube
  sudo cp -f /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  https://kubernetes.io/docs/concepts/cluster-administration/addons/

You can now join any number of machines by running the following on each node
as root:

  kubeadm join 10.0.0.91:6443 --token xdsk4i.g2dskzoy18syn184 --discovery-token-ca-cert-hash sha256:f008db0468cd8b6111d6fa39e6d9731d15d1d27b6f1eb5964998627ced67c8f6
```
```text
[preflight] running pre-flight checks
	[WARNING RequiredIPVSKernelModulesAvailable]: the IPVS proxier will not be used, because the following required kernel modules are not loaded: [ip_vs ip_vs_rr ip_vs_wrr ip_vs_sh] or no builtin kernel ipvs support: map[ip_vs:{} ip_vs_rr:{} ip_vs_wrr:{} ip_vs_sh:{} nf_conntrack_ipv4:{}]
you can solve this problem with following methods:
 1. Run 'modprobe -- ' to load missing kernel modules;
2. Provide the missing builtin kernel ipvs support

	[WARNING Hostname]: hostname "minion2" could not be reached
	[WARNING Hostname]: hostname "minion2" lookup minion2 on 10.0.2.3:53: server misbehaving
[discovery] Trying to connect to API Server "10.0.0.91:6443"
[discovery] Created cluster-info discovery client, requesting info from "https://10.0.0.91:6443"
[discovery] Requesting info from "https://10.0.0.91:6443" again to validate TLS against the pinned public key
[discovery] Cluster info signature and contents are valid and TLS certificate validates against pinned roots, will use API Server "10.0.0.91:6443"
[discovery] Successfully established connection with API Server "10.0.0.91:6443"
[kubelet] Downloading configuration for the kubelet from the "kubelet-config-1.12" ConfigMap in the kube-system namespace
[kubelet] Writing kubelet configuration to file "/var/lib/kubelet/config.yaml"
[kubelet] Writing kubelet environment file with flags to file "/var/lib/kubelet/kubeadm-flags.env"
[preflight] Activating the kubelet service
[tlsbootstrap] Waiting for the kubelet to perform the TLS Bootstrap...
[patchnode] Uploading the CRI Socket information "/var/run/dockershim.sock" to the Node API object "minion2" as an annotation

This node has joined the cluster:
* Certificate signing request was sent to apiserver and a response was received.
* The Kubelet was informed of the new secure connection details.

Run 'kubectl get nodes' on the master to see this node join the cluster.

```



```text
kubeadm init --apiserver-advertise-address=172.12.78.51 --kubernetes-version=v1.12.2 --pod-network-cidr=10.244.0.0/16
kubeadm join 172.12.78.51:6443 --token t9vliy.nmjgrf3oa5em7key --discovery-token-ca-cert-hash sha256:f67d90c4073a3dd40b05b6f64a8dbe0dcae135f02d39ce52df21c2cfb2b2b28d
```
```text
kubectl create rolebinding default-view --clusterrole=view --serviceaccount=default:default
kubectl create rolebinding default-admin --clusterrole=admin --serviceaccount=default:default

```
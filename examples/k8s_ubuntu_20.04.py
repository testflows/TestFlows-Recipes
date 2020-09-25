# Copyright 2020 Katteli Inc.
# TestFlows.com Open-Source Software Testing Framework (http://testflows.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from testflows.recipes import *

def argparser(parser):
    parser.add_argument("--sudo-password", type=str, help="password to execute commands using 'sudo'", required=True)

@RecipeStep(Given)
def terminal(self):
    with Shell() as bash:
        yield bash

@RecipePlan
@ArgumentParser(argparser)
def recipe(self, sudo_password, hostname=None):
    with Given("terminal to server"):
        bash = terminal()

    with Step("enter sudo"):
        with bash("sudo echo", name="sudo", asyncronous=True):
            c = bash.expect(f"(?P<prompt>{bash.prompt})|(?P<password>password for user)")
            if c.group("password"):
                bash.send(sudo_password, delay=0.5)
                bash.expect(bash.prompt)

    with Step("install utilities"):
        bash("sudo apt -y install vim git curl wget")

    return

    with Step("install Docker"):
        bash("sudo apt update")
        bash("sudo apt -y install docker.io")

    with And("enable Docker service on boot"):
        bash("sudo systemctl start docker")
        bash("sudo systemctl enable docker")

#    with Step("add k8s repository"):
#        bash("sudo apt -y install curl apt-transport-https")
#        bash("curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -")
#        bash("echo \"deb https://apt.kubernetes.io/ kubernetes-xenial main\" | sudo tee /etc/apt/sources.list.d/kubernetes.list")
#        bash("sudo apt-get update")
#
#    with And("install kubelet, kubeadm and kubectl"):
#        bash("sudo apt -y install kubelet kubeadm kubectl kubernetes-cni")
#
#    with And("mark as hold kubelet, kubeadm and kubectl"):
#        bash("sudo apt-mark hold kubelet kubeadm kubectl kubernetes-cni ")
#
#    with Then("check the version of kubectl and kubeadm"):
#        bash("kubectl version --client", message="Client Version:")
#        bash("kubeadm version", message="kubeadm version:")
#
#    with Step("disable swap"):
#        bash("sudo sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab")
#        bash("sudo swapoff -a")
#
#    if hostname is not None:
#        with Step("set hostname"):
#            bash(f"sudo hostnamectl set-hostname {hostname}")
#
#    if node == "master":
#        with Step("initialize Kubernetes master server"):
#            bash("sudo kubeadm init")

if main():
    recipe()

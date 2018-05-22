#coding:utf-8
__author__ = 'WangDy'
__date__ = '2018/5/21 15:07'

from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase

#InvertoryManager类
loader = DataLoader()
inventory = InventoryManager(loader=loader,sources=['imoocc_hosts'])
host = inventory.get_host('192.168.19.130')

#VariableManager类
variable_manager = VariableManager(loader=loader,inventory=inventory)
variable_manager.get_vars() #获取所以的主机
variable_manager.get_vars(host=host) #获取指定的主机

variable_manager.set_host_variable(host,'ansible_ssh_user','wangdaoyun')
var = variable_manager.get_vars(host=host)
variable_manager.extra_vars={'myname':'zhidianlife'} 
var1 = variable_manager.get_vars(host=host)
print var1


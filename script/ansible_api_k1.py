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


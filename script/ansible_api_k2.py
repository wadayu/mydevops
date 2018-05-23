#coding:utf-8
'''
play-book模式
'''
__author__ = 'WangDy'
__date__ = '2018/5/21 15:07'

import json
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
from ansible.executor.playbook_executor import PlaybookExecutor

#InvertoryManager类
loader = DataLoader()
inventory = InventoryManager(loader=loader,sources=['imoocc_hosts'])
#host = inventory.get_host('192.168.19.130')

#VariableManager类
variable_manager = VariableManager(loader=loader,inventory=inventory)
#variable_manager.get_vars() #获取所以的主机
#variable_manager.get_vars(host=host) #获取指定的主机

#variable_manager.set_host_variable(host,'ansible_ssh_user','wangdaoyun')
#var = variable_manager.get_vars(host=host)
#variable_manager.extra_vars={'myname':'zhidianlife'} 
#var1 = variable_manager.get_vars(host=host)
#print var1

#Options执行选项
Options = namedtuple('Options',
                     ['connection',
                      'remote_user',
                      'ask_sudo_pass',
                      'verbosity',
                      'ack_pass',
                      'module_path',
                      'forks',
                      'become',
                      'become_method',
                      'become_user',
                      'check',
                      'listhosts',
                      'listtasks',
                      'listtags',
                      'syntax',
                      'sudo_user',
                      'sudo',
                      'diff',])
options = Options(connection='smart',
                       remote_user=None,
                       ack_pass=None,
                       sudo_user=None,
                       forks=5,
                       sudo=False,
                       ask_sudo_pass=None,
                       verbosity=5,
                       module_path=None,
                       become=True,
                       become_method='sudo',
                       become_user='root',
                       check=False,
                       diff=False,
                       listhosts=None,
                       listtasks=None,
                       listtags=None,
                       syntax=None,)

class PlayBookResultsCollector(CallbackBase):
    """
    重写callbackBase类的部分方法
    """
    def __init__(self, *args, **kwargs):
        super(PlayBookResultsCollector, self).__init__(*args, **kwargs)
        self.task_ok = {}
        self.task_unreachable = {}
        self.task_failed = {}
        self.task_status = {}
        self.task_skipped = {}
    def v2_runner_on_unreachable(self, result):
        self.task_unreachable[result._host.get_name()] = result
    def v2_runner_on_ok(self, result,*args,**kwargs):
        self.task_ok[result._host.get_name()] = result
    def v2_runner_on_failed(self, result,ignore_errors=False,*args,**kwargs):
        self.task_failed[result._host.get_name()] = result
    def v2_runner_on_skipped(self,result):
	self.task_skipped[result._host.get_name()] = result
    def v2_playbook_on_stats(self,stats):
	hosts = sorted(stats.processed.keys())
	for h in hosts:
	    t = stats.summarize(h)
	    self.task_status[h]={
		'ok':t['ok'],
		'changed':t['changed'],
		'unreachable':t['unreachable'],
		'skipped':t['skipped'],
		'failed':t['failed']
            }	

callback =  PlayBookResultsCollector()

passwords = dict()
playbook = PlaybookExecutor(
	playbooks=['f1.yml'],
	inventory = inventory,
	variable_manager = variable_manager,
	loader = loader,
	options = options,
	passwords = passwords,
)

playbook._tqm._stdout_callback = callback
playbook.run()

#print callback.host_ok.items()
result_raw = {'ok':{},'failed':{},'unreachable':{},'skipped':{},'status':{}}
for host,result in callback.task_ok.items():
    result_raw['ok'][host] = result._result
for host,result in callback.task_failed.items():
    result_raw['failed'][host] = result._result
for host,result in callback.task_unreachable.items():
    result_raw['unreachable'][host] = result._result
for host,result in callback.task_status.items():
    result_raw['status'][host] = result._result
for host,result in callback.task_skipped.items():
    result_raw['skipped'][host] = result._result

print json.dumps(result_raw,indent=4)


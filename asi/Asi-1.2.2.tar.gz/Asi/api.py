#!/usr/bin/env python
#-*- coding:utf8 -*-
import shutil
from collections import namedtuple
from Asi.callback import CallbackModule as JsonCallBack
from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
import ansible.constants as C


class Api(object):

	def __init__(self):
		# disable check the host key at ansible running
		C.HOST_KEY_CHECKING = False
		self._callback = None
		self._loader = DataLoader()
		self._inventory = InventoryManager(loader=self._loader, sources=",")
		self._variable_manager = VariableManager(loader=self._loader, inventory=self._inventory)
		self._tasks = []

	def _parse_host(self, hosts):
		for host in hosts:
			hostname = host.get("hostname", None)
			if hostname is None:
				raise ValueError("error: not found hostname")
			port = host.get("port", 22)
			variables = host.get("vars", {})
			self._add_host(hostname, port, variables)
	
	def _add_host(self, hostname, port, variables):
		self._inventory.add_host(host=hostname, port=port)
		host = self._inventory.get_host(hostname)
		for varname, value in variables.items():
			self._set_variable(host, varname, value)

	def _set_variable(self, host, varname, value):
		self._variable_manager.set_host_variable(host, varname, value)
	
	def json(self):
		self._callback = JsonCallBack()
		return self

	def module(self, module, task_name=None, args=None, **kwargs):
		'''
		Args:
			module: string, ansible模板名称
			task_name: string, 此任务的名称，如果为None, 则使用模块名称
			args: string, dict, 模块的参数
			kwargs: dict, 任务的其它参数
		Return:
			Api对象实例
		'''
		if args is not None:
			if isinstance(args, str) or isinstance(args, dict):
				self._tasks.append(dict(action=dict(module=module, args=args), name=task_name, **kwargs))
			else:
				raise ValueError("args type is error")
		else:
			self._tasks.append(dict(action=dict(module=module), name=task_name, **kwargs))
		return self
	
	def run(self, hosts, play_name="Ansible Play", gather_facts="no", callback=None, **kwargs):
		'''
		Args:
			hosts: list, example:
				[
					{
						"hostname": "127.0.0.1",
						"port": 22,
						"vars": {
							"asisble_ssh_pass": "pass"
						}
					}
				]
			play_name: string, ansible play name
			gather_facts: string, no/yes; 是否在运行任务前使用steup模块收集主机信息
			callback: object, Ansible CallbackBase实现 
			kwargs: dict, 选项参数
		'''
		Options = namedtuple("Options",[
			"connection",
			"module_path",
			"forks",
			"become",
 			"become_method",
			"become_user",
			"check",
			"diff"
		])
		options = Options(
			connection=kwargs.get("connection", "smart"),
			module_path=kwargs.get("module_path", []),
			forks=kwargs.get("forks", 10),
			become=kwargs.get("become", None),
			become_method=kwargs.get("become_method", None),
			become_user=kwargs.get("become_method", None),
			check=kwargs.get("check", False),
			diff=kwargs.get("diff", False)
		)
		if self._callback is None:
			self._callback = callback

		self._parse_host(hosts)
		
		play_source = dict(
			name=play_name,
			hosts=[host["hostname"] for host in hosts],
			gather_facts=gather_facts,
			tasks=self._tasks
		)

		play = Play().load(play_source, variable_manager=self._variable_manager, loader=self._loader)

		tqm = None
		try:
			tqm = TaskQueueManager(
				inventory=self._inventory,
				variable_manager=self._variable_manager,
				loader=self._loader,
				options=options,
				passwords=dict(),
				stdout_callback=self._callback
			)
			tqm.run(play)
		finally:
			if tqm is not None:
				tqm.cleanup()
			shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)
		results = getattr(self._callback, "results", None)
		return results

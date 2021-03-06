# -*- coding: utf-8 -*-

from BaseApp import KBEngine
# import KBEngine
# from KBEDebug import *

class Account(KBEngine.Proxy):
	def __init__(self):
		KBEngine.Proxy.__init__(self)
		
	def onTimer(self, id, userArg):
		"""
		KBEngine method.
		使用addTimer后， 当时间到达则该接口被调用
		@param id		: addTimer 的返回值ID
		@param userArg	: addTimer 最后一个参数所给入的数据
		"""
		DEBUG_MSG(id, userArg)
		
	def onEntitiesEnabled(self):
		"""
		KBEngine method.
		该entity被正式激活为可使用， 此时entity已经建立了client对应实体， 可以在此创建它的
		cell部分。
		"""
		INFO_MSG("account[%i] entities enable. mailbox:%s" % (self.id, self.client))
			
	def onLogOnAttempt(self, ip, port, password):
		"""
		KBEngine method.
		客户端登陆失败时会回调到这里
		"""
		INFO_MSG(ip, port, password)
		return KBEngine.LOG_ON_ACCEPT
		
	def onClientDeath(self):
		"""
		KBEngine method.
		客户端对应实体已经销毁
		"""
		DEBUG_MSG("Account[%i].onClientDeath:" % self.id)
		self.destroy()

	def reqAvatarList(self):
		pass

	def reqCreateAvatar(self,roleType,name):
		prop = {
			'roleType':roleType,
			'name':name,
			'level':1
		}
		avatar = KBEngine.createBaseLocally('Avatar',prop)
		if avatar:
			avatar.writeToDB(self._onCharacterSaved)

	def _onCharacterSaved(self, success, avatar):
		if success:
			info = AVATAR_INFO_TYPE()
			info.extend([avatar.databaseID, avatar.name, avatar.roleType, 1])
			self.character = info
			self.writeToDB()
			avatar.destroy()
		if self.client:
			self.client.onCreateAvatarResult(0, info)


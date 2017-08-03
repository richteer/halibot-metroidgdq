import requests
from halibot import HalModule
from halibot import Message

class Metroid(HalModule):

	url = "https://gamesdonequick.com/tracker/api/v1/search/?type=bidtarget&runname=super%20metroid&event=20"
	cxt = None

	def init(self):
		self.task = self.eventloop.call_soon(self.loop_)

	def deinit(self):
		self.task.cancel()

	def receive(self, msg):
		if not msg.body.startswith("!ks"):
			return
		self.cxt = msg.context #TODO remove this
		self.display(msg)

	def make_request(self):
		return requests.get(self.url).json()

	def process(self, js):
		ls = []
		for j in js:
			ls.append((j['fields']['name'],j['fields']['total']))

		ls = sorted(ls, key=lambda x: x[1])
		return {"sec":ls[0][0], "sa":ls[0][1], "lead":ls[1][0], "la":ls[1][1]}

	def display(self, msg):
		ret = self.process(self.make_request())		
		self.log.debug(ret)
		self.reply(msg, body="{lead}: ${la},  {sec}: ${sa}".format(**ret))

	def loop_(self):
		self.task = self.eventloop.call_later(3600,self.loop_)
		if self.cxt:
			m = Message(context=self.cxt)
			self.display(m)

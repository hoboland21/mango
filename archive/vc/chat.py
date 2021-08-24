from rsvn.tools.misc import *
from rsvn.models import *
from rsvn.vc.vclass import VClass


#=====================================================================
class ChatView (VClass)	 :
#=====================================================================
	def main (self) :
		self.template_name = "revise/chat.html"

















#=====================================================================
class LogView (MView)	 :
#=====================================================================
	def main (self) :
		self.template_name = "revise/log.html"

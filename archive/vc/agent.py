from rsvn.tools.misc import *



#=====================================================================
class AgentView (MView)	 :
#=====================================================================
	def main (self) :
		# check and set the jquery tab
		self.template_name = "revise/agents.html"
		self.agent = Agent()
		self.agent_form = AgentForm(instance=self.agent)
		self.agent_list = Agent.objects.all()
		# pack all existing rates
		
		if self.arg_check('add') :
			self.agentid = self.args_put['add']
			self.add()

		if self.arg_check('edit') :
			self.agentid = self.args_put['edit']
			self.edit()

		if self.arg_check('update') :
			self.agentid = self.args_put['update']
			self.update()

		if self.arg_check('delete') :
			self.agentid = self.args_put['delete']
			agent= Agent.objects.get(pk=self.agentid)
			agent.delete()




	#Here is a one time updating function for the agents
		if RateHeading.objects.filter(title__exact = 'Tour Agency') :
			rateheading = RateHeading.objects.get(title__exact = 'Tour Agency') 
			for agent in self.agent_list :
				if not AgentRate.objects.filter(agent=agent.id) :
					agentRate = AgentRate(agent = agent,rateheading=rateheading)
					agentRate.save()
			
		# load list with rates
		for agent in self.agent_list :
			agent.rate = agent.agentrate_set.all()[0]

		self.result['rateHeadings'] = RateHeading.objects.all()
		
		self.result['agent_form'] = self.agent_form
		self.result['agent_list'] = self.agent_list
		self.result['agent'] = self.agent

		
	#------------------------------
	def add(self) :
	#------------------------------
		self.agent_form = AgentForm(self.args_put)
		
		if self.agent_form.is_valid() :
			agent = self.agent_form.save(commit=False)
			agent.clerk = self.request.user.username
			agent.save()
		self.agent_form = AgentForm()
	
	#------------------------------
	def edit(self) :
	#------------------------------
		self.agent= Agent.objects.get(pk=self.agentid)
		self.agentRate = AgentRate.objects.get(agent = self.agent.id)
		self.agent_form = AgentForm(instance=self.agent)
		self.result['currRH'] = self.agentRate.rateheading.id
		
		
	#------------------------------
	def update(self) :
	#------------------------------
		self.agent= Agent.objects.get(pk=self.agentid)
		self.agent_form = AgentForm(self.args_put, instance=self.agent)

		if self.agent_form.is_valid() :
			if self.arg_check("rateHead") :
				rHead = self.args_put["rateHead"]
				rateHead = RateHeading.objects.get(pk = rHead)
				agentRate = AgentRate.objects.get(agent=self.agent.id)
				agentRate.rateheading = rateHead
				agentRate.save()
				self.agent_form.save()
				self.result['currRH'] = agentRate.rateheading.id
				 								
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				

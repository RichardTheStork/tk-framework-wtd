import sys
sys.path.append (r'Z:\Shotgun_Studio\install\core\python')

import sgtk
SEQ_PREFIX = "q"
SHOT_PREFIX = "s"


class sequence():
	name = ""
	id = None
	entity = None

	
class shot():
	name = ""
	sequence = None
	id = None
	entity = None


class shotManager():
	projectPath = r"W:\RTS"
	tk = None
	
	def __init__(self, projectPath = None):
		if projectPath != None:
			self.projectPath = projectPath
		self.tk = sgtk.sgtk_from_path(self.projectPath)
		print 'Initialize Done.'
		
	def __str__(self):
		try:
			return "<shotManager path = %s>" %(self.tk.roots)
		except:
			return "<shotManager projectpath = %s>" %(self.projectPath)
			
	def findSequences(self, seq = None):
		hier = self.tk.templates["sequence_root"]
		if seq == None:
			fields = {}
		elif len(seq) <= 3:
			seq = "%s%s" %(SEQ_PREFIX, seq)
			fields = {"Sequence" : seq}
		else:
			fields = {"Sequence" : seq}
			
		print 'testing fields : %s' %( fields )
		result = self.tk.abstract_paths_from_template(hier, fields)
		# result = self.tk.entity_from_path()
		return result
		
	def findSequence(self, seq):
		seqList = self.findSequences(seq)
		if len(seqList) >= 1:
			return seqList[0]
		else:
			return None
		
	def findShots(self, seq, shot = None):
		hier = self.tk.templates["shot_root"]
		if len(seq) <= 3:
			seq = "%s%s" %(SEQ_PREFIX, seq)
		fields = {"Sequence" : seq}
		if shot != None:
			if len(shot) <= 3:
				shot = "%s%s" %(SHOT_PREFIX, shot)
			fields["Shot"] = shot
		
		print 'testing fields : %s' %( fields )
		result = self.tk.abstract_paths_from_template(hier, fields)
		return result
		
	def findShot(self, seq, shot):
		shotList = self.findShots(seq, shot)
		if shotList == None:
			return None
		elif len(shotList) >= 1:
			return shotList[0]
		else:
			return None
	
	def	getEntities(self, input):
		if type(input) == list:
			tempList = []
			for i in input:
				tempList.append(self.getEntity(i))
			return tempList
		else:
			return self.getEntity(input)
		
	def getEntity(self, input):
		return self.tk.context_from_path(input)

def main():
	Manager = shotManager()
	print Manager
	print "###############"
	tempVar1 = Manager.findSequence("999")
	print tempVar1
	print Manager.getEntities(tempVar1)
	print "_________________"
	tempVar2 = Manager.findSequences()
	print tempVar2
	print Manager.getEntities(tempVar2)
	print "_________________"
	tempVar3 = Manager.findShot("001","001")
	print tempVar3
	print Manager.getEntities(tempVar3)
	print "_________________"
	
if __name__ == "__main__":
	main()

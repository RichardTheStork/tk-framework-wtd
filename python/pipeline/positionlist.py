import os


class Positionlist():
	path = ""
	shot = None
	
	def __init__(self):
		return None
		
	def getPath(self):
		return self.path

	def getList(self):
		return '# TODO POSLISTSTUFF #' * 5
		

def printList():
	poslist = Positionlist()
	print poslist.getList()
	
def main():
	printList()
	

if __name__ == "__main__":
	main()
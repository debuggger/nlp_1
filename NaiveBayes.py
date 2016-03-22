import sys
from collections import defaultdict
from operator import mul
from itertools import product

class NaiveBayes:
	def __init__(self, trainFile, n, lambdaVal):
		self.n = n
		self.lambd = lambdaVal
		self.lines = open(trainFile).readlines()
		self.totalDocs = len(self.lines)
		self.train()

	def nGrams(self, text):
		text = '#'*(self.n-1) + text
		return [text[i: i + self.n] for i in range(len(text) - self.n)]

	def textProcess(self):
		self.documents = []
		for line in self.lines:
			fields = line.split('|')
			self.documents.append((self.nGrams(fields[1]), fields[2].strip()))
				
		return self.documents

	def train(self):
		self.langWordMap = defaultdict(lambda: defaultdict(lambda: 0))
		self.vocab = defaultdict(lambda: 0)

		self.textProcess()

		for doc in self.documents:
			for word in doc[0]:
				self.vocab[word] += 1
				self.langWordMap[doc[1]][word] += 1

		self.languages = self.langWordMap.keys()

	def p_language(self, language):
		return sum(self.langWordMap[language].values())/self.totalDocs

	def p_wordGivenLanguage(self, word, language):
		return (self.langWordMap[language][word] + self.lambd)/(sum(self.langWordMap[language].values()) + (self.lambd*len(self.vocab)))

	def p_wordAndLanguage(self, text, language):
		return self.p_language(language)*reduce(mul, [self.p_wordGivenLanguage(word, language) for word in self.nGrams(text)], 1.0)


	def test(self, text):
		prob = defaultdict(lambda: 0)
		for language in self.languages:	
			prob[language] = self.p_wordAndLanguage(text, language) 

		return max(prob.items(), key = lambda x: x[1])[0]
			

def test(nb, testFile):
	lines = open(testFile).readlines()
	c = 0
	res = []
	for line in lines:
		fields = line.split('|')
		#print nb.test(fields[1])
		res.append(fields[0]+'|'+nb.test(fields[1]))
	return res		
	
def dump(res, n, lambd):
	f = open('output_'+str(n)+'_'+str(lambd)+'.out', 'w')
	for r in res:
		f.write(r+'\n')
	f.close()

	
if __name__ == '__main__':
	print sys.argv
	try:
		trainFile = sys.argv[1]
		testFile = sys.argv[2]
		n = int(sys.argv[3])
		lambd = float(sys.argv[4])

	except:
		print "Incorrect arguments"
	n_set = set(range(4,6))
	lambd_set = set([0.1, 0.5, 0.9, 1])
	for n,lambd in product(n_set, lambd_set):
		print 'n = ',n, ' lambda = ',lambd	
		nb = NaiveBayes(trainFile, n, lambd)
		res = test(nb, testFile)
		dump(res, n, lambd)
		print 'done'

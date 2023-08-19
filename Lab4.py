from graphviz import Digraph

class Tree_Node:
	def __init__(self, val):
		self.value = val
		self.L = None
		self.R = None

	def __str__(self):
		if self.value.isalnum(): return f"{self.value}"
		else: return f"({self.value} {str(self.L)} {str(self.R)})"

def syntaxTree(expr) -> Tree_Node | None:
	Stack = []
	for Char in expr:
		if Char in ['*', '+', '?', '.' , '|']:
			Node = Tree_Node(Char)
			try: Node.R = Stack.pop()
			except: pass
			try:
				if Char != '*': Node.L = Stack.pop()
			except: pass
			Stack.append(Node)
		else:
			Node = Tree_Node(Char)
			Stack.append(Node)
	return Stack[0] if Stack else None

def drawTree(graph: Digraph, node: Tree_Node):
	if node:
		graph.node(str(id(node)), label=node.value)
		if node.R:
			graph.node(str(id(node.R)), label=node.R.value)
			graph.edge(str(id(node)), str(id(node.R)))
			drawTree(graph, node.R)
		if node.L:
			graph.node(str(id(node.L)), label=node.L.value)
			graph.edge(str(id(node)), str(id(node.L)))
			drawTree(graph, node.L)

def itemPrecenedce(item):
	if item=='(': return 1
	elif item=='|': return 2
	elif item=='.': return 3
	elif item=='?': return 4
	elif item=='*': return 4
	elif item=='+': return 4

def simplifyRegex(regex):
	while '+' in regex:
		index = regex.index('+')
		if regex[index-1] != ')': regex.replace(regex[index-1] + '+', regex[index-1] + regex[index-1] + '*')
		elif regex[index-1] == ')':
			interior = index -2
			Group = 0
			while (regex[interior] != '(' or Group != 0)and interior>= 0:
				if regex[interior] == ')': Group += 1
				elif regex[interior] == '(': Group -= 1
				interior -= 1
			if regex[interior] == '(' and Group==0:
				expression = regex[interior:index]
				regex = regex.replace(expression + '+', expression + expression + '*')
		break
	while '?' in regex:
		index = regex.index('?')
		if regex[index-1] != '(': regex.replace(regex[index-1] + '?',"("+ regex[index-1] + '|ε)')
		elif regex[index-1] == ')':
			interior = index -2
			Group = 0
			while (regex[interior] != '(' or Group != 0)and interior>= 0:
				if regex[interior] == ')': Group += 1
				elif  regex[interior] == '(': Group -= 1
				interior -= 1
			if regex[interior] == '(' and Group==0:
				expression = regex[interior:index]
				regex = regex.replace(expression + '?', '(' + expression + '|ε)')
		break
	return regex

def formatRegEx(regex):
	regex = simplifyRegex(regex)
	OPs = ['|','?','+','*']
	binOPs = ['|']
	Result = ''
	for i in range(len(regex)):
		c1 = regex[i]
		if i+1<len(regex):
			c2 = regex[i+1]
			if c1=='\\':
				c1+=c2
				if i+2<len(regex): c2 = regex[i+2]
				else: c2 = ''
			elif c1=='[':
				j = i+1
				while j < len(regex) and regex[j]!=']':
					c1+=regex[j]
					j+=1
				c1+=regex[j]
				i = j
				if i+1<len(regex): c2 = regex[i+1]
				else: c2 = ''
			Result+=c1
			if c2!='' and c1!='(' and c2!=')' and c2 not in OPs and c1 not in binOPs: Result+='.'
		else: Result+=c1
	return Result

def infixToPostfix(expression):
	postfixExpr = ''
	OP = ['|','?','+','*','.']
	Stack = []
	formattedRegEx = formatRegEx(expression)
	i=0
	while i < len(formattedRegEx):
		c = formattedRegEx[i]
		if c=='(':
			Stack.append(c)
		elif c==')':
			while Stack[-1] != '(':
				postfixExpr+=Stack.pop()
			Stack.pop()
		elif c in OP:
			while len(Stack) > 0:
				peekedChar = Stack[-1]
				peekedCharPrecedence = itemPrecenedce(peekedChar)
				currentCharPrecedence = itemPrecenedce(c)
				if peekedCharPrecedence>=currentCharPrecedence:
					postfixExpr+=Stack.pop()
				else:
					break
			Stack.append(c)
		elif c=='\\':
			if i + 1 < len(formattedRegEx):
				postfixExpr += formattedRegEx[i + 1]
				i += 1
		else:
			postfixExpr+=c
		i += 1
	while len(Stack) > 0: postfixExpr += Stack.pop()
	return postfixExpr

def simulate_NFA(node: Tree_Node, string):
	if not node:
		return False
	
	if node.value.isalnum():
		if len(string) == 0:
			return False
		elif string[0] == node.value:
			return simulate_NFA(node.R, string[1:])
		else:
			return False
	else:
		if node.value == '.':
			for i in range(len(string) + 1):
				if simulate_NFA(node.L, string[:i]) and simulate_NFA(node.R, string[i:]):
					return True
			return False
		elif node.value == '|':
			return simulate_NFA(node.L, string) or simulate_NFA(node.R, string)
		elif node.value == '*':
			for i in range(len(string) + 1):
				if simulate_NFA(node.L, string[:i]) and simulate_NFA(node.R, string[i:]):
					return True
			return simulate_NFA(node.L, string)
		elif node.value == '+':
			return simulate_NFA(node.L, string) and simulate_NFA(node.R, string[1:])
		elif node.value == '?':
			return simulate_NFA(node.L, string) or simulate_NFA(node.R, string)


expresion = input("Cadena w:  ")

with open("./Expressions.txt" , 'r', encoding = 'utf-8') as File:
	for i, File_Line in enumerate(File):
		infix_expr = File_Line.strip()
		postfix_expr = infixToPostfix(infix_expr)
		tree = syntaxTree(postfix_expr)
		#graph = Digraph(f"{i}",format='png')
		#drawTree(graph, tree)
		#graph.view()
		print("La expresión: " + expresion + " pertenece a " + File_Line.strip() + "        ?: " + str(simulate_NFA(tree, expresion)))


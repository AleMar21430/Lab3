import re
import graphviz as pgv

def infix_to_postfix(infix_expr):
	operator_precedence = {
		'+': 2,
		'*': 2,
		'?': 2,
		'|': 1,
		'.': 0,
	}

	def is_operator(char):
		return char in operator_precedence

	output_queue = []
	operator_stack = []

	for char in infix_expr:
		if char.isalnum():
			output_queue.append(char)
		elif char == '(':
			operator_stack.append(char)
		elif char == ')':
			while operator_stack and operator_stack[-1] != '(':
				output_queue.append(operator_stack.pop())
			operator_stack.pop()  # Pop the '(' from the stack
		elif is_operator(char):
			while (operator_stack and is_operator(operator_stack[-1])
				and operator_precedence[operator_stack[-1]] >= operator_precedence[char]):
				output_queue.append(operator_stack.pop())
			operator_stack.append(char)

	while operator_stack:
		output_queue.append(operator_stack.pop())

	return ''.join(output_queue)

def simplify_expression(expr):
	expr = re.sub(r'(\w)\+', r'\1\1*', expr)
	expr = re.sub(r'(\w)\?', r'(\1|𝜀)', expr)
	return expr

class TreeNode:
	def __init__(self, value):
		self.value = value
		self.left = None
		self.right = None

def build_syntax_tree(postfix_expr):
	stack = []
	for char in postfix_expr:
		if char.isalnum():
			node = TreeNode(char)
			stack.append(node)
		else:
			right_node = stack.pop()
			if char == '.':
				left_node = stack.pop()
				node = TreeNode(char)
				node.left = left_node
				node.right = right_node
			else:
				node = TreeNode(char)
				node.left = right_node
			stack.append(node)
	return stack[0]

def view_graph(root_node, title):
	graph = pgv.Graph(name=title)
	
	def add_edge(child_node, graph):
		graph.node(str(id(child_node)), label=str(child_node.value))

		if child_node.left:
			graph.edge(str(id(child_node)), str(id(child_node.left)), label="left")
			add_edge(child_node.left, graph)

		if child_node.right:
			graph.edge(str(id(child_node)), str(id(child_node.right)), label="right")
			add_edge(child_node.right, graph)
	add_edge(root_node, graph)

	graph.view()

file_name = './expresiones regulares.txt'
with open(file_name, 'r', encoding = 'utf-8') as file:
	for i, line in enumerate(file):
		expression = line.strip()
		postfix_expr = infix_to_postfix(expression)
		postfix_expr = simplify_expression(postfix_expr)
		syntax_tree = build_syntax_tree(postfix_expr)
		view_graph(syntax_tree, str(i))
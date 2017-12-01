"""
InstantiationAnalyzer.py
====================================
The module that defines InstantiationAnalyzer.

"""
import parso
from collections import defaultdict

class InstantiationAnalyzer:
    """InstantiationAnalyzer parses the code to get the instantiation of models."""
    def __init__(self, model_name):
        """Initialize the InstantiationAnalyzer.
        
        Parameters
        ----------
        model_name: string
            model to be analyzed for instantiation
        
        Returns
        -------

        object
            returns an initialized InstantiationAnalyzer object.

        """
        self.model_name = model_name
        self.d = defaultdict(lambda : defaultdict(int))
        self.counter = 0

    def parse(self,code):
        """Parse code and analyze for instantiation.
        
        Parameters
        ----------
        code: string
            code string to be parsed.

        """
        node = parso.parse(code)
        self._dfs(node)
    
    def _dfs(self, node):
        if hasattr(node, 'children'):
            for child in node.children:
                self._dfs(child)
        else:
            if node.value == self.model_name:
                p = node.parent
                if p.type =="atom_expr" and p.children[0] == node:
                    self._parseArg(p.children[1].children[1])

    def _parseArg(self,node):
        if node.type == "arglist":
            for child in node.children:
                if child.type == "argument":
                    keyword = self._getVal(child.children[0])
                    val = None
                    if len(child.children) >= 3:
                        val = self._getVal(child.children[2])
                    self.d[keyword][val] += 1
                    self.counter += 1
        elif node.type == "argument":        
            keyword = self._getVal(node.children[0])
            val = None
            if len(node.children) >= 3:
                val = self._getVal(node.children[2])
            else:
                keyword = node
            self.d[keyword][val] += 1
            self.counter += 1

    def _getVal(self, node):
        if node.type != "factor" and node.type != "atom" and node.type != "atom_expr" and node.type != "term" and node.type != "arith_expr":
            return node.value
        else:
            return node
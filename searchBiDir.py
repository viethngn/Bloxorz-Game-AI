from display import Displayable, visualize
from searchProblem import Path, Arc
from searchGeneric import Searcher

class BidirectionalSeacher(Searcher):
    """returns a searcher for a problem.
    Paths can be found by repeatedly calling search().
    This does depth-first search unless overridden
    """
    
    def __init__(self, problem):
        """creates a searcher from a problem
        """
        self.problem = problem
        self.initialize_Ffrontier()
        self.initialize_Bfrontier()
        self.num_expanded_forward = 0
        self.num_expanded_backward = 0
        self.num_expanded = 0
        self.forward = {}
        self.backward = {}
        self.add_to_Ffrontier(Path(problem.start_node()))
        self.add_to_Bfrontier(Path(problem.goal_node()))
        super().__init__(problem)

    def initialize_Ffrontier(self):
        self.Ffrontier = []

    def initialize_Bfrontier(self):
        self.Bfrontier = []
        
    def empty_frontier(self):
        return self.Ffrontier == [] or self.Bfrontier == []
        
    def add_to_Ffrontier(self,path):
        self.Ffrontier.append(path)

    def add_to_Bfrontier(self,path):
        self.Bfrontier.append(path)

    def result(self, path1, path2):
    	current = path2
    	result = path1
    	while current.arc != None:
    		result = Path(result, Arc(current.arc.to_node, current.arc.from_node, 1, current.arc.action))
    		current = current.initial
    	#print(result)
    	return result
        
    @visualize
    def search(self):
        """returns (next) path from the problem's start node
        to a goal node. 
        Returns None if no path exists.
        """
        while not self.empty_frontier():
        	#forward
            path = self.Ffrontier.pop(0)
            if (path.end() in self.forward):
            	continue
            self.forward[path.end()] = path
            self.display(2, "Expanding:",path,"(cost:",path.cost,")")
            self.num_expanded_forward += 1
            if self.problem.is_goal(path.end()):    # solution found
                self.display(1, self.num_expanded_forward, "forward paths have been expanded and",
                            len(self.Ffrontier), "paths remain in the Ffrontier")
                self.solution = path   # store the solution found
                return path
            else:
                neighs = self.problem.neighbors(path.end())
                self.display(3,"Neighbors are", neighs)
                for arc in reversed(neighs):
                	#intersect, solution found
                	if arc.to_node in self.backward:
                		result = self.result(Path(path,arc), self.backward[arc.to_node])
                		self.num_expanded = self.num_expanded_forward + self.num_expanded_backward
                		self.solution = result
                		return result
                	elif arc.to_node not in self.forward:
                		self.add_to_Ffrontier(Path(path,arc))
                self.display(3,"FFrontier:",self.Ffrontier)

            #backward
            path = self.Bfrontier.pop(0)
            if (path.end() in self.backward):
            	continue
            self.backward[path.end()] = path
            self.display(2, "Expanding:",path,"(cost:",path.cost,")")
            self.num_expanded_backward += 1
            if self.problem.is_start(path.end()):    # solution found
                self.display(1, self.num_expanded_backward, "backward paths have been expanded and",
                            len(self.Bfrontier), "paths remain in the Bfrontier")
                self.solution = path   # store the solution found
                return path
            else:
                neighs = self.problem.neighbors(path.end(), True)
                self.display(3,"Neighbors are", neighs)
                for arc in reversed(neighs):
                	#intersect, solution found
                	if arc.to_node in self.forward:
                		result = self.result(self.forward[arc.to_node], Path(path,arc))
                		self.num_expanded = self.num_expanded_forward + self.num_expanded_backward
                		self.solution = result
                		return result
                	elif arc.to_node not in self.backward:
                		self.add_to_Bfrontier(Path(path,arc))
                self.display(3,"BFrontier:",self.Bfrontier)
        self.num_expanded = self.num_expanded_forward + self.num_expanded_backward
        self.display(1,"No (more) solutions. Total of",
                     self.num_expanded,"paths expanded.")

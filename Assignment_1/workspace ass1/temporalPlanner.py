import sys
from cspProblem import CSP, Constraint
from cspConsistency import Con_solver, Search_with_AC_from_CSP, select, copy_with_assign, partition_domain
from searchGeneric import Searcher, AStarSearcher
from searchProblem import Arc



# get data
task_tank = []
binary_constraints_tank = []
domain_constraints_tank = []
tank_temp = []
file = str(sys.argv[1])
for i in open(file, "r"):
     line = i.strip('\n')
     tank_temp.append(line)
#get data in list
for i in range(len(tank_temp)):
    temp = tank_temp[i].split( )
    if temp[0] == 'task':
        task_tank.append(tank_temp[i])
    elif temp[0] == 'constraint':
        binary_constraints_tank.append(tank_temp[i])
    elif temp[0] == 'domain':
        domain_constraints_tank.append(tank_temp[i])


# get domains
domains = {}
for i in range(len(task_tank)):
    value = []
    temp = task_tank[i].split( )
    temp_value = int(temp[2])
    for i in range(0, 99):
        value.append(i)
    value = set(value)
    domains.update({temp[1]: value})
duration = {}
for i in range(len(task_tank)):
    temp = task_tank[i].split( )
    duration.update({temp[1]: int(temp[2])})

#get binary constrains
constraints = []
for i in range(len(binary_constraints_tank)):
    temp = binary_constraints_tank[i].split( )
    temp_set = [temp[1], temp[2], temp[3]]
    constraints.append(temp_set)

#get domain constrains1
constraints1 = []
for i in range(len(domain_constraints_tank)):
    temp = domain_constraints_tank[i].split( )
    if len(temp) == 4:
        temp_set = [temp[1], temp[2], int(temp[3])]
        constraints1.append(temp_set)
    elif len(temp) == 5:
        temp_set = [temp[1], temp[2], int(temp[3]), int(temp[4])]
        constraints1.append(temp_set)

#definiation constrains functions
def before_ (C):
    def before(A, B):
        return A + C - 1  < B
    return before
def after_ (C):
    def after(A, B):
        return B + C - 1  < A
    return after
def starts (A, B):
    return A == B
def ends_ (C, D):
    def ends(A, B):
        return A + C == B + D
    return ends
def meets_ (C):
    def meets(A, B):
        return A + C - 1 < B + 1
    return meets
def overlaps_ (C, D):
    def overlaps(A, B):
        return A < B and B < A + C - 1 and A + C < B + D
    return overlaps
def during_ (C, D):
    def during(A, B):
        return A > B and A + C < B + D
    return during
def equals_ (C, D):
    def equals(A, B):
        return A == B and A + C == B + D
    return equals
def starts_before_ (B):
    def starts_before(A):
        return A <= B
    return starts_before
def starts_after_ (B):
    def starts_after(A):
        return A >= B
    return starts_after
def ends_before_ (C):
    def ends_before(A, B):
        return A + C <= B
    return ends_before
def ends_after_ (C):
    def ends_after(A, B):
        return A + C >= B
    return ends_after
def starts_in_ (B1, B2):
    def starts_in(A):
        return B1 <= A <= B2
    return starts_in
def ends_in_ (C):
    def ends_in(A, B1, B2):
        return B1 <= A + C - 1 <= B2
    return ends_in
def between_ (C):
    def between(A, B1, B2):
        return B1 <= A <= B2 and B1 <= A + C - 1 <= B2
    return between

#get constraints list: constraint_all
constraint_all = []
for i in constraints:
    if i[1] == 'before':
        for j in duration:
            if j == i[0]:
                constraint_all.append(Constraint([i[0], i[2]], before_(duration[j])))
    elif i[1] == 'after':
        for j in duration:
            if j == i[2]:
                constraint_all.append(Constraint([i[0], i[2]], after_(duration[j])))
    elif i[1] == 'starts':
        constraint_all.append(Constraint([i[0], i[2]], starts))
    elif i[1] == 'ends':
        for j in duration:
            for k in duration:
                if j == i[0] and k == i[2]:
                    constraint_all.append(Constraint([i[0], i[2]], ends_(duration[j], duration[k])))
    elif i[1] == 'meets':
        for j in duration:
            if j == i[0]:
                constraint_all.append(Constraint([i[0], i[2]], meets_(duration[j])))
    elif i[1] == 'overlaps':
        for j in duration:
            for k in duration:
                if j == i[0] and k == i[2]:
                    constraint_all.append(Constraint([i[0], i[2]], overlaps_(duration[j], duration[k])))
    elif i[1] == 'during':
        for j in duration:
            for k in duration:
                if j == i[0] and k == i[2]:
                    constraint_all.append(Constraint([i[0], i[2]], during_(duration[j], duration[k])))
    elif i[1] == 'equals':
        for j in duration:
            for k in duration:
                if j == i[0] and k == i[2]:
                    constraint_all.append(Constraint([i[0], i[2]], equals_(duration[j], duration[k])))
for i in constraints1:
    if i[1] == 'starts-before':
        constraint_all.append(Constraint([i[0]], starts_before_(i[2])))
    elif i[1] == 'starts-after':
        constraint_all.append(Constraint([i[0]], starts_after_(i[2])))
    elif i[1] == 'ends-before':
        for j in duration:
            if j == i[0]:
                constraint_all.append(Constraint([i[0], i[2]], ends_before_(duration[j])))
    elif i[1] == 'ends-after':
        for j in duration:
            if j == i[0]:
                constraint_all.append(Constraint([i[0], i[2]], ends_after_(duration[j])))
    elif i[1] == 'starts-in':
        constraint_all.append(Constraint([i[0]], starts_in_(i[2], i[3])))
    elif i[1] == 'ends-in':
        for j in duration:
            if j == i[0]:
                constraint_all.append(Constraint([i[0], i[2], i[3]], ends_in_(duration[j])))
    elif i[1] == 'between':
        for j in duration:
            if j == i[0]:
                constraint_all.append(Constraint([i[0], i[2], i[3]], between_(duration[j])))



#rewrite classes
class myCSP(CSP):

    def __init__(self, domains, constraints, duration):
        self.duration = duration
        super().__init__(domains, constraints)

    def cost(self, domains):
        temp_h = 0
        for i in domains.keys():
            temp_res = []
            for j in domains[i]:
                temp = j + duration[i] - 1
                temp_res.append(temp)
            minmum = min(temp_res)
            #print(i,':',minmum - duration[i]+1)
            temp_h = temp_h + minmum
        #print('cost:', temp_h)
        return temp_h


class mySearcher(Search_with_AC_from_CSP):
    def __init__(self, csp):
        super().__init__(csp)

    def is_goal(self, node):
        """node is a goal if all domains have 1 element"""
        return all(len(node[var])==1 for var in node)

    def start_node(self):
        return self.domains

    def neighbors(self, node):
        """returns the neighboring nodes of node.
        """
        neighs = []
        var = select(x for x in node if len(node[x]) > 1)
        if var:
            dom1, dom2 = partition_domain(node[var])
            self.display(2, "Splitting", var, "into", dom1, "and", dom2)
            to_do = self.cons.new_to_do(var, None)
            for dom in [dom1, dom2]:
                newdoms = copy_with_assign(node, var, dom)
                cons_doms = self.cons.make_arc_consistent(newdoms, to_do)
                if all(len(cons_doms[v]) > 0 for v in cons_doms):
                    # all domains are non-empty
                    neighs.append(Arc(node, cons_doms))
                else:
                    self.display(2, "...", var, "in", dom, "has no solution")
        return neighs

    def heuristic(self, path):
        return myCSP.cost(path, self.domains)

class myAstar(AStarSearcher):
    def __init__(self, problem):
        super().__init__(problem)
    def add_to_frontier(self,path):
        """add path to the frontier with the appropriate cost"""
        value = self.problem.heuristic(path.end())
        self.frontier.add(path, value)


#out put
csp = myCSP(domains, constraint_all, duration)
solution_temp = myAstar(mySearcher(csp))
Searcher.max_display_level = 0
solution = solution_temp.search().end()
res = Con_solver(csp).make_arc_consistent()
for i in solution:
    print(i,':',list(solution[i])[0])
print('cost :',csp.cost(res))
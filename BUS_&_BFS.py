from queue import Queue
import time

class Node:
    def toString(self):
        raise Exception('Unimplemented method')

    def interpret(self):
        raise Exception('Unimplemented method')

    def grow(self, plist, new_plist):
        pass

class Not(Node):
    def __init__(self, left):
        self.left = left
    
    def complete(self):
        if "S" in self.left.toString() or "B" in self.left.toString():
            return False
        else:
            return True

    def children(self, prod_rules, conditions):
        children = []
        if "B" in self.left.toString():
            for l_c in self.left.children(prod_rules=prod_rules,conditions=conditions):
                children.append(Not(l_c))
        return children

    def toString(self):
        return 'not (' + self.left.toString() + ')'

    def interpret(self, env):
        return not (self.left.interpret(env))

    def grow(plist, new_plist,size):
        for s1 in plist.keys():
            if "bool" in plist[s1]:
                for p1 in [a for a in plist[s1]["bool"]]:
                    if s1+1 == size:
                        new_plist+=[Not(p1)]
        return new_plist
        

class And(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def complete(self):
        if "B" in self.right.toString() or "B" in self.left.toString():
            return False
        else:
            return True

    def children(self, prod_rules, conditions):
        children = []
        if "S" in self.left.toString() or "B" in self.left.toString():
            for l_c in self.left.children(prod_rules=prod_rules,conditions=conditions):
                children.append(And(l_c,self.right))
        else:
            for r_c in self.right.children(prod_rules=prod_rules,conditions=conditions):
                children.append(And(self.left,r_c))
        return children

    def toString(self):
        return "(" + self.left.toString() + " and " + self.right.toString() + ")"

    def interpret(self, env):
        return self.left.interpret(env) and self.right.interpret(env)

    def grow(plist, new_plist, size):
        for s1 in plist.keys():
            for s2 in plist.keys():
                if "bool" in plist[s1] and "bool" in plist[s2]:
                    for (p1,p2) in [(a,b) for a in plist[s1]["bool"] for b in plist[s2]["bool"]]:
                        if s1+s2+1 == size:
                            new_plist+=[And(p1,p2)]
        return new_plist

class Lt(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def complete(self):
        if "S" in self.left.toString() or "S" in self.right.toString():
            return False
        else:
            return True

    def children(self, prod_rules, conditions):
        children = []
        if "S" in self.left.toString():
            for l_c in self.left.children(prod_rules=prod_rules,conditions=conditions):
                children.append(Lt(l_c,self.right))
        else:
            for r_c in self.right.children(prod_rules=prod_rules,conditions=conditions):
                children.append(Lt(self.left,r_c))
        return children

    def toString(self):
        return "(" + self.left.toString() + " < " + self.right.toString() + ")"

    def interpret(self, env):
        return self.left.interpret(env) < self.right.interpret(env)

    def grow(plist, new_plist, size):
        for s1 in plist.keys():
            for s2 in plist.keys():
                if "int" in plist[s1] and "int" in plist[s2]:
                    for (p1,p2) in [(a,b) for a in plist[s1]["int"] for b in plist[s2]["int"]]:
                        if s1+s2+1 == size:
                            new_plist+=[Lt(p1,p2)]
        return new_plist

class Ite(Node):
    def __init__(self, condition, true_case, false_case):
        self.condition = condition
        self.true_case = true_case
        self.false_case = false_case

    def complete(self):
        if "S" in self.true_case.toString() or "S" in self.false_case.toString() or "B" in self.condition.toString() or "S" in self.condition.toString():
            return False
        else:
            return True

    def children(self, prod_rules, conditions):
        children = []
        if "B" in self.condition.toString() or "S" in self.condition.toString():
            for c_c in self.condition.children(prod_rules=prod_rules,conditions=conditions):
                children.append(Ite(c_c,self.true_case,self.false_case))
        elif "S" in self.true_case.toString() or "B" in self.true_case.toString():
            for t_c in self.true_case.children(prod_rules=prod_rules,conditions=conditions):
                children.append(Ite(self.condition,t_c,self.false_case))
        else:
            for f_c in self.false_case.children(prod_rules=prod_rules,conditions=conditions):
                children.append(Ite(self.condition,self.true_case,f_c))
        return children

    def toString(self):
        return "(if " + self.condition.toString() + " then " + self.true_case.toString() + " else " + self.false_case.toString() + ")"

    def interpret(self, env):
        if self.condition.interpret(env):
            return self.true_case.interpret(env)
        else:
            return self.false_case.interpret(env)

    def grow(plist, new_plist, size):
        for s1 in plist.keys():
            for s2 in plist.keys():
                for s3 in plist.keys():
                    if "bool" in plist[s1] and "int" in plist[s2] and "int" in plist[s3]:
                        for (p1,p2,p3) in [(a,b,c) for a in plist[s1]["bool"] for b in plist[s2]["int"] for c in plist[s3]["int"]]:
                            if s1+s2+s3+1 == size:
                                new_plist+=[Ite(p1,p2,p3)]
        return new_plist

class Num(Node):
    def __init__(self, value):
        self.value = value
    
    def complete(self):
            return True

    def toString(self):
        return str(self.value)

    def interpret(self, env):
        return self.value

class Var(Node):
    def __init__(self, name):
        self.name = name
    
    def complete(self):
            return True

    def toString(self):
        return self.name

    def interpret(self, env):
        return env[self.name]

class Plus(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def complete(self):
        if "S" in self.left.toString() or "S" in self.right.toString():
            return False
        else:
            return True

    def children(self, prod_rules, conditions):
        children = []
        if "S" in self.left.toString():
            for l_c in self.left.children(prod_rules=prod_rules,conditions=conditions):
                children.append(Plus(l_c,self.right))
        else:
            for r_c in self.right.children(prod_rules=prod_rules,conditions=conditions):
                children.append(Plus(self.left,r_c))
        return children

    def toString(self):
        return "(" + self.left.toString() + " + " + self.right.toString() + ")"

    def interpret(self, env):
        return self.left.interpret(env) + self.right.interpret(env)

    def grow(plist, new_plist, size):
        for s1 in plist.keys():
            for s2 in plist.keys():
                if "int" in plist[s1] and "int" in plist[s2]:
                    for (p1,p2) in [(a,b) for a in plist[s1]["int"] for b in plist[s2]["int"]]:
                        if s1+s2+1 == size:
                            new_plist+=[Plus(p1,p2)]
        return new_plist

class Times(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def complete(self):
        if "S" in self.left.toString() or "S" in self.right.toString():
            return False
        else:
            return True

    def children(self, prod_rules, conditions):
        children = []
        if "S" in self.left.toString():
            for l_c in self.left.children(prod_rules=prod_rules,conditions=conditions):
                children.append(Times(l_c,self.right))
        else:
            for r_c in self.right.children(prod_rules=prod_rules,conditions=conditions):
                children.append(Times(self.left,r_c))
        return children

    def toString(self):
        return "(" + self.left.toString() + " * " + self.right.toString() + ")"

    def interpret(self, env):
        return self.left.interpret(env) * self.right.interpret(env)
    
    def grow(plist, new_plist, size):
        for s1 in plist.keys():
            for s2 in plist.keys():
                if "int" in plist[s1] and "int" in plist[s2]:
                    for (p1,p2) in [(a,b) for a in plist[s1]["int"] for b in plist[s2]["int"]]:
                        if s1+s2+1 == size:
                            new_plist+=[Times(p1,p2)]
        return new_plist

class S(Node):
    def __init__(self):
        pass
    def toString(self):
        return "S"
    def children(self, prod_rules, conditions):
        children = []
        for r in  prod_rules:
            if r == Times or r == Plus or r == Lt:
                c = r(S(),S())
            elif r == 'x' or r == 'y':
                c = Var(r)
            elif type(r).__name__ == "int":
                c = Num(r)
            elif r == Ite:
                c = r(B(),S(),S())
            children.append(c)
        return (children)



class B(Node):
    def __init__(self):
        pass
    def toString(self):
        return "B"
    def children(self, prod_rules, conditions):
        children = []
        for r in  conditions:
            if r == Lt:
                c = r(S(),S())
            elif r == And:
                c = r(B(),B())           
            elif r == Not:
                c = r(B())
            children.append(c)
        return (children)



class TopDownSearch():
    def getOutput(self, program):
        output = []
        for in_out in self.env:
            output.append(program.interpret(in_out))
        return output

    def synthesize(self, bound, operations, integer_values, variables, input_output):
        start = time.time()
        generated = 0
        evaluated = 0
        self.true_outputs = []
        for in_out1 in input_output:
            self.true_outputs.append(in_out1['out'])
        self.env = input_output
        all_prod_rules = [Ite, Times, Plus, Var, Num]
        all_conditions = [Not, And, Lt]
        self.prod_rules = []
        self.conditions = []
        for o in operations:
            if o in all_prod_rules:
                self.prod_rules.append(o)
            else:
                self.conditions.append(o)
        self.prod_rules += variables + integer_values
        openSet = Queue()
        openSet.put((S(),0))
        while True:
            p = openSet.get()
            size = p[1]
            if size == bound+1:           
                return None, print(f"BFS: Could not find the solution, until size {size+1}"), print(f"Running time: {time.time() - start} seconds.", print(f"{generated} programs generated. {evaluated} programs evaluated! \n"))
            children = p[0].children(prod_rules=self.prod_rules,conditions=self.conditions)
            for c in children:
                generated+=1       
                if c.complete():
                    evaluated+=1
                    if self.getOutput(c) == self.true_outputs:
                        return c, print(f"BFS: Synthesis was successful. Here is the program: {c.toString()} of size: {size+1}"), print(f"Running time: {time.time() - start} seconds."), print(f"{generated} programs generated. {evaluated} programs evaluated! \n")
                else:
                    openSet.put((c, size+1))

class BottomUpSearch():
    def getOutput(self, program):
        output = []
        for in_out in self.env:
            output.append(program.interpret(in_out))
        return tuple(output)

    def grow(self, plist, operations, size):
        new_plist = []
        for o in operations:
            new_plist = o.grow(plist, new_plist, size)
        for p in new_plist:
            self.generated+=1
            self.evaluated+=1
            output = self.getOutput(p)
            pre_len = len(self.outputs)
            self.outputs.add(output)
            if len(self.outputs) != pre_len:
                self.added = True
                if size not in plist.keys():
                    plist[size] = {}
                if str(type(output[0]).__name__) not in plist[size].keys():
                    plist[size][str(type(output[0]).__name__)] = []
                plist[size][str(type(output[0]).__name__)].append(p)

        return plist

    def synthesize(self, bound, operations, integer_values, variables, input_output):
        start = time.time()
        self.generated = 0
        self.evaluated = 0
        self.env = input_output
        self.true_outputs = []
        for in_out1 in input_output:
            self.true_outputs.append(in_out1['out'])
        self.true_outputs = tuple(self.true_outputs) 
        self.outputs = set()
        plist = {1: {"int":[Num(integer_value) for integer_value in integer_values]+[Var(variable) for variable in variables]}}
        for program in plist[1]["int"]:
                    output_ = self.getOutput(program)
                    
                    if output_ == self.true_outputs:
                        return program, print("BUS: Synthesis was successful. Here is the program:", program.toString()), print(f"Running time: {time.time() - start} seconds."), print(f"{self.generated} programs generated. {self.evaluated} programs evaluated! \n")

        for i in range(2,bound+1):
            found = True
            self.added = False
            plist = self.grow(plist, operations, i)
            if self.added == True:
                for t in plist[i].keys():
                    for program in plist[i][t]:
                        output_ = self.getOutput(program)
                        if output_ == self.true_outputs:
                            found = False
                            return program, print(f"BUS: Synthesis was successful. Here is the program: {program.toString()} with size {i}"), print(f"Running time: {time.time() - start} seconds."), print(f"{self.generated} programs generated. {self.evaluated} programs evaluated! \n")
        if found:
            return None, print(f"BUS: Could not find the solution until size {i}"), print(f"Running time: {time.time() - start} seconds."), print(f"{self.generated} programs generated. {self.evaluated} programs evaluated! \n")

       

BUS = BottomUpSearch()
BFS = TopDownSearch()

program, _, _, _ = BUS.synthesize(10, [Lt, Ite], [1, 2], ['x', 'y'], [{'x':5, 'y': 10, 'out':5}, {'x':10, 'y': 5, 'out':5}, {'x':4, 'y': 3, 'out':3}]) 
program, _, _, _ = BFS.synthesize(10, [Lt, Ite], [1, 2], ['x', 'y'], [{'x':5, 'y': 10, 'out':5}, {'x':10, 'y': 5, 'out':5}, {'x':4, 'y': 3, 'out':3}]) 

program, _, _, _  = BUS.synthesize(12, [Ite, And, Times, Lt], [10], ['x', 'y'], [{'x':5, 'y': 10, 'out':5}, {'x':10, 'y': 5, 'out':5}, {'x':4, 'y': 3, 'out':4}, {'x':3, 'y': 4, 'out':4}]) 
program, _, _, _  = BFS.synthesize(12, [Ite, And, Times, Lt], [10], ['x', 'y'], [{'x':5, 'y': 10, 'out':5}, {'x':10, 'y': 5, 'out':5}, {'x':4, 'y': 3, 'out':4}, {'x':3, 'y': 4, 'out':4}]) 

program, _, _, _ = BUS.synthesize(11, [Ite, Plus, Times, Lt], [-1], ['x', 'y'], [{'x':10, 'y':7, 'out':17}, {'x':4, 'y':7, 'out':-7}, {'x':10, 'y':3, 'out':13}, {'x':1, 'y':-7, 'out':-6}, {'x':1, 'y':8, 'out':-8}])
program, _, _, _ = BFS.synthesize(11, [Ite, Plus, Times, Lt], [-1], ['x', 'y'], [{'x':10, 'y':7, 'out':17}, {'x':4, 'y':7, 'out':-7}, {'x':10, 'y':3, 'out':13}, {'x':1, 'y':-7, 'out':-6}, {'x':1, 'y':8, 'out':-8}])

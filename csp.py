from cnf import CNF

class CSP:
    def __init__(self, cnf: CNF, use_mcv=True, use_mrv=True, use_lcv=True):
        self.cnf = cnf
        self.use_mcv = use_mcv
        self.use_mrv = use_mrv
        self.use_lcv = use_lcv
        self.degree_variables = {}
        self.variables = {}
        self.assigned_variables = {}
        self.constraints = []
        self.var_constraints = {}

    def add_variable(self, variable, domain):
        self.variables[variable] = domain
        self.degree_variables[variable] = 0
        self.var_constraints[variable] = []

    def prepare(self):
        for var in self.cnf.variables:
            if var[0] != '~' and var not in self.variables:
                self.add_variable(var, [False, True])

        for clause in self.cnf.hard_clauses:
            self.add_constraint(self.cnf.evaluate_clause, clause)
        
        for i in range(len(self.cnf.soft_clauses)):
            self.cnf.soft_clauses[i] = (self.cnf.soft_clauses[i][:-1], self.cnf.soft_clauses[i][-1])

    def unassigned_variables(self):
        return [var for var in self.variables if var not in self.assigned_variables]

    def add_constraint(self, constraint_function, variables):
        constraint = (constraint_function, variables)
        self.constraints.append(constraint)
        for var in variables:
            base_var = var[1:] if var.startswith('~') else var
            if base_var in self.variables:
                self.degree_variables[base_var] += 1
                self.var_constraints[base_var].append(constraint)

    def assign(self, variable, value):
        self.assigned_variables[variable] = value

    def unassign(self, variable):
        if variable in self.assigned_variables:
            del self.assigned_variables[variable]

    def is_constraint_satisfied(self, constraint, assignement):
        func, clause = constraint
        return func(clause, assignement)

    def is_consistent(self, variable, value):
        temp = self.assigned_variables.copy()
        temp[variable] = value
        for constraint in self.var_constraints.get(variable, []):
            if not self.is_constraint_satisfied(constraint, temp):
                return False
        return True

    def is_complete(self):
        return len(self.assigned_variables) == len(self.variables)

    def select_unassigned_variable(self):
        unassigned = self.unassigned_variables()
        if not unassigned:
            return None
        if self.use_mrv:
            return self.minimum_remaining_value()
            
        if self.use_mcv:
            return self.most_constraining_variable(unassigned)

        return unassigned[0]


    def count_conflicts(self, var, value):
        count = 0
        temp = self.assigned_variables.copy()
        temp[var] = value
        for constraint in self.var_constraints.get(var, []):
            if not self.is_constraint_satisfied(constraint, temp):
                count += 1
        return count

    def solve(self):
        self.best_solution = None
        self.best_weight = -1
        self.branch_and_bound()
        return self.best_solution, self.best_weight

    def backtrack(self):
        if self.is_complete():
            current_weight = self.cnf.calculate_weight(self.assigned_variables)
            if current_weight > self.best_weight:
                self.best_solution = self.assigned_variables.copy()
                self.best_weight = current_weight
            return

        var = self.select_unassigned_variable()
        if var is None:
            return

        for value in self.least_constraining_value(var):
            if self.is_consistent(var, value):
                self.assign(var, value)
                self.backtrack()  
                self.unassign(var)
    
    def branch_and_bound(self):
        if self.is_complete():
            current_weight = self.cnf.calculate_weight(self.assigned_variables)
            if current_weight > self.best_weight:
                self.best_solution = self.assigned_variables.copy()
                self.best_weight = current_weight
            return

        remaining_weight = self._calculate_remaining_weight()
        if self.cnf.calculate_weight(self.assigned_variables) + remaining_weight <= self.best_weight:
            return  

        var = self.select_unassigned_variable()
        if var is None:
            return

        for value in self.least_constraining_value(var):
            if self.is_consistent(var, value):
                self.assign(var, value)
                self.branch_and_bound() 
                self.unassign(var)  

    def _calculate_remaining_weight(self):
        remaining_weight = 0
        for clause, weight in self.cnf.soft_clauses:
            clause_status = self.cnf.evaluate_clause(clause, self.assigned_variables, True)
            if clause_status is None:  
                remaining_weight += int(weight)
        return remaining_weight

    def minimum_remaining_value(self):
        unassigned = self.unassigned_variables()
        min_variable = unassigned[0]
        min_value = 2
        for var in unassigned:
            with_true = self.is_consistent(var, True)
            with_false = self.is_consistent(var, False)
            len_true = len([val for val in [with_true] + [with_false] if val])
            
            if len_true < min_value:
                min_value = len_true
                min_variable = var
        return min_variable
                    
            
        # min = float('inf')
        # unassigned = self.unassigned_variables()
        # min_variable = unassigned[0]
        # for var in unassigned:
        #     unsatisified = 0
        #     for const in self.var_constraints[var]:
        #         if not self.cnf.evaluate_clause(const[1], self.assigned_variables):
        #             unsatisified += 1
        #     if unsatisified < min:
        #         min_variable = var
        #         min = unsatisified
        
        # return min_variable


    def most_constraining_variable(self, unassigned_variables):
        return max(unassigned_variables, key=lambda var: self.degree_variables[var])

    def least_constraining_value(self, var):
        if self.use_lcv:
            return sorted(self.variables[var], key=lambda val: self.count_conflicts(var, val))
        return self.variables[var]

class CNF:
    def __init__(self, variables, hard_clauses, soft_clauses):
        self.hard_clauses = hard_clauses
        self.soft_clauses = soft_clauses
        self.variables = variables

    def evaluate_clause(self, clause, assignments, is_soft=False):
        if not is_soft:
            for literal in clause:
                if literal.startswith('~'):
                    var = literal[1:]
                    value = not assignments.get(var, False)
                else:
                    var = literal
                    value = assignments.get(var, True)
                if value:
                    return True
            return False
        else:
            for literal in clause:
                if literal.startswith('~'):
                    var = literal[1:]
                    value = assignments.get(var, None)
                    if value != None:
                        value = not value
                else:
                    var = literal
                    value = assignments.get(var, None)
                if value:
                    return True
                if value == None:
                    return None
            return False

    def evaluate_negation(self, clause, assignments):
        for literal in clause:
            var = literal[1:] if literal.startswith('~') else '~' + literal
            if var in assignments and assignments[var]:
                return True
        return False

    def calculate_weight(self, assignments):
        total = 0
        for clause in self.soft_clauses:
            const, weight = clause
            if self.evaluate_clause(const, assignments, True):
                total += int(weight)
        return total
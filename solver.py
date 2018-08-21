from intexp import *
from model import *
from oracle import *

def synthesize(model, add_flag = False, const_flag = True):
    constraint_list = model.get_constraints()
    var_name_list = model.get_var_names()
    function_name = model.get_function()

    
    points_to_check = []

    # list of results encountered for the expression, encoded into a bit vector
    # used to determine whether or not something goes in used_expressions
    signatures_to_check = {}

    expressions = [] # queue of expressions to check the constraints against

    used_expressions = {} # solely for the purposes of forming new expressions

    # size of the expressions to form
    target_size = 3

    for i in range(1, 1000):
        used_expressions[i] = []


    bool_expressions_to_use = [] # queue of boolean expressions to use for ITE

    # initialize the first terms
    for var in var_name_list:
        expressions.append(Variable(var))
    
    if const_flag:
        expressions.append(Const(0))
        expressions.append(Const(1))
    


    # initialize the first booleans out of the constants and variables
    for i in range(len(expressions) - 1):
        for j in range(i + 1, len(expressions)):
            if not (expressions[i].is_constant() and expressions[j].is_constant()):
                bool_expressions_to_use.append(GTE(expressions[i], expressions[j]))
                bool_expressions_to_use.append(LTE(expressions[i], expressions[j]))
                bool_expressions_to_use.append(Equals(expressions[i], expressions[j]))



    i = 0
    cc1 = 0
    cc2 = 0
    left_bound = 1
    num_stored = 0
    num_enumerated = 0
    num_const = 2
    # how big we want our boolean to be
    bool_target_size = 3
    while (1):
        i += 1
        if (len(expressions) == 0):
            #make more candidate expressions
            iters = 0
            for index_left in range(left_bound, int((target_size + 1) / 2), 2):
                if (iters > 10000):
                    left_bound = index_left
                    break
                index_right = target_size - index_left - 1
                for exp1 in used_expressions[index_left]:
                    for exp2 in used_expressions[index_right]:
                        iters += 1
                        if (add_flag):
                            expressions.append(Add(exp1, exp2))
                            expressions.append(Subtract(exp1, exp2))
                            expressions.append(Subtract(exp2, exp1))
                            expressions.append(Multiply(exp1, exp2))
                        
                        for bool_exp in bool_expressions_to_use:
                            if not (exp1.contains_bool(bool_exp) or exp2.contains_bool(bool_exp)):
                                if not (exp1.equals(exp2)):
                                    # No reason to have an expression with two of the same bool value
                                    expressions.append(ITE(bool_exp, exp1, exp2))
                                    expressions.append(ITE(bool_exp, exp2, exp1))
            num_enumerated += len(expressions)

            if (iters <= 10000 and len(expressions) != 0):
                target_size += 2
                left_bound = 1


        if (len(expressions) == 0):
            # add another layer of boolean expressions
            iters = 0
            for exp1 in used_expressions[bool_target_size]:
                for exp2 in used_expressions[1]:
                    if iters > 20:
                        break
                    iters += 1
                    if not exp1.type() == "ite":
                        bool_expressions_to_use.append(GTE(expressions[i], expressions[j]))
                        bool_expressions_to_use.append(LTE(expressions[i], expressions[j]))
                        bool_expressions_to_use.append(Equals(expressions[i], expressions[j]))
                if iters > 20:
                    break
            if iters <= 20:
                bool_target_size = target_size - 2
            iters = 0
            continue

        if (i % 1000 == 0):
            print(i)


        exp = expressions.pop(0)

    
        flag = True
        new_signature = []
        for k in range(len(points_to_check)):
            points_to_check[k][function_name] = exp
            if not check(constraint_list, points_to_check[k]):
                flag = False
            new_signature.append(exp.execute(points_to_check[k]))
        if flag:

            ''''''''' Just shows how much was stored '''''''''
            stored_size = 0
            for k in range(1, 15):
                stored_size += len(used_expressions[k])
            print("NUM STORED: " + str(stored_size))
            ''''''''''''''''''''''''''''''''''''''''''''
            new_point = query(constraint_list, exp, var_name_list, function_name)
            if new_point == None:
                print(num_const)
                print("INPUT")
                for c in constraint_list:
                    print(c.exp_to_string())
                print("OUTPUT")
                print(exp.exp_to_string())
                wait = input("Completed")
                return exp
            else:
                points_to_check.append(new_point)

                for k in range(1, 1000):
                    used_expressions[k] = []

                expressions = []
                signatures_to_check = {}
                left_bound = 1
                target_size = 3
                for var in var_name_list:
                    expressions.append(Variable(var))
                if const_flag:
                    for m in range(num_const):
                        expressions.append(Const(m))

                num_const += 1
                
                
        else:
            cc1 += 1
            if new_signature not in signatures_to_check.values():
                num_stored += 1
                used_expressions[exp.size()].append(exp)
                signatures_to_check[exp] = new_signature
            
    
    print("Did not find anything!")
    return None
    

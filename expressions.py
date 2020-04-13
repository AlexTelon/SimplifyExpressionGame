import itertools
import random
from collections import defaultdict

_error_reason = ""

_all_possible_expressions = []
# Two or one variables. Eg: (True, 'a'), (True), ('a', 'a'), ('a', 'b')
for variables in itertools.chain(itertools.product([True, False, 'a', 'b'], repeat=2), itertools.product([True, False, 'a', 'b'], repeat=1)):
    if len(variables) == 1:
        for unary in ['not ', '']:
            exp = f"{unary}{variables[0]}"
            _all_possible_expressions.append(exp)
    else:
        for unary in itertools.product(['not ', ''], repeat=2):
            for binary in ['or', 'and']:
                exp = f"{unary[0]}{variables[0]} {binary} {unary[1]}{variables[1]}"
                _all_possible_expressions.append(exp)

                # also add expressions of the form: 'not (a or b)'
                exp = f"not ({unary[0]}{variables[0]} {binary} {unary[1]}{variables[1]})"
                _all_possible_expressions.append(exp)


def generate_expression():
    return random.choice(_all_possible_expressions)


def eval_expression(expression):
    # Eval an expression on all combinations of True False for two variables
    # Then return the results for these.
    names = ['a', 'b']
    result = []
    for values in itertools.product([True, False], repeat=2):
        context = dict(zip(names, values))
        result.append(eval(expression, globals(), context))
    return tuple(result)


def build_equivalence_dict():
    table = defaultdict(list)
    for exp in _all_possible_expressions:
        key = eval_expression(exp)
        table[key].append(exp)

    return table

_equivalence_dict = build_equivalence_dict()


def expression_in_simplest_form(original, suggestion):
    """Returns False if suggestion is not equivalent and in the shortest form of original.
    
    Example:
    
    expression_in_simplest_form('True and not False', 'True') -> True
    expression_in_simplest_form('a and a', 'a and a') -> False # (a is the shortest form)
    expression_in_simplest_form('a and True', 'a') -> False # (a is not equivalent. (True is the correct answer))
    """
    global _error_reason
    # if suggestion not in _equivalence_dict:
    #     _error_reason = f"{suggestion} not found in _equivalence_dict! (it is not a combination the program though resonable to consider.)"
    #     return False

    def is_equivalent(a, b):
        a_key = eval_expression(suggestion)
        b_key = eval_expression(original)
        return a_key == b_key
    
    equivalence_options = _equivalence_dict[eval_expression(original)]
    simplest = min([option for option in equivalence_options], key=len)

    if is_equivalent(original, suggestion):
        # Make sure suggestion is the shortest one.
        if suggestion == simplest:
            return True
        else:
            _error_reason = f'"{suggestion}" is not the shortest form "{simplest}"'
            return False
    else:
        _error_reason = f'"{suggestion}" is not equivalent to "{original}" == "{simplest}"'
        return False


def expressions_are_logically_same(original, suggestion, names=None):
    """Tests if two expressions are the same using a truth table."""
    global _error_reason
    if names is None:
        names = ['a', 'b']

    if not any(original) and not any(suggestion):
        return True

    if not any(suggestion):
        return False


    n = len(names)

    expected = []
    actual = []
    for values in itertools.product([True, False], repeat=n):
        context = dict(zip(names, values))
        context2 = dict(zip(names, values)) # copy just in case eval changes something
        expected.append(eval(original, globals(), context))
        try:
            actual.append(eval(suggestion, globals(), context2))
        except (SyntaxError, NameError) as e:
            _error_reason = f"{type(e)}: {e}"
            return False

    if actual == expected:
        return True
    else:
        _error_reason = f'"{suggestion}" != "{original}"!\n'
        for i, combination in enumerate(itertools.product([True, False], repeat=2)):
            if actual[i] != expected[i]:
                _error_reason += f"Example faulty combination: {combination} -> {actual[i]}\n"
                # # only add one error example
                # break
        return False

if __name__ == "__main__":
    # testing.
    assert(expressions_are_logically_same("a", "a"))
    assert(not expressions_are_logically_same("a", "b"))
    assert(expressions_are_logically_same("a and b", "b and a"))
    assert(not expressions_are_logically_same("a and b", "b or a"))
    assert(expressions_are_logically_same("not a and not b", "not (b or a)"))


    print("Sample of generate_expressions:")
    for i in range(10):
        print(generate_expression())
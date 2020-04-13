import itertools
import random

_error_reason = ""

_all_possible_expressions = []
for variables in itertools.product([True, False, 'a', 'b'], repeat=2):
    for unary in itertools.product(['not ', ''], repeat=2):
        for binary in ['or', 'and']:
            _all_possible_expressions.append(f"{unary[0]}{variables[0]} {binary} {unary[1]}{variables[1]}")


def generate_expression():
    return random.choice(_all_possible_expressions)


def classify_all_possible_expressions():
    # take all possible expressions that the user can be tasked with.
    # Create a dictionary of equivalent ones.
    # True, True and True, False or True, etc
    # We want to find all expressions that are always True, False and others such that we can always inform the user if a simpler form is possible.

    # Solution 1:
    # Start with an expression True, then apply different rules to it such that a bunch of resonably longer forms are found.

    # Solution 2:
    # Make the generator of expressions one based on a full list of expressions and it returns a random one of those.
    # That way we can go over each possible expression one by one.
    # Then using a truth table find all equivalence classes.

    def expressions():
        pass

    pass
    


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
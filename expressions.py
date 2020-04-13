import itertools
import random

_error_reason = ""

def generate_expression():
    def random_negation():
        """Gives not or nothing"""
        return random.choice(['not ', ''])

    def random_and_or_or():
        """Gives and or or"""
        return random.choice(['or', 'and'])

    def random_variable():
        return random.choice(['a', 'b', 'True', 'False'])


    expression = f"{random_negation()}{random_variable()} {random_and_or_or()} {random_negation()}{random_variable()}"
    # TODO add ()
    return expression

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
        actual.append(eval(suggestion, globals(), context2))

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
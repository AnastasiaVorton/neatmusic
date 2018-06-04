tests = [
    [(0.0, 0.0), (0.0, 1.0), (0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (1.0, 0.0), (0.0, 0.0)],
    [(0.0, 0.0), (0.0, 1.0), (0.0, 0.0), (0.0, 1.0)],
    [(0.0, 0.0), (1.0, 0.0), (0.0, 0.0), (1.0, 0.0)],
    [(1.0, 1.0), (1.0, 0.0), (1.0, 1.0), (1.0, 0.0)],
    [(1.0, 1.0), (1.0, 0.0), (0.0, 0.0), (1.0, 0.0)],
    [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (1.0, 0.0), (0.0, 0.0), (0.0, 1.0), (1.0, 1.0)]
]

valid_tests = [
    [(1.0, 1.0), (0.0, 1.0), (1.0, 1.0), (0.0, 1.0)],
    [(1.0, 1.0), (0.0, 1.0), (0.0, 0.0), (0.0, 1.0)],
    [(1.0, 1.0), (0.0, 1.0), (1.0, 1.0), (1.0, 0.0)],
    [(1.0, 0.0), (0.0, 1.0), (1.0, 1.0), (0.0, 1.0), (0.0, 0.0)],
]

def is_valid(test) -> bool:
    start = True
    for i, o in test:
        if (o >= 0.5) == (start ^ (i >= 0.5)):
            return False
        start = not start
    return True

def eval_function(net, test) -> float:
    cur = len(test)
    net.reset()
    for xi, xo in test:
        output = net.activate((xi,))
        cur -= (output[0] - xo) ** 2
    return cur / len(test)

def eval_tests(net) -> float:
    value = 0.0
    for test in tests:
        value += eval_function(net, test)
    return value / len(tests)
        
xor_inputs = [(0.0, 0.0), (0.0, 1.0), (1.0, 0.0), (1.0, 1.0)]
xor_outputs = [(0.0,), (1.0,), (1.0,), (0.0,)]


def eval_function(func) -> float:
    cur = 4.0
    for xi, xo in zip(xor_inputs, xor_outputs):
        output = func(xi)
    cur -= (output[0] - xo[0]) ** 2
    return cur

import random

def gen_test(size):
    return [random.choice([0.0, 1.0]) for _ in range(10)]

def answer_test(test):
    return [float((i % 2 != 0) ^ bool(round(j))) for i, j in enumerate(test)]

def is_valid(test) -> bool:
    start = True
    for i, o in test:
        if (o >= 0.5) == (start ^ (i >= 0.5)):
            return False
        start = not start
    return True

def eval_function(net) -> float:
    cur = 0
    for _ in range(10):
        size = random.randint(8, 10)
        val = size
        test = gen_test(size)
        answer = answer_test(test)
        net.reset()
        for i in range(size):
            output = net.activate((test[i],))
            val -= (output[0] - answer[i]) ** 2
        val /= size
        cur += val
    return cur / 10

from time import time


class Checker(object):
    def __init__(self):
        self.called = 0

    def __call__(self, x):
        self.called += 1
        return x ** 2 + x


checker = Checker()
limit = 10000

start = time()
xs = [checker(x) for x in range(limit)][::-1]
print('inline for:', time() - start, ' called:', checker.called)

checker = Checker()
start = time()
xs = list(map(checker, range(limit)))[::-1]
print('map:', time() - start, ' called:', checker.called)

from pyfunc.not_bad import (
    curry_tail_r_map,
    straightforward_tail_r_map,
    straightforward_tail_r_map_2,
    straightforward_tail_r_map_3,
)

checker = Checker()
calculate = curry_tail_r_map(checker)
start = time()
xs = calculate(range(limit))[::-1]
print('r_map without pattern matching:', time() - start, ' called:', checker.called)

from pyfunc.recursion import r_map_really_tail_curry

checker = Checker()
calculate = r_map_really_tail_curry(checker)
start = time()
xs = calculate(range(limit))[::-1]
print('r_map with pattern matching:', time() - start, ' called:', checker.called)

checker = Checker()
calculate = straightforward_tail_r_map(checker)
start = time()
xs = calculate(range(limit))[::-1]
print('straightforward map:', time() - start, ' called:', checker.called)

checker = Checker()
calculate = straightforward_tail_r_map_2(checker)
start = time()
xs = calculate(range(limit))[::-1]
print('straightforward map 2:', time() - start, ' called:', checker.called)

checker = Checker()
calculate = straightforward_tail_r_map_3(checker)
start = time()
xs = calculate(range(limit))[::-1]
print('straightforward map 3:', time() - start, ' called:', checker.called)

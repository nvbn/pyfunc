from time import time

checker = lambda x: x ** 2 + x
limit = 20000

start = time()
xs = [checker(x) for x in range(limit)][::-1]
print('inline for:', time() - start)

start = time()
xs = list(map(checker, xs))[::-1]
print('map:', time() - start)

from pyfunc.not_bad import curry_tail_r_map

calculate = curry_tail_r_map(checker)

start = time()
xs = calculate(xs)[::-1]
print('r_map without pattern matching:', time() - start)

from pyfunc.recursion import r_map_really_tail_curry


calculate = r_map_really_tail_curry(checker)

start = time()
xs = calculate(xs)[::-1]
print('r_map with pattern matching:', time() - start)


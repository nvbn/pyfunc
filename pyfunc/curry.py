from functools import partial


curry_2 = lambda fn: lambda x: lambda y: fn(x, y)


curry_map = curry_2(map)


@curry_map
def twice_or_increase(n):
    if n % 2 == 0:
        n += 1
    if n % 3:
        n *= 2
    return n


def curry_n(fn, n):
    def aux(x, n=None, args=None):
        args = args + [x]
        return partial(aux, n=n - 1, args=args) if n > 1 else fn(*args)
    return partial(aux, n=n, args=[])


curry_map_2 = curry_n(map, 3)
sum_arrays = curry_map_2(lambda x, y: x + y)
sum_with_range_10 = sum_arrays(range(10))

curry_2_2 = partial(curry_n, n=2)

curry_filter = curry_2_2(filter)
only_odd = curry_filter(lambda n: n % 2)


if __name__ == '__main__':
    print('twice or increase:')
    print(*twice_or_increase(range(10)))
    print(*twice_or_increase(range(30)))

    print('sum arrays:')
    print(*sum_with_range_10(range(100, 0, -10)))
    print(*sum_with_range_10(range(10)))

    print('only odd:')
    print(*only_odd(range(10)))
    print(*only_odd(range(-10, 0, 1)))

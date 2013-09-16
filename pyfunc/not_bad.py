from pyfunc.curry import curry_2
from pyfunc.recursion import tail_fnc


def tail_r_map(fn, arr_):
    @tail_fnc
    def aux(arr, acc=None):
        x, *xs = arr
        if xs:
            return aux(xs, acc + [fn(x)])
        else:
            return acc + [fn(x)]
    return aux(arr_, [])


curry_tail_r_map = curry_2(tail_r_map)


@curry_tail_r_map
def twice_if_odd(x):
    if x % 2 == 0:
        return x * 2
    else:
        return x

if __name__ == '__main__':
    print(twice_if_odd(range(100)))

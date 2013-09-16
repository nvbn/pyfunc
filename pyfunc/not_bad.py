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


class TailFunctor(object):
    """Tail functor"""

    def __init__(self, fnc):
        self._fnc = fnc
        self._calls = []
        self._called = False

    def __call__(self, *args):
        self._calls.append(args)
        if not self._called:
            self._called = True
            return self.run()

    def run(self):
        while self._calls:
            res = self._fnc(*self._calls.pop(0))
        return res


@curry_2
def straightforward_tail_r_map(fn, arr_):
    @TailFunctor
    def aux(arr, acc=None):
        x, *xs = arr
        if xs:
            return aux(xs, acc + [fn(x)])
        else:
            return acc + [fn(x)]
    return aux(arr_, [])


@curry_2
def straightforward_tail_r_map_2(fn, arr_):
    @TailFunctor
    def aux(arr, acc=None):
        x = arr[0]
        xs = arr[1:]
        if xs:
            return aux(xs, acc + [fn(x)])
        else:
            return acc + [fn(x)]
    return aux(arr_, [])


@curry_2
def straightforward_tail_r_map_3(fn, arr_):
    @TailFunctor
    def aux(arr, acc=None):
        x = arr[0]
        xs = arr[1:]
        acc.append(fn(x))
        if xs:
            return aux(xs, acc)
        else:
            return acc
    return aux(arr_, [])


if __name__ == '__main__':
    print(twice_if_odd(range(100)))

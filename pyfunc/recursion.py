from pyfunc.curry import curry_n
from pyfunc.pattern_match import (
    pattern_match, hd_tl_partial, is_blank, identity, match_curry,
)


r_map = lambda fn, arg: pattern_match((
    (hd_tl_partial(identity, is_blank), lambda arr: [fn(arr[0])]),
    (
        hd_tl_partial(identity, identity),
        lambda arr: [fn(arr[0])] + r_map(fn, arr[1])
    ),
), arg)

r_map_curry = curry_n(r_map, 2)
twice = r_map_curry(lambda x: x * 2)

is_none = match_curry(lambda obj: obj is None)
pair = lambda match_x, match_y: lambda arr: (match_x(arr[0]), match_y(arr[1]))


def r_map_tail(fn, arg):
    aux = lambda arg: pattern_match((
        (pair(identity, is_none), lambda arr: aux([arr[0], []])),
        (
            pair(hd_tl_partial(identity, is_blank), identity),
            lambda arr: arr[1] + [fn(arr[0][0])]
        ),
        (
            pair(hd_tl_partial(identity, identity), identity),
            lambda arr: aux([arr[0][1], arr[1] + [fn(arr[0][0])]])
        ),
    ), arg)
    return aux([arg, None])

r_map_tail_curry = curry_n(r_map_tail, 2)
twice_tail = r_map_tail_curry(lambda x: x * 2)


def tail_fnc(fn):
    called = False
    calls = []

    def run():
        while len(calls):
            res = fn(*calls.pop())
        return res

    def call(*args):
        nonlocal called
        calls.append(args)
        if not called:
            called = True
            return run()
    return call


def r_map_really_tail(fn, arg):
    aux = tail_fnc(lambda arg: pattern_match((
        (pair(identity, is_none), lambda arr: aux([arr[0], []])),
        (
            pair(hd_tl_partial(identity, is_blank), identity),
            lambda arr: arr[1] + [fn(arr[0][0])]
        ),
        (
            pair(hd_tl_partial(identity, identity), identity),
            lambda arr: aux([arr[0][1], arr[1] + [fn(arr[0][0])]])
        ),
    ), arg))
    return aux([arg, None])

r_map_really_tail_curry = curry_n(r_map_really_tail, 2)
twice_really_tail = r_map_really_tail_curry(lambda x: x * 2)


if __name__ == '__main__':
    print('try recursion map:')
    print(r_map(lambda x: x**2, range(10)))

    print('twice:')
    print(twice(range(10)))
    try:
        print(twice(range(1000)))
    except RuntimeError as e:
        print(e)

    print('tail recursion:')
    print(twice_tail(range(10)))
    try:
        print(twice_tail(range(10000)))
    except RuntimeError as e:
        print(e)

    print('really tail:')
    print(twice_really_tail(range(1000)))

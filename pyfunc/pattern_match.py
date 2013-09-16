from functools import partial
from pyfunc.curry import curry_n

identity = lambda x: x


class NotMatch(Exception):
    pass


def not_match(x):
    raise NotMatch(x)


match = lambda check, obj: obj if check(obj) else not_match(obj)
match_curry = curry_n(match, 2)
instance_of = lambda type_: match_curry(lambda obj: isinstance(obj, type_))

is_int = instance_of(int)

is_array_of = lambda matcher: match_curry(lambda obj: all(map(matcher, obj)))
is_array_of_int = is_array_of(is_int)


def hd_tl(match_x, match_xs, arr):
    x, *xs = arr
    return match_x(x), match_xs(xs)


hd_tl_identity = partial(hd_tl, identity, identity)

hd_tl_ints = partial(hd_tl, is_int, is_array_of_int)

is_blank = match_curry(lambda xs: len(xs) == 0)
is_str = instance_of(str)
is_array_of_str = is_array_of(is_str)


def pattern_match(patterns, args):
    for pattern, fnc in patterns:
        try:
            return fnc(pattern(args))
        except NotMatch:
            continue
    raise NotMatch(args)

hd_tl_partial = lambda match_x, match_xs: partial(hd_tl, match_x, match_xs)

pattern_match_curry = curry_n(pattern_match, 2)
sum_or_multiply = pattern_match_curry((
    (hd_tl_partial(identity, is_blank), lambda arr: arr[0]),
    (hd_tl_ints, lambda arr: arr[0] * sum_or_multiply(arr[1])),
    (hd_tl_partial(is_str, is_array_of_str), lambda arr: arr[0] + sum_or_multiply(arr[1])),
))


if __name__ == '__main__':
    print('identity:')
    print(identity(10))
    print(identity(20))

    print('is int:')
    print(is_int(2))
    try:
        is_int('str')
    except NotMatch:
        print('not int')

    print('is array of int:')
    print(is_array_of_int([1, 2, 3]))
    try:
        is_array_of_int('str')
    except NotMatch:
        print('not int')


    print('hd tl:')
    print(hd_tl_identity(range(10)))

    print('hd tl ints:')
    print(hd_tl_ints(range(10, 20)))
    try:
        hd_tl_ints(['str', 1, 2])
    except NotMatch:
        print('not ints')

    print('sum or multiply:')
    print(sum_or_multiply(range(1, 10)))
    print(sum_or_multiply(['a', 'b', 'c']))

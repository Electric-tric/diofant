"""Tests for functions for generating interesting polynomials. """

import pytest

from diofant import Poly, symbols
from diofant.abc import x, y, z
from diofant.polys.specialpolys import (cyclotomic_poly, fateman_poly_F_1,
                                        fateman_poly_F_2, fateman_poly_F_3,
                                        interpolating_poly, random_poly,
                                        swinnerton_dyer_poly, symmetric_poly)


__all__ = ()


def test_swinnerton_dyer_poly():
    pytest.raises(ValueError, lambda: swinnerton_dyer_poly(0, x))

    assert swinnerton_dyer_poly(1, x, polys=True) == Poly(x**2 - 2)
    assert swinnerton_dyer_poly(1, polys=True) == Poly(x**2 - 2)

    assert swinnerton_dyer_poly(1, x) == x**2 - 2
    assert swinnerton_dyer_poly(2, x) == x**4 - 10*x**2 + 1
    assert swinnerton_dyer_poly(3, x) == (x**8 - 40*x**6 +
                                          352*x**4 - 960*x**2 + 576)
    assert swinnerton_dyer_poly(4, x) == (x**16 - 136*x**14 + 6476*x**12 -
                                          141912*x**10 + 1513334*x**8 -
                                          7453176*x**6 + 13950764*x**4 -
                                          5596840*x**2 + 46225)


def test_cyclotomic_poly():
    pytest.raises(ValueError, lambda: cyclotomic_poly(0, x))

    assert cyclotomic_poly(1, x, polys=True) == Poly(x - 1)
    assert cyclotomic_poly(1, polys=True) == Poly(x - 1)

    assert cyclotomic_poly(1, x) == x - 1
    assert cyclotomic_poly(2, x) == x + 1
    assert cyclotomic_poly(3, x) == x**2 + x + 1
    assert cyclotomic_poly(4, x) == x**2 + 1
    assert cyclotomic_poly(5, x) == x**4 + x**3 + x**2 + x + 1
    assert cyclotomic_poly(6, x) == x**2 - x + 1


def test_symmetric_poly():
    pytest.raises(ValueError, lambda: symmetric_poly(-1, x, y, z))
    pytest.raises(ValueError, lambda: symmetric_poly(5, x, y, z))

    assert symmetric_poly(1, x, y, z, polys=True) == Poly(x + y + z)
    assert symmetric_poly(1, (x, y, z), polys=True) == Poly(x + y + z)

    assert symmetric_poly(0, x, y, z) == 1
    assert symmetric_poly(1, x, y, z) == x + y + z
    assert symmetric_poly(2, x, y, z) == x*y + x*z + y*z
    assert symmetric_poly(3, x, y, z) == x*y*z


def test_random_poly():
    poly = random_poly(x, 10, -100, 100, polys=False)

    assert Poly(poly).degree() == 10
    assert all(-100 <= coeff <= 100 for coeff in Poly(poly).coeffs()) is True

    poly = random_poly(x, 10, -100, 100, polys=True)

    assert poly.degree() == 10
    assert all(-100 <= coeff <= 100 for coeff in poly.coeffs()) is True


def test_interpolating_poly():
    x0, x1, x2, y0, y1, y2 = symbols('x:3, y:3')

    assert interpolating_poly(0, x) == 0
    assert interpolating_poly(1, x) == y0

    assert interpolating_poly(2, x) == \
        y0*(x - x1)/(x0 - x1) + y1*(x - x0)/(x1 - x0)

    assert interpolating_poly(3, x) == \
        y0*(x - x1)*(x - x2)/((x0 - x1)*(x0 - x2)) + \
        y1*(x - x0)*(x - x2)/((x1 - x0)*(x1 - x2)) + \
        y2*(x - x0)*(x - x1)/((x2 - x0)*(x2 - x1))


def test_fateman_poly_F_1():
    f, g, h = map(lambda x: x.rep.to_dense(), fateman_poly_F_1(1))

    assert f == [[1], [2, 3], [1, 3, 2]]
    assert g == [[-3, 0], [], [-3, 1, -3, -1], [], [1, 0, 0, 0, -1]]
    assert h == [[1]]

    f, g, h = map(lambda x: x.rep.to_dense(), fateman_poly_F_1(3))

    assert f == [[[[1]]], [[[2]], [[2], [2, 3]]],
                 [[[1]], [[2], [2, 3]], [[1], [2, 3], [1, 3, 2]]]]
    assert g == [[[[-3]], [[]]], [[[]]],
                 [[[-3]], [[1]], [[-3], [], [-3, 0, -3]], [[-1]]],
                 [[[]]], [[[1]], [[]], [[1], [], [1, 0, 0]],
                          [[]], [[-1], [], [-1, 0, -1]]]]
    assert h == [[[[1]]]]


def test_fateman_poly_F_2():
    f, g, h = map(lambda x: x.rep.to_dense(), fateman_poly_F_2(1))

    assert f == [[1], [-2], [-2, -6, -3], [2, 6, 4], [1, 6, 13, 12, 4]]
    assert g == [[1], [4, 6], [6, 18, 13], [4, 18, 26, 12], [1, 6, 13, 12, 4]]
    assert h == [[1], [2, 2], [1, 2, 1]]

    f, g, h = map(lambda x: x.rep.to_dense(), fateman_poly_F_2(3))

    assert f == [[[[1]]], [[[-2]]], [[[-2]], [[-4], [-4, -6]],
                                     [[-2], [-4, -6], [-2, -6, -3]]],
                 [[[2]], [[4], [4, 6]], [[2], [4, 6], [2, 6, 4]]],
                 [[[1]], [[4], [4, 6]], [[6], [12, 18], [6, 18, 13]],
                  [[4], [12, 18], [12, 36, 26], [4, 18, 26, 12]],
                  [[1], [4, 6], [6, 18, 13], [4, 18, 26, 12],
                   [1, 6, 13, 12, 4]]]]
    assert g == [[[[1]]], [[[4]], [[4], [4, 6]]],
                 [[[6]], [[12], [12, 18]], [[6], [12, 18], [6, 18, 13]]],
                 [[[4]], [[12], [12, 18]], [[12], [24, 36], [12, 36, 26]],
                  [[4], [12, 18], [12, 36, 26], [4, 18, 26, 12]]],
                 [[[1]], [[4], [4, 6]], [[6], [12, 18], [6, 18, 13]],
                  [[4], [12, 18], [12, 36, 26], [4, 18, 26, 12]],
                  [[1], [4, 6], [6, 18, 13], [4, 18, 26, 12],
                   [1, 6, 13, 12, 4]]]]
    assert h == [[[[1]]], [[[2]], [[2], [2, 2]]],
                 [[[1]], [[2], [2, 2]], [[1], [2, 2], [1, 2, 1]]]]


def test_fateman_poly_F_3():
    f, g, h = map(lambda x: x.rep.to_dense(), fateman_poly_F_3(1))

    assert f == [[1], [], [-2], [], [-2, 0, -6, 0, -3], [],
                 [2, 0, 6, 0, 4], [], [1, 0, 6, 0, 13, 0, 12, 0, 4]]
    assert g == [[1], [], [4, 0, 6], [], [6, 0, 18, 0, 13], [],
                 [4, 0, 18, 0, 26, 0, 12], [], [1, 0, 6, 0, 13, 0, 12, 0, 4]]
    assert h == [[1], [], [2, 0, 2], [], [1, 0, 2, 0, 1]]

    f, g, h = map(lambda x: x.rep.to_dense(), fateman_poly_F_3(3))

    assert f == [[[[1]]], [[[]]], [[[]]], [[[]]], [[[-2]]], [[[]]], [[[]]],
                 [[[]]], [[[-2]], [[]], [[]], [[]],
                          [[-4], [], [], [], [-4, 0, 0, 0, -6]], [[]], [[]],
                          [[]], [[-2], [], [], [], [-4, 0, 0, 0, -6], [], [],
                                 [], [-2, 0, 0, 0, -6, 0, 0, 0, -3]]],
                 [[[]]], [[[]]], [[[]]],
                 [[[2]], [[]], [[]], [[]],
                  [[4], [], [], [], [4, 0, 0, 0, 6]], [[]], [[]], [[]],
                  [[2], [], [], [], [4, 0, 0, 0, 6], [], [], [],
                   [2, 0, 0, 0, 6, 0, 0, 0, 4]]],
                 [[[]]], [[[]]], [[[]]],
                 [[[1]], [[]], [[]], [[]],
                  [[4], [], [], [], [4, 0, 0, 0, 6]], [[]], [[]], [[]],
                  [[6], [], [], [], [12, 0, 0, 0, 18], [], [], [],
                   [6, 0, 0, 0, 18, 0, 0, 0, 13]], [[]], [[]], [[]],
                  [[4], [], [], [], [12, 0, 0, 0, 18], [], [], [],
                   [12, 0, 0, 0, 36, 0, 0, 0, 26], [], [], [],
                   [4, 0, 0, 0, 18, 0, 0, 0, 26, 0, 0, 0, 12]],
                  [[]], [[]], [[]],
                  [[1], [], [], [], [4, 0, 0, 0, 6], [], [],
                   [], [6, 0, 0, 0, 18, 0, 0, 0, 13], [], [], [],
                   [4, 0, 0, 0, 18, 0, 0, 0, 26, 0, 0, 0, 12], [], [], [],
                   [1, 0, 0, 0, 6, 0, 0, 0, 13, 0, 0, 0, 12, 0, 0, 0, 4]]]]
    assert g == [[[[1]]], [[[]]], [[[]]], [[[]]],
                 [[[4]], [[]], [[]], [[]], [[4], [], [], [], [4, 0, 0, 0, 6]]],
                 [[[]]], [[[]]], [[[]]],
                 [[[6]], [[]], [[]], [[]],
                  [[12], [], [], [], [12, 0, 0, 0, 18]], [[]], [[]], [[]],
                  [[6], [], [], [], [12, 0, 0, 0, 18], [], [], [],
                   [6, 0, 0, 0, 18, 0, 0, 0, 13]]], [[[]]], [[[]]], [[[]]],
                 [[[4]], [[]], [[]], [[]], [[12], [], [], [], [12, 0, 0, 0, 18]],
                  [[]], [[]], [[]], [[12], [], [], [], [24, 0, 0, 0, 36], [], [], [],
                  [12, 0, 0, 0, 36, 0, 0, 0, 26]], [[]], [[]], [[]],
                  [[4], [], [], [], [12, 0, 0, 0, 18], [], [], [],
                   [12, 0, 0, 0, 36, 0, 0, 0, 26], [], [], [],
                   [4, 0, 0, 0, 18, 0, 0, 0, 26, 0, 0, 0, 12]]], [[[]]], [[[]]],
                 [[[]]], [[[1]], [[]], [[]], [[]], [[4], [], [], [], [4, 0, 0, 0, 6]],
                 [[]], [[]], [[]], [[6], [], [], [], [12, 0, 0, 0, 18],
                                    [], [], [], [6, 0, 0, 0, 18, 0, 0, 0, 13]],
                 [[]], [[]], [[]],
                 [[4], [], [], [], [12, 0, 0, 0, 18], [], [], [],
                  [12, 0, 0, 0, 36, 0, 0, 0, 26], [], [], [],
                  [4, 0, 0, 0, 18, 0, 0, 0, 26, 0, 0, 0, 12]], [[]], [[]], [[]],
                 [[1], [], [], [], [4, 0, 0, 0, 6], [], [], [],
                  [6, 0, 0, 0, 18, 0, 0, 0, 13], [], [], [],
                  [4, 0, 0, 0, 18, 0, 0, 0, 26, 0, 0, 0, 12],
                  [], [], [], [1, 0, 0, 0, 6, 0, 0, 0, 13, 0, 0, 0, 12, 0, 0, 0, 4]]]]
    assert h == [[[[1]]], [[[]]], [[[]]], [[[]]],
                 [[[2]], [[]], [[]], [[]], [[2], [], [], [], [2, 0, 0, 0, 2]]],
                 [[[]]], [[[]]], [[[]]], [[[1]], [[]], [[]], [[]],
                 [[2], [], [], [], [2, 0, 0, 0, 2]], [[]], [[]], [[]],
                 [[1], [], [], [], [2, 0, 0, 0, 2], [], [], [],
                  [1, 0, 0, 0, 2, 0, 0, 0, 1]]]]

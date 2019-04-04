from math import sqrt
from pytest import approx

from energy_tools.complex import EleComplex


def test_init():
    assert EleComplex(1, 2) == complex(1, 2)


def test_phase_simple():
    assert EleComplex(1, 1).phase == 45


def test_phase_quadran_1():
    assert EleComplex(1 + 1j).phase == 45.0


def test_phase_quadran_2():
    assert EleComplex(-1 + 1j).phase == 135.0


def test_phase_quadran_3():
    assert EleComplex(-1 - 1j).phase == 225.0


def test_phase_quadran_4():
    assert EleComplex(1 - 1j).phase == 315.0


def test_phase_0_degres():
    assert EleComplex(1 + 0j).phase == 0.0


def test_phase_90_degres():
    assert EleComplex(0 + 1j).phase == 90.0


def test_phase_180_degres():
    assert EleComplex(-1 + 0j).phase == 180.0


def test_phase_270_degres():
    assert EleComplex(0 - 1j).phase == 270.0


def test_phase_entier_positif():
    assert EleComplex(2).phase == 0.0


def test_phase_decimal_negatif():
    assert EleComplex(-2.12).phase == 180.0


def test_module():
    assert EleComplex(1, 1).module == sqrt(2)


def test_round_2_digits():
    ans = round(EleComplex(1.1032 + 1.1240j), 2)
    assert ans == EleComplex(1.10 + 1.12j)
    assert ans.__class__ == EleComplex


def test_round():
    ans = round(EleComplex(1.1032 + 1.1240j))
    assert ans == EleComplex(1.0 + 1.0j)
    assert ans.__class__ == EleComplex


def test_round_str():
    ans = round(EleComplex(1.1032 + 1.1240j), 3)
    assert ans.__str__() == "(1.103+1.124j)"
    assert ans.__class__ == EleComplex


def test_pf_cadran_0():
    ans = EleComplex(4.0 + 1.0j).pf
    assert ans == approx(4.0 / (4.0**2 + 1.0**2)**0.5)


def test_pf_cadran_1():
    ans = EleComplex(-2.0 + 3.0j).pf
    assert ans == approx(-2.0 / (2.0**2 + 3.0**2)**0.5)


def test_pf_cadran_2():
    ans = EleComplex(-0.5 - 0.1j).pf
    assert ans == approx(0.5 / (0.5**2 + 0.1**2)**0.5)


def test_pf_cadran_3():
    ans = EleComplex(4.7 - 2.1j).pf
    assert ans == approx(-4.7 / (4.7**2 + 2.1**2)**0.5)


def test_mul_elecomplexes():
    ans_0 = EleComplex(2.3 + 1.7j) * EleComplex(-1.2 - 8.9j)
    ans_1 = (2.3 + 1.7j) * (-1.2 - 8.9j)
    assert ans_0.real == approx(ans_1.real)
    assert ans_0.imag == approx(ans_1.imag)
    assert ans_0.__class__ == EleComplex


def test_mul_elecomplex_complex():
    ans_0 = EleComplex(2.3 + 1.7j) * (-1.2 - 8.9j)
    ans_1 = (2.3 + 1.7j) * (-1.2 - 8.9j)
    assert ans_0.real == approx(ans_1.real)
    assert ans_0.imag == approx(ans_1.imag)
    assert ans_0.__class__ == EleComplex


def test_div_elecomplexes():
    ans_0 = EleComplex(2.3 + 1.7j) / EleComplex(-1.2 - 8.9j)
    ans_1 = (2.3 + 1.7j) / (-1.2 - 8.9j)
    assert ans_0.real == approx(ans_1.real)
    assert ans_0.imag == approx(ans_1.imag)
    assert ans_0.__class__ == EleComplex


def test_div_elecomplex_complex():
    ans_0 = EleComplex(2.3 + 1.7j) / (-1.2 - 8.9j)
    ans_1 = (2.3 + 1.7j) / (-1.2 - 8.9j)
    assert ans_0.real == approx(ans_1.real)
    assert ans_0.imag == approx(ans_1.imag)
    assert ans_0.__class__ == EleComplex

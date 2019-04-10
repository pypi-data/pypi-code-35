import sympy as sp
import numpy as np

from cotpy import model


class TestModel:
    def test_create_model(self):
        expr = "a0+a1*x(t-1)+a2*x(t-2)+a3*u(t-6)+a4*u(t-7)+a5*z1(t-1)+a6*z2(t-1)"
        expectation_expr = sp.S('a0 + a1*x0_1 + a2*x0_2 + a3*u0_6 + a4*u0_7 + a5*z1_1 + a6*z2_1')
        expectation_vars = sp.var('a0, a1, a2, a3, a4, a5, a6, x0_1, x0_2, u0_6, u0_7, z1_1, z2_1')
        m = model.create_model(expr)
        assert isinstance(m, model.Model)
        assert m.sp_expr == expectation_expr
        assert m.sp_var == list(expectation_vars)

        args = [1, 1, 1, 1, 1, 1, 1, 10, 15, 20, 25, 30, 35]
        expectation_grad = [1.0] + args[7:]
        res = m.get_grad_value(*args)
        # print(res)
        assert isinstance(res, list)
        assert res == expectation_grad
        # assert m.get_grad_value(a=[1, 1, 1, 1, 1, 1, 1], x=[10, 15], u=[20, 25], z=[30, 35]) == expectation_grad

        assert m.func_model(*args) == 136

        assert m.model_vars['output'][0].max_tao == 2
        assert m.model_vars['input'][0].max_tao == 7

        a = [[1, 1, 1, 1, 1, 0, 5], [1, 1, 1, 1, 1, 1, 6],
             [1, 1, 1, 1, 1, 2, 7], [1, 1, 1, 1, 1, 3, 8],
             [1, 1, 1, 1, 1, 4, 9], [1, 1, 1, 1, 1, 3, 10], [1, 1, 1, 1, 1, 2, 11]]

        m.initialization(type_memory='max', memory_size=0, a=a)

        print('last a:', m.last_a)
        assert m.last_a == [k[-1] for k in a]
        # var_values = m.get_all_var_values()
        # assert var_values['output'][0] == np.array([0 for _ in range(8)])
        # assert var_values['input'][0] == np.array([0 for _ in range(13)])
        # assert var_values['add_input'] == [np.array([0 for _ in range(7)]) for _ in range(2)]

    def test_func_model(self):
        pass

    def test_grad_funcs(self):
        pass

    def test_sp_var(self):
        pass

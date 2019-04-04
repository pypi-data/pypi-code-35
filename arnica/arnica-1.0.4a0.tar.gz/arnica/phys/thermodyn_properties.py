from __future__ import absolute_import, division
import math
import numpy as np

PRANDTL = 0.71
PRANDTL_TURB = 0.86
VKARMAN = 0.41
VAN_DRIEST = 5.5
BETA_KADER = ((3.85 * PRANDTL**(1.0/3.0) - 1.3)**2
              + 2.12 * math.log(PRANDTL))
K_KADER = ((BETA_KADER
            - PRANDTL_TURB * VAN_DRIEST
            + PRANDTL_TURB / VKARMAN - 2.12)
           - (PRANDTL_TURB / VKARMAN - 2.12)
           * (200.0*math.log(200.0) - 100*math.log(100.0))
           / (200.0 - 100.0))


def h_kader(t_wall,
            rho_wall,
            y_wall,
            u_2,
            t_2,
            temp_adiab):
    """ compute h at the wall as in kader
    names taken equalt to  loglaw_cwm.f90 AVBP"""
    _, heat_cp, mu_wall = lambda_cp_visco_fluid(t_2)
    # mu_wall : Kg / m.s
    # 1.0 Compute y_plus and u_tau
    # first estimation of y_plus
  
    yplus_guess = np.maximum(
        0.157 * (u_2 * y_wall * rho_wall / mu_wall)**(7.0/8.0),
        1.0e-3)
    #           [m/s *   m    *   Kg/m3  *s.m/ kg] = [-]
    # Linear part
    u_tau_lin = np.sqrt(u_2 / y_wall * mu_wall / rho_wall)
    #              sqrt[m/s /   m    * kg / m.s  *   m3/kg] =
    #              sqrt[m/s               /   s  *   m    ] =
    #              sqrt[m2/s2] = m/s

    #Log part
    def _get_u_tau_log():
        """ evaluate u tau in log region """
        u_tau_log = 0
        epsilon = 1.0
        yplus_log = yplus_guess

        def _loop_u_tau(u_tau_log, yplus_log):
            """ recursive loop to evaluate u_tau """
            utau_old = u_tau_log
            u_tau_log = u_2 / (1 / VKARMAN * np.log(yplus_log)
                               + VAN_DRIEST)
            yplus_log = u_tau_log * y_wall * rho_wall / mu_wall
            epsilon = np.abs(u_tau_log - utau_old)
            return u_tau_log, yplus_log, epsilon

        while np.min(epsilon) >= 1.e-5:
            (u_tau_log,
             yplus_log,
             epsilon) = _loop_u_tau(u_tau_log,
                                    yplus_log)

        return u_tau_log


    u_tau_log = _get_u_tau_log()
    # fusion of the two
    u_tau_cwm = np.where(yplus_guess < 11.25,
                         u_tau_lin,
                         u_tau_log)
    y_plus = u_tau_cwm * y_wall * rho_wall / mu_wall

    # 2.0 Compute T_tau
    kader_g = ((0.01 * (PRANDTL * y_plus)**4)
               / (1.0 + 5.0 * PRANDTL**3 * y_plus))
    t_tau_cwm = (
        (t_wall - t_2)
        / ((PRANDTL * y_plus * np.exp(-kader_g))
           + (PRANDTL_TURB*u_2/u_tau_cwm + K_KADER) * np.exp(-1.0/kader_g)))

    # unused tau_wall = rho_wall * u_tau_cwm * u_tau_cwm
    q_wall = rho_wall * heat_cp * u_tau_cwm * t_tau_cwm
    
    #print "qwall" ,t_wall.mean(),  (t_wall - t_2).min() , (t_wall - t_2).max()
    # resize h wall depending on the T adiab found -and not t_2-
    h_wall = -q_wall / (temp_adiab - t_wall)

    #raise ValueError("for some reason, the h coef is negative, i.e. your t_guess is too high")
    #h_wall = np.clip(h_wall, 1, 100000)

    return h_wall


def lambda_cp_visco_fluid(t_guess):
    """ compute Fluid properties lambda , cp, visco """
    def _visco_sutherland(t_guess):
        """ compute visocity as in sutherland"""
        mu_wall = (1.716e-5
                   * (t_guess / 273.15)**1.5
                   * (273.15 + 110.4) / (t_guess + 110.4))
        return mu_wall

    def _cp_correl(t_guess):
        """ compute cp of fluid"""
        # ADD CLIPPING
        #t_clip = np.max(t_guess, 300.0)
        #t_clip = np.min(t_clip, 2500.0)
        t_clip = t_guess

        heat_cp = (513.46
                   + 1.6837 * t_clip
                   - 0.0019275 * t_clip**2
                   + 1.2773e-6 * t_clip**3
                   - 4.2773e-10 * t_clip**4
                   + 5.6735e-14 * t_clip**5)
        return heat_cp
    heat_cp = _cp_correl(t_guess)
    mu_wall = _visco_sutherland(t_guess)
    lam = heat_cp / PRANDTL * mu_wall

    return lam, heat_cp, mu_wall

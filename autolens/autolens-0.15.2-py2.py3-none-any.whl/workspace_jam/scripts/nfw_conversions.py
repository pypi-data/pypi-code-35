from astropy import cosmology
from scipy.optimize import fsolve

import numpy as np

def convert_to_lens_unit(m_nfw, c_nfw, z_nfw, z_source, cosmo=cosmology.LambdaCDM):
    '''
    Trying to convert los subhalo with a given mass and concentration
    to lens units.

    m_nfw: m_200 [solar mass]
    c_nfw: concentration
    z_nfw: Redshift of the halo
    z_source: Redshift of the background source

    return kappa_s & rs [arcsec]
    '''
    H_l = (cosmo.H0).value  # Hubble constant
    G_l = 4.302e-9  # Mpc M_sun^-1 (km/s)
    J_c = 3. * H_l ** 2. / (8. * np.pi * G_l) / 10. ** (9.)  # M_sun/kpc^(3)
    C_v = 3 * 10 ** 5.  # light velocity [km/s]
    G_crit = 4.302e-6  # kpc M_sun^-1 (km/s)^2

    r200 = (m_nfw / (200. * J_c * (4. * np.pi / 3.))) ** (1. / 3.)  # R_200
    c = c_nfw
    # print(c)
    de_c = 200. / 3. * (c * c * c / (np.log(1. + c) - c / (1. + c)))  # delta_c
    rs = r200 / c  # rs
    rhos = J_c * de_c  # rhos
    s_crit = (C_v * C_v * cosmo.angular_diameter_distance(z_source) / (4. * np.pi *
                                                                       cosmo.angular_diameter_distance(z_nfw) *
                                                                       cosmo.angular_diameter_distance_z1z2(z_nfw,
                                                                                                            z_source)) / (
                          1000.0
                          * G_crit)).value  # critical density at los halo
    kappa_s = rs * rhos / s_crit
    arctokpc = np.pi / 180.0 / 3600.0 * (cosmo.angular_diameter_distance(z_nfw) *
                                         1000.0).value
    rs_arcsec = rs / arctokpc
    return kappa_s, rs_arcsec

def convert_to_physical_unit(kappa_s, rs_arcsec, z_nfw, z_source, cosmo=cosmology.LambdaCDM):
    '''
    Trying to convert NFW lens units to physical units.

    kappa_s: rhos*rs/s_crit
    rs_arcsec: scale radius [arcsec]
    z_nfw: Redshift of the halo
    z_source: Redshift of the background source

    return m200 [solar mass] & concentration: c
    '''
    H_l = cosmo.H0.value  # Hubble constant
    G_l = 4.302e-9  # Mpc M_sun^-1 (km/s) # Gravitational constnat
    J_c = 3. * H_l ** 2. / (8. * np.pi * G_l) / 10. ** (9.)  # cosmic average density M_sun/kpc^(3)
    C_v = 3 * 10 ** 5.  # light velocity [km/s]
    G_crit = 4.302e-6  # kpc M_sun^-1 (km/s)^2 # Gravitational constant

    arctokpc = np.pi / 180.0 / 3600.0 * (cosmo.angular_diameter_distance(z_nfw) *
                                         1000.0).value
    rs = rs_arcsec * arctokpc

    s_crit = (C_v * C_v * cosmo.angular_diameter_distance(z_source) / (4. * np.pi *
                                                                       cosmo.angular_diameter_distance(z_nfw) *
                                                                       cosmo.angular_diameter_distance_z1z2(z_nfw,
                                                                                                            z_source)) / (
                          1000.0
                          * G_crit)).value  # critical density

    rhos = kappa_s * s_crit / rs  # rho_s

    print(rhos)

    de_c = rhos / J_c  # delta_c

    c = fsolve(solve_c, 10.0, args=(de_c,))[0]  # concentration

    r200 = c * rs  # R_200

    m200 = 200.0 * (4. / 3. * np.pi) * J_c * r200 ** 3.0  # M_200

    return m200, c

def solve_c(c, de_c):
    '''
    Equation need for solving concentration c for a given delta_c
    '''
    return 200.0/3.0*(c*c*c/(np.log(1+c) - c/(1+c))) - de_c

def convert_to_physical_unit_tNFW(kappa_s, rs_arcsec, z_nfw, z_source, cosmo=cosmology.LambdaCDM, rt_arcsec=None):
    '''
    Trying to convert tNFW lens units to physical units.

    kappa_s: rhos*rs/s_crit

    rs_arcsec: scale radius [arcsec]

    rt_arcsec: truncation radius [arcsec]
    if rt_arcsec is not given, then rt is set to be 2.0*R_200

    z_nfw: Redshift of the halo

    z_source: Redshift of the background source

    return m200 [solar mass], m_t [solar_mass], & concentration: c, r200 [kpc]
    '''
    H_l = (cosmo.H0).value # Hubble constant
    G_l = 4.302e-9 # Mpc M_sun^-1 (km/s) # Gravitational constnat
    J_c = 3.*H_l**2./(8.*np.pi*G_l)/10.**(9.) # cosmic average density M_sun/kpc^(3)
    C_v = 3*10**5. # light velocity [km/s]
    G_crit = 4.302e-6 # kpc M_sun^-1 (km/s)^2 # Gravitational constant

    arctokpc = np.pi/180.0/3600.0*(cosmo.angular_diameter_distance(z_nfw)*
            1000.0).value

    rs = rs_arcsec*arctokpc

    s_crit = (C_v*C_v*cosmo.angular_diameter_distance(z_source)/(4.*np.pi*
            cosmo.angular_diameter_distance(z_nfw)*
            cosmo.angular_diameter_distance_z1z2(z_nfw, z_source))/(1000.0
                    *G_crit)).value # critical density

    rhos = kappa_s*s_crit/rs # rho_s

    de_c = rhos/J_c # delta_c

    c = fsolve(solve_c, 10.0, args=(de_c,))[0] # concentration

    r200 = c*rs # R_200

    m200 = 200.0*(4./3.*np.pi)*J_c*r200**3.0 # M_200

    if rt_arcsec is not None:
        tau = rt_arcsec/rs_arcsec
    else:
        tau = 2.0*c
    # if rt is given, calculate the tau
    # if rt is not given, set rt = 2.0*r_200, which means tau = 2.0*c

    m_t = m200*(tau*tau/(tau*tau + 1.0)**2.0)*((tau*tau - 1)*np.log(tau) +
            tau*np.pi - (tau*tau + 1))

    # m_t is the truncation mass.

    return m200, m_t, c, r200

cosmo = cosmology.LambdaCDM(H0=70.0, Om0=0.3, Ode0=0.7)
print(cosmo)
print(cosmo.critical_density(z=0.6))
C_v = 3 * 10 ** 5.  # light velocity [km/s]
H_l = (cosmo.H0).value  # Hubble constant
G_l = 4.302e-9  # Mpc M_sun^-1 (km/s) # Gravitational constnat
print(3.*H_l**2./(8.*np.pi*G_l)/10.**(9.))
G_crit = 4.302e-6  # kpc M_sun^-1 (km/s)^2 # Gravitational constant

z_source = 2.5
z_nfw = 0.6

s_crit = (C_v * C_v * cosmo.angular_diameter_distance(z_source) / (4. * np.pi *
                                                                   cosmo.angular_diameter_distance(z_nfw) *
                                                                   cosmo.angular_diameter_distance_z1z2(z_nfw,
                                                                                                        z_source)) / (
                      1000.0
                      * G_crit)).value

print(s_crit)
stop

mass_200, m_t, concentration, r200 = convert_to_physical_unit_tNFW(kappa_s=0.002, rs_arcsec=5.0, z_nfw=0.6, z_source=2.5, cosmo=cosmology.FlatLambdaCDM(H0=70.0, Om0=0.3), rt_arcsec=20.0)

print(mass_200, m_t, concentration, r200)
stop

mass_200, concentration = convert_to_physical_unit(kappa_s=0.002, rs_arcsec=1.0, z_nfw=0.6, z_source=2.5,
                                                   cosmo=cosmology.FlatLambdaCDM(H0=70.0, Om0=0.3)  )

print("{:.4e}".format(mass_200), concentration)

mass_200, concentration = convert_to_physical_unit_tNFW(kappa_s=0.002, rs_arcsec=30.0, z_nfw=0.6, z_source=2.5,
                                                   cosmo=cosmology.FlatLambdaCDM(H0=70.0, Om0=0.3)  )

print("{:.4e}".format(mass_200), concentration)

mass_200, concentration = convert_to_physical_unit_tNFW(kappa_s=0.00001, rs_arcsec=5.0, z_nfw=0.6, z_source=2.5,
                                                   cosmo=cosmology.FlatLambdaCDM(H0=70.0, Om0=0.3)  )

print("{:.4e}".format(mass_200), concentration)

mass_200, concentration = convert_to_physical_unit_tNFW(kappa_s=0.00001, rs_arcsec=1.0, z_nfw=0.6, z_source=2.5,
                                                   cosmo=cosmology.FlatLambdaCDM(H0=70.0, Om0=0.3)  )

print("{:.4e}".format(mass_200), concentration)

mass_200, concentration = convert_to_physical_unit_tNFW(kappa_s=0.00001, rs_arcsec=30.0, z_nfw=0.6, z_source=2.5,
                                                   cosmo=cosmology.FlatLambdaCDM(H0=70.0, Om0=0.3)  )

print("{:.4e}".format(mass_200), concentration)
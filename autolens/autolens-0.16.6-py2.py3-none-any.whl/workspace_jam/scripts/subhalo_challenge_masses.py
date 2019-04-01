from autofit import conf
import os

workspace_path = '{}/../'.format(os.path.dirname(os.path.realpath(__file__)))
conf.instance = conf.Config(config_path=workspace_path + 'config', output_path=workspace_path + 'output')

from autolens.model.profiles import mass_profiles as mp

nfw = mp.SphericalTruncatedNFWChallenge(kappa_s=0.009, scale_radius=1.079)

sigma_cr = 1940654909.4133248
cos_den = 262.30319684750657

mass = nfw.mass_at_200(critical_surface_mass_density_arcsec=sigma_cr, cosmic_average_mass_density_arcsec=cos_den)
print("{:.4e}".format(mass))

nfw = mp.SphericalTruncatedNFWChallenge(kappa_s=0.008, scale_radius=1.079)

sigma_cr = 1940654909.4133248
cos_den = 262.30319684750657

mass = nfw.mass_at_200(critical_surface_mass_density_arcsec=sigma_cr, cosmic_average_mass_density_arcsec=cos_den)
print("{:.4e}".format(mass))
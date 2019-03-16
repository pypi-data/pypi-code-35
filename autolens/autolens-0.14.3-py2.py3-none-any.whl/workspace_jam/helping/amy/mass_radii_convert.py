from autolens.data.array import grids
from autolens.model.profiles import mass_profiles as mp
from autolens.model.profiles.plotters import profile_plotters

import numpy as np

regular = grids.RegularGrid.from_shape_and_pixel_scale(shape=(100, 100), pixel_scale=0.05)

axis_ratio = 1.0

sie_02 = mp.EllipticalIsothermal(centre=(0.0, 0.0), einstein_radius=0.2, axis_ratio=1.0)
sie_04 = mp.EllipticalIsothermal(centre=(0.0, 0.0), einstein_radius=0.4, axis_ratio=1.0)
sie_06 = mp.EllipticalIsothermal(centre=(0.0, 0.0), einstein_radius=0.6, axis_ratio=1.0)
sie_08 = mp.EllipticalIsothermal(centre=(0.0, 0.0), einstein_radius=0.8, axis_ratio=1.0)
sie_10 = mp.EllipticalIsothermal(centre=(0.0, 0.0), einstein_radius=1.0, axis_ratio=1.0)

print(sie_02.angular_mass_within_circle(radius=sie_02.einstein_radius))
print(sie_04.angular_mass_within_circle(radius=sie_04.einstein_radius))
print(sie_06.angular_mass_within_circle(radius=sie_06.einstein_radius))
print(sie_08.angular_mass_within_circle(radius=sie_08.einstein_radius))
print(sie_10.angular_mass_within_circle(radius=sie_10.einstein_radius))
print()

print(sie_02.angular_mass_within_circle(radius=sie_02.einstein_radius) / 0.2)
print(sie_04.angular_mass_within_circle(radius=sie_04.einstein_radius) / 0.4)

sie_02_einstein_mass = sie_02.angular_mass_within_circle(sie_02.einstein_radius)
sie_04_einstein_mass = sie_04.angular_mass_within_circle(sie_04.einstein_radius)
sie_06_einstein_mass = sie_06.angular_mass_within_circle(sie_06.einstein_radius)
sie_08_einstein_mass = sie_08.angular_mass_within_circle(sie_08.einstein_radius)
sie_10_einstein_mass = sie_10.angular_mass_within_circle(sie_10.einstein_radius)

print()
print(sie_02_einstein_mass / 0.2)
print(sie_04_einstein_mass / 0.4)
print(sie_06_einstein_mass / 0.6)
print(sie_08_einstein_mass / 0.8)
print(sie_10_einstein_mass / 1.0)

nfw = mp.SphericalNFW(centre=(0.0, 0.0), kappa_s=0.2, scale_radius=8.0)

# profile_plotters.plot_surface_density(mass_profile=sis, grid=regular)

mass = sis.angular_mass_within_circle(radius=1.0)

print(sis.radius_where_average_convergence_in_circle_is_one)

radius = 0.8116039549729345

mass = nfw.angular_mass_within_circle(radius=radius)
area = np.pi * radius ** 2.0

print(mass / area)

print(nfw.radius_where_average_convergence_in_circle_is_one)
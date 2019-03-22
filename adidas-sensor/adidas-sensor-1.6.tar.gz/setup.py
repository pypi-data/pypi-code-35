from setuptools import setup


setup(
    name="adidas-sensor",
    version="1.6",
    description="Adidas Sensor Tool",
    author="Real Python",
    author_email="office@realpython.com",
    license="MIT",
    packages=["adidasSensor", "adidasSensor.serial"],
    include_package_data=True,
    install_requires=[
        "numpy>=1.15.4",
        "matplotlib>=3.0.2",
        "pandas>=0.23.4"
    ],
    entry_points={
        "console_scripts": [
            "adidas-sensor=adidasSensor.__main__:main",
            "adidas-sensor-plot=adidasSensor.plot:main",
            "adidas-sync-video=adidasSensor.sync:main"
        ]
    },
)

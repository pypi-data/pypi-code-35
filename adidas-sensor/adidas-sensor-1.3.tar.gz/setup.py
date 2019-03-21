from setuptools import setup


setup(
    name="adidas-sensor",
    version="1.3",
    description="Adidas Sensor Tool",
    author="Real Python",
    author_email="office@realpython.com",
    license="MIT",
    packages=["adidasSensor","adidasSensor.serial"],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "adidas-sensor=adidasSensor.__main__:main",
            "adidas-sensor-plot=adidasSensor.plot:main", 
        ]
    },
)
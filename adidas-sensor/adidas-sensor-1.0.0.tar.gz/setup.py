from setuptools import setup


setup(
    name="adidas-sensor",
    version="1.0.0",
    description="Adidas Sensor Tool",
    author="Real Python",
    author_email="office@realpython.com",
    license="MIT",
    packages=["adidasSensor"],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "adidas_sensor=adidasSensor.__main__:main",
        ]
    },
)
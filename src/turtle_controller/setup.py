from setuptools import find_packages, setup

package_name = 'turtle_controller'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='roar',
    maintainer_email='zeiadt43@gmail.com',
    description='TODO: Package description',
    license='MIT babiee',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': ['triangle = turtle_controller.triangle:main',
                            'parallelogram = turtle_controller.parallelogram:main',
                            'trapezoid = turtle_controller.trapezoid:main',
                            'sun= turtle_controller.sun:main',
                            'shapes=turtle_controller.shapes:main'
        ],
    },
)

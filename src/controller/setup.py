from setuptools import setup

package_name = 'controller'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    package_dir={'': 'src'},
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='vedant',
    maintainer_email='vedantchoudhary07@gmail.com',
    description='ODrive controller package',
    license='Apache License 2.0',
    # tests_require=['pytest'],
    extras_require={
        'test': ['pytest'],
    },
    entry_points={
        'console_scripts': [
            'odrive_control = controller.odrive_control:main',
        ],
    },
)
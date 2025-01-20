from setuptools import setup, find_packages
package_name = 'controller'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/config', ['config/impedance_params.yaml']),  # config 파일 추가
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='vedant',
    maintainer_email='vedantchoudhary07@gmail.com',
    description='ODrive controller package',
    license='Apache License 2.0',
    extras_require={
        'test': ['pytest'],
    },
    entry_points={
        'console_scripts': [
            'friction_compensation_node = controller.friction_compensation_node:main',
            'Impedance_Control = controller.impedance_control:main',
            'odrive_controller = controller.odrive_control:main',
        ],
    },
)
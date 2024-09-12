from setuptools import find_packages, setup

package_name = 'odrive_control_py'

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
    maintainer='vedant',
    maintainer_email='vedant@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'odrive_control_node = odrive_control_py.control_node:main',
            'trial_odrive_control_node = odrive_control_py.trial_controlnode:main',
            'record_data_node = odrive_control_py.record_odrive_data:main',
            'matlab_tcp_node = odrive_control_py.matlab_tcp_node:main',
        ],
    },
)

from setuptools import find_packages, setup

package_name = 'data_logging'

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
    maintainer_email='vedantchoudhary07@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    # tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'data_logging_goniometer = data_logging.data_recording_node:main',
            'data_logging_full = data_logging.data_recording_node_2:main',
            'recording_flag = data_logging.recording_flag_node:main',
        ],
    },
)

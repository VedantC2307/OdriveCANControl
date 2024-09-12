import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/vedant/gaitlab_ws/install/bag_recorder_nodes_py'

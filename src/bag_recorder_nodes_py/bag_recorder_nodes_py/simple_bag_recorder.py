import sqlite3
from rosidl_runtime_py.utilities import get_message
from rclpy.serialization import deserialize_message
import pandas as pd
import os

class BagFileParser():
    def __init__(self, bag_file):
        self.conn = sqlite3.connect(bag_file)
        self.cursor = self.conn.cursor()

        # Create a message type map
        topics_data = self.cursor.execute("SELECT id, name, type FROM topics").fetchall()
        self.topic_type = {name_of: type_of for id_of, name_of, type_of in topics_data}
        self.topic_id = {name_of: id_of for id_of, name_of, type_of in topics_data}
        self.topic_msg_message = {name_of: get_message(type_of) for id_of, name_of, type_of in topics_data}

    def __del__(self):
        self.conn.close()

    # Return [(timestamp0, message0), (timestamp1, message1), ...]
    def get_messages(self, topic_name):
        topic_id = self.topic_id[topic_name]
        # Get from the db
        rows = self.cursor.execute("SELECT timestamp, data FROM messages WHERE topic_id = {}".format(topic_id)).fetchall()
        # Deserialize all and timestamp them
        return [(timestamp, deserialize_message(data, self.topic_msg_message[topic_name])) for timestamp, data in rows]

def save_to_csv(messages, output_file):
    # Assuming messages are tuples of (timestamp, message)
    data = []
    for timestamp, msg in messages:
        data.append([
            timestamp, 
            msg.pos_estimate, 
            msg.vel_estimate, 
            msg.torque_target, 
            msg.torque_estimate, 
            msg.iq_setpoint, 
            msg.iq_measured, 
            msg.active_errors, 
            msg.axis_state, 
            msg.procedure_result, 
            msg.trajectory_done_flag
        ])
    
    # Define column names based on the actual fields
    df = pd.DataFrame(data, columns=[
        'timestamp', 
        'pos_estimate', 
        'vel_estimate', 
        'torque_target', 
        'torque_estimate', 
        'iq_setpoint', 
        'iq_measured', 
        'active_errors', 
        'axis_state', 
        'procedure_result', 
        'trajectory_done_flag'
    ])
    df.to_csv(output_file, index=False)

if __name__ == "__main__":
    # Path to the .db3 file and the output CSV file
    db3_file_path = os.path.expanduser('~/gaitlab_ws/bag_files/rosbag2_2024_08_22-12_20_42/rosbag2_2024_08_22-12_20_42_0.db3')
    csv_file_path = os.path.expanduser('~/gaitlab_ws/bag_files/controller1.csv')

    parser = BagFileParser(db3_file_path)

    # Change the topic name to the one you want to extract
    topic_name = '/odrive_axis0/controller_status'  # Update this with the actual topic name
    messages = parser.get_messages(topic_name)

    save_to_csv(messages, csv_file_path)

    print(f"Data saved to {csv_file_path}")
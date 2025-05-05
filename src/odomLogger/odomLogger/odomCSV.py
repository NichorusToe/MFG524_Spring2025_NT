import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
import csv
import os

class odomLogger(Node):
    def __init__(self):
        super().__init__('odomLogger')

	# Creates a subscriber for logging
        self.subscription = self.create_subscription(
            Odometry,
            '/odom',
            self.listenerCaller,
            10)

	# Saves to ~/turtlebot4_ws/logs/
        workspacePath = os.path.join(os.path.expanduser('~'), 'turtlebot4_ws')
        logDir = os.path.join(workspacePath, 'logs')
        os.makedirs(logDir, exist_ok=True)
        filePath = os.path.join(logDir, 'robotLog.csv')

        self.csv_file = open(filePath, 'w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(['Time (s)', 'X', 'Y', 'Z', 'Orientation_Z', 'Orientation_W']) # column names

        self.get_logger().info(f"Logging odometry to {filePath}") # prints if logs check

    def listenerCaller(self, msg):
	# Publisher for the subscriber
        time_now = self.get_clock().now().seconds_nanoseconds()[0]
        position = msg.pose.pose.position
        orientation = msg.pose.pose.orientation

        self.csv_writer.writerow([
            time_now,
            position.x,
            position.y,
            position.z,
            orientation.z,
            orientation.w
        ])
        self.get_logger().info(f'Logged position: x={position.x:.2f}, y={position.y:.2f}') # prints while logging check

    def destNode(self):
        self.csv_file.close()
        super().destNode()

def main(args=None):
    rclpy.init(args=args)
    logger = odomLogger()
    try:
        rclpy.spin(logger)
    except KeyboardInterrupt:
        logger.get_logger().info("Shutting down logger...")
    finally:
        logger.destNode()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

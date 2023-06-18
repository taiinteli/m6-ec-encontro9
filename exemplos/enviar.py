# Basic ROS 2 program to subscribe to real-time streaming
# video from your built-in webcam
# Author:
# - Addison Sears-Collins
# - https://automaticaddison.com
# Import the necessary libraries
import rclpy # Python library for ROS 2
from rclpy.node import Node # Handles the creation of nodes
from sensor_msgs.msg import Image # Image is the message type
from cv_bridge import CvBridge # Package to convert between ROS and OpenCV Images
import cv2 # OpenCV library
import httpx
import requests
# from ultralytics import YOLO
# model = YOLO("best.pt")
class ImageSubscriber(Node):
  """
  Create an ImageSubscriber class, which is a subclass of the Node class.
  """
  def __init__(self):
    """
    Class constructor to set up the node
    """
    # Initiate the Node class's constructor and give it a name
    super().__init__('image_subscriber')
    # Create the subscriber. This subscriber will receive an Image
    # from the video_frames topic. The queue size is 10 messages.
    self.subscription = self.create_subscription(
      Image,
      'video_frames',
      self.listener_callback,
      10)
    self.subscription # prevent unused variable warning
    # Used to convert between ROS and OpenCV images
    self.br = CvBridge()
  def listener_callback(self, data):
    """
    Callback function.
    """
    # Display the message on the console
    self.get_logger().info('Receiving video frame')
    # Convert ROS Image message to OpenCV image
    current_frame = self.br.imgmsg_to_cv2(data)
    # results = model(current_frame)
    # annotated_frame = results[0].plot()
    # Convert the frame to a byte array
    _, img_encoded = cv2.imencode('.png', current_frame)
    frame_data = img_encoded.tobytes()
    import requests
    url = "http://127.0.0.1:3000/upload"
    files=[
      ('content',('lala.png',frame_data,'image/png'))
    ]
    response = requests.request("POST", url, files=files)
    # Check the response status code
    if response.status_code == 200:
        print('Frame sent successfully!')
    else:
        print('Failed to send frame. Status code:', response.status_code)
    cv2.imshow("Camera", current_frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
      cv2.destroyAllWindows()
      return
def main(args=None):
  # Initialize the rclpy library
  rclpy.init(args=args)
  # Create the node
  image_subscriber = ImageSubscriber()
  # Spin the node so the callback function is called.
  rclpy.spin(image_subscriber)
  # Destroy the node explicitly
  # (optional - otherwise it will be done automatically
  # when the garbage collector destroys the node object)
  image_subscriber.destroy_node()
  # Shutdown the ROS client library for Python
  rclpy.shutdown()

  
if __name__ == '__main__':
  main()


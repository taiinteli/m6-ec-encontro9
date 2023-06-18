import rclpy # Biblioteca cliente Python para ROS 2
from rclpy.node import Node # Lida com a criação de nós
from sensor_msgs.msg import Image # Image é o tipo de mensagem
from cv_bridge import CvBridge # Pacote para converter entre imagens ROS e OpenCV
import cv2 # Biblioteca OpenCV

class ImagePublisher(Node):
  """
  Cria uma classe ImagePublisher, que é uma subclasse da classe Node.
  """
  def __init__(self):
    """
    Construtor da classe para configurar o nó
    """
    # Inicializa o construtor da classe Node e dá um nome a ele
    super().__init__('image_publisher')
      
    # Cria o publicador. Esse publicador vai publicar uma Image
    # no tópico 'video_frames'. O tamanho da fila é de 10 mensagens.
    self.publisher_ = self.create_publisher(Image, 'video_frames', 10)
      
    # Vamos publicar uma mensagem a cada 0.1 segundos
    timer_period = 0.1  # segundos
      
    # Cria o temporizador
    self.timer = self.create_timer(timer_period, self.timer_callback)
         
    self.cap = cv2.VideoCapture('./assets/siu.mp4')
         
    # Usado para converter imagens entre ROS e OpenCV
    self.br = CvBridge()
   
  def timer_callback(self):
    """
    Função de retorno de chamada.
    Essa função é chamada a cada 0.1 segundos.
    """
    # Captura o frame
    # Esse método retorna True/False e também o frame do vídeo.
    ret, frame = self.cap.read()
    
    if not ret:
      self.get_logger().info("O vídeo parece ter terminado. Reiniciando...")
      self.cap = cv2.VideoCapture('./assets/siu.mp4')
      return
          
    # Publica a imagem.
    # O método 'cv2_to_imgmsg' converte uma imagem OpenCV em uma mensagem de imagem ROS 2
    self.publisher_.publish(self.br.cv2_to_imgmsg(frame))
 
    # Exibe a mensagem no console
    self.get_logger().info('Publicando frame de vídeo')
  
def main(args=None):
  
  # Inicializa a biblioteca rclpy
  rclpy.init(args=args)
  
  # Cria o nó
  image_publisher = ImagePublisher()
  
  # Faz o nó rodar para que a função de retorno de chamada seja chamada.
  rclpy.spin(image_publisher)
  
  # Destroi explicitamente o nó
  # (opcional - caso contrário, será feito automaticamente
  # quando o coletor de lixo destruir o objeto do nó)
  image_publisher.destroy_node()
  
  # Encerra a biblioteca cliente ROS para Python
  rclpy.shutdown()
  
if __name__ == '__main__':
  main()






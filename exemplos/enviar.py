import rclpy # Biblioteca Python para ROS 2
from rclpy.node import Node # Lida com a criação dos nós
from sensor_msgs.msg import Image # Image é o tipo de mensagem
from cv_bridge import CvBridge # Pacote para converter entre Imagens ROS e OpenCV
import cv2 # Biblioteca OpenCV
import httpx
import requests

class ImageSubscriber(Node):
  """
  Cria uma classe ImageSubscriber, que é uma subclasse da classe Node.
  """
  def __init__(self):
    """
    Construtor da classe para configurar o nó
    """
    # Inicializa o construtor da classe Node e dá um nome a ele
    super().__init__('image_subscriber')
    # Cria o assinante. Esse assinante receberá uma Imagem
    # do tópico 'video_frames'. O tamanho da fila é de 10 mensagens.
    self.subscription = self.create_subscription(
      Image,
      'video_frames',
      self.listener_callback,
      10)
    self.subscription # evita um aviso de variável não utilizada
    # Usado para converter imagens entre ROS e OpenCV
    self.br = CvBridge()
  
  def listener_callback(self, data):
    """
    Função de retorno de chamada.
    """
    # Exibe a mensagem no console
    self.get_logger().info('Recebendo frame de vídeo')
    # Converte a mensagem de Imagem ROS para imagem OpenCV
    current_frame = self.br.imgmsg_to_cv2(data)
    # Realiza operações no frame, como detecção de objetos
    # results = model(current_frame)
    # annotated_frame = results[0].plot()
    # Converte o frame para um array de bytes
    _, img_encoded = cv2.imencode('.png', current_frame)
    frame_data = img_encoded.tobytes()
    import requests
    url = "http://127.0.0.1:3000/upload"
    files=[
      ('content',('lala.png',frame_data,'image/png'))
    ]
    response = requests.request("POST", url, files=files)
    # Verifica o código de status da resposta
    if response.status_code == 200:
        print('Frame enviado com sucesso!')
    else:
        print('Falha ao enviar o frame. Código de status:', response.status_code)
    # Exibe o frame na janela "Camera"
    cv2.imshow("Camera", current_frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
      cv2.destroyAllWindows()
      return

def main(args=None):
  # Inicializa a biblioteca rclpy
  rclpy.init(args=args)
  # Cria o nó
  image_subscriber = ImageSubscriber()
  # Faz o nó rodar para que a função de retorno de chamada seja chamada.
  rclpy.spin(image_subscriber)
  # Destroi explicitamente o nó
  # (opcional - caso contrário, será feito automaticamente
  # quando o coletor de lixo destruir o objeto do nó)
  image_subscriber.destroy_node()
  # Encerra a biblioteca cliente ROS para Python
  rclpy.shutdown()

if __name__ == '__main__':
  main()


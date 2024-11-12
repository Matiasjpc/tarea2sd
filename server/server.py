from concurrent import futures
import grpc
import orders_pb2
import orders_pb2_grpc
from kafka import KafkaProducer
from elasticsearch import Elasticsearch
import json
import datetime

class OrderService(orders_pb2_grpc.OrderServiceServicer):
    def __init__(self):
        # Configura el productor de Kafka
        self.producer = KafkaProducer(
            bootstrap_servers='localhost:9092',
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            retries=5,
            request_timeout_ms=10000
        )

        # Configura la conexión a Elasticsearch con autenticación
        self.es = Elasticsearch(
                "http://localhost:9200",
                basic_auth=("elastic", "matias")  # Asegúrate de usar solo cadenas de texto aquí
        )

       # Crear índice en Elasticsearch si no existe
        if not self.es.indices.exists(index="orders"):
            self.es.indices.create(index="orders")
            print("Created 'orders' index in Elasticsearch")

    def CreateOrder(self, request, context):
        print(f"Received order for product: {request.product_name}")
        order_data = {
            "product_name": request.product_name,
            "price": request.price,
            "payment_gateway": request.payment_gateway,
            "card_brand": request.card_brand,
            "bank": request.bank,
            "region": request.region,
            "address": request.address,
            "email": request.email,
            "status": "Procesando",
            "timestamp": datetime.datetime.now().isoformat()
        }

        # Enviar el mensaje a Kafka
        self.producer.send('order_events', order_data)
        print("Order sent to Kafka.")

        # Enviar el pedido a Elasticsearch
        self.es.index(index="orders", document=order_data)
        print("Order indexed in Elasticsearch.")

        return orders_pb2.OrderResponse(message="Order created", order_id=123)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    orders_pb2_grpc.add_OrderServiceServicer_to_server(OrderService(), server)
    server.add_insecure_port('[::]:50051')
    print("Server is running on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

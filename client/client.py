import sys
sys.path.insert(0, '../server')  # Asegurarse de que pueda importar orders_pb2 desde el servidor
import grpc
import orders_pb2
import orders_pb2_grpc

def run():
    # Configurar la conexión con el servidor gRPC
    print("Connecting to gRPC server...")
    channel = grpc.insecure_channel('localhost:50051')
    stub = orders_pb2_grpc.OrderServiceStub(channel)

    # Crear un pedido
    try:
        print("Attempting to create order...")
        response = stub.CreateOrder(orders_pb2.OrderRequest(
            product_name="Product A",
            price=10.0,
            payment_gateway="WebPay",
            card_brand="VISA",
            bank="BankX",
            region="RegionX",
            address="123 Main St",
            email="user@example.com"
        ))
        print("Order created:", response.message)
    except Exception as e:
        print("Error creating order:", e)
        return  # Terminar si ocurre un error en la creación

    # Actualizar el estado del pedido
    try:
        print("Attempting to update order status...")
        update_response = stub.UpdateOrderStatus(orders_pb2.OrderStatusUpdate(
            order_id=response.order_id,
            status="Enviado"
        ))
        print("Order updated:", update_response.message)
    except Exception as e:
        print("Error updating order status:", e)

if __name__ == '__main__':
    run()

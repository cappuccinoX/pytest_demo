import  grpc
import  helloworld_pb2
import  helloworld_pb2_grpc
from concurrent import futures
import  time
import os



class HelloWorldServicer(helloworld_pb2_grpc.GreeterServicer):
   def SayHello(self,request,context):
      '''客户端与服务端之间进行交互'''
      return helloworld_pb2.HelloReply(message='Hello {0}'.format(request.name))

def serve():
   server=grpc.server(futures.ThreadPoolExecutor(max_workers=os.cpu_count()))
   helloworld_pb2_grpc.add_GreeterServicer_to_server(HelloWorldServicer(),server)
   #指定服务端的测试地址信息
   server.add_insecure_port('[::]:50051')
   server.start()
   try:
      while True:
         time.sleep(60*60*24)
   except KeyboardInterrupt:
      server.stop(0)

if __name__ == '__main__':
   serve()
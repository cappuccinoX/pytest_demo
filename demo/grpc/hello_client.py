import grpc
import helloworld_pb2
import helloworld_pb2_grpc
import requests

def getData():
    r = requests.get(url="https://api.muxiaoguo.cn/api/QqInfo?qq=2839168630")
    return r.text

def run():
    # 连接服务端的程序
    channel = grpc.insecure_channel("localhost:50051")
    # 调用rcp服务
    stub = helloworld_pb2_grpc.GreeterStub(channel)
    r = stub.SayHello(helloworld_pb2.HelloRequest(name = getData()))
    print("'server response data:{0}".format(r.message))

if __name__ == "__main__":
    run()
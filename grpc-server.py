from concurrent import futures
import logging
import grpc
import grpc_pb2
import grpc_pb2_grpc
import io
from PIL import Image
import traceback
import base64

class Lab6GrpcServicer(grpc_pb2_grpc.Lab6GrpcServicer):
    def PerformAdd(self, request, context):
        sum = request.a + request.b
        return grpc_pb2.addReply(sum=sum)
    
    def ImageDimensions(self, request, context):
        # convert the data to a PIL image type so we can extract dimensions
        try:
            ioBuffer = io.BytesIO(request.img)
            img = Image.open(ioBuffer)
            return lab6_grpc_pb2.imageReply(width=img.size[0], height=img.size[1])
        except:
            traceback.print_exc()
            return grpc_pb2.imageReply(width=0, height=0)
    
    def PerformDotProduct(self, request, context):
        if (len(request.a) != len(request.b)):
            print('Length of the 2 list should be the same.')
            return grpc_pb2.dotProductReply(dotproduct=0)
    
        sum = 0
        for ind in range(len(request.a)):
            sum += request.a[ind]*request.b[ind]
        
        return grpc_pb2.dotProductReply(dotproduct=sum)
    
    def JsonImageDimensions(self, request, context):
        try:
            ioBuffer = io.BytesIO(base64.b64decode(request.img))
            img = Image.open(ioBuffer)
            return lab6_grpc_pb2.imageReply(width=img.size[0], height=img.size[1])
        except:
            traceback.print_exc()
            return grpc_pb2.imageReply(width=0, height=0)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    grpc_pb2_grpc.add_Lab6GrpcServicer_to_server(Lab6GrpcServicer(), server)
    server.add_insecure_port('[::]:5000')
    server.start()
    print("Server started, listening on 5000")
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
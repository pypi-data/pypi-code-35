import pickle

import grpc
import numpy
import os
from data_class_detection.parser.ast import ASTParser
from data_class_detection.parser.ast import compress
from data_class_detection.parser.sample import gen_samples
from data_class_detection.parser.sample import batch_samples
import tensorflow as tf
from tensorflow_serving.apis import predict_pb2, prediction_service_pb2_grpc

embed_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'embed.pkl')
node_map_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'node_map100.pkl')
with open(embed_path, 'rb') as fh:
    embeddings, embed_lookup = pickle.load(fh, encoding='bytes')
with open(node_map_path, 'rb') as fh:
    node_list, _, _, _ = pickle.load(fh)


def is_data_class(path):
    channel = grpc.insecure_channel("162.105.89.54:8503")
    stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)

    request = predict_pb2.PredictRequest()
    request.model_spec.name = 'data_class_detection'
    request.model_spec.signature_name = 'predict'

    ast = ASTParser(path)
    ast = compress(ast.tree)

    for nodes, children in batch_samples(gen_samples([ast], embeddings, embed_lookup, node_list), 1):
        node = numpy.array(nodes)
        child = numpy.array(children)
        request.inputs['tree'].CopyFrom(
            tf.contrib.util.make_tensor_proto(node, dtype=tf.float32))
        request.inputs['children'].CopyFrom(
            tf.contrib.util.make_tensor_proto(child, dtype=tf.int32))
        result_future = stub.Predict(request, 30.0)
        p = result_future.outputs['prediction'].float_val
    p = numpy.argmax(p)
    return p == 1


if __name__ == '__main__':
    print(is_data_class("1.java"))



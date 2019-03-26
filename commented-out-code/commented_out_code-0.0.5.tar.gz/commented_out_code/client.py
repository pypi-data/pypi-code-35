import collections
import threading
import grpc
import numpy
from tensorflow.contrib import learn
from tensorflow_serving.apis import prediction_service_pb2_grpc, predict_pb2
import tensorflow as tf
import os

hostport = "162.105.89.54:8502"

def finditer_with_line_numbers(pattern, string):
    '''
    A version of 're.finditer' that returns '(match, line_number)' pairs.
    '''
    import re

    matches = list(re.finditer(pattern, string, re.DOTALL | re.MULTILINE))
    if not matches:
        return []

    end = matches[-1].start()
    # -1 so a failed 'rfind' maps to the first line.
    newline_table = {-1: 0}
    for i, m in enumerate(re.finditer(r'\n', string), 1):
        # don't find newlines past our last match
        offset = m.start()
        if offset > end:
            break
        newline_table[offset] = i

    # Failing to find the newline is OK, -1 maps to 0.
    for m in matches:
        newline_offset = string.rfind('\n', 0, m.start())
        line_number = newline_table[newline_offset] + 1
        yield (m, line_number)


def find_comment(text):
    pattern = r'//.*?$|/\*.*?\*/'
    comment_list = []
    for m, lineno in finditer_with_line_numbers(pattern=pattern, string=text):
        comment_list.append((m.group(0), lineno))

    comment_content = []
    for comment, lineno in comment_list:
        comment = comment.strip()
        if comment.startswith('//'):
            while len(comment)>0 and comment[0] == '/':
                comment = comment[1:].strip()
            if len(comment)>0:
                comment_content.append((comment, lineno))
        else:
            _comments = comment[2:-2]
            _comments = _comments.splitlines()
            k = lineno
            for com in _comments:
                com = com.strip()
                if len(com) > 0:
                    comment_content.append((com, k))
                k += 1

    return comment_content


def _callback1(_condition, predictions, comment, lineno):

    def callback(result_future):
        with _condition:
            predictions.append((result_future.result().outputs['prediction'].int64_val, comment, lineno))
            _condition.notify()
    return callback


def tokenizer(text):
    return [x for x in text]


def cpp(text):
    comment_lineno = find_comment(text)

    vocab_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'vocab')
    vocab_processor = learn.preprocessing.VocabularyProcessor.restore(vocab_path)

    channel = grpc.insecure_channel(hostport)
    stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)
    _condition = threading.Condition()
    _condition.acquire()

    predictions = []
    dropout_keep_prob = 1.0
    for comment, lineno in comment_lineno:
        input_x = numpy.array(list(vocab_processor.transform([comment])))
        request = predict_pb2.PredictRequest()
        request.model_spec.name = 'dead_comment_detection'
        request.model_spec.signature_name = 'predict'
        request.inputs['input_x'].CopyFrom(
            tf.contrib.util.make_tensor_proto(input_x))
        request.inputs["dropout_keep_prob"].CopyFrom(
            tf.contrib.util.make_tensor_proto(dropout_keep_prob, dtype=tf.float32))

        result_future = stub.Predict.future(request, 5.0)  # 5 seconds
        result_future.add_done_callback(_callback1(_condition, predictions, comment, lineno))

    with _condition:
        while len(predictions) != len(comment_lineno):
            _condition.wait()

    commented_out_code = {lineno: comment for predictions, comment, lineno in predictions if predictions[0] == 1}
    commented_out_code = collections.OrderedDict(sorted(commented_out_code.items()))
    return commented_out_code


def search(text, lang):
    if lang == 'cpp':
        return cpp(text)
    else:
        raise Exception("only support c/c++ language")

import boto3
def get_backlog(queueURL):
    sqs = boto3.client('sqs')
    qa = sqs.get_queue_attributes(QueueUrl=queueURL)
    print(qa)
    return qa["ApproximateNumberOfMessages"]
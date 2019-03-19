

class SubTopicCache(object):

    def __init__(self):
        self.topicMap = dict()

    def exists(self, topic):
        return topic in self.topicMap

    def put(self, topic):
        self.topicMap[topic] = ''

    def clean(self):
        self.topicMap.clear()
from pykson import JsonObject, Pykson, IntegerField, StringField, ObjectListField, ListField, DateField, DateTimeField, TimestampSecondsField, ObjectField

#
# class Score(JsonObject):
#     score = IntegerField()
#     course = StringField()
#
#     def __str__(self):
#         return str(self.course) + ": " + str(self.score)
#
#
# class Student(JsonObject):
#
#     first_name = StringField(serialized_name="fn")
#     last_name = StringField()
#     age = IntegerField()
#     birth = DateField(serialized_name='b')
#     birth_time = TimestampSecondsField(serialized_name='bt')
#     # scores = ListField(int)
#     # scores = ObjectListField(Score)
#     score = Score()
#
#     def __str__(self):
#         return "first name:" + str(self.first_name) + ", last name: " + str(self.last_name) + ", birth: " + str(self.birth_time) + ", age: " + str(self.age) + ", score: " + str(self.score)
#
#
# # print(JsonObject.get_fields(Student))
#
#
# # json_text = '{"fn":"ali", "last_name":"soltani", "age": 25, "scores": [ 20, 19]}'
# # json_text = '{"fn":"ali", "last_name":"soltani", "b":"2015-10-21", "bt": 1553717064, "age": 25, "scores": [ {"course": "algebra", "score": 20}, {"course": "statistics", "score": 19} ]}'
# json_text = '{"fn":"ali", "last_name":"soltani", "b":"2015-10-21", "bt": 1553717064, "age": 25, "score": {"course": "algebra", "score": 20}}'
# item = Pykson.from_json(json_text, Student)
#
# print(item)
# print(type(item))
#
# print(Pykson.to_json(item))




# from pykson import Pykson, JsonObject, IntegerField, StringField, ObjectField


class Score(JsonObject):
    score = IntegerField(serialized_name='s')
    course = StringField(serialized_name='c')


class Student(JsonObject):

    first_name = StringField(serialized_name="fn")
    last_name = StringField(serialized_name="ln")
    age = IntegerField(serialized_name="a")
    score = ObjectField(Score, serialized_name="s")


json_text = '{"fn":"John", "ln":"Smith", "a": 25, "s": {"s": 100, "c":"Algebra"}}'
student = Pykson.from_json(json_text, Student)
print(Pykson.to_json(student))
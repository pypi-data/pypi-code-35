import math


class DynamicObjectData:
    """
        Root object of Dynamic Object Data
        Attributes:
            start_time  script starting time
            end_time    script ending time
            collections list of trajectories collection
    """
    def __init__(self, start_time, end_time, collections):
        self.start_time = start_time
        self.end_time = end_time
        self.collections = collections

    @staticmethod
    def from_json(data):
        return DynamicObjectData(data['start_time'],
                                 data['end_time'],
                                 list(map(lambda json: TrajectoriesCollection.from_json(json), data['trajectory_collections'])))


class TrajectoriesCollection:
    """A TrajectoriesCollection contain tracking of related objects

           Attributes:
               objects  script starting time
               coordinate_system    coordinate system
    """
    def __init__(self, coordinate_system, objects):

        self.coordinate_system = coordinate_system
        self.objects = objects

    @staticmethod
    def from_json(json_data):
        return TrajectoriesCollection(json_data['coordinate_system'],
            map(lambda json_object: Object.from_json(json_object), json_data['objects']))


class Object:
    """A TrajectoriesCollection contain tracking of related objects

               Attributes:
                   id  object unique id
                   states    list of object states in time series
    """
    def __init__(self, id, states):
        self.id = id
        self.states = states

    @staticmethod
    def from_json(json_data):
        return Object(json_data['id'], list(map(lambda json_states: State.from_json(json_states), json_data['states'])))

    def get_moving_distance(self):
        """Get the total distance that this object moves"""
        distances = 0.0
        from_state = self.states[0]

        for i in range(1, len(self.states)):
            to_state = self.states[i];
            distances += Point3.distance(from_state.center, self.states[i].center)
            from_state = to_state
        return distances


class State:
    """A State contain object information at a certain time.

                   Attributes:
                       shape  the shape type (e.g. cuboid)
                       size    object size box
                       orientation
                       center
                       velocity
                       acceleration
                       timestamp_ns timestamp of this state.
        """

    def __init__(self, shape, size, orientation, center, velocity, acceleration, timestamp_ns):
        self.shape = shape
        self.size = size
        self.orientation = orientation
        self.center = center
        self.velocity = velocity
        self.acceleration = acceleration
        self.timestamp_ns = timestamp_ns

    @staticmethod
    def from_json(json_data):
        return State(
            shape=json_data['shape'],
            size=Point3.from_json(json_data['size']),
            orientation=Orientation.from_json((json_data['orientation'])),
            center=Point3.from_json((json_data['center'])),
            acceleration=Point3.from_json((json_data['acceleration'])),
            velocity=Point3.from_json((json_data['velocity'])),
            timestamp_ns=json_data['timestamp_ns']
        )


class Point3:
    """
        3d point (x, y, z)
    """
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z

    @staticmethod
    def from_json(json_data):
        return Point3(json_data['x'], json_data['y'], json_data['z'])

    @staticmethod
    def distance(p1, p2):
        return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2 + (p1.z - p2.z)**2)


class Orientation:
        """ Orientation to apply Quaternion (x, y, z, w)
        """
        def __init__(self, x, y, z, w):
            self.x = x
            self.y = y
            self.z = z
            self.w = w

        @staticmethod
        def from_json(json_data):
            return Orientation(json_data['x'], json_data['y'], json_data['z'], json_data['w'])
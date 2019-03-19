"""Module for working with Adams Drill Hole (.hol) files
"""
class DrillHole():
    _SCALAR_PARAMETERS = [
        'File_Type',
        'File_Version',
        'Length',
        'Mass',
        'Angle',
        'Time'
    ]

    _DEFAULT_PARAMETER_SCALARS = {
        'File_Type': 'event',
        'File_Version': 1.0,
        'Length': 'foot',
        'Mass': 'pound_mass',
        'Angle': 'degrees',
        'Time': 'seconds'
    }

    _ARRAY_PARAMETERS = [
        'Centerline',
        'Diameter'
    ]

    _DEFAULT_PARAMETER_ARRAYS = {
        'Centerline': ((), (), ()),
        'Diameter': ((), ()),
        'Wall_Contact': ((-1,), (1e6,), (1e3)),
        'Wall_Friction': ((), (), (), (), ())
    }
    
    def __init__(self, hole_name, **kwargs):
        self.parameters = kwargs
        self.parameters['Hole_Name'] = hole_name
        
        self._apply_defaults()

        self.filename = ''
        
    def _apply_defaults(self):
        """
        Applies defaults from class variables
        """
        # Applies normal parameter defaults
        for scalar_parameter, value in self._DEFAULT_PARAMETER_SCALARS.items():
            if scalar_parameter not in self.parameters:
                self.parameters[scalar_parameter] = value

        # Applies defaults to all ramp parameters
        for array_parameter, array in self._DEFAULT_PARAMETER_ARRAYS.items():
            self.parameters[array_parameter] = [list(tup) for tup in array]
            self.parameters['_' + array_parameter] = zip(*self.parameters[array_parameter])
    
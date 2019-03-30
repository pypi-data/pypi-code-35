import numpy as np
class particle:
    """Short summary.

    Parameters
    ----------
    *args : any types
        Catch-all for parameters which are not defined but passed into the
        particle class
    **kwargs :
        dimensions : int
            number of dimensions that the particle can move along
        upper_bounds : list or 1-D array of float or int elements
            upper limit to dimensions (this is used to create the starting
            position for the particle establishes the ceiling)
        lower_bounds : list or 1-D array of float or int elements
            lower_bounds limit to dimensions (this is used to create the starting
            position for the particle establishes the floor)
        record : True or False
            if True it initializes a recording attribute dictionary for the
            particle's position and fitness values as the particle updates
            position
        shift : float, int
            scaling factor for bounds. Only applied when bounding limits are not
            specified
    Attributes
    ----------
    __initialize_position__ :
        initializes particle with position, value, best value and best position.
        Description of attribute `__initialize_position__`.
    __record__ :
        initializes recorder attribute

    Methods
    ----------
    move :
        updates particle position based on a given velocity and optional weight
        component
    """
    def __init__(self,*args,**kwargs):

        dimensions          = kwargs.get('dimensions',  None)
        upper_bounds        = kwargs.get('upper_bounds',None)
        lower_bounds        = kwargs.get('lower_bounds',None)
        record              = kwargs.get('record',      False)
        shift               = kwargs.get('shift',       None)

        if dimensions == None:
            print('ERROR: No dimensions given. '+
                  'Cannot initialize particle.')
            return
        elif upper_bounds == None and lower_bounds == None:
            self.__initialize_position__(0,dimensions,shift=shift)
        elif upper_bounds != None and lower_bounds != None:
            self.__initialize_position__(1,dimensions,lower_bounds,upper_bounds)
        elif upper_bounds != None:
            self.__initialize_position__(2,dimensions,upper_bounds,shift=shift)
        elif lower_bounds != None:
            self.__initialize_position__(3,dimensions,lower_bounds,shift=shift)
        else:
            pass

        if record:
            self.__record__()
            self.history['position'].append(self.position)
            self.history['value'].append(self.pbest_value)
        else:
            pass

        return

    def __record__(self):
        """Initializes a recorder for the particle's position. This recorder can
        be updated as the particle changes its position.

        Parameters
        ----------
        **Only initialized if the "record" boolean is True during particle
          initialization

        Returns
        -------
        particle attribute (particle.history)
            Dict object containing 'position' and 'value' data as the particle
            is updated.

        """
        self.history  = { 'position':    [],
                             'value':    []}
        return

    def __initialize_position__(self,case,dimensions,*args,**kwargs):
        self.pbest_value   = float('inf')
        self.current_value = float('inf')
        self.pvelocity     = np.zeros((1,dimensions))
        self.position      = np.zeros((1,dimensions))
        if case == 1:
            for limit in range(dimensions):
                self.position[0,limit] = np.random.uniform(low=float(args[0][limit]),
                                                           high=float(args[1][limit]))
        elif case == 0:
            try:
                shift = kwargs.get('shift',1)
                lower_bound = -1*shift
                upper_bound = 1*shift
            except:
                lower_bound = -1
                upper_bound = 1
            self.position = np.random.uniform(size=(1,dimensions),low=lower_bound,
                                              high=upper_bound)
        elif case == 2:
            try:
                shift = kwargs.get('shift')
            except:
                shift = 2
            try:
                lower_bounds = [bound - shift*abs(bound) for bound in args[0]]
                print(lower_bounds)
            except:
                print('ERROR: shift must be float or int type.')
                return
            for limit in range(dimensions):
                self.position[0,limit] = np.random.uniform(low=lower_bounds[limit],
                                                           high=float(args[0][limit]))
        elif case == 3:
            try:
                shift = kwargs.get('shift')
            except:
                shift = 2
            try:
                upper_bounds = [shift*abs(bound)+bound for bound in args[0]]
            except:
                print('ERROR: shift must be float or int type.')
                return
            for limit in range(dimensions):
                self.position[0,limit] = np.random.uniform(low=float(args[0][limit]),
                                                           high=upper_bounds[limit])
        else:
          pass
        self.pbest_position = self.position

    def __exclaim__(self):
        """Declares a particle's position and current value with reference to the
        cost function being optimized.

        Parameters
        ----------

        No inputs

        Returns
        -------
        string
            Prints the current
            'Particle at position: (N-dimensional position) with value (particle fitness).

        """
        print('Particle at position: ', self.position,' with value ',
              self.current_value)


    def move(self,velocity,**kwargs):
        """Moves particle to a new position based upon the given input velocity and
        the particle's current position.

        Parameters
        ----------
        velocity : float, int
            Amount of displacement from the current position.

        weight (optional) : float, int

        Returns
        -------
        type
            Description of returned object.

        """
        weight = kwargs.get('weight',0.5)
        self.position = self.position + weight*velocity
        try:
            self.history['position'].append(self.position)
        except:
            pass

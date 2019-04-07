# -*- coding: utf-8 -*-
"""
Created on Sat Dec 29 08:27:01 2018

@author: yoelr
"""
from .utils import dim
from .unit_registry import Quantity
from .unit_manager import UnitManager
from .exceptions import BookkeepWarning
from numpy import asarray, ndarray
from warnings import warn

class SmartBook(dict):
    """Create a dictionary that represents values with units of measure and alerts when setting an item out of bounds. Bounds are always inclusive.
    
    **Parameters**
    
        **units:** [UnitManager or dict] Dictionary of units of measure.
        
        **bounds:** [dict] Dictionary of bounds.
        
        ***args:** Key-value pairs to initialize.
        
        **source:** [str] Should be one of the following [-]:
            * Short description of the smartbook.
            * Object which the smartbook belongs to.
            * None
        
        ****kwargs:** Key-value pairs to initialize.
    
    **Class Attribute**
    
        **Quantity:** `pint Quantity <https://pint.readthedocs.io/en/latest/>`__ class for compatibility.
    
    **Examples**
    
    SmartBook objects provide an easy way to keep track of units of measure and enforce bounds.
    
        Create a SmartBook object with *units*, *bounds*, a *source* description, and *arguments* to initialize the dictionary:
         
        >>> sb = SmartBook(units={'T': 'K', 'Duty': 'kJ/hr'},
        ...                bounds={'T': (0, 1000)},
        ...                source='Operating conditions',
        ...                T=350)
        >>> sb
        {'T': 350 (K)}
        
        The *units* attribute becomes a :doc:`UnitManager` object with a reference to all dictionaries (*clients*) it controls. These include the SmartBook and its bounds.
    
        >>> sb.units
        UnitManager:
        {'T': 'K',
         'Duty': 'kJ/hr'}
        >>> sb.units.clients
        [{'T': 350 (K)}, {'T': (0, 1000)}]
        
        Change units:
         
        >>> sb.units['T'] = 'degC'
        >>> sb
        {'T': 76.85 (degC)}
        >>> sb.bounds
        {'T': array([ -273.15, 726.85])}
        
        Add items:
            
        >>> sb['P'] = 101325
        >>> sb
        {'T': 76.85 (degC),
         'P': 101325}
            
        Add units:
            
        >>> sb.units['P'] = 'Pa'
        >>> sb
        {'T': 76.85 (degC),
         'P': 101325 (Pa)}
             
        A BookkeepWarning is issued when a value is set out of bounds:
            
        >>> sb['T'] = -300
        __main__:1: BookkeepWarning: @Operating conditions: T (-300 degC) is out of bounds (-273.15 to 726.85 degC).
        
    Nested SmartBook objects are easy to read, and can be made using the same units and bounds.
    
        Create new SmartBook objects:
        
        >>> sb1 = SmartBook(sb.units, sb.bounds,
        ...                 T=25, P=500)
        >>> sb2 = SmartBook(sb.units, sb.bounds,
        ...                 T=50, Duty=50)
        >>> sb1
        {'T': 25 (degC),
         'P': 500 (Pa)}
        >>> sb2
        {'T': 50 (degC),
         'Duty': 50 (kJ/hr)})
            
        Create a nested SmartBook object:
            
        >>> nsb = SmartBook(units=sb.units, sb1=sb1, sb2=sb2)
        {'sb1':
            {'T': 25 (degC),
             'P': 500 (Pa)},
         'sb2':
            {'T': 50 (degC),
             'Duty': 50 (kg/hr)}}
    
    `pint Quantity <https://pint.readthedocs.io/en/latest/>`__ objects are also compatible, so long as the corresponding Quantity class is set as the Quantity attribute.
    
        Set a Quantity object:
            
        >>> Q_ = SmartBook.Quantity
        >>> sb1.bounds['T'] = Q_((0, 1000), 'K')
        >>> sb1['T'] = Q_(100, 'K')
        >>> sb1
        {'T': -173.15 degC,
         'P': 500 (Pa)}
        
        Setting a Quantity object out of bounds will issue a warning:
            
        >>> sb1['T'] = Q_(-1, 'K')
         __main__:1: BookkeepWarning: T (-274.15 degC) is out of bounds (-273.15 to 726.85 degC).
        
        Trying to set a Quantity object with wrong dimensions will raise an error:
            
        >>> Q_ = SmartBook.Quantity    
        >>> sb1['T'] = Q_(100, 'meter')
        DimensionalityError: Cannot convert from 'meter' ([length]) to 'degC' ([temperature])
    
    .. Note:: Numpy arrays are also compatible with bounds checking. Give it a shot!
    
    """
    __slots__ = ('_source' ,'_units', '_bounds')
    
    Quantity = Quantity
    Warning = BookkeepWarning
    
    def __init__(self, units={}, bounds={}, *args,
                 source=None, **kwargs):
        # Make sure units is a UnitManager and add clients
        if isinstance(units, UnitManager):
            clients = units.clients
            clients.append(self)
        else:
            units = UnitManager([self], **units)
            clients = units.clients                
        if bounds not in clients:
            clients.append(bounds)
        
        # Set all attributes and items
        self._units = units
        self._bounds = bounds
        self._source = source
        super().__init__(*args, **kwargs)
        
        # Make sure bounds are arrays for boundscheck
        for key, value in bounds.items():
            bounds[key] = asarray(bounds[key])
        
        # Check values
        for key, value in self.items():
            self.unitscheck(key, value)
            self.boundscheck(key, value)
    
    def __setitem__(self, key, value):
        self.unitscheck(key, value)
        self.boundscheck(key, value)
        dict.__setitem__(self, key, value)
    
    @classmethod
    def _checkbounds(cls, key, value, units, bounds,
                     stacklevel, source):
        """A lower level, functional version of "boundscheck". Return True if value within bounds. Return False if value is out of bounds and issue a warning.
        
        **Parameters**
        
            **key:** [str] Name of value
            
            **value:** [number, Quantity, or array]
            
            **units:** [str] Units of measure
            
            **bounds:** [array or Quantity-array] Lower and upper bounds
            
            **stacklevel:** [int] Stacklevel for warning.
        
            **source:** [str or object] Short description or object it describes.
        
        **Example**
        
            >>> SmartBook._checkbounds('Temperature', -1, 'Kelvin', (0, 1000), (True, True), 2, 'Thermocouple')
            False
        
        """
        # Include bound limits for inclusive values
        lb, ub = bounds
        try: within_bounds = (lb<=value).all() and (ub>=value).all()
        # Handle exception when value or bounds is a Quantity object but the other is not
        except ValueError as VE:
            Q_ = cls.Quantity
            value_is_Q = isinstance(value, Q_)
            bounds_is_Q = isinstance(bounds, Q_)
            if value_is_Q and not bounds_is_Q:           
                value.ito(units)
                value = value.magnitude
                is_Q = 'value'
                not_Q = 'bounds'                        
            elif bounds_is_Q and not value_is_Q:
                bounds.ito(units)
                bounds = bounds.magnitude
                is_Q = 'bounds'
                not_Q = 'value'
            else: raise VE
            # Warn to prevent bad usage of SmartBook
            name = "'" + key + "'" if isinstance(key, str) else key
            msg = f"For key, {name}, {is_Q} is a Quantity object, while {not_Q} is not."
            warn(cls._warning(source, msg, RuntimeWarning),
                 stacklevel=stacklevel)
            # Try again recursively
            return cls._checkbounds(key, value, units, bounds,
                                    stacklevel+1, source)
        
        # Handle exception when bounds is not an array
        except AttributeError as AE:
            if not isinstance(bounds, ndarray):
                # Warn to prevent bad usage of SmartBook
                name = f"'{key}'" if isinstance(key, str) else key
                msg = f"For key, {name}, bounds should be an array, not {type(bounds).__name__}."
                warn(cls._warning(source, msg, RuntimeWarning),
                     stacklevel=stacklevel)
                # Try again recursively
                return cls._checkbounds(key, value, units, asarray(bounds),
                                        stacklevel+1, source)
            else:
                raise AE
                
        # Warn when value is out of bounds
        if not within_bounds:
            units = ' ' + units
            try:
                msg = f"{key} ({value:.4g}{units}) is out of bounds ({lb:.4g} to {ub:.4g}{units})."
            except:  # Handle format errors
                msg = f"{key} ({value:.4g}{units}) is out of bounds ({lb} to {ub} {units})."
            
            warn(cls._warning(source, msg, cls.Warning),
                              stacklevel=stacklevel)
        
        return within_bounds
    
    def unitscheck(self, key, value):
        """Adjust Quantity objects to correct units and return True."""
        if isinstance(value, self.Quantity):
            units = self._units.get(key, '')
            value.ito(units)
        return True
    
    def boundscheck(self, key, value):
        """Return True if value is within bounds. Return False if value is out of bounds and issue a warning.
        
        **Parameters**
        
            **key:** [str] Name of value
            
            **value:** [number, Quantity, or array]
            
        """
        bounds = self._bounds.get(key)
        stacklevel = 4
        source = self._source
        units = self._units.get(key, '')
        if bounds is None:
            within_bounds = True
        else:
            within_bounds = self._checkbounds(key, value, units, bounds,
                                              stacklevel, source)
        
        return within_bounds
    
    @classmethod
    def enforce_boundscheck(cls, val):
        """If *val* is True, issue RuntimeWarning whenever an item is set out of bounds. If *val* is False, ignore bounds."""
        if val: cls.boundscheck = cls._boundscheck
        else: cls.boundscheck = cls._boundsignore

    @classmethod
    def enforce_unitscheck(cls, val):
        """If *val* is True, adjust Quantity objects to correct units. If *val* is False, ignore units."""
        if val: cls.unitscheck = cls._unitscheck
        else: cls.unitscheck = cls._unitsignore
     
    _boundscheck = boundscheck
    _unitscheck = unitscheck
    def _boundsignore(*args, **kwargs): pass
    def _unitsignore(*args, **kwargs): pass    

    @property
    def units(self):
        """Dictionary of units of measure."""
        return self._units
    
    @property
    def bounds(self):
        """Dictionary of bounds."""
        return self._bounds
    
    @property
    def source(self):
        """Short description or object it describes"""
        return self._source
        
    def nested_keys(self):
        """Return all keys of self and nested SmartBook objects."""
        yield from self._nested_keys([self], isinstance)
        
    def _nested_keys(self, prev, inst):
        for key, val in self.items():
            if inst(val, SmartBook) and not val in prev:
                if val:
                    prev.append(val)
                    yield from val._nested_keys(prev, inst)
                    prev.remove(val)
            else: yield key
    
    def nested_values(self):
        """Return all values of self and nested SmartBook objects."""
        yield from self._nested_values([self], isinstance)
        
    def _nested_values(self, prev, inst):
        for key, val in self.items():
            if inst(val, SmartBook) and not val in prev:
                if val:
                    prev.append(val)
                    yield from val._nested_values(prev, inst)
                    prev.remove(val)
            else: yield val
    
    def nested_items(self):
        """Return all key-value pairs of self and nested SmartBook objects."""
        yield from self._nested_items([self], isinstance)
            
    def _nested_items(self, prev, inst):
        """Return all key-value pairs of self and nested SmartBook objects."""
        for key, val in self.items():
            if inst(val, SmartBook) and not val in prev:
                if val:
                    prev.append(val)
                    yield from val._nested_items(prev, inst)
                    prev.remove(val)
            else: yield key, val    
    
    @staticmethod
    def _warning(source, msg, category=Warning):
        """Return a Warning object with source description."""
        if isinstance(source, str):
            msg = f'@{source}: ' + msg
        elif source:
            msg = f'@{type(source).__name__} {str(source)}: ' + msg
        return category(msg)
    
    def show(self, depth=1):
        """Print representation with specified *depth*.
        
        **Parameters**
        
            **depth:** [int] Number of nested dictionaries represented.
        
        """
        print(self._info([], 0, depth))
    
    def __repr__(self):
        return self._info()
    
    def _info(self, previous_dicts=[], N_recursive=0, depth=1):
        """Return representation of self recursively.
        
        **Parameters**

            **previous_dicts:** List of dictionaries that self is nested in.
        
            **N_recursive:** Current number of SmartBook recursions.
            
            **depth:** Maximum allowable recursions.
        
        """
        if depth < 0:
            raise ValueError(f'depth must be 0 or higher, not {depth}.')
        add_line = self._info_item
        udict = self._units
        out = ''
        
        N_spaces = 4*(N_recursive)
        if N_recursive == 0:
            new_line = ''
        elif N_recursive < depth+1:
            new_line = '\n' + N_spaces*' '
        else:
            return f'<{type(self).__name__}>,\n '
        N_recursive += 1
        
        if self:
            # Log self to prevent infinite recursion later
            previous_dicts.append(self)
            
            # Add lines of key-value pairs
            out += new_line + '{'
            for key, value in self.items():
                units = udict.get(key, '')
                out += add_line(key, value, units, previous_dicts, N_recursive, depth)
            out = out[:-(4*N_recursive - 1)] + '},\n '
            
            # Log out self
            del previous_dicts[-1]
        else:
            out += new_line + '{},\n '
        
        if N_recursive == 1:
            return out[:-4] + '}'
        else:
            return out
    
    def _info_item(self, key, value, units, previous_dicts, N_recursive, depth):
        """Represent key-value pair recursively."""
        Q_ = self.Quantity
        out = f"'{key}': "
        
        if isinstance(value, dict):
            if value in previous_dicts:
                # Prevent infinite recursion
                out += "{...},\n "
            elif value and isinstance(value, SmartBook):
                # Pretty representation of inner smart book
                out += value._info(previous_dicts, N_recursive, depth)
            else:
                # Normal representation of dictionaries
                out += repr(value) + ',\n '
        else:
            if units:
                if isinstance(value, Q_):
                    value.ito(units)
                    value = value.magnitude
                    units = ' ' + units
                else:
                    units = dim(' (' + units + ')')
            
            try:
                out += f"{value:.3g}{units},\n "
            except:  # Values may not have g-format
                out += f"{repr(value)}{units},\n "
        
        # Include spaces for next line
        out += 4*(N_recursive - 1)*' '
        return out
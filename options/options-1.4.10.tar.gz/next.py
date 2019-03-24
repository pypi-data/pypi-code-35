

"""
Rough outline of what next gen options might look like
"""

from options import *

class DoesStuff(OptionsClass):
    options = Options(
       one = 1,
       two = 'two',
       tree = 'xyz'
    )

    @init_options
    def __init__(self, opts):

        self.options = self.__class__.options.push(kwargs)
        # from show:
        # self.options = self.opts = Show.options.push(kwargs)
        # not clear that self.opts is all that useful



    @method_options
    def stuff(self, opts):
        pass
        # takes same params as instance
        # no need for:
        # opts = self.opts = self.options.push(kwargs)
        # also, instance vars not set by default; though above
        # shows a sly thing - it isn't self.options being set, but
        # self.opts


    @method_options(four=4)
    def things(self, opts):
        print(opts.one + opts.four)
        # takes same options as instance, plus four

    # returns a function that
    # 1. takes kwargs
    # 2. checks the resulting function for method-level attributes
    #    (really the decorated function, not the innermost)
    #    and, if present, pushes an options layer over the instance options
    # 3. pushes the kwargs (call args) over the method / instance options
    # 4. invokes the function passing call options via opts variable

    @method_options
    def buff(self, value, opts):
        # takes same options as instance, plus local value

        # note, method is itself implicitly in the option chain

        # class
        # instance
        # method
        # method call

        # for efficiency, perhaps don't add ChainMap layer for method
        # if method doesn't add its own options

        # probably need a generic callable_hasattr, callable_setattr,
        # callable_getattr set of functions


class Other(OptionsClass):

    options = Options(
        spork = 'like a fork',
        spife = 'like a knife',
    )

    @init_options
    def __init__(self, opts):
        self.options = Other.options.push(**kwargs) # or impicit?
        self.ds = DoesStuff()
        # in the init, is opts == self.options or self.opts ?

    @method_options
    def things(self, opts):
        self.ds(opts=opts)


"""
One of the great complexities is that traditional
global, module, class, and instance variables still
exist and are useable. As are function / method arguments
unrelated to options, including even *args and **kwargs

Most often, options are the ones that should be used.
But not always.
"""

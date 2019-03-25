""" Recalls the method or class property used as an input parameter by the calling frame"""
import inspect
import re


def arcane_recall(calling_frame, target_argument_pos=0):
    """
    This is some super sneaky shit.

    And I know!  I know!  "You're not supposed to mess with the stack, it's a bad idea, there be dragons!!!"

    Blah blah blah.

    Look!  If you're not willing to push some limits while being as mindful as you can be, you're never going
    to get ahead in life.  You already know this, so stop being such a baby!  We have frontiers to cross and
    dragons to slay!

    With that said, here's what I'm doing (currently).

    Let's say that you're calling a method which is taking another method as an input parameter.

    The return value of the input parameter method is acquired first and then passed into the scope of
    the calling method.

    Once the returned value of the input parameter method is calculated and passed into the calling method's
    scope, it is it's own thing in memory.  Whatever that value is, that's the only value it will ever be and
    it does not contain within it any knowledge of what originally created (returned) it ancestrally.

    So, one might ask, how can you find out what created/returned the value that was passed in to the calling
    method from the input parameter method?

    And, more importantly, how can you re-call/re-access the object which gave us the value passed into our
    calling function?

    Yes, you could simply pass in the pointer to the method which you might want to re-call and that would be easy,
    BUT, that only really works for functions.  It doesn't work for class instance properties, not in any way that
    is clean, intuitive to use, and doesn't require the user to do more work than they should have to.

    What we really want is something that can be completely dynamic and figure out everything for us.

    That's what this method is for.  It does all of the magic for you of determining the if what we need to recall
    is a class method (which needs to be called using parentheses), or a class instance property.

    Furthermore, if what we want to recall is at the end of a dot-notation chain, this method will do what it
    needs to do to traverse the objects in this notation chain within the calling frames' local scope until it
    gets to the bottom of the chain in order to call/access the target.

    Args:
        calling_frame (Any):
        target_argument_pos (int):

    Returns:
        The a new return value of the argument passed in the method from the calling frame.

    """
    arguments = re.compile('\\(.*\\)')

    # The setup to gain access to the calling frames method call.
    calling_code = calling_frame.code_context[0].strip('\n')
    calling_locals = calling_frame.frame.f_locals
    target_call = arguments.search(calling_code)[0].strip('\\(').strip('\\)').split(', ')[target_argument_pos]

    # Get a list of the complete dot notation call chain from the calling frames method argument list
    target_call_attrs = target_call.split('.')

    # Reverse the call chain so we can work from the logical start point since we will never have any idea of what to expect
    target_call_attrs.reverse()

    # Get a copy of primary target that we want to eventually call/access (removing it from the call chain list)
    prime_target_id = target_call_attrs.pop(0).strip('()')

    # We'll store the string "id" of the top most level object here later
    top_level_target_id = ''

    # Our eventual dot notation call chain that we might need to iterate through.
    dot_notation_chain = []

    # Check to see if our primary target is a callable method within calling frames locals before making this more complicated than it has to be.
    if prime_target_id in calling_locals and callable(calling_locals[prime_target_id]):
        return calling_locals[prime_target_id]()
    else:
        # If we're here, we need to loop through each of the target call attributes to find the top most level object we need to access first
        for attribute in target_call_attrs:
            if attribute.strip('()') in calling_locals:
                top_level_target_id = attribute.strip('()')
                break
            else:
                # Until we find the top most level, we need to construct a chain of attributes between the top most level object and our target so we can drill down to access it.
                dot_notation_chain.append(attribute.strip('()'))

    # Store the reference to the top level object that we need to access
    top_level_object = calling_frame.frame.f_locals[top_level_target_id]

    # If we've gotten this far we now need to traverse dot notation chain to drill down into the object references
    current_level_object = top_level_object
    for index, command in enumerate(dot_notation_chain):
        # Is the command a class or a callable object within the current level object we're inspecting?
        if inspect.isclass(type(getattr(current_level_object, command))) or callable(getattr(current_level_object, command)):
            # If so, store the reference to the command as the new current level object and keep digging.
            current_level_object = getattr(current_level_object, command)
        else:
            # Than the current level object must be the parent to our prime target, return the value.
            return getattr(current_level_object, prime_target_id)

    # If we're here then we've drilled down to the bottom and we can recall the original calling frames argument.
    if callable(getattr(current_level_object, prime_target_id)):
        return getattr(current_level_object, prime_target_id)()
    else:
        return getattr(current_level_object, prime_target_id)

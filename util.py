"""
Contains shared utility functions

@func   : log   : Logs the given obejc to console if the VERBOSE flag is set
"""

VERBOSE = True

def log(thing):
    """
    Logs the given obejc to console if the VERBOSE flag is set
    
    @pre    : `thing` must be some stringifieable object
    @post   : if `thing` is stringifieable, it will be logged to console if the 
    global VERBOSE is True
    
    @param  : thing   : object    : what to (try to) print to console
    @return : None
    """
    try:
        if globals().get("VERBOSE", False): print(thing)
    except Exception as e:
        print("Can't print it nuh nuh na nuh")

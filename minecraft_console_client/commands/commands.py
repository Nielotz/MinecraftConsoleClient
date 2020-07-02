"""
Command format:
    :command value1[ value2...]

Available commands:
    goto x y z  # floats

"""

from commands import chat_commands
from collections import namedtuple

Command = namedtuple('Command', 'args_types func')
""" :param args_types: to which try to convert to """

""" 

    Bot object is automatically passed as first parameter.


Has to be in priority order. Sample:
    'a': ...,
    'a b': ...
will never interpreted as 'a b', because always 'a' will be hit firstly.
Instead use: 
    'a b': ...  <- Will check for 'a b' in given str  
    'a': ...,   <- When 'a b' will not be found, check for 'a' 


"""
GOTO = {
    #"pause": Command((), chat_commands.),
    "clear": Command((), chat_commands.__goto_clear),
    "xyz": Command((float, float, float), chat_commands.__goto),
}


COMMAND = {
    "goto": GOTO,

}



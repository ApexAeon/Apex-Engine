last_id = -1
def spawn(data):
    if data['type'] == 'tele':
        return 
    elif data['type'] == 'pickup':
        return
    elif data['type'] == 'prop':
        return
    elif data['type'] == 'change':
        return
    elif data['type'] == 'trigger':
        return
    elif data['type'] == 'spawn':
        return
 
class tele(): # On a trigger input, they are teleported to another area of the same or different room.
    def __init__(self, data, uid):
        self.data = data
        self.uid = uid
class pickup(): # On player contact, executes some action such as putting an item into the players inventory, then becomes inactive and dissapears.
    def __init__(self, data, uid):
        self.data = data
        self.uid = uid
class prop(): # Something that displays a sprite.
    def __init__(self, data, uid):
        self.data = data
        self.uid = uid
class change(): # On a trigger input, can change the state of itself or any other entity. Example: On input, change "propfile" of "entity-360" to "chair.png."
    def __init__(self, data, uid):
        self.data = data
        self.uid = uid
class trigger(): # On arbitrary met condition, trigger another object's trigerable input.
    def __init__(self, data, uid):
        self.data = data
        self.uid = uid
class spawn(): # On a trigger input, creates a new entity.
    def __init__(self, data, uid):
        self.data = data
        self.uid = uid

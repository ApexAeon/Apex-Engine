import game

last_id = -1
def spawn(data):
    if data['type'] == 'generic':
        return generic(data, last_id + 1)
    elif data['type'] == 'tele':
        return tele(data, last_id + 1)
    elif data['type'] == 'pickup':
        return pickup(data, last_id + 1)
    elif data['type'] == 'prop':
        return prop(data, last_id + 1)
    elif data['type'] == 'change':
        return change(data, last_id + 1)
    elif data['type'] == 'trigger':
        return trigger(data, last_id + 1)
    elif data['type'] == 'spawn':
        return spawn(data, last_id + 1)
    last_id += 1
 
class generic():
    def __init__(self, data, uid):
        self.data = data
        self.uid = uid
    def tick():
        print('Hello, World!')
    def trigger():
        print('TRIGGERED! REEEEEEE!')
class tele(): # On a trigger input, they are teleported to another area of the same or different room.
    def __init__(self, data, uid):
        self.data = data
        self.uid = uid
    def tick():
        print('Object "' + self.data['name'] + '" # ' + self.uid + ' of type "tele" was ticked!')
    def trigger():
        gamestate = game.getGamestate()
        gamestate['x'] = self.data['x']
        gamestate['y'] = self.data['y']
        gamestate['z'] = self.data['z']
        game.setGamestate(gamestate)
class pickup(): # On player contact, executes some action such as putting an item into the players inventory, then becomes inactive and dissapears.
    def __init__(self, data, uid):
        self.data = data
        self.uid = uid
    def tick(gamestate, objects):
        print('TRIGGERED! REEEEEEE!')
    def trigger(gamestate):
        print('TRIGGERED! REEEEEEE!')

class prop(): # Something that displays a sprite.
    def __init__(self, data, uid):
        self.data = data
        self.uid = uid
    def tick(gamestate, objects):
        print('TRIGGERED! REEEEEEE!')
    def trigger(gamestate):
        print('TRIGGERED! REEEEEEE!')
class change(): # On a trigger input, can change the state of itself or any other entity. Example: On input, change "propfile" of "entity-360" to "chair.png."
    def __init__(self, data, uid):
        self.data = data
        self.uid = uid
    def tick(gamestate, objects):
        print('TRIGGERED! REEEEEEE!')
    def trigger(gamestate):
        print('TRIGGERED! REEEEEEE!')
class trigger(): # On arbitrary met condition, trigger another object's trigerable input.
    def __init__(self, data, uid):
        self.data = data
        self.uid = uid
    def tick(gamestate, objects):
        print('Object "' + self.data['name'] + '" # ' + self.uid + ' of type "trigger" was ticked!')
        if game.getGamestate['x'] >= self.data['x_minimum'] and game.getGamestate['y'] >= self.data['y_minimum'] and game.getGamestate['z'] >= self.data['z_minimum'] and game.getGamestate['x'] <= self.data['x_maximum'] and game.getGamestate['y'] <= self.data['y_maximum'] and game.getGamestate['z'] <= self.data['z_maximum']:
            game.trigger(self.data['output'])
    def trigger(gamestate):
        print('TRIGGERED! REEEEEEE!')
class spawn(): # On a trigger input, creates a new entity.
    def __init__(self, data, uid):
        self.data = data
        self.uid = uid
    def tick(gamestate, objects):
        print('TRIGGERED! REEEEEEE!')
    def trigger(gamestate):
        print('TRIGGERED! REEEEEEE!')


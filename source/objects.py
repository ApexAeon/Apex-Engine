import common
import resources
import game

last_id = -1
class Generic():
    def __init__(self, data, uid):
        self.data = data
        self.uid = uid
    def tick(self):
        pass
    def trigger(self):
        pass
class Item():
    def __init__(self, data, uid):
        self.data = data
        self.uid = uid
        self.entities = []
    def tick(self):
        pass
    def trigger(self): # Add self to inventory.
        for item in common.gamestate['player']['items']:
            if item.name == self.name:
                item.add()
                return 0
        if self.data['enabled']:
            for item in common.gamestate['player']['items']:
                if item.data['name'] == self.data['name']:
                    item.add()
                    return 0
            common.gamestate['player']['items'].append(self)
            self.data['enabled'] = False
            for entity in self.data['entities']:
                self.entities.append(spawn(entity))
    def use(self):
        if self.data['count'] > 0:
            self.data['count'] -= 1
            for entity in self.entities:
                if entity.data['name'] == self.data['on_use']:
                    entity.trigger()
    def equip(self):
        if not self.data['equipped']:
            self.data['equipped'] = True
            for entity in self.data['entities']:
                if entity.data['name'] == self.data['on_equip']:
                    entity.trigger()
    def unequip(self):
        if self.data['equipped']:
            self.data['equipped'] = False
            for entity in self.data['entities']:
                if entity.data['name'] == self.data['on_unequip']:
                    entity.trigger()
    def add(self):
        self.data['count'] += 1
class Tele(): # On a trigger input, they are teleported to another area of the same or different room.
    def __init__(self, data, uid):
        self.data = data
        self.uid = uid
    def tick(self):
        print('Object "' + self.data['name'] + '" # ' + str(self.uid) + ' of type "tele" was ticked!')
    def trigger(self):
        common.gamestate['x'] = self.data['x']
        common.gamestate['y'] = self.data['y']
        common.gamestate['z'] = self.data['z']
class Pickup(): # On player contact, executes some action such as putting an item into the players inventory, then becomes inactive and dissapears.
    def __init__(self, data, uid):
        self.data = data
        self.uid = uid
    def tick(self):
        pass
    def trigger(self):
        pass

class Prop(): # Something that displays a sprite.
    def __init__(self, data, uid):
        self.data = data
        self.uid = uid
        #level['props'][data[prop]]['hitbox'] = loadAsset(data[prop])
    def tick(self):
        common.DISPLAYSURF.blit(resources.loadAsset('../game/assets/props/'+self.data['prop']+'.png'), (game.calcX(self.data['x'], 0, self.data['y']),game.calcY(self.data['x'], 0, self.data['y'])))
    def trigger(self):
        pass
class Change(): # On a trigger input, can change the state of itself or any other entity. Example: On input, change "propfile" of "entity-360" to "chair.png."
    def __init__(self, data, uid):
        self.data = data
        self.uid = uid
    def tick(self):
        pass
    def trigger(self):
        print('Change entity triggered.')
        changeMain(self.data['output'], self.data['key'], self.data['value'])
        
class Trigger(): # On arbitrary met condition, trigger another object's trigerable input.
    def __init__(self, data, uid):
        self.data = data
        self.uid = uid
    def tick(self):
        if common.gamestate['x'] >= self.data['x_minimum'] and common.gamestate['y'] >= self.data['y_minimum'] and common.gamestate['z'] >= self.data['z_minimum'] and common.gamestate['x'] <= self.data['x_maximum'] and common.gamestate['y'] <= self.data['y_maximum'] and common.gamestate['z'] <= self.data['z_maximum']:
            triggerMain(self.data['output'])
            print('Player is within the bounds of the trigger.')
    def trigger(self):
        pass
class Spawner(): # On a trigger input, creates a new entity.
    def __init__(self, data, uid):
        self.data = data
        self.uid = uid
    def tick(self):
        pass
    def trigger(self):
        pass
class Hurt():
    def __init__(self, data, uid):
        self.data = data
        self.uid = uid
    def tick(self):
        pass
    def trigger(self):
        print('hurt u')
        if self.data['bypass']:
            if self.data['set']:
                common.gamestate['player']['health'] = self.data['health']
            elif self.data['change']:
                common.gamestate['player']['health'] -= self.data['health']
        else:
            common.gamestate['player']['armor'] -= common.gamestate['player']['armor_percent'] * self.data['health'] # Hit the armor.
            common.gamestate['player']['health'] -= self.data['health'] - (common.gamestate['player']['armor_percent'] * self.data['health']) # Hit the player.
            if gamestate['player']['armor'] < 0:
                common.gamestate['player']['health'] += common.gamestate['player']['armor']
                common.gamestate['player']['armor'] = 0
        if common.gamestate['player']['health'] > common.gamestate['player']['max_health']:
            common.gamestate['player']['health'] = common.gamestate['player']['max_health']
def spawn(data):
    if data['type'] == 'item':
        return Item(data, last_id + 1)
    elif data['type'] == 'tele':
        return Tele(data, last_id + 1)
    elif data['type'] == 'pickup':
        return Pickup(data, last_id + 1)
    elif data['type'] == 'prop':
        return Prop(data, last_id + 1)
    elif data['type'] == 'change':
        return Change(data, last_id + 1)
    elif data['type'] == 'trigger':
        return Trigger(data, last_id + 1)
    elif data['type'] == 'spawner':
        return Spawner(data, last_id + 1)
    elif data['type'] == 'hurt':
        return Hurt(data, last_id + 1)
def changeMain(name, key, value):
    for entity in common.entities:
        if entity.data['name'] == name:
            entity.data[key] = value
def triggerMain(name):
    for entity in common.entities:
        if entity.data['name'] == name:
            entity.trigger()

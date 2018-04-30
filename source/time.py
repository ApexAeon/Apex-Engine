continuum = {}
indicies = []
gamestate = {}
def retrieve(index):
  while True:
    pass
def capture(state, index):
  if len(indicies) is 0: # If this is the first capture, place the entire state into the continuum.
    continuum[index] = state
  else: # If this is not the first capture, place the difference between the previous state and the new state into the continuum.
    past = {} 
    for change in indicies: # Compile all the past state changes leading up to but excluding the present state.
      past.update(continuum[change])
    for key in past: # Compare the past and the present.
      if state[key] != past[key]: # If they differ
        continuum[index].update({key:state[key]}) # Update the continuum
    indicies.append(index) # Add the time index to the indicies list.
while True:  
  gamestate = {
    "apples":"3",
    "action":"none",
    "thoughts":"im hungry",
    "hunger":"100"
  }
  capture(gamestate, 0)
  gamestate = {
    "apples":"2",
    "action":"eating",
    "thoughts":"yum",
    "hunger":"50"
  }
  capture(gamestate, 1)
  gamestate = {
    "apples":"1",
    "action":"eating",
    "thoughts":"i like apples",
    "hunger":"25"
  }
  capture(gamestate, 2)
  gamestate = {
    "apples":"0",
    "action":"none",
    "thoughts":"feelin good",
    "hunger":"0"
  }
  capture(gamestate, 4)
  print(indicies)
  print(continuum)
  input()

continuum = {}
indicies = []
def retrieve(index):
  while True:
    
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
      

  
   


import pygame.mixer

pygame.mixer.init()

ss = {
'currentSong':"null",
'playing':False,
'playanyway':False
}
def play(a):
    if a['music']['songPlaysInLevel']:
        ss['playing'] = True
        if ss['currentSong'] != a['music']['song']:
            print('We loaded it.')
            pygame.mixer.music.load(a['music']['song'])
            ss['currentSong'] = a['music']['song']
    else:
        ss['currentSong'] = "null"
        ss['playing'] = False
        pygame.mixer.music.stop()
    if a['music']['resetMusic']:
        ss['playanyway'] = True
        
def ping():
    if ss['playing'] and not pygame.mixer.music.get_busy():
        print('It\'s time to play')
        pygame.mixer.music.play()
    if ss['playanyway']:
        print('Surprise! We\'re doing it now!')
        pygame.mixer.music.play()
        ss['playanyway'] = False
    

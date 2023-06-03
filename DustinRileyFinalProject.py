# INF360 - Programming in Python
# Dustin Riley
# Final Project - memory game with brute force protection
# got images from itch.io free to use assets
# no modules need downloaded

import logging
from tkinter import *
import random

logging.basicConfig(level = logging.DEBUG, format = '%(asctime)s - %(levelname)s - %(message)s')
#logging.disable(logging.CRITICAL)
logging.debug('Start of program')

count = 0           # how many times select() is called
matches = 0         # number of matched images
matched = [0]*36    # matched images
num1 = 0            # index of button pressed first
num2 = 0            # index of button pressed second
dup = 0             # how many times the same button was pressed without matching in a row
prevspot1 = ''      # previous button that was pressed first
prevspot2 = ''      # previous button that was pressed second

window = Tk()                                       # use tkinter to create a window object
window.title("Memory With Bruteforce Protection")   # set window title
window.configure(bg = 'black')                      # set background color

label = Label(window, text = "Click any button", bg = 'black', fg = 'light blue')    # game label bg background fg text color
label.grid(row = 0, column = 0)                     # place label into grid

def cont():                                         # when continue button is pressed
    logging.debug('Start of cont()')
    for i in range(36):
        btn[i]['state'] = 'normal'          # enable all btn[]
    btn[num1].grid()                        # restore hidden buttons 1 and 2, remembers position
    btn[num2].grid()
    label.config(text = "Click any button") # reset game label
    con.grid_remove()                       # hide continue button
    logging.debug('End of cont')

def closeGame():
    window.quit()                               # closes game

def duplicate(num):
    global dup
    logging.debug('Start of duplicate(%s)' %(num))
    if(num == prevspot1 or num == prevspot2):   # check if duplicate button
        dup += 1                                # increment duplicate count
        logging.debug('dup %s' %(dup))
    logging.debug('End of duplicate(%s)' %(num))

def done():
    global matches
    logging.debug('Start of done()')
    matches += 1                                # increment matches
    logging.debug('matches %s' %(matches))
    if(matches == 18):                          # all matches found yay
        label.config(text = "Congrats! again?")
        yes.grid()                              # show yes button
        no.grid()                               # show no button
    logging.debug('End of done()')

def resetDup():
    global prevspot1, prevspot2, dup
    logging.debug('Start of resetDup()')
    prevspot1 = ''                              # reset prevspot1
    prevspot2 = ''                              # reset prevspot2
    dup = 0                                     # reset dup
    logging.debug('End of resetDup()')

def check():
    logging.debug('num1 %s, num2 %s' %(num1, num2))
    if(img[num1]['file'] == img[num2]['file']): # check if same image behind button 1 and 2
        label.config(text = "You got a match!")
        matched[matches] = img[num1]['file']    # save matched image into matched list
        done()                                  # check if done
        resetDup()                              # reset duplication trackers
    elif(dup == 2):                             # bruteforce detected
        label.config(text = "Cheater! *shake*")
        shuffle()                               # reshuffle images
        resetDup()                              # reset duplication trackers
    else:
        label.config(text = "Too bad")          # set game label to too bad
        for i in range(36):
            btn[i]['state'] = 'disabled'        # disable all btn[]
        con.grid()                              # show continue button
        # this is a way to pause the game until continue is clicked, otherwise you will not see the image behind button 2
        # P.S. I tried time.sleep(x) the button would just stay in clicked animation, would not disappear or reveal image behind it
    logging.debug('End of check()')

def select(num):
    global count, num1, num2, prevspot1, prevspot2
    logging.debug('Start of select(%s)' %(num))
    if(count == 0):
        duplicate(num)
        label.config(text = "Click another")        # set game label to say click another
        num1 = num                                  # save button 1 number to global num1
        prevspot1 = num                             # save button 1 number to global prevspot1
        btn[num].grid_remove()                      # hide button 1
        count += 1                                  # increment count
        logging.debug('count %s, num1 %s, prevspot1 %s' %(count, num1, prevspot1))
    elif(count == 1):
        duplicate(num)
        num2 = num                                  # save button 2 number to global num2
        prevspot2 = num                             # save button 2 number to global prevspot2
        btn[num].grid_remove()                      # hide button 2
        check()
        count = 0                                   # reset count
        logging.debug('count %s, num2 %s, prevspot2 %s' %(count, num2, prevspot2))
    logging.debug('End of select(%s)' %(num))

def shuffle():
    logging.debug('Start of shuffle()')
    random.random()                         # randomize
    random.shuffle(img)                     # shuffle images
    for i in range(36):
        images[i].config(image = img[i])    # assign shuffled img to label
        btn[i].grid()                       # restore hidden buttons
    for i in range(36):
        for j in range(18):
            if(matched[j] == img[i]['file']):   # check if image is in matched list
                btn[i].grid_remove()            # hide matched items' buttons
    logging.debug('End of shuffle()')

def init():
    global matched, count, matches
    logging.debug('Start of init()')
    matches = 0                 # reset matches
    matched = [0]*18            # reset matched
    count = 0                   # reset count
    shuffle()
    logging.debug('count %s, matches %s' %(count, matches))
    logging.debug('End of init()')

def reset():
    logging.debug('Start of reset()')
    yes.grid_remove()           # hide yes button
    no.grid_remove()            # hide no button
    label.config(text = "Click any button")
    init()
    logging.debug('End of reset()')

# list of PhotoImages
img = ['0']*36
# initiate list of PhotoImages
for i in range(18):
    img[i] = PhotoImage(file = 'images/' + str(i) + '.png')
    img[i + 18] = PhotoImage(file = 'images/' + str(i) + '.png')
# button image
btnimg = PhotoImage(file = 'images/btn.png', height = 100, width = 100)
# list of image labels
images = []
# list of buttons
btn = []
# initiate list of labels
index = 0
for i in range(36):
    images.append(Label(window, image = img[index], background = 'black'))    # append label to images list
    btn.append(Button(window, image = btnimg, borderwidth = 0))  # append button to btn list
    btn[i].config(command = lambda i=i: select(i))      # when clicked call select(i)
    # must include lambda to send parameters and i=i to send the value of i at this moment
    # if i do not include i=i, every button will be set to the same value that i was last
    index += 1                                          # increment index
    if(index == 18):                                    # 18 pictures total 32 labels/buttons reset index to 0
        index = 0
index = 0
for k in range(6):                                      # place images and buttons into grid position
    for j in range(6):
        images[index].grid(row = k + 1, column = j)     # sets images in grid position
        btn[index].grid(row = k + 1, column = j)        # sets buttons in grid position
        index += 1                                      # increment index

#continue button
con = Button(window, text = "Continue", command = cont)
con.grid(row = 0, column = 3)   # place continue button in grid
con.grid_remove() # hide continue button
#yes button
yes = Button(window, text = "yes", command = reset)
yes.grid(row = 0, column = 4)   # place yes button in grid
yes.grid_remove() # hide yes button
#no button
no = Button(window, text = "no", command = closeGame)
no.grid(row = 0, column = 5)    # place no button in grid
no.grid_remove() # hide no button

init()

window.mainloop()   # starts window
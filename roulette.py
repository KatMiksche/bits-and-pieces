import random
cash = float(input('how much money you have? '))
play = 'yes'
def roulette(cash):
    user_colour = input('what colour do you bet on? (red/black) ')
    user_number = float(input('what number do you bet on? (1-99) '))
    stake = float(input('whats your stake? '))
    gain=0
    if stake>cash:
        print('you dont have so much money :-D!')
    else:
        rcolour = random.randint(0,1)
        rnumber = random.randint(1,99)
        colourmatch=False
        if rcolour==1 and user_colour=='red':
            colourmatch=True
        elif  rcolour==0 and user_colour=='black':
            colourmatch=True
        if rcolour==1:
            print('ball landed on RED-{}'.format(rnumber))
        else:
            print('ball landed on BLACK-{}'.format(rnumber))
        if colourmatch==True and user_number==rnumber:
            gain = 100 * stake
            print(' ITS FULL MATCH! YOU WON ${}!'.format(100*stake))
        elif user_number==rnumber:
            gain = 2 * stake
            print('its number match, you won ${}.'.format(2*stake))
        elif colourmatch==True:
            gain=stake
            print('its colour match, you keep your stake')
        else:
            gain = gain - stake
            print(' NO MATCH AT ALL! YOU LOST YOUR STAKE!')
    return gain
while play=='yes':
    print('your balance is ',cash)
    play = input('ready to play? ')
    if cash>0 and play=='yes':
        cash=cash + roulette(cash)
    elif cash==0:
        play='no'
        print('YOU ARE OUT OF MONEY. GAME IS OVER.')

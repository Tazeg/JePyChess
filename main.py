#!/usr/bin/env python3
########################################################################
# JeffProd Simple Python Chess Program
########################################################################
# AUTHOR	: Jean-Francois GAZET
# WEB 		: http://www.jeffprod.com
# TWITTER	: @JeffProd
# MAIL		: jeffgazet@gmail.com
# LICENCE	: GNU GENERAL PUBLIC LICENSE Version 2, June 1991
########################################################################

# Import object classes
from board import *
from engine import *

b=Board()
e=Engine()

while(True):

    b.render()

    c=input('>>> ')

    if(c=='quit' or c=='exit'):
        exit(0)

    elif(c=='undomove'):
        e.undomove(b)

    elif('setboard' in c):
        e.setboard(b,c) 

    elif(c=='getboard'):
        e.getboard(b)

    elif(c=='go'):
        e.search(b)

    elif(c=='new'):
        e.newgame(b)

    elif(c=='bench'):
        e.bench(b)        

    elif('sd ' in c):
        e.setDepth(c)

    elif('perft ' in c):
        e.perft(c,b)        

    elif(c=='legalmoves'):
        e.legalmoves(b)
        
    else:
        # coup à jouer ? ex : e2e4
        e.usermove(b,c)

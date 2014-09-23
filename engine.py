########################################################################
# JeffProd Simple Python Chess Program
########################################################################
# AUTHOR	: Jean-Francois GAZET
# WEB 		: http://www.jeffprod.com
# TWITTER	: @JeffProd
# MAIL		: jeffgazet@gmail.com
# LICENCE	: GNU GENERAL PUBLIC LICENSE Version 2, June 1991
########################################################################

from piece import *
import time

class Engine:
    
    "The chess engine"
    
    ####################################################################
    
    def __init__(self):
        
        self.MAX_PLY=32
        self.pv_length=[0 for x in range(self.MAX_PLY)]
        self.INFINITY=32000        
        self.init()

    ####################################################################
    
    def usermove(self,b,c):
        
        """Move a piece for the side to move, asked in command line.
        The command 'c' in argument is like 'e2e4' or 'b7b8q'.
        Argument 'b' is the chessboard.
        """
        
        if(self.endgame):
            self.print_result(b)
            return        
              
        # Testing the command 'c'. Exit if incorrect.
        chk=self.chkCmd(c)
        if(chk!=''):
            print(chk)
            return
            
        # Convert cases names to int, ex : e3 -> 44
        pos1=b.caseStr2Int(c[0]+c[1])
        pos2=b.caseStr2Int(c[2]+c[3])
        
        # Promotion asked ?
        promote=''
        if(len(c)>4):
            promote=c[4]
            if(promote=='q'):
                promote='q'
            elif(promote=='r'):
                promote='r'
            elif(promote=='n'):
                promote='n'
            elif(promote=='b'):
                promote='b'
            
        # Generate moves list to check 
        # if the given move (pos1,pos2,promote) is correct
        mList=b.gen_moves_list()
        
        # The move is not in list ? or let the king in check ?
        if(((pos1,pos2,promote) not in mList) or \
        (b.domove(pos1,pos2,promote)==False)):
            print("\n"+c+' : incorrect move or let king in check'+"\n")
            return
        
        # Display the chess board
        b.render()
        
        # Check if game is over
        self.print_result(b)
        
        # Let the engine play
        #self.search(b)
        
    ####################################################################

    def chkCmd(self,c):
        
        """Check if the command 'c' typed by user is like a move,
        i.e. 'e2e4','b7b8n'...
        Returns '' if correct.
        Returns a string error if not.
        """
        
        err=(
        'The move must be 4 or 5 letters : e2e4, b1c3, e7e8q...',
        'Incorrect move.'
        )        
        letters=('a','b','c','d','e','f','g','h')
        numbers=('1','2','3','4','5','6','7','8')
                
        if(len(c)<4 or len(c)>5):
            return err[0]
        
        if(c[0] not in letters):
            return err[1]
            
        if(c[1] not in numbers):
            return err[1]
            
        if(c[2] not in letters):
            return err[1]
            
        if(c[3] not in numbers):
            return err[1]
            
        return ''

    ####################################################################
    
    def search(self,b):
        
        """Search the best move for the side to move,
        according to the given chessboard 'b'
        """
        
        if(self.endgame):
            self.print_result(b)
            return
            
        # TODO
        # search in opening book

        self.clear_pv()
        self.nodes=0
        b.ply=0
        
        print("ply\tnodes\tscore\tpv")
        
        for i in range(1,self.init_depth+1):
           
            score=self.alphabeta(i,-self.INFINITY,self.INFINITY,b)

            print("{}\t{}\t{}\t".format(i,self.nodes,score/10),end='')
            
            # print PV informations : ply, nodes...
            j=0
            while(self.pv[j][j]!=0):
                c=self.pv[j][j]
                pos1=b.caseInt2Str(c[0])
                pos2=b.caseInt2Str(c[1])
                print("{}{}{}".format(pos1,pos2,c[2]),end=' ')
                j+=1
            print()

            # Break is MAT is found
            if(score>self.INFINITY-100 or score<-self.INFINITY+100):
                break

        # root best move found, do it, and print result
        best=self.pv[0][0]
        b.domove(best[0],best[1],best[2])
        self.print_result(b)

    ####################################################################

    def alphabeta(self,depth,alpha,beta,b):

        # We arrived at the end of the search : return the board score
        if(depth==0):
            return b.evaluer()
            # TOTO : return quiesce(alpha,beta)

        self.nodes+=1
        self.pv_length[b.ply] = b.ply

        # Do not go too deep
        if(b.ply >= self.MAX_PLY-1):
            return b.evaluer()
            
        # Extensions
        # If king is in check, let's go deeper
        chk=b.in_check(b.side2move) # 'chk' used at the end of func too
        if(chk):
            depth+=1
            
        # TODO
        # sort moves : captures first

        # Generate all moves for the side to move. Those who 
        # let king in check will be processed in domove()
        mList=b.gen_moves_list()

        f=False # flag to know if at least one move will be done
        for i,m in enumerate(mList):
           
            # Do the move 'm'.
            # If it lets king in check, undo it and ignore it
            # remind : a move is defined with (pos1,pos2,promote)
            # i.e. : 'e7e8q' is (12,4,'q')
            if(not b.domove(m[0],m[1],m[2])):
                continue
                
            f=True # a move has passed
            
            score=-self.alphabeta(depth-1,-beta,-alpha,b)

            # Unmake move
            b.undomove()

            if(score>alpha):
                    
                # TODO
                # this move caused a cutoff,
                # should be ordered higher for the next search
                
                if(score>=beta):
                    return beta
                alpha = score

                # Updating the triangular PV-Table
                self.pv[b.ply][b.ply] = m
                j = b.ply + 1
                while(j<self.pv_length[b.ply+1]):
                    self.pv[b.ply][j] = self.pv[b.ply+1][j]
                    self.pv_length[b.ply] = self.pv_length[b.ply + 1]
                    j+=1
                    
        # If no move has been done : it is DRAW or MAT
        if(not f):
            if(chk):
                return -self.INFINITY + b.ply # MAT
            else:
                return 0 # DRAW
                
        # TODO
        # 50 moves rule
            
        return alpha

    ####################################################################

    def print_result(self,b):
        
        "Check if the game is over and print the result"
        
        # Is there at least one legal move left ?
        f=False
        for pos1,pos2,promote in b.gen_moves_list():
            if(b.domove(pos1,pos2,promote)):
                b.undomove()
                f=True # yes, a move can be done
                break
                
        # No legal move left, print result
        if(not f):
            if(b.in_check(b.side2move)):
                if(b.side2move=='blanc'):
                    print("0-1 {Black mates}")
                else:
                    print("1-0 {White mates}")
            else:
                print("1/2-1/2 {Stalemate}")
            self.endgame=True
         
        # TODO
        # 3 reps
        # 50 moves rule
            
    ####################################################################

    def clear_pv(self):
        
        "Clear the triangular PV table containing best moves lines"
        
        self.pv=[[0 for x in range(self.MAX_PLY)] for x in range(self.MAX_PLY)]
                
    ####################################################################

    def setboard(self,b,c):
        
        """Set the chessboard to the FEN position given by user with 
        the command line 'setboard ...'.
        'c' in argument is for example :
        'setboard 8/5k2/5P2/8/8/5K2/8/8 w - - 0 0'
        """
        
        cmd=c.split() # split command with spaces
        cmd.pop(0) # drop the word 'setboard' written by user

        # set the FEN position on board
        if(b.setboard(' '.join(cmd))):
            self.endgame=False # success, so no endgame
            
    ####################################################################

    def setDepth(self,c):
        
        """'c' is the user command line, i.e. 'sd [x]'
        to set the search depth.
        """
        
        # Checking the requested value
        cmd=c.split()
        #cmd[0]='sd'
        #cmd[1] should be an integer
        
        try:
            d=int(cmd[1])
        except ValueError:
            print('Depth isn\'t an integer. Please type i.e. : sd 5')
            return
            
        if(d<2 or d>self.MAX_PLY):
            print('Depth must be between 2 and',self.MAX_PLY)
            return
        
        # Things seems to be all right
        self.init_depth=d
        print('Depth set to',d)
        
    ####################################################################

    def perft(self,c,b):
       
        """PERFformance Test :
        This is a debugging function through the move generation tree
        for the current board until depth [x].
        'c' is the command line written by user : perft [x]
        """
        
        # Checking the requested depth
        cmd=c.split()
        #cmd[0]='perft'
        
        try:
            d=int(cmd[1])
        except ValueError:
            print('Please type an integer as depth i.e. : perft 5')
            return
            
        if(d<1 or d>self.MAX_PLY):
            print('Depth must be between 1 and',self.MAX_PLY)
            return
        
        print("Depth\tNodes\tCaptures\tE.p.\tCastles\tPromotions\tChecks\tCheckmates")
        
        time1 = time.time()
        for i in range(1,d+1):
            total=self.perftoption(0,i-1,b)
            print("{}\t{}".format(i,total))
        time2 = time.time()
        timeDiff = round((time2-time1),2)
        print('Done in',timeDiff,'s')

    def perftoption(self,prof,limit,b):        
        cpt=0

        if(prof>limit):
            return 0

        l=b.gen_moves_list()

        for i,m in enumerate(l):
           
            if(not b.domove(m[0],m[1],m[2])):
                continue

            cpt+=self.perftoption(prof+1,limit,b)

            if(limit==prof):
                cpt+=1

            b.undomove()

        return cpt
        
    ####################################################################
    
    def legalmoves(self,b):
        
        "Show legal moves for side to move"
        
        mList=b.gen_moves_list()
        
        cpt=1
        for m in mList:
            if(not b.domove(m[0],m[1],m[2])):
                continue            
            print('move #',cpt,':',b.caseInt2Str(m[0])+b.caseInt2Str(m[1])+m[2])
            b.undomove()
            cpt+=1
            
    ####################################################################

    def getboard(self,b):
        
        """The user requests the current FEN position
        with the command 'getboard'"""
        
        print(b.getboard())
        
    ####################################################################

    def newgame(self,b):
        
        self.init()
        b.init()
        
    ####################################################################

    def bench(self,b):
        
        """Test to calculate the number of nodes a second.
        The position used is the 17th move of the game :
        Bobby Fischer vs. J. Sherwin, New Jersey State 
        Open Championship, 9/2/1957 :
        1rb2rk1/p4ppp/1p1qp1n1/3n2N1/2pP4/2P3P1/PPQ2PBP/R1B1R1K1 w - - 0 1
        The engine searches to a given depth, 3 following times.
        The kilonodes/s is calculated with the best time.
        """

        oldDepth=self.init_depth
        self.init_depth=3
        timeDiff=[]

        for i in range(3):

            print('Searching to depth',self.init_depth,'...')
            
            if(not b.setboard('1rb2rk1/p4ppp/1p1qp1n1/3n2N1/2pP4/2P3P1/PPQ2PBP/R1B1R1K1 w - - 0 1')):
                print('Could not set board ???!#!')
                return
            
            start_time=time.time()       
            self.search(b)
            stop_time=time.time() 
            timeDiff.append(round((stop_time-start_time),2))
            print('Time:',timeDiff[i],'ms\n')
            
        if(timeDiff[1] < timeDiff[0]):
            timeDiff[0] = timeDiff[1]
        if(timeDiff[2] < timeDiff[0]):
            timeDiff[0] = timeDiff[2]

        print('Best time:',timeDiff[0],'ms')
        print('Nodes:',self.nodes)
        
        nps = self.nodes / timeDiff[0]
        nps *= 1000
        print('Nodes per second:',round(nps/1000,2),'kn/s')
        
        # Restoring changed values
        self.init_depth=oldDepth
        
    ####################################################################

    def undomove(self,b):
        
        "The user requested a 'undomove' in command line"
        
        b.undomove()
        self.endgame=False

    ####################################################################

    def init(self):
        self.endgame=False    
        self.init_depth=4 # search in fixed depth
        self.nodes=0 # number of nodes
        self.clear_pv()
        
    ####################################################################

        

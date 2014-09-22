########################################################################
# JeffProd Simple Python Chess Program
########################################################################
# AUTHOR	: Jean-Francois GAZET
# WEB 		: http://www.jeffprod.com
# TWITTER	: @JeffProd
# MAIL		: jeffgazet@gmail.com
# LICENCE	: GNU GENERAL PUBLIC LICENSE Version 2, June 1991
########################################################################

class Piece:
    
    "Chess set class"
    
    VIDE='.' # empty piece name (=empty square '.' in console)

    # Name of the pieces
    nomPiece=(VIDE,'ROI','DAME','TOUR','CAVALIER','FOU','PION')
        
    # Give a score value for each piece : KING=0, QUEEN=9, ROOK=5...
    valeurPiece=(0,0,9,5,3,3,1)
    
    # For the pieces moves, using method "mail box" from Robert Hyatt
    # It helps to know if a piece is not moved outside the board !
    tab120 = (
	-1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
	-1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
	-1,  0,  1,  2,  3,  4,  5,  6,  7, -1,
	-1,  8,  9, 10, 11, 12, 13, 14, 15, -1,
	-1, 16, 17, 18, 19, 20, 21, 22, 23, -1,
	-1, 24, 25, 26, 27, 28, 29, 30, 31, -1,
	-1, 32, 33, 34, 35, 36, 37, 38, 39, -1,
	-1, 40, 41, 42, 43, 44, 45, 46, 47, -1,
	-1, 48, 49, 50, 51, 52, 53, 54, 55, -1,
	-1, 56, 57, 58, 59, 60, 61, 62, 63, -1,
	-1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
	-1, -1, -1, -1, -1, -1, -1, -1, -1, -1
	)
    tab64 = (
	21, 22, 23, 24, 25, 26, 27, 28,
	31, 32, 33, 34, 35, 36, 37, 38,
	41, 42, 43, 44, 45, 46, 47, 48,
	51, 52, 53, 54, 55, 56, 57, 58,
	61, 62, 63, 64, 65, 66, 67, 68,
	71, 72, 73, 74, 75, 76, 77, 78,
	81, 82, 83, 84, 85, 86, 87, 88,
	91, 92, 93, 94, 95, 96, 97, 98
	)
    
    # Moving vectors according to the 'tab64',
    deplacements_tour=(-10,10,-1,1)
    deplacements_fou=(-11,-9,11,9)
    deplacements_cavalier=(-12,-21,-19,-8,12,21,19,8)
    # KING and QUEEN = BISHOP + ROOK !
   
    ####################################################################
    
    def __init__(self,nom=VIDE,couleur=''):
        
        """Creating a piece object, with its attributes :
        - 'nom' as name (ROI, DAME...);
        - 'couleur' as color (blanc,noir);
        - 'valeur' as its value"""
        
        self.nom=nom
        self.couleur=couleur        
        self.valeur=self.valeurPiece[self.nomPiece.index(nom)]
        
    ####################################################################
    
    def isEmpty(self):
        
        """Returns TRUE or FALSE if this piece object is defined, 
        As any square on board can have a piece on it, or not,
        we can set a null piece on a square."""
        
        return (self.nom==self.VIDE)
        
    ####################################################################
    
    def pos2_roi(self,pos1,cAd,echiquier,dontCallIsAttacked=False):

        """Returns the list of moves for the king :
        - which is at square 'pos1'
        - which opponent color is 'cAd' (blanc,noir)
        - dontCallIsAttacked is set to avoid recursives calls 
        between is_attacked() and gen_moves_list().
        """
        
        liste=[]
        
        for i in (self.deplacements_tour+self.deplacements_fou):
            n=self.tab120[self.tab64[pos1]+i]
            if(n!=-1):
                if(echiquier.cases[n].isEmpty() or echiquier.cases[n].couleur==cAd):
                    liste.append((pos1,n,''))
        
        if(dontCallIsAttacked):
            return liste # we just wanted moves that can attack
            
        # The current side to move is the opposite of cAd
        c=echiquier.oppColor(cAd)
        
        # Castle moves
        if(c=='blanc'):
            if(echiquier.white_can_castle_63):
                # If a rook is at square 63
                # And if squares between KING and ROOK are empty
                # And if squares on which KING walks are not attacked
                # And if KING is not in check
                # Then we can add this castle move
                if(echiquier.cases[63].nom=='TOUR' and \
                echiquier.cases[63].couleur=='blanc' and \
                echiquier.cases[61].isEmpty() and \
                echiquier.cases[62].isEmpty() and \
                echiquier.is_attacked(61,'noir')==False and \
                echiquier.is_attacked(62,'noir')==False and \
                echiquier.is_attacked(pos1,'noir')==False):
                    liste.append((pos1,62,''))
            if(echiquier.white_can_castle_56):
                # S'il y a une tour en 56, etc...
                if(echiquier.cases[56].nom=='TOUR' and \
                echiquier.cases[56].couleur=='blanc' and \
                echiquier.cases[58].isEmpty() and \
                echiquier.cases[59].isEmpty() and \
                echiquier.is_attacked(58,cAd)==False and \
                echiquier.is_attacked(59,cAd)==False and \
                echiquier.is_attacked(pos1,cAd)==False):
                    liste.append((pos1,58,''))
        else:
            if(echiquier.black_can_castle_7):
                if(echiquier.cases[7].nom=='TOUR' and \
                echiquier.cases[7].couleur=='noir' and \
                echiquier.cases[5].isEmpty() and \
                echiquier.cases[6].isEmpty() and \
                echiquier.is_attacked(5,cAd)==False and \
                echiquier.is_attacked(6,cAd)==False and \
                echiquier.is_attacked(pos1,cAd)==False):
                    liste.append((pos1,6,''))
            if(echiquier.black_can_castle_0):
                if(echiquier.cases[0].nom=='TOUR' and \
                echiquier.cases[7].couleur=='noir' and \
                echiquier.cases[1].isEmpty() and \
                echiquier.cases[2].isEmpty() and \
                echiquier.cases[3].isEmpty() and \
                echiquier.is_attacked(2,cAd)==False and \
                echiquier.is_attacked(3,cAd)==False and \
                echiquier.is_attacked(pos1,cAd)==False):
                    liste.append((pos1,2,''))

        return liste
        
    ####################################################################
    
    def pos2_tour(self,pos1,cAd,echiquier):
        
        """Returns the list of moves for a ROOK :
        - at square number 'pos1' (0 to 63)
        - opponent color is cAd (blanc,noir)"""
        
        liste=[]
        
        for k in self.deplacements_tour:        
            j=1
            while(True):
                n=self.tab120[self.tab64[pos1] + (k * j)]
                if(n!=-1): # as we are not out of the board
                    if(echiquier.cases[n].isEmpty() or echiquier.cases[n].couleur==cAd):
                        liste.append((pos1,n,'')) # append the move if square is empty of opponent color
                else:
                    break # stop if outside of the board
                if(not echiquier.cases[n].isEmpty()):
                    break # destination square is not empty (opponent or not) then the rook won't pass through
                j=j+1

        return liste
        
    ####################################################################
    
    def pos2_cavalier(self,pos1,cAd,echiquier):
        
        """Returns the list of moves for a KNIGHT :
        - at square number 'pos1' (0 to 63)
        - opponent color is cAd (blanc,noir)"""
        
        liste=[]
        
        for i in self.deplacements_cavalier:
            n=self.tab120[self.tab64[pos1]+i]
            if(n!=-1):
                if(echiquier.cases[n].isEmpty() or echiquier.cases[n].couleur==cAd):
                    liste.append((pos1,n,''))

        return liste
        
    ####################################################################
    
    def pos2_fou(self,pos1,cAd,echiquier):
        
        """Returns the list of moves for a BISHOP :
        - at square number 'pos1' (0 to 63)
        - opponent color is cAd (blanc,noir)"""
        
        liste=[]
        
        for k in self.deplacements_fou:
            j=1
            while(True):
                n=self.tab120[self.tab64[pos1] + (k * j)]
                if(n!=-1): # as we are not out of the board
                    if(echiquier.cases[n].isEmpty() or echiquier.cases[n].couleur==cAd):
                        liste.append((pos1,n,'')) # append the move if square is empty of opponent color
                else:
                    break # stop if outside of the board
                if(not echiquier.cases[n].isEmpty()):
                    break # destination square is not empty (opponent or not) then the bishop won't pass through
                j=j+1

        return liste
        
    ####################################################################
    
    def pos2_pion(self,pos1,couleur,echiquier):
        
        """Returns the list of moves for a PAWN :
        - at square number 'pos1' (0 to 63)
        - opponent color is cAd (blanc,noir)"""
        
        liste=[]
        
        # White PAWN ---------------------------------------------------
        if(couleur=='blanc'):

            # Upper square
            n=self.tab120[self.tab64[pos1]-10]
            if(n!=-1):
                if(echiquier.cases[n].isEmpty()):
                    # If the PAWN has arrived to rank 8 (square 0 to 7), 
                    if(n<8):
                        # it will be promoted
                        liste.append((pos1,n,'q'))
                        liste.append((pos1,n,'r'))
                        liste.append((pos1,n,'n'))
                        liste.append((pos1,n,'b'))
                    else:
                        liste.append((pos1,n,''))
                    
            # 2nd square if PAWN is at starting square
            if(echiquier.ROW(pos1)==6):
                # If the 2 upper squares are empty
                if(echiquier.cases[pos1-8].isEmpty() and echiquier.cases[pos1-16].isEmpty()):
                    liste.append((pos1,pos1-16,''))

            # Capture upper left
            n=self.tab120[self.tab64[pos1]-11]
            if(n!=-1):
                if(echiquier.cases[n].couleur=='noir' or echiquier.ep==n):
                    if(n<8): # Capture + promote
                        liste.append((pos1,n,'q'))
                        liste.append((pos1,n,'r'))
                        liste.append((pos1,n,'n'))
                        liste.append((pos1,n,'b'))
                    else:
                        liste.append((pos1,n,''))

            # Capture upper right
            n=self.tab120[self.tab64[pos1]-9]
            if(n!=-1):
                if(echiquier.cases[n].couleur=='noir' or echiquier.ep==n):
                    if(n<8):
                        liste.append((pos1,n,'q'))
                        liste.append((pos1,n,'r'))
                        liste.append((pos1,n,'n'))
                        liste.append((pos1,n,'b'))
                    else:
                        liste.append((pos1,n,''))
        
        # Black PAWN ---------------------------------------------------    
        else:
            
            # Upper square
            n=self.tab120[self.tab64[pos1]+10]
            if(n!=-1):
                if(echiquier.cases[n].isEmpty()):
                    # PAWN has arrived to 8th rank (square 56 to 63), 
                    # it will be promoted
                    if(n>55):
                        liste.append((pos1,n,'q'))
                        liste.append((pos1,n,'r'))
                        liste.append((pos1,n,'n'))
                        liste.append((pos1,n,'b'))
                    else:
                        liste.append((pos1,n,''))

            # 2nd square if PAWN is at starting square
            if(echiquier.ROW(pos1)==1):
                # If the 2 upper squares are empty
                if(echiquier.cases[pos1+8].isEmpty() and echiquier.cases[pos1+16].isEmpty()):
                    liste.append((pos1,pos1+16,''))
                     
            # Capture bottom left
            n=self.tab120[self.tab64[pos1]+9]
            if(n!=-1):
                if(echiquier.cases[n].couleur=='blanc' or echiquier.ep==n):
                    if(n>55):
                        liste.append((pos1,n,'q'))
                        liste.append((pos1,n,'r'))
                        liste.append((pos1,n,'n'))
                        liste.append((pos1,n,'b'))
                    else:
                        liste.append((pos1,n,''))

            # Capture bottom right
            n=self.tab120[self.tab64[pos1]+11]
            if(n!=-1):
                if(echiquier.cases[n].couleur=='blanc' or echiquier.ep==n):
                    if(n>55):
                        liste.append((pos1,n,'q'))
                        liste.append((pos1,n,'r'))
                        liste.append((pos1,n,'n'))
                        liste.append((pos1,n,'b'))
                    else:
                        liste.append((pos1,n,''))
            
        return liste
        
    ####################################################################

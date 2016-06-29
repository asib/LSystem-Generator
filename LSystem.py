import math
import pygame
from pygame.locals import *

DRAW_LETTERS = [chr(i) for i in range(65, 71)]
FORWARD_LETTERS = [chr(i) for i in range(71, 77)]
NON_CONSTRUCTION_LETTERS = DRAW_LETTERS + FORWARD_LETTERS

class LSystem:
    '''
    *   A class for generating L-Systems from
    *   a given set of rule definitions.
    '''

    __mRules = {}             #  Dictionary holding all conversion rules
    __mAxiom = ''             #  Initial axiom
    __mCompleteLSys = ''      #  The L-System after calling lsys.GenerateLSystem(recurs)
    __mLineCoordinates = []   #  The list of line coordinates after calling lsys.GenerateLines(origin, angle, lineLength)
    __mLineLength = 0         #  The length of the lines when drawn.
    __mStartAngle = 0         #  The initial angle to draw with.
    
    def __init__(self):
        pass
    
    def SetAxiom(self, axiom):
        '''
        *   Set the axiom for the L-System.
        '''
        self.__mAxiom = axiom
        self.__mCompleteLSys = axiom
    
    def NewRule(self, rule):
        '''
        *   Takes a string of the format "X=X+Y-Z-Y+X".
        *
        *   Defines a new rule.
        '''
        self.__mRules[rule[0]] = rule[2:]
    
    def GetLSystem(self):
        '''
        *   Returns the completed LSystem.
        '''
        return self.__mCompleteLSys
    
    def GenerateLSystem(self, recursions):
        '''
        *   Produces L-System using axiom supplied at instantiation
        *   with 'recursions' number of recursions.
        '''
        self.__mCompleteLSys = self.__genLSys(self.__mAxiom, recursions)
    
    def __genLSys(self, axiom, recursions):
        '''
        *   Private method for generating L-System.
        *   Keeps self.__mAxiom intact.
        '''
        if recursions == 0:
            return axiom
        else:
            newAxiom = []
            for i in range(len(axiom)):
                if axiom[i] in self.__mRules and axiom[i] not in ['-', '+']:
                    newAxiom.append(self.__mRules[axiom[i]])
                else:
                    newAxiom.append(axiom[i])
            return self.__genLSys(''.join(newAxiom), (recursions - 1))
            
    def GetLines(self):
        '''
        *   Returns list of line coordinates.
        '''
        return self.__mLineCoordinates

    def GenerateLines(self, startPoint, angle, lineLength):
        '''
        *   Takes the origin of the draw, the initial angle to start
        *   drawing at, and the length of each line.
        *
        *   Populates self.__mLineCoordinates with the coordinates of
        *   all lines required to draw the L-System.
        '''
        self.__mLineLength = lineLength
        self.__mStartAngle = angle
        self.__mLineCoordinates = []
        stack = []
        for ch in self.__mCompleteLSys:
            if ch in self.__mRules:
                if ch in DRAW_LETTERS:
                    newLine = [startPoint]
                    startPoint = self.__findNextPoint(startPoint, angle, lineLength)
                    newLine.append(startPoint)
                    self.__mLineCoordinates.append(newLine)
                elif ch in FORWARD_LETTERS:
                    startPoint = self.__findNextPoint(startPoint, angle, lineLength)
                elif ch == '+':
                    angle = self.__turnLeft(angle)
                elif ch == '-':
                    angle = self.__turnRight(angle)
            elif ch == '[':
                stack.append([startPoint, angle])
            elif ch == ']':
                startPoint, angle = stack.pop()
    
    def __turnLeft(self, angle):
        '''
        *   Private drawing method.
        *   Increases draw angle by amount specified 
        *   when '+' rule was created.
        '''
        angle += math.radians(int(self.__mRules['+']))
        angle %= (2 * math.pi)
        return angle

    def __turnRight(self, angle):
        '''
        *   Private drawing method.
        *   Decreases draw angle by amount specified
        *   when '-' rule was created.
        '''    
        angle -= math.radians(int(self.__mRules['-']))
        angle %= (2 * math.pi)
        return angle

    def __findNextPoint(self, origin, angle, lineLength):
        '''
        *   Private drawing method.
        *   Returns the end point of a line.
        '''
        return (origin[0] + lineLength * math.cos(angle), origin[1] + lineLength * math.sin(angle))
        
    def PygameDraw(self, windowSize, color):
        '''
        *   Takes the size of the Pygame window,
        *   and the colour to use for the lines.
        *   Draws the LSystem using Pygame.
        '''
        pygame.init()
        windowSurfaceObj = pygame.display.set_mode(windowSize)
    
        running = True
        startPoint = self.__mLineCoordinates[0][0]
        redraw = False
    
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
            keys = pygame.key.get_pressed()
            if keys[K_LEFT]:
                startPoint = (startPoint[0] + 5, startPoint[1])
                redraw = True
            if keys[K_RIGHT]:
                startPoint = (startPoint[0] - 5, startPoint[1])
                redraw = True
            if keys[K_UP]:
                startPoint = (startPoint[0], startPoint[1] + 5)
                redraw = True
            if keys[K_DOWN]:
                startPoint = (startPoint[0], startPoint[1] - 5)
                redraw = True
            if keys[K_x]:
                self.__mLineLength += 0.2
                redraw = True
            if keys[K_z]:
                self.__mLineLength -= 0.2
                redraw = True
                
            if redraw:
                self.GenerateLines(startPoint, self.__mStartAngle, self.__mLineLength)

            windowSurfaceObj.fill((255,255,255))
            self.__drawLSystem(windowSurfaceObj, color)
            pygame.display.flip()
            
    def __drawLSystem(self, surface, color):
        '''
        *   Private drawing method.
        *   Draws each line segment produced
        *   after calling obj.GenerateLines(origin, angle, lineLength)
        '''
        for line in self.__mLineCoordinates:
            pygame.draw.line(surface, color, line[0], line[1], 1)

    @staticmethod
    def UnitTest():
        '''
        *   Unit test for LSystem class.
        '''
        ls = LSystem()
        ls.NewRule("F=F-F++F-F")
        ls.NewRule("+=60")
        ls.NewRule("-=60")
        ls.SetAxiom("-F++F++F")
        ls.GenerateLSystem(5)
        ls.GenerateLines((320,480), 0, 4)
        ls.PygameDraw((1024,768),(255,0,0))
        
if __name__ == '__main__':
    LSystem.UnitTest()
''' Generate plant
myLSys = LSystem()
myLSys.NewRule("X=F-[[X]+X]+F[+FX]-X")
myLSys.NewRule("F=FF")
myLSys.NewRule("+=25")
myLSys.NewRule("-=25")
myLSys.SetAxiom("X")
myLSys.GenerateLSystem(5)
myLSys.GenerateLines((512, 768), 270 * (math.pi/180), 5)
myLSys.PygameDraw((1024, 768), (255, 0, 0))
'''

''' Generate Quadratic Koch Island
myLSys = LSystem()
myLSys.NewRule("F=F+L-FF+F+FF+FL+FF-L+FF-F-FF-FL-FFF")
myLSys.NewRule("L=LLLLLL")
myLSys.NewRule("+=90")
myLSys.NewRule("-=90")
myLSys.SetAxiom("F+F+F+F")
myLSys.GenerateLSystem(3)
myLSys.GenerateLines((320, 480), 3 * math.pi / 2, 4)
myLSys.PygameDraw((1024, 768), (255, 0, 0))
'''

''' Generate Koch Snowflake
ls = LSystem()
ls.NewRule("F=F-F++F-F")
ls.NewRule("+=60")
ls.NewRule("-=60")
ls.SetAxiom("-F++F++F")
ls.GenerateLSystem(5)
ls.GenerateLines((320,480), 0, 4)
ls.PygameDraw((1024,768),(255,0,0))
'''

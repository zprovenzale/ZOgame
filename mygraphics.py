# JORourke
# mygraphics.py: Various graphics functions to
# augment Zelle's graphics.py
# Version: 7Nov2019

from graphics import *
from random import randint,uniform
import math


def RegularPolygon( xcent,ycent, r, n ):
    '''Returns a regular polygon, centered on xcent,ycent.  
       r = radius, n = number of sides
    '''
    Lpts = [] # Grow list of points
    p0 = Point( xcent,ycent ) # center
    p = Point( xcent + r, ycent ) # 1st point
    for i in range(1,n+1):
        angdeg = round( 360/n )
        p = RotatePoint( p, angdeg, p0 )
        Lpts.append( p )

    poly = Polygon( Lpts )
    # Draw in main() or elsewhere. Returns polygon object.
    return poly

def RotatePoint( p, angdeg, pcent ):
    '''
    Rotate the point object p about center point object pcent) by angdeg in degrees.
    Counterclockwise rotation is positive; clockwise rotation negative.
    Returns the rotated point object prot.
    Needs import math.
    '''

    x = p.getX()
    y = p.getY()
    x0 = pcent.getX()
    y0 = pcent.getY()
    # (xt,yt) is the point (x,y) translated so that (x0,y0) is the origin.
    # Convert to float for subsequent computation, just in case
    xt = float( x - x0 )
    yt = float( y - y0 )

    # Convert the angle into radians: angrad.
    angrad = angdeg * math.pi / 180.
    
    cos = math.cos( angrad )
    sin = math.sin( angrad )

    # These are the rotation equations:
    xr = xt * cos - yt * sin
    yr = xt * sin + yt * cos

    # Now translate back.
    xr = xr + x0
    yr = yr + y0

    prot = Point( xr, yr )

    return prot

def RandColor( ):
    '''Generate a random color and return it'''
    r = randint( 0, 255 )
    g = randint( 0, 255 )
    b = randint( 0, 255 )
    color = color_rgb( r, g, b )
    return color

def MyOval( xcent, ycent, width2, height2 ):
    '''Oval centered on (xcent,ycent), with "radii"
    half-width width2 and half-height height2.
    Returns oval object.'''
    # Construct p1 & p2
    p1 = Point( xcent-width2, ycent-height2 )
    p2 = Point( xcent+width2, ycent+height2 )
    oval = Oval( p1, p2 )
    return oval

def MyRectangle( xcent, ycent, width2, height2 ):
    '''Rectangle centered on (xcent,ycent), with "radii"
    half-width width2 and half-height height2.
    Returns rect object.'''
    # Construct p1 & p2
    p1 = Point( xcent-width2, ycent-height2 )
    p2 = Point( xcent+width2, ycent+height2 )
    rect = Rectangle( p1, p2 )
    return rect

# CreateButton will be replaced by class Button eventually...
def CreateButton( win, xcent, ycent, width2, height2, color, slabel ):
    '''Create a rectangle with text to serve as a button.
    Returns the rect object'''
    # Rectangle:
    rect = MyRectangle( xcent, ycent, width2, height2 )
    rect.setFill( color )
    rect.draw( win )

    # Text placement requires center pt:
    pcent = Point( xcent, ycent )
    text = Text( pcent, slabel )
    text.draw( win )
    return rect

def PtInRect( p, rect ):
    '''Is point p inside the rectangle?
       Both p and rect are objects.
    '''
    # Extract the pt coords:
    xp,yp = p.getX(),p.getY()

    # Extract the rect corners:
    p1 = rect.getP1()
    x1,y1 = p1.getX(),p1.getY()
    p2 = rect.getP2()
    x2,y2 = p2.getX(),p2.getY()
    # Assume p1 is lower-left, p2 upper-right

    # In the rect when between both x&y are in:
    if (x1 <= xp <= x2) and (y1 <= yp <= y2):
        return True
    else:
        return False

def PtInCirc( p, circ ):
    '''Is point p inside the circle?
       Both p and circ are objects.
    '''
    # Extract the pt coords:
    xp,yp = p.getX(),p.getY()

    # Extract the circ data:
    r = circ.getRadius()
    pcent = circ.getCenter()
    xc,yc = pcent.getX(),pcent.getY()
    

    # Pythagorean Theorem:
    if (xc-xp)**2 + (yc-yp)**2 < r*r:
        # Strictly inside (not on boundary)
        return True
    else:
        return False

def MoveObjTo( obj, xnew,ynew ):
    '''Move the obj to new coords. No return value.
       Similar to Zelle's move() method, except this
       moves to specific coords.
    '''
    # Extract the object center coords:
    pcent = obj.getCenter( )
    xc,yc = pcent.getX(), pcent.getY()

    # Compute displacement: from current to new:
    dx = xnew - xc
    dy = ynew - yc

    obj.move( dx, dy )
    

    
def WrapObj( obj, w ):
    '''Wrap the coords if outside +/- w.
    Assumes window coords are (-w,-w,+w,+w)
    Move obj to wrapped coords.
    '''
    # Extract the object center coords:
    pcent = obj.getCenter( )
    xc,yc = pcent.getX(), pcent.getY()

    # Initialize new coords to old (in case no wrapping):
    xnew,ynew = xc,yc

    # Note: Full width of window is 2*w.
    # Wrap x, horiz:
    if xc > w:
        xnew = xc - 2*w
    elif xc < -w:
        xnew = xc + 2*w

    # Wrap y, vertical
    if yc > w:
        ynew = yc - 2*w
    elif yc < -w:
        ynew = yc + 2*w

    # If wrapping, then move:
    if (xnew != xc) or (ynew != yc):
        MoveObjTo( obj, xnew,ynew )

def Reflect( circ, w, sx, sy):
    '''Reflects sx,sy if outside of +/-w.
       Angle of incidence = angle of reflection.
       Accomplished by negating speeds.
    '''
    cent = circ.getCenter( )
    xc,yc = cent.getX( ), cent.getY( )
    xnew, ynew = xc,yc

    # If outside, reset to boundary,
    # as well as reflect speed.
    if xc > w:
        xnew = w
        sx = -sx
    elif xc < -w:
        xnew = -w
        sx = -sx

    if yc > w:
        ynew = w
        sy = -sy
    elif yc < -w:
        ynew = -w
        sy = -sy

    # If reflection, then move:
    if (xnew != xc) or (ynew != yc):
        MoveObjTo( circ, xnew,ynew )

    # Need to return new speeds:
    return sx,sy
    
def ReflectRect( circ, rect, sx, sy):
    '''Reflect the moving circ from the fixed rect.
       the circ is moving at speed sx,sy. Returns new sx,sy.
       Only reflects from top and bot of rect, not sides.
       So keep rectangle thin w.r.t. ball/circ.
    '''
    # Extract data from circ & rect:
    cent = circ.getCenter()
    r = circ.getRadius()
    cx,cy = cent.getX(),cent.getY()
    xnew,ynew = cx,cy
    p1,p2 = rect.getP1(), rect.getP2()
    # Coords of SW corner & NE corner:
    x1,y1 = p1.getX(), p1.getY()
    x2,y2 = p2.getX(), p2.getY()

    # Effectively fatten the rect by r in all dimensions
    if ((x1-r) < cx < (x2+r)) and ((y1-r) < cy < (y2+r)):
        # Collision. Reflect from top or bot (not sides)
        if sy < 0: # moving down
            sy = -sy
            ynew = y2+r # top
        elif sy > 0: # moving up
            sy = -sy
            ynew = y1-r # bot

    if (xnew != cx) or (ynew != cy):
        MoveObjTo( circ, xnew, ynew )
    return sx,sy 
    



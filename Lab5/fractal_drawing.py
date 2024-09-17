"""Classes for drawing some fractals. """
from tkinter import *
from fractal_canvas import FractalCanvas
import math

# using a global counter is handy when keeping track
# of the number of things that are drawn by multiple levels
# of recursive functions.
COUNTER = 0


# To draw quickly change the TRACER_SETTING from None to 0.
# This will turn off animation but still refresh every step.
# Changing 0 to an integer n will skip n steps of the drawing and speed up
# even more. For example self.turtleScreen.tracer(9) will skip 9 frames
# and effectively update every 10th.
TRACER_SETTING = 0


class SierpinskiTriangle(FractalCanvas):
    """Implements draw method so that a Sierpinski triangle is drawn."""

    def draw(self, width, height):
        """Sets up various bits for the initial draw."""
        # Setup colour gradient from dark orange-brown to light
        step = 255.0 / max(1, self.levels)
        colour_vals = [1 * step * k for k in range(self.levels + 1)]
        colours = [(int(k), int(k /2), int(k /4)) for k in colour_vals]

        # Keep the triangle bounded inside a square
        t_size = min(width, height)

        # And keep it centred
        outer_triangle = [
            ((width / 2) - (t_size / 2), -(height / 2) - (t_size / 2)),
 (width / 2, (-height / 2) + (t_size / 2)),
 ((width / 2) + (t_size / 2), -(height / 2) - (t_size / 2))]

        # Start recursively drawing the triangle
        global COUNTER
        COUNTER = 0
        self.turtle.reset()
        self.turtleScreen.tracer(TRACER_SETTING)
        self.turtle.penup()
        self.draw_triangle(outer_triangle, colours, self.levels)

    def draw_triangle(self, points, colours, level):
        """
        Recursively draws the Sierpinski triangle.
        'points' is a list of three (x,y) tuples containing
        the co-ordinates of where to draw the triangle.
        'level' is which level of the triangle we're up to
           (where 0 is the innermost level).
        """
        global COUNTER

        # Set the fill colour
        self.turtle.fillcolor(colours[level])

        # Draw the triangle
        self.turtle.begin_fill()
        self.turtle.goto(*points[0])   # Move to the first point
        self.turtle.pendown()          # Put the turtle pen down
        self.turtle.goto(*points[1])   # Draw move round 3 points of triangle
        self.turtle.goto(*points[2])
        self.turtle.goto(*points[0])
        self.turtle.penup()            # Lift the pen up
        self.turtle.end_fill()         # Finish the colour fill

        self.update_screen()

        # If we still have more levels to draw...
        if level > 0:
            # Calculate the position of the three inner triangles and recursively
            # draw them and their inner triangles
            point0, point1, point2 = points

            inner_points = [point0,
                            self.midpoint(point0, point1),
                            self.midpoint(point0, point2)]
            self.draw_triangle(inner_points, colours, level - 1)

            inner_points = [point1,
                            self.midpoint(point0, point1),
                            self.midpoint(point1, point2)]
            self.draw_triangle(inner_points, colours, level - 1)

            inner_points = [point2,
                            self.midpoint(point2, point1),
                            self.midpoint(point0, point2)]
            self.draw_triangle(inner_points, colours, level - 1)

    def midpoint(self, point0, point1):
        """Returns a tuple of the midpoint between two (x,y) point tuples."""
        return ((point0[0] + point1[0]) / 2.0,
                (point0[1] + point1[1]) / 2.0)


# -------------------------------------------------------------------------
class KochCurve(FractalCanvas):
    """Implements draw method so that a Koch curve is drawn."""

    # angle is a class level constant
    # You can access angle by using KochCurve.angle
    angle = 60

    # Try an angle of 80 for fun results:)
    # An angle of -60 will give an inverse KochCurve
    #    which makes for a cool snowflake

    def draw(self, width, height):
        """ Non recursive draw method.
        This method will make the first call to the recursive method - draw_koch
        """
        # Reset the turtle
        self.turtle.reset()
        self.turtleScreen.tracer(TRACER_SETTING)

        # Position the turtle at the centre-left of the screen
        self.turtle.penup()
        self.turtle.goto(0, -height / 2)
        self.turtle.pendown()

        # call the recursive draw_koch function
        self.draw_koch(self.levels, width)
        self.turtleScreen.update()

    def draw_koch(self, level, length):
        """Recursive function.
        At level zero just draws a forward line of given length.
        At higher levels does the following:
           divides length by 3
           draws a (level-1) koch_curve then turns KochCurve.angle degrees left
           draws a (level-1) koch_curve then turns 2*KochCurve.angle degrees right
           draws a (level-1) koch_curve then turns KochCurve.angle degress left
           draws a (level-1) koch_curve.
        """
        if level == 0:
            self.turtle.forward(length)
            self.update_screen()
        else:
            length = length / 3
            # ---start student section---
            pass
            # ===end student section===


# -------------------------------------------------------------------------
class KochSnowflake(KochCurve):
    """
    Implements draw method so that a Koch snowflake is drawn.
    Note: inherits draw_koch so
    can use self.draw_koch(self.levels, length) to draw a koch curve.
    """

    def draw(self, width, height):
        # Reset the turtle
        self.turtle.reset()
        self.turtleScreen.tracer(TRACER_SETTING)

        # Position the turtle just below the centre-top of the screen
        self.turtle.penup()
        self.turtle.goto(width / 2, -height / 12)
        self.turtle.pendown()
        self.turtle.right(60)

        if self.levels <= 2:
            length = math.sqrt((width / 3)**2 + (height / 3)**2)
        else:
            length = math.sqrt((width / 2)**2 + (height / 2)**2)

        KochCurve.angle = 60
        # Now draw three kochcurves, turning 120 degrees right in between
        # Note you can use self.draw_koch(....) to draw each koch curve
        # as it is inherited from the super class
        # ---start student section---
        pass
        # ===end student section===


# ------------------------------------------------------------------------------
class KochStarFlake(KochCurve):
    """Extra bonus drawing:)
        Implements draw method so that a square snowflake is drawn.
        Try changing number of turns to 4, 5 or more for some cool shapes
    """

    def draw(self, width, height):
        # Reset the turtle
        self.turtle.reset()
        self.turtleScreen.tracer(TRACER_SETTING)

        # Position the turtle just below the top centre of the screen
        self.turtle.penup()
        self.turtle.goto(width / 2, -height / 8)
        self.turtle.pendown()
        self.turtle.right(45)

        # The interesting bits
        # --------------------
        KochCurve.angle = 80  # makes for starry curves
        number_of_turns = 6   # must be an int

        # squash to fit in window
        if self.levels <= 2:
            length = math.sqrt((width / 3)**2 + (height / 3)**2)
        else:
            length = (math.sqrt((width / 3)**2 + (height / 3)**2) *
                      self.levels / number_of_turns * 3)

        # Now draw number_of_turns koch_curves,
        #    turning 360//number_of_turns right in between
        # ---start student section---
        pass
        # ===end student section===
        self.turtleScreen.update()


# -------------------------------------------------------------------------
class HilbertCurve(FractalCanvas):
    """Implements draw method so that a Hilbert curve is drawn."""

    def draw(self, width, height):
        """ Base draw method
        Sets up sizing and calls draw_hilbert
        which is the recusive drawing method
        """
        # Reset the turtle
        self.turtle.reset()
        self.turtleScreen.tracer(None)

        # Scale the line length such that the entire curve fits on the screen
        total_length = 2 ** self.levels - (1.0 / 2 ** self.levels)
        line_length = width / total_length

        # start drawing recursively with level = highest level
        self.draw_hilbert(self.levels, line_length, 90)
        self.update_screen()

    def draw_hilbert(self, level, line_length, angle):
        """ This is the recursive drawing method for the hilbert curve"""
        # note, base case is level=0 and nothing is done in this case.
        if level > 0:
            # ---start student section---
            pass
            # ===end student section===


# -------------------------------------------------------------------------
class DragonCurve(FractalCanvas):
    """Implements draw method so that a dragon curve is drawn."""

    def draw(self, width, height):
        """ Non recursive method to get things started """
        # Reset the turtle
        self.turtle.reset()
        self.turtleScreen.tracer(TRACER_SETTING)

        # Position the turtle at the centre of the screen
        self.turtle.penup()
        self.turtle.goto(width / 4, -height / 3)
        self.turtle.pendown()
        # Call the recursive drawing funciton
        self.draw_dragon(self.levels, width / 2, 45)
        self.turtleScreen.update()

    def draw_dragon(self, level, length, angle):
        """Recursive method for drawing dragon curves."""
        if level == 0:
            self.turtle.forward(length)
            self.update_screen()
            return
        else:
            # ---start student section---
            pass
            # ===end student section===


def main():
    """ The main event! """
    # Setup tk canvas
    global COUNTER
    root = Tk()
    frame = Frame(root)
    frame.pack(fill=BOTH, expand=YES)

    # NOTE:
    # Try drawing the 0, 1, and 2 level versions of all of these by hand
    # This will give you a feeling for how they are constructed

    # IMPORTANT NOTE:
    # Only run one fractal at a time, or you will get crazy stacking...
    # If you run without calling any drawings then your shell will be stuck waiting
    # so click on Options - Restart Shell from the shell menu bar.

    # Draw a SierpinskiTriangle to 0 level
    # Drawing level 0 is a good idea as it shows you the
    # base unit when drawing the fractal.
    # # t = SierpinskiTriangle(frame, 0)

    # We draw a 5 to start with to see the overall shape
    # triangle = SierpinskiTriangle(frame, 7)

    # Draw a KochCurve to 0 level
    # Try more levels after you have seen the base case
    # k = KochCurve(frame, 3)


    # Draw full snowflake at level 0
    # Try more levels after you have seen the base case
    f = KochSnowflake(frame, 3)



    # Draw a dragon curve at level 0
    # Try more levels after you have seen the base case
    # d = DragonCurve(frame, 0)

    # k = HilbertCurve(frame, 1)

    root.mainloop()


if __name__ == '__main__':
    main()

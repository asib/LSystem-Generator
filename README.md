LSystemGenerator
================

Python class for generating and drawing LSystems


Generation
------------------

To import module, call `from LSystem import LSystem`.

To create an LSystem object, call `obj = LSystem()`.

To add a new rule, call `obj.NewRule("F=FFXYFF")`.

The parser recognises letters A-F as draw forward letters, and G-L as move forward without drawing letters.
All other letters have no effect on the drawing of the LSystem.

Use `obj.NewRule("+=ANGLE")` and `obj.NewRule("-=ANGLE")` to define left and right turns, where 'ANGLE' is the angle to turn.

Use `obj.SetAxiom("F")` to set the starting point for the LSystem.

To generate the LSystem, call `obj.GenerateLSystem(recursions)` where 'recursions' is the number of recursions to execute.

To generate the lines, call `obj.GenerateLines(origin, angle, lineLength)` where 'origin' is the start point of the drawing, 'angle' is the angle to start drawing at, and 'lineLength' is the length of each line segment.

Drawing
---------------

Call `obj.PygameDraw(windowSize, color)` to draw the lines using Pygame, on a window of size 'windowSize', with lines of colour 'color'. Use the arrow keys to move around, the 'Z' key to zoom out, and the 'X' key to zoom in.

Other methods
-------------

Call `obj.GetLSystem()` to print out the text version of the LSystem produced by `obj.GenerateLSystem(recursions)`.


Call `obj.GetLines()` to print out the list of line coordinates produced by `obj.GenerateLines(origin, angle, lineLength)`.

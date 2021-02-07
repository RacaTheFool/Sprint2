"""
This code has been altered to use Sprites.

Editor: Dylan Furrows

"""
import arcade
import math
import random

from abc import ABC
from abc import abstractmethod

# These are Global constants to use throughout the game
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 500

RIFLE_WIDTH = 100
RIFLE_HEIGHT = 20
RIFLE_COLOR = arcade.color.DARK_RED
START_RIFLE_ANGLE = 45
RIFLE_SCALE = 0.1

BULLET_RADIUS = 3
BULLET_COLOR = arcade.color.BLACK_OLIVE
BULLET_SPEED = 15
BULLET_SCALE = 0.01

TARGET_RADIUS = 20
TARGET_COLOR = arcade.color.CARROT_ORANGE
TARGET_SCALE = 0.1

DRAW_START = 0

BACKGROUND_CHANGE_DELAY = 4




class Game(arcade.Window):
   """
   This is where the magic happens.
   Everything for running the game is found in here.
   """

   def __init__(self):
      """
      Sets up the initial conditions of the game
      :param width: Screen width
      :param height: Screen height
      """
      super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT)

      # Sprite list variables
      self.rifle_list = arcade.SpriteList()
      self.bullet_list = arcade.SpriteList()
      self.target_list = arcade.SpriteList()
      
      # Player/Rifle data
      self.score = 0
      self.rifle_sprite = arcade.Sprite("gray_rectangle.png", RIFLE_SCALE)
      self.rifle_sprite.center_x = 0
      self.rifle_sprite.center_y = 0
      self.rifle_sprite.angle = 45
      self.rifle_list.append(self.rifle_sprite)

      # My added background color measurement variables
      self.fade_in = True
      self.make_blue = 255 * BACKGROUND_CHANGE_DELAY

      arcade.set_background_color(arcade.color.WHITE)

   def on_draw(self):
      """
      Called automatically by the arcade framework.
      Handles the responsibility of drawing all elements.
      """

      # clear the screen to begin drawing
      arcade.start_render()
      
      # My added background change
      if self.fade_in:
         self.make_blue -= 1
         arcade.set_background_color((self.make_blue // BACKGROUND_CHANGE_DELAY, self.make_blue // BACKGROUND_CHANGE_DELAY, 255))
         if (self.make_blue // BACKGROUND_CHANGE_DELAY) <= 150:
            self.fade_in = False
      else:
         self.make_blue += 1
         arcade.set_background_color((self.make_blue // BACKGROUND_CHANGE_DELAY, self.make_blue //BACKGROUND_CHANGE_DELAY, 255))
         if (self.make_blue // BACKGROUND_CHANGE_DELAY) >= 255:
            self.fade_in = True
            

      # draw all sprites
      self.bullet_list.draw()
      self.rifle_list.draw()
      self.target_list.draw()

      self.draw_score()

   def draw_score(self):
      """
      Puts the current score on the screen
      """
      score_text = "Score: {}".format(self.score)
      start_x = 10
      start_y = SCREEN_HEIGHT - 20
      arcade.draw_text(score_text, start_x=start_x, start_y=start_y, font_size=12, color=arcade.color.NAVY_BLUE)

   def create_target(self):
      """
      Creates a new target
      """
      # Create the target
      target = arcade.Sprite("orange_circle.png", TARGET_SCALE)
      
      # Have the target start from somewhere along the edge
      # of the screen
      target.center_x = 0.0
      target.center_y = random.uniform(SCREEN_HEIGHT / 2, SCREEN_HEIGHT)

      # Give it a velocity in a random direction and speed
      target.change_x = random.uniform(1, 5)
      target.change_y = random.uniform(-2, 5)

      # Add the new target to the target list
      self.target_list.append(target)
     
   def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
      # set the rifle angle in degrees
      self.rifle_sprite.angle = self._get_angle_degrees(x, y)
      self.rifle_list.update()

   def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
      """ Fire! """
      # Get the angle
      angle = self._get_angle_degrees(x, y)

      # Create the bullet
      bullet = arcade.Sprite("black_triangle.png", BULLET_SCALE)
      
      # Have it start in the center of the rifle
      bullet.center_x = 0
      bullet.center_y = 0

      # Give the bullet it's angle
      bullet.angle = angle

      # Adjust it's velocity accordingly
      bullet.change_x = math.cos(angle) * BULLET_SPEED
      bullet.change_y = math.sin(angle) * BULLET_SPEED
      
      # Add it to the list of bullets
      self.bullet_list.append(bullet)

   def _get_angle_degrees(self, x, y):
      """
      Gets the value of an angle (in degrees) defined
      by the provided x and y.
      Note: This could be a static method, but we haven't
      discussed them yet...
      """
      # get the angle in radians
      angle_radians = math.atan2(y, x)

      # convert to degrees
      angle_degrees = math.degrees(angle_radians)

      return angle_degrees

   def on_update(self, delta_time):
      """ Movement and game logic """

      # decide if we should start a target
      if random.randint(1, 50) == 1:
         self.create_target()


      # Call update on all sprites
      self.bullet_list.update()
      self.target_list.update()
      self.rifle_list.update()

      # Loop through each bullet
      for bullet in self.bullet_list:

         # Check this bullet to see if it hit a target
         hit_list = arcade.check_for_collision_with_list(bullet, self.target_list)

         # If it did, get rid of the bullet
         if len(hit_list) > 0:
               bullet.remove_from_sprite_lists()

         # For every target we hit, add to the score and remove the targets
         for target in hit_list:
               target.remove_from_sprite_lists()
               self.score += 1

         # If the bullet flies off-screen, remove it.
         if bullet.bottom > self.height or bullet.top < 0 or bullet.right < 0 or bullet.left > self.width:
               bullet.remove_from_sprite_lists()

      # Check if any targets have flown off-screen.
      # If so, remove it.
      for target in self.target_list:
         if target.bottom > self.height or target.top < 0 or target.right < 0 or target.left > self.width:
               target.remove_from_sprite_lists()


# Creates the game and starts it going
window = Game()
arcade.run()

from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1' # Squish 'hello from pygame community'
import pygame
import eclipse_calculation
from datetime import datetime


# date_input is a string to be converted into a datetime
def is_valid_date(date_input):
  try:
    datetime.strptime(date_input, '%m/%d/%Y')
    return True
  except ValueError:
    print('Incorrect date format, should be (mm/dd/yyyy)')
    return False


def run_animation():
  # Setup 
  pygame.init()
  screen = pygame.display.set_mode((500,500)) # set the screen 
  pygame.display.set_caption('Solar Eclipse Calculator') # add caption
  clock = pygame.time.Clock() # create game clock (looks like this controlls frame-rate(?) *shrug*)
 
  # State managment variable
  # Used to show the different itterations (versions) of the program
  counter = 0

  # Create button
  font = pygame.font.Font(None, 20) # font object for button
  decrement_button_surface = pygame.Surface((75, 50)) # Create a surface for the button
  text = font.render("Version -1", True, (0, 0, 0))
  decrement_text_rect = text.get_rect(center=(decrement_button_surface.get_width()/2, decrement_button_surface.get_height()/2))

  # Create a pygame.Rect object that represents the button's boundaries
  button_rect = pygame.Rect(10, 440, 75, 50)

  # Create button
  increment_button_surface = pygame.Surface((75, 50)) # Create a surface for the button
  increment_text = font.render("Version +1", True, (0, 0, 0))
  increment_text_rect = text.get_rect(center=(increment_button_surface.get_width()/2, increment_button_surface.get_height()/2))

  # Create a pygame.Rect object that represents the button's boundaries
  increment_button_rect = pygame.Rect(85, 440, 75, 50)

  # Create input box
  input_box = pygame.Rect(280, 450, 100, 32)
  color_inactive = pygame.Color('dodgerblue2')
  color_active = pygame.Color('black')
  text_box_color = color_inactive
  active = False
  text_box = '(mm/dd/yyyy)'

  # input date variable
  date_input = None

  # invalid input
  invalid_input = False



  # sun coordinates & velocity
  sun_x, sun_y = 173,215
  sun_x_velocity = 19
  sun_y_velocity = -19

  # moon coordinates & velocity
  moon_x, moon_y = 150,250
  moon_x_velocity = -19
  moon_y_velocity = 0

  # big moon coordinates
  big_moon_x = 600
  big_moon_y = 600
  big_moon_x_velocity = 0
  big_moon_y_velocity = 0

  frames = 0

  while True: # During the animation
    for events in pygame.event.get(): # Check if game closed & quit
      if events.type == pygame.QUIT:
        pygame.quit()
        quit()

          # Check for the mouse button down event
      if events.type == pygame.MOUSEBUTTONDOWN and events.button == 1: # if button pressed
        # Call the on_mouse_button_down() function
        if button_rect.collidepoint(events.pos):  # if mouse over button
          counter -= 1
          if counter < 0:
            counter = 0
          print("counter:", counter)
        elif increment_button_rect.collidepoint(events.pos):  # if mouse over button
          counter += 1
          if counter > 4:
            counter = 4
          print("counter:", counter)
        
        #input box button
        if input_box.collidepoint(events.pos): # if mouse over input box
            # Toggle the active variable.
            active = not active
            text_box = ''
        else:
            active = False
            invalid_input = False
            lune_data = None

            text_box = '(mm/dd/yyyy)'
        # Change the current color of the input box.
        text_box_color = color_active if active else color_inactive

      #record user date input
      if events.type == pygame.KEYDOWN:
        if active:
          if events.key == pygame.K_RETURN:
            date_input = text_box
            text_box = '(mm/dd/yyyy)' # reset default display

            lune_data = None    # reset lune & big moon
            big_moon_x = 600
            big_moon_y = 600

            if not is_valid_date(date_input):
              invalid_input = True
              date_input = None
            else:
              invalid_input = False

          elif events.key == pygame.K_BACKSPACE:
            text_box = text_box[:-1]
          else:
            text_box += events.unicode


    # initial version (bouncing sun)
    if (counter == 0):
      screen.fill('sky blue') # screen background
      pygame.draw.circle(screen, 'yellow', (sun_x,sun_y), 20) # draw the sun
      
      sun_x += sun_x_velocity
      sun_y += sun_y_velocity

      if sun_x > 480 or sun_x < 20:   # move sun around screen
        sun_x_velocity *= -1
      if sun_y > 480 or sun_y < 20:
        sun_y_velocity *= -1

    # Added a moon
    if (counter == 1):
      screen.fill('sky blue') # screen background
      pygame.draw.circle(screen, 'yellow', (sun_x,sun_y), 20) # draw the sun
      pygame.draw.circle(screen, 'white', (moon_x,moon_y), 20) # draw the moon

      
      sun_x += sun_x_velocity
      moon_x += moon_x_velocity

      if sun_x > 480 or sun_x < 20:   # move sun around screen
        sun_x_velocity *= -1
      if moon_x > 480 or moon_x < 20:
        moon_x_velocity *= -1

    # Moved sun to center screen
    if (counter == 2):
      screen.fill('sky blue') # screen background
      pygame.draw.circle(screen, 'yellow', (sun_x,250), 20) # draw the sun
      pygame.draw.circle(screen, 'white', (moon_x,moon_y), 20) # draw the moon

      
      sun_x += sun_x_velocity   # move sun around screen
      moon_x += moon_x_velocity

      if sun_x > 480 or sun_x < 20:   # bounce off the walls
        sun_x_velocity *= -1
      if moon_x > 480 or moon_x < 20:
        moon_x_velocity *= -1

    # Added text input & display calculation results 
    if (counter == 3):
      # Todo: change 15ish lines below to moon covering sun animation
      screen.fill('sky blue') # screen background

      pygame.draw.circle(screen, 'yellow', (sun_x,250), 20) # draw the sun
      pygame.draw.circle(screen, 'white', (moon_x,moon_y), 20) # draw the moon

      
      sun_x += sun_x_velocity   # move sun around screen
      moon_x += moon_x_velocity

      if sun_x > 480 or sun_x < 20:   # bounce off the walls
        sun_x_velocity *= -1
      if moon_x > 480 or moon_x < 20:
        moon_x_velocity *= -1
  
      # Render the text_box text.
      text_font = pygame.font.Font(None, 32)
      txt_surface = text_font.render(text_box, True, text_box_color)

      # Resize the box if the text is too long.
      width = max(200, txt_surface.get_width()+10)
      input_box.w = width

      # Display the text.
      screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
      pygame.draw.rect(screen, text_box_color, input_box, 2)

      if invalid_input: # display invalid
        invalid_input_surface = text_font.render("invalid date", True, 'red')
        screen.blit(invalid_input_surface, (350, 420))
      
      if (date_input != None): # If there's a valid date
        date_input = datetime.strptime(date_input, '%m/%d/%Y') # format it
        date_input = datetime(date_input.year, date_input.month, date_input.day, 0, 0, 0) # beginning of day
        lune_data = eclipse_calculation.calc_lune_percentage(date_input) # calculate eclipse peak & time

        date_input = None # clear input
      
      if (lune_data != None): #if we calculated an eclipse
        lune_percent_surface = text_font.render("Eclipse percent: " + lune_data[0], True, 'black') # format percent
        lune_time_surface = text_font.render("At: " + lune_data[1], True, 'black') # format time / date

        screen.blit(lune_percent_surface, (250, 390))   # display both
        screen.blit(lune_time_surface, (200, 420))

    # Animated moon to cover the sun match calculated %eclipsed result (not geometircally accurate)
    if (counter == 4):
      screen.fill('sky blue') # screen background

      pygame.draw.circle(screen, 'yellow', (250,175), 150) # draw the sun
      pygame.draw.circle(screen, 'white', (big_moon_x,big_moon_y), 145) # draw the moon off screen
  
      # Render the text_box text.
      text_font = pygame.font.Font(None, 32)
      txt_surface = text_font.render(text_box, True, 'black')

      # Resize the box if the text is too long.
      width = max(200, txt_surface.get_width()+10)
      input_box.w = width

      # Display the text.
      screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
      pygame.draw.rect(screen, text_box_color, input_box, 2)

      if invalid_input: # display invalid
        invalid_input_surface = text_font.render("invalid date", True, 'red')
        screen.blit(invalid_input_surface, (350, 420))
      
      if (date_input != None): # If there's a valid date
        date_input = datetime.strptime(date_input, '%m/%d/%Y') # format it
        date_input = datetime(date_input.year, date_input.month, date_input.day, 0, 0, 0) # beginning of day
        lune_data = eclipse_calculation.calc_lune_percentage(date_input) # calculate eclipse peak & time

        date_input = None # clear input
      
      if (lune_data != None): #if we calculated an eclipse
        lune_percent_surface = text_font.render("Eclipse percent: " + lune_data[0], True, 'black') # format percent
        lune_time_surface = text_font.render("At: " + lune_data[1], True, 'black') # format time / date

        screen.blit(lune_percent_surface, (250, 390))   # display both
        screen.blit(lune_time_surface, (200, 420))

        lune = float(lune_data[0])
        y_endpoint = 475 - (300 * (lune/100)) # calculate endpoint based on percent

        
        if(big_moon_x > 250): # moon x axis animation
          big_moon_x_velocity = -4
        else:
          big_moon_x = 250
          big_moon_x_velocity = 0

        if(big_moon_y > y_endpoint): # moon y axis animation
          big_moon_y_velocity = -((600 - y_endpoint) / 88)
        else:
          big_moon_y = y_endpoint
          big_moon_y_velocity = 0

        big_moon_x += big_moon_x_velocity
        big_moon_y += big_moon_y_velocity
      


    # Check if the mouse is over the button. This will create the button hover effect
    if button_rect.collidepoint(pygame.mouse.get_pos()):
      pygame.draw.rect(decrement_button_surface, (127, 255, 212), (1, 1, 148, 48))
    else:
      pygame.draw.rect(decrement_button_surface, (0, 0, 0), (0, 0, 150, 50))
      pygame.draw.rect(decrement_button_surface, (255, 255, 255), (1, 1, 148, 48))
      pygame.draw.rect(decrement_button_surface, (0, 0, 0), (1, 1, 148, 1), 2)
      pygame.draw.rect(decrement_button_surface, (0, 100, 0), (1, 48, 148, 10), 2)
    
        # Check if the mouse is over the button 2. This will create the button hover effect
    if increment_button_rect.collidepoint(pygame.mouse.get_pos()):
      pygame.draw.rect(increment_button_surface, (127, 255, 212), (1, 1, 148, 48))
    else:
      pygame.draw.rect(increment_button_surface, (0, 0, 0), (0, 0, 150, 50))
      pygame.draw.rect(increment_button_surface, (255, 255, 255), (1, 1, 148, 48))
      pygame.draw.rect(increment_button_surface, (0, 0, 0), (1, 1, 148, 1), 2)
      pygame.draw.rect(increment_button_surface, (0, 100, 0), (1, 48, 148, 10), 2)


    decrement_button_surface.blit(text, decrement_text_rect) # Show the button text
    increment_button_surface.blit(increment_text, increment_text_rect) # Show the button text

    screen.blit(decrement_button_surface, (button_rect.x, button_rect.y))  # Draw the button on the screen
    screen.blit(increment_button_surface, (increment_button_rect.x, increment_button_rect.y))  # Draw the button on the screen


    pygame.display.update()
    clock.tick(30)


def main():
  run_animation()


if __name__ == "__main__":
    main()
  
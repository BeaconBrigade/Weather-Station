#Popup Window
#Jan 5, 2021
#Ryan Cullen

from guizero import App, PushButton, yesno, question, warn, TextBox, Text, Window, info, Picture, Box #Guizero Functions.
from time import sleep #Timeout.
from csv import reader, writer #Working with files.
from requests import get #Call API.
import os # secrets

app = App() 
app.hide() #Don't show the blank app window.
tries = 5 
timer = 30 #30 sec timer.
guest = 0
API_KEY = os.environ['API_KEY']
WS_URL = "http://api.weatherstack.com/current" #API location.
devs = ['ryan cullen', 'dev man']

with open('users.csv', 'r') as f: #Open user csv file to read into dictionary.
  validcode = dict(filter(None, reader(f))) #Use filter to read row by row into a dictionary.
  f.close() 

logwin = Window(app, title = 'Login', layout = 'grid', width = 350, height = 350) #Log in window.
logo1 = Picture(logwin, image = 'pics/fox.png', grid = [2,0,1,4], width = 100, height = 100) #Logo
text_first = Text(logwin, text = 'First name:', grid = [0,0])
first = TextBox(logwin, grid = [1,0]) #First name box.
text_last = Text(logwin, text = 'Surname:', grid = [0,1])
last = TextBox(logwin, grid = [1,1]) #Last name box.
log_pass_t = Text(logwin, text = 'Password:', grid = [0,2])
log_pass_b = TextBox(logwin, grid = [1,2], hide_text = True) #Password box with hidden text.

def login() : #When the enter button is pressed in logwin
  global tries, fr
  fr = (first.value).lower() + ' ' + (last.value).lower() #fr is global so the user can be called later.
  if int(tries) > 0 : #If the the user still has tries.
    if fr not in validcode.keys() :
      tries -= 1 #Lose a try if wrong, tell user how many tries are remaining.
      toomany = warn('Warning', text = 'Incorrect, you only have ' + str(tries) + ' tries left.')
      if int(tries) == 0 :
        failedenter() #No more tries, move to the failed enter function.
    else :
      codecheck() #Input is valid, then move on to check their passcode.
  
def codecheck() :
  global tries
  while True :
    if int(tries) > 0 : #If user has tries...
      logwin.hide() #Close log in window.
      var = validcode[fr] #Corresponding passcode of the user.
      if str(var) == str(log_pass_b.value): #Check if corresponding pass matches the user input.
        weather.show() #Open the weather page.
        return #Finish loop.
      else :
        tries -= 1
        badcode = warn('Incorrect Password', text = 'Your Password was incorrect. You have' + str(tries) + 'tries left.') #Tell user how many tries they have left.
    else :
      failedenter() #Failedenter function if too many fails.

timerwind = Window(app, title = 'Timeout', width = 350, height = 350) #Timeout window.
tim = Text(timerwind, text = timer, size = 20, align = 'left', color = 'red') #Countdown timer.
logo2 = Picture(timerwind, image = 'pics/fox.png', width = 100, height = 100, align = 'right') #Logo.

def failedenter() : #User ran out of tries.
  global tries, timer
  fail = warn('Timeout', text = 'You are timed out for 30 seconds.') #Popup to say user is timed out.
  logwin.hide() #Hide log in window
  timer = 30 #Reset timer in case the user has been timed out multiple times.
  timerwind.show() #Open timeout window.
  while timer > 0 :
    sleep(1) #Wait one second and then subtract time.
    timer -= 1
    tim.value = timer
    timerwind.update() #Update the window so the new time shows.
  more = info('Try again', text = 'You get two tries before being locked out again.') #Tell user they have more tries.
  tries = 2 #Reset tries.
  timerwind.hide() #Close timeout window and open log in window.
  logwin.show()

def f_sign() : #If the sign in button is pressed hide the startpage and open the sign up page.
  startpage.hide() 
  signup.show()

def f_logs() : #If the log in button is pressed hidethe startpage and opent the sign up page.
  startpage.hide()
  logwin.show()

def signreturn() : #If the return button in sign up is pressed, clear all the textboxes and switch pages.
  startpage.show()
  signup.hide()
  user_b.value = ''
  last_b.value = ''
  fcode_b.value = ''
  scode_b.value = ''

def logreturn() : #The log in return button, clear textboxes.
  startpage.show()
  logwin.hide()
  first.value = ''
  last.value = ''
  log_pass_b.value = ''

def signout() : #Signout from the main page.
  global tries, guest
  sure = yesno('Are you sure?', text = 'Are you sure you want to sign out?') #Check if user is sure. If no, then do nothing.
  if sure == True : #If yes
    weather.hide()
    startpage.show() #Close weather page, and show startpage.
    tries = 5 #Reset tries and clear EVERY textbox and text value in log in, sign up, and weather page.
    first.value = ''
    last.value = ''
    user_b.value = ''
    last_b.value = ''
    fcode_b.value = ''
    scode_b.value = ''
    post_code.value = ''
    temperature.value = ''
    dates.value = ''
    wind_speed.value = ''
    wind_dir.value = ''
    humid.value = ''
    descrip.value = ''
    precip.value = ''
    feels_like.value = ''
    log_pass_b.value = ''
    location.value = ''
    guest = 0 #Reset the guest value.

log = PushButton(logwin, text = 'Enter', command = login, grid = [0,3]) #The enter pushbutton in the the login window.
l_return = PushButton(logwin, text = 'Return', grid = [1,3], command = logreturn) #Return button in the log in window.

def signup_enter() : #When the signup button is pressed in the signup window.
  global validcode, guest
  if user_b.value != '' and last_b.value != '' : #If the first and last name inputs aren't empty.
    if fcode_b.value != '' and scode_b.value != '' : #If the passcode inputs aren't empty.
      if str(fcode_b.value).lower() == str(scode_b.value).lower() : #Check if passwords are the same.
        name = (user_b.value).lower() + ' ' + (last_b.value).lower() #String of both names
        if name not in validcode.keys() : #Check if name already exists.
          save = yesno('Save?', text = 'Would you like your account saved?')
          if save == True :
            validcode[name] = fcode_b.value #Add name and passcode to the dictionary.
            inp = [name, fcode_b.value] #To save to file, the name and pass have to be inputed as a list.
            with open('users.csv', 'a') as f : #Open file in append mode.
              w = writer(f)
              w.writerow(inp) #Write on a new row.
              f.close()
            signup.hide() #Open the log in page for user to log in.
            logwin.show()
          else :
            guest = 1 #Guest mode is on.
            signup.hide() 
            weather.show() #Skip right to the main page.
        else : 
          already_exists = warn('Account already Exists', text = 'This name already has an account. Pick a new one.') #Tell the user the account already exists.
      else :
        notmatch = warn('Password doesn\'t match.', text = 'Your password needs to be the same.') #Tell the user their passwords don't match.
    else :
      otherpick = warn('Password required', text = 'A Password is required.') #Tell the user to input a password.
  else :
    pick = warn('Name required', text = 'A first and last name are required.') #Tell user a first and last name are required.

signup = Window(app, title = 'Signup', layout = 'grid', width = 350, height = 350) #Signup window.
logo3 = Picture(signup, image = 'pics/fox.png', grid = [2,0,1,4], width = 100, height = 100) #Logo.
user_t = Text(signup, text = 'First name:', grid = [0,0])
user_b = TextBox(signup, grid = [1,0]) #First name box.
last_t = Text(signup, text = 'Surname', grid = [0,1])
last_b = TextBox(signup, grid = [1,1]) #Last name box.
fcode_t = Text(signup, text = 'Password:', grid = [0,2])
fcode_b = TextBox(signup, grid = [1,2], hide_text = True) #First passcode text box with hidden text.
scode_t = Text(signup, text = 'Confirm password:', grid = [0,3]) 
scode_b = TextBox(signup, grid = [1,3], hide_text = True)#Confirm passcode text box with hidden text.
sign_enter = PushButton(signup, text = 'Enter', grid = [0,4], command = signup_enter) #Sign up enter button.
s_return = PushButton(signup, text = 'Return', grid = [1,4], command = signreturn) #Sign up return button.

def post_enter() : #Main page enter button.
  city = ((post_code.value).upper()).strip() #Input is all uper case and unnecesary characters are removed.
  parameters = {'access_key': API_KEY, 'query': city} #Key and location stored in dictionary as values.
  response = get(WS_URL, parameters) #Ready for API call.
  js = response.json() #Use json to store response.
  
  temperature.value = 'Temperature: ' + str(js['current']['temperature']) + '°C' #Call temperature
  dates.value = 'Date and Time: ' + str(js['location']['localtime']) #Call date and time.
  wind_speed.value = 'Wind speed: ' + str(js['current']['wind_speed']) + 'km/h' #Call wind speed.
  wind_dir.value = 'Wind direction: ' + js['current']['wind_dir'] #Call wind direction
  humid.value = 'Humidity: ' + str(js['current']['humidity']) + '%' #Call humidity.
  desc = 'Currently: ' + str(js['current']['weather_descriptions']) #Call description of the weather.
  b = '[\'\']' #Remove the characters in b from desc.
  for char in b:
    desc = desc.replace(char, "") #Replace characters with nothing.
  descrip.value = desc.title() #Set text to the clean call.
  precip.value = 'Precipitation: ' + str(js['current']['precip']) + 'mm' #Call the precipitation.
  feels_like.value = 'Feels like: ' + str(js['current']['feelslike']) + '°C' #Call the feels like temperature.
  location.value = 'Location: ' + str(js['location']['name']+ ', ' + str(js['location']['country']))

def feedback_f() : #Feedback button on main page.
  global feedback_box, more_info
  if guest == 0 : #If not in guest mode.
    if fr not in devs: #If user isn't developer.
      feedback_q = question('Feedback', question = 'Do you have any feedback for the developer?') #Ask for feedback.
      if feedback_q is not None : #If there's an input
        with open('feedback.csv', 'a') as f : #Open csv to append.
          feed_input = [feedback_q, fr] #Record feedback and the user who wrote in list for saving.
          feed = writer(f) 
          feed.writerow(feed_input) #Write into the file
          f.close()
    else : #If user is developer
      read = yesno('Read Feedback?', text = 'Would you like to read feedback?') #Ask if they want to read feedback.
      if read == True : #If yes.
        weather.hide()
        feedback_window.show() #Open feedback window.
        with open('feedback.csv', 'r') as f : #Open feedback to read.
          feed = dict(filter(None, reader(f))) #Open as dictionary.
          x = 1 #For counting feedback.
          feedback_box.destroy() #Delete and remake feedback box so if this window is opened multiple times it doesn't repeat feedback.
          feedback_box = Box(feedback_window)
          for row in feed : #For every row in the dictionary.
            more_info = Text(feedback_box, text = f'{x}. {list(feed.keys())[list(feed.values()).index(feed[row])]}, from {feed[row].title()}', size = 9) #Text that uses formatted string to print the user, and finds the key from the value to print the feedback.
            x += 1
          f.close()
  else :
    not_logged_in = info('Log In', text = 'Log in to a saved account to give feedback.') #Tell user they can't be in guest mode to give feedback.

def feed_leave_f() :
  feedback_window.hide()
  weather.show() #Close feedback window.

def feed_clear() :
  with open('feedback.csv', 'w+') as f: #Open file as w+ clears the file.
    f.close() 
  feedback_box.hide() #Hide the text box since it still has the text saved. Whenever the window is opened again this box will be destroyed and remade. 

feedback_window = Window(app, title = 'Feedback', width = 350, height = 350) #Feedback window.

feedback_title = Text(feedback_window, text = 'User Feedback', size = 16) #Title text.
feed_leave = PushButton(feedback_window, align = 'bottom', command = feed_leave_f, text = 'Return') #Return button.
feedback_clear = PushButton(feedback_window, align = 'bottom', text = 'Clear', command = feed_clear) #Clear button.
feedback_box = Box(feedback_window) #Blank box for feedback.

weather = Window(app, title = 'Weather Station', width = 350, height = 350, layout = 'grid') #Main page window.

title = Box(weather, grid = [0,0], width = 'fill') #Title box.
place = Box(weather, grid = [0,1]) #Location box.
inform = Box(weather, grid = [0,2], layout = 'grid') #Information box.
feed_box = Box(weather, grid = [0,3], width = 'fill') #Feedback button box.

w_title = Text(title, text = 'Weather Station', size = 16, font = 'trebuchet', align = 'left') #Title text.
leave = PushButton(title, text = 'Sign Out', align = 'right', command = signout) #Signout button.

post = Text(place, text = 'Postal/Post/Zip Code:', align = 'left', size = 9) 
post_code = TextBox(place, align = 'left') #Textbox for location input.
post_enter_b = PushButton(place, align = 'left', text = 'enter', command = post_enter) #Enter location box.

temperature = Text(inform, grid = [0,2], size = 9) #Weather information textboxes.
location = Text(inform, grid = [0,1], size = 9)
dates = Text(inform, grid = [0,0], size = 9)
wind_speed = Text(inform, grid = [0,5], size = 9)
wind_dir = Text(inform, grid = [0,6], size = 9)
humid = Text(inform, grid = [0,7], size = 9)
descrip = Text(inform, grid = [0,4], size = 9)
precip = Text(inform, grid = [0,8], size = 9)
feels_like = Text(inform, grid = [0,3], size = 9)

logo5 = Picture(feed_box, image = 'pics/fox.png', align = 'left', width = 100, height = 100) #Logo at bottom.
feed_button = PushButton(feed_box, align = 'right', text = 'Feedback', command = feedback_f) #Feedback button.

startpage = Window(app, layout = 'grid', title = 'Weather Station', width = 350, height = 350) #Startpage window.
title = Text(startpage, text = 'Welcome to the Weather Station!', size = 15, font = 'Calibri', grid = [0,0,3,1]) #Title text. 
sign = PushButton(startpage, text = 'Sign Up', grid = [0,1], command = f_sign) #Sign up button.
logo4 = Picture(startpage, image = 'pics/fox.png', grid = [1,1], width = 75, height = 75) #Logo.
logs = PushButton(startpage, text = 'Log In', grid = [2,1], command = f_logs) #Log in button.
picture = Picture(startpage, image = 'pics/the_globe.jpg', grid = [0,2,3,1], width = 350, height = 350) #Picture.

signup.hide() #Hide all the windows that aren't open at the start.
timerwind.hide()
logwin.hide()
app.hide()
weather.hide()
feedback_window.hide()
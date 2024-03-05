import ephem
import math
from operator import itemgetter
from pytz import timezone

def check_non_zero(x):
    return x > 0

 # timetuple should look like (year, month, day, hour, minute, second)
 # i.e: (2024, 4, 8, 0, 0, 0)
def calc_lune_percentage(timetuple):
  # Credit for the function: https://www.chromosphere.co.uk/2015/03/18/eclipse-calculations-using-python/
  # It wasn't working until I added some guards to prevent sqrt(negative) and trig function of numbers > 1.0

  cst = timezone('America/Chicago')   #time zone

  # Location
  observer = ephem.Observer()
  observer.lat, observer.lon = '30.288379354549612', '-97.75060867083091' #Austin

  # Objects
  sun, moon = ephem.Sun(), ephem.Moon()

  # Output list
  results=[]

  for x in range(0,86400): # for every second of the day
    observer.date = (ephem.date(ephem.date(timetuple)+ x*ephem.second))
    sun.compute(observer)
    moon.compute(observer)
    r_sun=sun.size/2
    r_moon=moon.size/2
    s=math.degrees(ephem.separation((sun.az, sun.alt), (moon.az, moon.alt)))*60*60

    ## Calculate the size of the lune (http://mathworld.wolfram.com/Lune.html) in arcsec^2
    if s<(r_moon+r_sun):
      lunedelta=0.25*math.sqrt(abs((r_sun+r_moon+s)*(r_moon+s-r_sun)*(s+r_sun-r_moon)*(r_sun+r_moon-s))) # abs guard the sqrt
    else: ### If s>r_moon+r_sun there is no eclipse taking place
      lunedelta=None
      percent_eclipse=0
    if lunedelta and ((r_moon*r_moon)-(r_sun*r_sun)-(s*s))/(2*r_sun*s) < 1:   # guard for trig function
      lune_area=2*lunedelta + r_sun*r_sun*(math.acos(((r_moon*r_moon)-(r_sun*r_sun)-(s*s))/(2*r_sun*s))) - r_moon*r_moon*(math.acos(((r_moon*r_moon)+(s*s)-(r_sun*r_sun))/(2*r_moon*s)))
      percent_eclipse=(1-(lune_area/(math.pi*r_sun*r_sun)))*100 # Calculate percentage of sun's disc eclipsed using lune area and sun size
    
    results.append([observer.date.datetime(),s,sun.size,moon.size,lune_area if lunedelta else 0, percent_eclipse]) ### Append to list of lists

  gen=(x for x in results) ### Find Max percentage of eclipse...
  max_eclipse=max(gen, key=itemgetter(5))
  max_eclipse[0] = timezone('UTC').localize(max_eclipse[0]) # set to UTC

  print(max_eclipse)
  print("Max eclipse at: " + str(max_eclipse[0])) ### ...and return the time
  print("Max percent: " + '%.2f' % max_eclipse[5]) ### ...and return the percentage

  return [str(round(max_eclipse[5], 2)),(max_eclipse[0].astimezone(cst)).strftime("%I:%M %p. %b. %d, %Y")]

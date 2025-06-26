from machine import Pin, RTC, reset, lightsleep
from time import sleep_ms

pin1 = Pin(26, Pin.OUT)
pin2 = Pin(27, Pin.OUT)

pin1.off()
pin2.off()

# N.B.: Both RTC and time use differing 8-tuples:
#       RTC:  (year, month, day, weekday, hours, minutes, seconds, subseconds)
#       time: (year, month, mday, hour, minute, second, weekday, yearday)

# N.B.: Per https://forums.raspberrypi.com/viewtopic.php?t=354387 wiki:
#       Note that if you're using Thonny, it will quietly try to set the RTC for you.
#       There were many questions about how the RTC "magically" knew the time before this was worked out

# Set the RTC to UNIX EPOCH
RTC().datetime((1970, 1, 1, 3, 0, 0, 0, 0))
timetuple = RTC().datetime()
print(timetuple[0])
print(timetuple[1])
print(timetuple[2])
print(timetuple[3])
print(timetuple[4])
print(timetuple[5])
print(timetuple[6])
print(timetuple[7])

seconds_on = 5 + 1 # Add 1 because RTC seems to immediately increment second from 0 to 1 when set
#seconds_lightsleep = 1000 * ((24 * 60 * 60) - seconds_on)
milliseconds_lightsleep = 1000 * 5
print(seconds_on)
print(milliseconds_lightsleep)

while True:
    
    try:
        
        pin1.on()
        sleep_ms(6)
        pin1.off()
        sleep_ms(1)
        pin2.on()
        sleep_ms(6)
        pin2.off()
        sleep_ms(1)

        timetuple = RTC().datetime()
        hours = timetuple[4]
        minutes = timetuple[5]
        seconds = timetuple[6]
        
        if hours >= 0 and minutes >= 0 and seconds >= seconds_on:
            
            print("turn off LEDs")
            pin1.off()
            pin2.off()
            
            print("going to sleep until just a few seconds before midnight so can accurately restart the cycle 24 hours later")
            #sleep_ms(5000)
            # N.B.: lightsleep stops the RTC !!!
            #lightsleep(5000) # lightsleep 5000 msec
            lightsleep(milliseconds_lightsleep) # lightsleep milliseconds_lightsleep msec
            print("done sleep")
            
            #while True:
            #
            #    timetuple = RTC().datetime()
            #    hours = timetuple[4]
            #    minutes = timetuple[5]
            #    seconds = timetuple[6]
            #
            #    if hours >= 0 and minutes >= 0 and seconds >= 15:
            #        print("reset")
            #        reset()
            #    else:
            #        print("sleep 1 second")
            #        sleep_ms(1000)

            print("reset")
            reset()

    except KeyboardInterrupt:
        break

pin1.off()
pin2.off()

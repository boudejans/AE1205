hourHand = input("Hour: ")
minuteHand = input("Minutes: ")
print("Time: " + str(hourHand) + ":" + str(minuteHand))
hourAngle = int(hourHand)/12*360
minuteAngle = int(minuteHand)/60*360
angle = round(abs(hourAngle-minuteAngle))
if angle > 180:
    angle = 360-angle
print("Angle: " + str(angle))
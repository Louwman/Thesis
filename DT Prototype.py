import serial  # import Serial Library
import numpy  # Import numpy
import matplotlib.pyplot as plt  # import matplotlib library
from drawnow import *
import tkinter as tk



root = tk.Tk()
# root.withdraw()
works = tk.PhotoImage(file="pompworks.png")
notworks = tk.PhotoImage(file="pompisnotworking.png")

w1 = tk.Label(root, image=works)
w1.pack(side="right")



warning = tk.StringVar()
warning.set("")



w2 = tk.Message(root,
              justify=tk.LEFT,
              padx = 10,
              textvariable=warning)
w2.pack(side="left")
root.geometry("1000x600")

pressureP = [] #tempF
milliamps = [] #pressure
arduinoData = serial.Serial('/dev/cu.usbmodem14101')  # Import serial communication
plt.ion()  # Interactive live plot
cnt = 0


def makeFig():  #
    plt.ylim(1000, 1040)  #
    plt.title('My Live Streaming Sensor Data')
    plt.grid(True)
    plt.ylabel('Pressure (HPa)')
    plt.plot(pressureP, 'ro-', label='Pressure (HPa)')  # plot barometric pressure
    plt.legend(loc='upper left')
    plt2 = plt.twinx()
    plt.ylim(0, 2000)
    plt2.plot(milliamps, 'b^-', label='milliamps (mA)')  # electric current
    plt2.set_ylabel('milliamps (mA)')
    plt2.ticklabel_format(useOffset=False)  # don't autoscale the plot
    plt2.legend(loc='upper right')


while True:
    while (arduinoData.inWaiting() == 0):  # wait
        pass
    arduinoString = arduinoData.readline().decode("utf-8")  # read serial port and decode UTF8
    dataArray = arduinoString.split(',')
    pressure = float(dataArray[0])
    ma = float(dataArray[1])
    pressureP.append(pressure)
    milliamps.append(ma)
    drawnow(makeFig)
    plt.pause(.000001)  # pause for drawnow
    cnt = cnt + 1
    if (cnt > 100):  # safe 100 data points and remove the first when 100th datapoint is reached
        pressureP.pop(0)
        milliamps.pop(0)

    if (ma < 900) and (pressure < 1015): #threshold values determined from experiments
        w1.configure(image=notworks)
        warning.set("WARNING! The measured pressure is " + str(pressure) + " HPa. The measured current consuption is " + str(ma) + " Milliamps.\n\n You could: \n 1) unclog the pipe (worked 60% of the time) \n 2) reduce the operational speed (worked 40% of the time)")
    else:
        w1.configure(image=works)
        warning.set("The measured pressure is " + str(pressure) + " HPa. The measured current consuption is " + str(ma) + " Milliamps.\n\n ")
    root.update_idletasks()
    root.update()



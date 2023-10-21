from tkinter import *
from datetime import *

temp = 0
after_id = ''


def tick():
    global temp, after_id
    after_id = root.after(1000, tick)
    f_temp = datetime.fromtimestamp(temp)
    f_temp = f_temp.strftime('%M:%S')
    lb.configure(text=f_temp)
    temp += 1


def start_tick():
    btnStart.pack_forget()
    btnStop.pack()
    tick()


def stop_tick():
    btnStop.pack_forget()
    btnContinue.pack()
    btnReset.pack()
    root.after_cancel(after_id)


def continue_tick():
    btnContinue.pack_forget()
    btnReset.pack_forget()
    btnStop.pack()
    tick()


def reset_tick():
    global temp
    btnContinue.pack_forget()
    btnReset.pack_forget()
    btnStart.pack()
    root.after_cancel(after_id)
    lb.configure(text='00:00')
    temp = 0


root = Tk()
root.title('Секундомер')
root.geometry('300x200')
root.resizable(False, False)
lb = Label(text='00:00', font=('Colibri', 30))
lb.pack()
btnStart = Button(text='Старт', font=('Colibri', 20), width=15, command=start_tick)
btnStart.pack()
btnStop = Button(text='Стоп', font=('Colibri', 20), width=15, command=stop_tick)
btnContinue = Button(text='Продолжить', font=('Colibri', 20), width=15, command=continue_tick)
btnReset = Button(text='Сброс', font=('Colibri', 20), width=15, command=reset_tick)

root.mainloop()

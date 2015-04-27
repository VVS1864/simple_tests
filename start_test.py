# -*- coding: utf-8; -*-
from Tkinter import*
import ttk
import tkMessageBox
import os

appPath = os.getcwd()

base = {}

questions = {
    0:[u'Сколько будет 2+2?', {
        '1':False,
        '8':False,
        '4':True,
        '24':False,
        }],
    1:[u'Съедобна ли нефть?', {
        u'Да':False,
        u'Надо попробовать':False,
        u'Нет':True,
        }],
    2:[u'Какие числа больше 2+2*2?', {
        '6':False,
        '9':True,
        '7':True,
        }],
    }
questions_100 = questions.copy()
i = 1
while i<100:
    for x in questions.keys():
        i += 1
        questions_100[i] = questions[x]
questions = questions_100


    
    
posts = [
    u'Бурильщик',
    u'Геолог',
    u'Инженер',
    ]

subdivision = [
    u'Трубный участок 1',
    u'Трубный участок 2',
    u'Трубный участок 3',
    u'Трубный участок 4',
    ]

region = [
    u'Север',
    u'Юг',
    u'Запад',
    u'Восток',
    ]
        
class test_gui:
    def __init__(self, master):
        self.master = master
        self.master.title(u'Тест 4.0')
        #self.master.resizable(width=FALSE, height=FALSE)
        
        self.frame = Frame(self.master)
        self.frame.pack(side=TOP)

        self.frame2 = Frame(self.master)
        self.frame2.pack(side=TOP)
        
        self.row = 0
        self.widgets = []
        
        self.stroker(u'Фамилия')
        self.stroker(u'Имя')
        self.stroker(u'Отчество')
        self.stroker(u'Должность', 'combobox', posts)
        self.stroker(u'Таб. №')
        self.stroker(u'Подразделение/цех', 'combobox', subdivision)
        self.stroker(u'Регион', 'combobox', region)

        self.button_test = Button(self.frame2, text = u'Начать тест', bg = 'lightblue', command = self.start)
        self.button_test.pack()

        self.master.protocol('WM_DELETE_WINDOW', self.exitMethod)

    def start(self):
        profile = []
        for x in self.widgets:
            name = x[0]
            val = x[1].get()
            if not val:
                #tkMessageBox.showerror(u'Ошибка!', u'Незаполненно поле "%s"' %name)
                #return
                pass
            profile.append( [name, val])
            
        self.profile = profile
        self.wrapp_tests()

    def wrapp_tests(self):
        self.master.geometry('300x300')
        self.frame.pack_forget()
        self.frame2.pack_forget()

        self.frame_left = Frame(self.master)
        self.frame_left.pack(side=LEFT)

        self.frame_right = Frame(self.master)
        self.frame_right.pack(side=TOP, fill=BOTH, expand=1)
        
        self.listb = Listbox(self.frame_left, height = 30, width = 3)
        self.listb.pack(side="left")
        self.listb.bind("<<ListboxSelect>>", self.change_q)

        scrollbar = Scrollbar(self.frame_left)
        scrollbar.pack(side=LEFT, fill=Y)

        self.listb.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listb.yview)

        self.frame_q = Frame(self.frame_right, bg = 'green')
        self.frame_q.pack(side=TOP, fill=BOTH, expand=1)

        self.frame_apply = Frame(self.frame_right)
        self.frame_apply.pack(side=TOP, fill=BOTH, expand=1)

        self.button_next = Button(self.frame_apply, text = u'Следующий вопрос', bg = 'lightblue', command = self.next_q)
        self.button_next.pack(side='top') 

        self.button_apply = Button(self.frame_apply, text = u'Закончить тестирование', bg = 'lightblue', command = self.apply_test)
        self.button_apply.pack(side='bottom')        
        
        self.frames = []
        for i, j in enumerate(questions.keys()):
            q = questions[j]
            frame = Frame(self.frame_q)
            frame.pack(side='top', fill=BOTH, expand=1)
            frame_top = Frame(frame)
            frame_top.pack(side='top')
            frame_bot = Frame(frame)
            frame_bot.pack(side='top', fill=BOTH, expand=1)
            
            self.listb.insert("end", i)
            
            label = Label(frame_top, text = q[0])
            label.grid(row = 0, column = 0, sticky = 'e')
            var_dict = {}
            r = 1
            for c in q[1].keys():
                var = IntVar()
                cb = Checkbutton(
                    frame_bot, text = c,
                    variable = var)
                var_dict[c] = var
                cb.grid(row = r, column = 0, sticky = 'w')
                r += 1
                
            self.frames.append( [j, frame, var_dict] )
            frame.pack_forget()

        self.current_frame = self.frames[0][1]
        self.current_frame.pack(side='top', fill=BOTH, expand=1)
        self.listb.selection_set(0)

    def next_q(self):
        q_num = int(self.listb.curselection()[0]) + 1
        self.change_q(e = None, num = q_num)
        
        

    def change_q(self, e = None, num = None):
        if e:
            q_num = int(e.widget.curselection()[0])
        else:
            q_num = num
        try:
            current_frame = self.frames[q_num][1]
        except IndexError:
            return
        self.current_frame.pack_forget()
        self.current_frame = current_frame
        self.current_frame.pack(side='top', fill=BOTH, expand=1)
        self.listb.selection_clear(0, 30)
        self.listb.selection_set(q_num)
    

    def apply_test(self):
        bads = 0
        result = {}
        
        for frame in self.frames:
            right = True
            quest_ID = frame[0]
            result[quest_ID] = []

            var_dict = frame[2]
            for var_cb in var_dict.keys():
                
                answer = var_dict[var_cb].get()#Взять значение из checkbutton
                ist_answer = questions[quest_ID][1][var_cb]#Правильное значение
                if answer:
                    answer = True
                else:
                    answer = False
                    
                e = (ist_answer == answer)
                if not e and right:
                    right = False
                    bads += 1
                result[quest_ID].append([var_cb, ist_answer, answer, e])
            result[quest_ID].append(right)
                   
        for  r in result.keys():
            print r
            for  e in result[r]:
                print e
    
        print u'Всего = %s, Неправильно = %s, Правильно %s из %s' %(len(result), bads, len(result)-bads, len(result))
            
            
        
        

    def exitMethod(self):
        yes_no = tkMessageBox.askyesno(u'Закрыть', u'Закрыть программу?')
        if yes_no == True:
            self.master.destroy()

    def stroker(self, text, type_w = 'entry', vals = None):
        label = Label(self.frame, text = text)
        if type_w == 'entry':
            widget = Entry(self.frame)
        elif type_w == 'combobox':
            widget = ttk.Combobox(self.frame, values = vals, state='readonly')
            
        label.grid(row = self.row, column = 0, sticky = 'w', padx = 3, pady = 3)
        widget.grid(row = self.row, column = 1, sticky = 'w',padx = 3, pady = 3)

        self.widgets.append( [text, widget] )
        self.row += 1
        
        return label, widget

root = Tk()
test = test_gui(root)
root.mainloop()
    
        

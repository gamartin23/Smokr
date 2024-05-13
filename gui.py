import customtkinter as ct
from tkinter import *
import json
from testcase import TestCase
import requests
import copy
import os, sys
from PIL import Image
import random

class gui:
    def __init__(self) -> None:
        self.frameId = 0
        self.frames = {}        
        
        with open('endpoint.kova', "r") as apicaller: #remember to turn this into api calls
            self.endpoint = apicaller.read()
            #get uuid
            response = requests.get(f'{self.endpoint}/debug/uuid')
            self.uuid = response.json()["uuid"]
        
        self.window = ct.CTk()
        self.version = 1.0
        self.window.title(f'Smokr {self.version}')
        self.window.geometry("1000x700")
        #self.window.grid_rowconfigure((1),weight=0,minsize=1)
        ct.set_appearance_mode('dark')
        #self.window.iconbitmap(self.resourcePath('smokr.ico'))
        
        self.mainFrame = ct.CTkFrame(self.window,fg_color='transparent')
        self.mainFrame.grid(row=1,column=0,padx=(10,0),pady=(10,5),sticky=N,rowspan=3)
        self.mainFrame.grid_columnconfigure((0),weight=1)
        self.mainFrame.grid_rowconfigure(0,weight=1)
        self.updatebutton = ct.CTkButton(self.window,text='Update',command=self.update,width=260,height=40)
        #self.updatebutton.grid(row=1,column=1,padx=(5,10),pady=5,sticky=N)
        self.rightFrame = ct.CTkFrame(self.window)
        self.rightFrame.grid(row=1,column=1,pady=(5),padx=(0,10),sticky=NE)
        self.rightFrame2 = ct.CTkFrame(self.window)
        self.rightFrame2.grid(row=2,column=1,pady=(0,10),padx=(0,10),sticky=NSEW)
        self.scroller = ct.CTkScrollableFrame(self.mainFrame,width=650,height=500,)
        #self.scroller.grid(row=0,column=0,pady=10,padx=10)
        
        self.notesLabel = ct.CTkLabel(self.rightFrame,text='Notes',font=('helvetica',16,'bold'),text_color='#888888')
        self.notesLabel.grid(row=0,column=0,pady=(10,5),padx=10,sticky=SW)
        self.notesEntry = ct.CTkTextbox(self.rightFrame,state='disabled',height=80,width=250)
        self.notesEntry.grid(row=1,column=0,pady=(5,10),padx=10)
        self.relatedLabel = ct.CTkLabel(self.rightFrame,text='Related issues',font=('helvetica',16,'bold'),text_color='#888888')
        self.relatedLabel.grid(row=2,column=0,pady=(10,5),padx=10,sticky=SE)
        self.relatedEntry = ct.CTkTextbox(self.rightFrame,state='disabled',height=80,width=250)
        self.relatedEntry.grid(row=3,column=0,pady=(5),padx=10)
        self.relatedSend = ct.CTkButton(self.rightFrame,state='disabled',text='Save',command=self.saveNote)
        self.relatedSend.grid(row=4,column=0,pady=(5,10),padx=10)
        
        self.frameAbove = ct.CTkFrame(self.window)
        self.frameAbove.grid(row=0,column=0, pady=(10,5),padx=10,sticky=EW,columnspan=2)
        self.frameAbove.grid_columnconfigure(0,weight=0,minsize=1000)
        
        self.smokrimg = ct.CTkImage(Image.open(self.resourcePath("img/titler.png")),size=(188,49))
        self.smokrimg2 = ct.CTkImage(Image.open(self.resourcePath("img/titler2.png")),size=(188,49))
        self.title = ct.CTkLabel(self.frameAbove,text='',image=self.smokrimg)
        self.title.grid(row=0,column=0,pady=10,padx=10,sticky=W)
        self.title.bind('<Enter>',self.switcheroo)
        self.title.bind('<Leave>',self.deswitcheroo)
        self.workingon = ct.CTkLabel(self.frameAbove,text=f'Working on: {self.uuid}',font=('helvetica',28,'bold'),text_color='#888888')
        self.workingon.grid(row=1,column=0,pady=10,padx=10,sticky=SW)
        self.iconaboot = ct.CTkImage(Image.open(self.resourcePath("img/appicon.png")),size=(100,100))
        self.buttonaboot = ct.CTkButton(self.frameAbove,text='',image=self.iconaboot,command=self.aboot,height=100,width=100,fg_color='#2b2b2b',hover_color='#2b2b2b')
        self.buttonaboot.grid(row=0,column=0,rowspan=2,sticky=E,pady=10,padx=10)
        
        self.frameControls = ct.CTkFrame(self.mainFrame)
        self.frameControls.grid(row=2,column=0,pady=(0,10),padx=10,sticky=E)
        
        self.aidFrame = ct.CTkFrame(self.mainFrame,fg_color='transparent',bg_color='transparent')
        self.aidFrame.grid(row=0,column=0,pady=0,padx=0,sticky=N)
        self.aidFrame.grid_columnconfigure(1,weight=0,minsize=310)
        self.aidFrame.grid_columnconfigure((0,2,3),weight=0,minsize=80)
        self.aidFrame.grid_columnconfigure(4,weight=0,minsize=175)
        self.aidId = ct.CTkLabel(self.aidFrame,text='#',font=('helvetica',12,'bold'),text_color='#888888')
        self.aidId.grid(row=0,column=0,pady=5,padx=5,sticky=NSEW)
        self.aidName = ct.CTkLabel(self.aidFrame,text='Description',font=('helvetica',12,'bold'),text_color='#888888')
        self.aidName.grid(row=0,column=1,pady=5,padx=5,sticky=NSEW)
        self.iosimg = ct.CTkImage(Image.open(self.resourcePath("img/ios.png")))
        self.aidIos = ct.CTkLabel(self.aidFrame,text='',image=self.iosimg)
        self.aidIos.grid(row=0,column=2,pady=5,padx=5,sticky=NSEW)
        self.andimg = ct.CTkImage(Image.open(self.resourcePath("img/android.png")))
        self.aidAnd = ct.CTkLabel(self.aidFrame,text='',image=self.andimg)
        self.aidAnd.grid(row=0,column=3,pady=5,padx=5,sticky=E)
        
        self.newSmokeButton = ct.CTkButton(self.frameControls,text='New smoke', command=self.newSmoke,width=90)
        self.newSmokeButton.grid(row=0,column=0,pady=5,padx=(5),sticky=NSEW)
        self.newSmokeButton = ct.CTkButton(self.frameControls,text='Mark as done', command=self.doneSmoke,width=90)
        self.newSmokeButton.grid(row=0,column=1,pady=5,padx=(5),sticky=NSEW)
                
        self.window.after(100,self.loadPossibleStati())
        self.window.after(200,self.callJson())
        self.window.after(300,self.generateFrames())
                
        self.window.mainloop()
    
    def switcheroo(self,*args):
        self.title.configure(require_redraw=True,image=self.smokrimg2)
        
    def deswitcheroo(self,*args):
        self.title.configure(require_redraw=True,image=self.smokrimg)
    
    def aboot(self):
        aboutR=ct.CTkToplevel()
        ws=self.window.winfo_screenwidth()
        hs=self.window.winfo_screenheight()
        ws=(ws/2)
        hs=(hs/2)
        c=(ws-150)
        d=(hs-100)
        aboutR.geometry('%dx%d+%d+%d' % (300, 250, c, d))
        aboutR.resizable(False,False)
        aboutR.attributes('-topmost',True)
        #aboutR.iconbitmap('icon.ico')
        aboutR.title(f'About /recoder {self.version}')
        
        randomIQ=random.randint(1,20)
        if randomIQ == 1:
            randomIQ = f'{randomIQ}. Critical fail'
        elif randomIQ == 20:
            randomIQ = f'Nat {randomIQ}.'
        elif randomIQ == 19:
            randomIQ = f'{randomIQ}. Lmao'
        letrita=('Helvetica',11)
        
        needsAn=['8','11']
        
        labelabout=ct.CTkLabel(master=aboutR,text='Tool made with love in Tucumán.\nCode and UI by Kovadev.')
        labelabout.pack(pady=(25,10),padx=5,side=TOP)        
        aboutRF=ct.CTkFrame(master=aboutR)
        aboutRF.pack(pady=0,padx=0)    
        self.imageLica=ct.CTkImage(dark_image=(Image.open('img/appicon.png')),size=(90,90))
        buttonimgLica=ct.CTkButton(master=aboutRF,image=self.imageLica,text='',border_width=0,hover_color='#242424',fg_color='#242424',border_color='#242424',border_spacing=2,width=70)
        buttonimgLica.pack(pady=0,padx=(2,0),side=RIGHT)
        imageKova=ct.CTkImage(dark_image=Image.open('img/kovasp.png'),size=(90,90))
        buttonimgKova=ct.CTkButton(master=aboutRF,image=imageKova,text='',border_width=0,hover_color='#242424',fg_color='#242424',border_color='#242424',border_spacing=2,width=70)
        buttonimgKova.pack(pady=0,padx=(0,2),side=LEFT)

        if '8' in str(randomIQ) or '18' in str(randomIQ) or '11' in str(randomIQ):
            labelabout2=ct.CTkLabel(master=aboutR,text=f'Kova tools.  You rolled an {randomIQ}',font=(letrita))
        else:
            labelabout2=ct.CTkLabel(master=aboutR,text=f'Kova tools.  You rolled a {randomIQ}',font=(letrita))
        labelabout2.pack(pady=5,padx=5)
        buttonok=ct.CTkButton(master=aboutR,text='Ok',command=aboutR.destroy)
        buttonok.pack(pady=5,padx=5)
        if ct.get_appearance_mode()=='Light':
            buttonimgLica.configure(hover_color='#ebebeb',fg_color='#ebebeb',border_color='#ebebeb')
            buttonimgKova.configure(hover_color='#ebebeb',fg_color='#ebebeb',border_color='#ebebeb')
        #aboutR.after(200,lambda: aboutR.iconbitmap('icon.ico'))
        aboutR.mainloop()
    
    def resourcePath(args,relativePath):  # Function for relative paths
        basePath=getattr(sys,'_MEIPASS',os.path.dirname(os.path.abspath(__file__)))
        print(basePath)
        print(relativePath)
        return os.path.join(basePath,relativePath)
    
    def loadPossibleStati(self):
        with open(self.resourcePath('status_template.json'), "r") as tcstatus: #remember to turn this into api calls
            data = json.load(tcstatus)
        self.stati = []
        for status in data["Status"]:
            self.stati.append(status)
    
    def update(self):
        self.deleteFrames()
        self.callJson()
        self.generateFrames()
    
    def callJson(self):
        endpoint = self.endpoint
        self.test_cases = []

        try:
            response = requests.get(endpoint)
            data=response.json()
            for item in data:
                test_case = TestCase(item["id"], item["name"], item.get("android_state", "Untested"), item.get("ios_state", "Untested"), item.get("comments", ""), item.get("related_issues", [""]))
                self.test_cases.append(test_case.toJSON())
            self.oldData = copy.deepcopy(self.test_cases)
            #get uuid
            response = requests.get(f'{endpoint}/debug/uuid')
            self.uuid = response.json()["uuid"]
            self.workingon.configure(text=f'Working on: {self.uuid}')
        except Exception as e:
            print(e)
            # pass #have an error message
                     
    def generateFrames(self):
        self.frames = {}
        self.frameId = 0
        try:
            self.scroller.grid_remove()
        except:
            pass #just dont do anything if its not yet packed
        self.scroller.grid(row=1,column=0,pady=(2,10),padx=(0,10),sticky=EW,columnspan=5)
        self.scroller.grid_columnconfigure((0),weight=3,pad=5)
        try:
            for testcase in self.test_cases:
                frame = FrameTemplate(self.scroller,self.frameId,testcase,self.stati,self)
                self.frames[self.frameId] = frame
                self.frameId += 1
                #Let's be real, Tkinter was not made to support these many widgets. Don't fumble around with the screen. It'll be alright
        except Exception as e:
            print(e)
            pass #write error message here
        print(self.frameId,len(self.frames))

    def enableNotes(self, id, abutton):
        self.currentNote = id
        comment = self.test_cases[id]["comments"]
        issues = ', '.join(self.test_cases[id]["related_issues"])
        self.notesEntry.configure(state='normal')
        self.notesEntry.delete(0.0,END)
        self.notesEntry.insert(0.0,comment)
        self.relatedEntry.configure(state='normal')
        self.relatedEntry.delete(0.0,END)
        self.relatedEntry.insert(0.0,issues)
        self.relatedSend.configure(state='normal')
        
    def saveNote(self):
        comment = str(self.notesEntry.get(1.0,END)).strip()
        issues = str(self.relatedEntry.get(1.0,END)).strip().split(', ')
        self.test_cases[self.currentNote]["comments"] = comment
        self.test_cases[self.currentNote]["related_issues"] = issues
        #deberia devolverle a la api todo lo que es self.test_cases[self.currentNote]
        self.updateApi(self.test_cases[self.currentNote],self.currentNote)
        listToUpdate = self.differences(self.oldData,self.test_cases)
        self.updateFrame(listToUpdate)
        
    def changeStateIos(self,state,id):
        self.test_cases[id]["ios_state"] = state
        self.updateApi(self.test_cases[id],id)
        listToUpdate = self.differences(self.oldData,self.test_cases)
        self.updateFrame(listToUpdate)
        
    def changeStateAnd(self,state,id):
        self.test_cases[id]["android_state"] = state
        self.updateApi(self.test_cases[id],id)
        listToUpdate = self.differences(self.oldData,self.test_cases)
        self.updateFrame(listToUpdate)    
        
    def updateApi(self,item,index):
        updater = f'{self.endpoint}/{index}'
        data = item
        try:
            response = requests.put(updater,json=data)
            self.test_cases=response.json()
        except Exception as e:
            print(e)
            
    def differences(self, old, new): #aint working
        changed_indexes = [i for i in range(len(old)) if new[i] != old[i]]
        self.oldData = []
        self.oldData = copy.deepcopy(new)
        return changed_indexes
    
    def deleteFrames(self):
        for target in range(len(self.test_cases)):
            if isinstance (self.frames, dict):
                updateMe = self.frames.get(target)
            else:
                print('FUCK')
            if updateMe:
                updateMe.frame.destroy()
        self.frames = {}
        
    def updateFrame(self, listToUpdate):
        for target in listToUpdate:
            if isinstance (self.frames, dict):
                updateMe = self.frames.get(target)
            else:
                pass
            if updateMe:
                instance_=self.test_cases[target]
                updateMe.dropStatusIos.set(instance_["ios_state"])
                updateMe.dropStatusAnd.set(instance_["android_state"])
                if instance_["android_state"] == self.test_cases[target]["ios_state"]:
                    if self.test_cases[target]["android_state"] == 'Passed':
                        updateMe.frame.configure(fg_color='#27AE60')
                    elif self.test_cases[target]["android_state"] == 'Failed':
                        updateMe.frame.configure(fg_color='#C2392B')
                    elif self.test_cases[target]["android_state"] == 'Caution':
                        updateMe.frame.configure(fg_color='#D9A736')
                    elif self.test_cases[target]["android_state"] == 'N/A':
                        updateMe.frame.configure(fg_color='#7F8C8D')
                    elif self.test_cases[target]["android_state"] == 'CNT':
                        updateMe.frame.configure(fg_color='#2980B9')

    def newSmoke(self):
        try:
            response = requests.get(f'{self.endpoint}/new_smoke')
            data=response.json()
            self.test_cases = data
        except:
            pass #error message here
        self.callJson() 
        self.deleteFrames()
        self.generateFrames() 
        
    def doneSmoke(self):
        try:
            response = requests.get(f'{self.endpoint}/done')
            data=response.json()
            self.workingon.configure(text=f'Smoke marked as done: {self.uuid}')
        except:
            pass #error message here

#FALTA: Mensaje de error para botones
#FALTA: Grafico de completado android/ios
#FALTA: TOODO ERROR HANDLING

class FrameTemplate:
    def __init__(self, parent, frameId, element: TestCase, states, gui):
        self.frame_id = frameId
        self.gui = gui
        self.parent = parent
        self.tc = element
        
        self.frame = ct.CTkFrame(parent)
        if int(self.frame_id) % 2 == 0:
            self.frame.configure(fg_color='#3b3b3b')
        self.frame.grid(row=self.frame_id,column=0,pady=5,padx=5,sticky=EW,columnspan=2,)
        self.frame.grid_columnconfigure(1,weight=1,uniform='column',minsize=200)
        self.frame.grid_rowconfigure(0,weight=1)
        labelTc = ct.CTkLabel(self.frame,text=f'{self.tc["id"]}')
        labelTc.grid(row=0,column=0,pady=5,padx=10)
        labelName = ct.CTkLabel(self.frame,text=f'{self.tc["name"]}',wraplength=200,compound='left',justify='left')
        labelName.grid(row=0,column=1,pady=5,padx=10,sticky=W)
        self.dropStatusIos = ct.CTkComboBox(self.frame,values=states,width=90,state='readonly', command=self.changestateIos)
        self.dropStatusIos.grid(row=0,column=2,pady=5,padx=10,sticky=NSEW)
        self.dropStatusIos.set(self.tc["ios_state"])
        self.dropStatusAnd = ct.CTkComboBox(self.frame,values=states,width=90,state='readonly', command=self.changestateAnd)
        self.dropStatusAnd.grid(row=0,column=3,pady=5,padx=10,sticky=NSEW)
        self.dropStatusAnd.set(self.tc["android_state"])
        if self.tc["android_state"] == self.tc["ios_state"]:
            if self.tc["android_state"] == 'Passed':
                self.frame.configure(fg_color='#27AE60')
            elif self.tc["android_state"] == 'Failed':
                self.frame.configure(fg_color='#C2392B')
            elif self.tc["android_state"] == 'Caution':
                self.frame.configure(fg_color='#D9A736')
            elif self.tc["android_state"] == 'N/A':
                self.frame.configure(fg_color='#7F8C8D')
            elif self.tc["android_state"] == 'CNT':
                self.frame.configure(fg_color='#2980B9')
        notesEnableButton = ct.CTkButton(self.frame,text="Notes»",command=lambda:gui.enableNotes(self.frame_id,notesEnableButton),width=80) #Use the same method to trigger an API Post whenever you switch the state of a dropdown.
        #keep going tomorrow, im burntout for the day
        notesEnableButton.grid(row=0,column=4,pady=5,padx=10)

    def changestateIos(self,*args,**kwargs):
        state = self.dropStatusIos.get()
        gui.changeStateIos(self.gui,state,self.frame_id)
        
    def changestateAnd(self,*args,**kwargs):
        state = self.dropStatusAnd.get()
        gui.changeStateAnd(self.gui,state,self.frame_id)

if __name__=='__main__':
    app = gui()
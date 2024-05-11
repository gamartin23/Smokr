import customtkinter as ct
from tkinter import *
import json
from testcase import TestCase

class gui:
    def __init__(self) -> None:
        self.frameId = 0
        self.frames = {}        
        
        self.window = ct.CTk()
        self.version = 1.0
        self.window.title(f'Smokr {self.version}')
        self.window.geometry("800x500")
        ct.set_appearance_mode('dark')
        #self.window.iconbitmap(self.resourcePath('smokr.ico'))
        
        self.mainFrame = ct.CTkFrame(self.window)
        self.mainFrame.grid(row=0,column=0,padx=5,pady=5,sticky=NSEW)
        self.mainFrame.grid_columnconfigure((0),weight=1)
        self.mainFrame.grid_rowconfigure(0,weight=1)
        self.rightFrame = ct.CTkFrame(self.window)
        self.rightFrame.grid(row=0,column=1,pady=5,padx=5,sticky=EW)
        self.scroller = ct.CTkScrollableFrame(self.mainFrame,width=650,height=500)
        #self.scroller.grid(row=0,column=0,pady=10,padx=10)
        
        self.notesLabel = ct.CTkLabel(self.rightFrame,text='Notes')
        self.notesLabel.grid(row=0,column=0,pady=5,padx=5)
        self.notesEntry = ct.CTkTextbox(self.rightFrame,state='disabled')
        self.notesEntry.grid(row=1,column=0,pady=5,padx=5)
        self.relatedLabel = ct.CTkLabel(self.rightFrame,text='Related issues')
        self.relatedLabel.grid(row=2,column=0,pady=(10,5),padx=5)
        self.relatedEntry = ct.CTkTextbox(self.rightFrame,state='disabled')
        self.relatedEntry.grid(row=3,column=0,pady=5,padx=5)
        self.relatedSend = ct.CTkButton(self.rightFrame,state='disabled',text='Save',command=self.saveNote)
        self.relatedSend.grid(row=4,column=0,pady=5,padx=5)
        self.testbutton = ct.CTkButton(self.rightFrame,text='Test',command=self.updateFrame)
        self.testbutton.grid(row=5,column=0,pady=5,padx=5)
        
        self.window.after(100,self.loadPossibleStati())
        self.window.after(200,self.callJson())
        self.window.after(300,self.generateFrames())
                
        self.window.mainloop()
    
    def loadPossibleStati(self):
        with open('status_template.json', "r") as tcstatus: #remember to turn this into api calls
            data = json.load(tcstatus)
        self.stati = []
        for status in data["Status"]:
            self.stati.append(status)
        print(self.stati)
    
    def callJson(self):
        with open('template.json', "r") as tcsuite: #remember to turn this into api calls
            data = json.load(tcsuite)
        self.test_cases = []
        for item in data:
            test_case = TestCase(item["id"], item["name"], item.get("android_state", "Untested"), item.get("ios_state", "Untested"), item.get("comments", ""), item.get("related_issues", [""]))
            self.test_cases.append(test_case)
        print(self.test_cases[0].name)
        
    def generateFrames(self):
        self.frames = {}
        self.frameId = 0
        try:
            self.scroller.grid_forget()
        except:
            pass #just dont do anything if its not yet packed
        self.scroller.grid(row=0,column=0,pady=10,padx=10,sticky=EW)
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

    def enableNotes(self, id, abutton):
        self.currentNote = id
        comment = self.test_cases[id].comments
        issues = ', '.join(self.test_cases[id].related_issues)
        self.notesEntry.configure(state='normal')
        self.notesEntry.delete(0.0,END)
        self.notesEntry.insert(0.0,comment)
        self.relatedEntry.configure(state='normal')
        self.relatedEntry.delete(0.0,END)
        self.relatedEntry.insert(0.0,issues)
        self.relatedSend.configure(state='normal')
        
    def saveNote(self):
        comment = str(self.notesEntry.get(1.0,END))
        issues = str(self.relatedEntry.get(1.0,END)).strip().split(', ')
        self.test_cases[self.currentNote].comments = comment
        self.test_cases[self.currentNote].related_issues = issues
        print(self.test_cases[self.currentNote].comments,self.test_cases[self.currentNote].related_issues)

    def updateFrame(self, listToUpdate):
        for target in listToUpdate:
            if isinstance (self.frames, dict):
                updateMe = self.frames.get(target)
            else:
                pass
            if updateMe:
                updateMe.dropStatusIos.set(self.test_cases[target].ios_state)
                updateMe.dropStatusAnd.set(self.test_cases[target].android_state)
                if self.test_cases[target].android_state == self.test_cases[target].ios_state:
                    if self.test_cases[target].android_state == 'Passed':
                        updateMe.configure(fg_color='#27AE60')
                    elif self.test_cases[target].android_state == 'Failed':
                        updateMe.configure(fg_color='#C2392B')
                    elif self.test_cases[target].android_state == 'Caution':
                        updateMe.configure(fg_color='#D9A736')
                    elif self.test_cases[target].android_state == 'N/A':
                        updateMe.configure(fg_color='#7F8C8D')
                    elif self.test_cases[target].android_state == 'CNT':
                        updateMe.configure(fg_color='#2980B9')
                print('Success')


class FrameTemplate:
    def __init__(self, parent, frameId, element: TestCase, states, gui):
        self.frame_id = frameId
        self.gui = gui
        self.parent = parent
        self.tc = element
        
        frame = ct.CTkFrame(parent)
        frame.grid(row=self.frame_id,column=0,pady=2,padx=5,sticky=EW,columnspan=2)
        frame.grid_columnconfigure(1,weight=1,uniform='column',minsize=200)
        labelTc = ct.CTkLabel(frame,text=f'{self.tc.id}')
        labelTc.grid(row=0,column=0,pady=5,padx=5)
        labelName = ct.CTkLabel(frame,text=f'{self.tc.name}',wraplength=200)
        labelName.grid(row=0,column=1,pady=5,padx=5,sticky=W)
        self.dropStatusIos = ct.CTkComboBox(frame,values=states,width=90,state='readonly')
        self.dropStatusIos.grid(row=0,column=2,pady=5,padx=5,sticky=NSEW)
        self.dropStatusIos.set(self.tc.ios_state)
        self.dropStatusAnd = ct.CTkComboBox(frame,values=states,width=90,state='readonly')
        self.dropStatusAnd.grid(row=0,column=3,pady=5,padx=5,sticky=NSEW)
        self.dropStatusAnd.set(self.tc.android_state)
        if self.tc.android_state == self.tc.ios_state:
            if self.tc.android_state == 'Passed':
                frame.configure(fg_color='#27AE60')
            elif self.tc.android_state == 'Failed':
                frame.configure(fg_color='#C2392B')
            elif self.tc.android_state == 'Caution':
                frame.configure(fg_color='#D9A736')
            elif self.tc.android_state == 'N/A':
                frame.configure(fg_color='#7F8C8D')
            elif self.tc.android_state == 'CNT':
                frame.configure(fg_color='#2980B9')
        notesEnableButton = ct.CTkButton(frame,text="Notes»",command=lambda:gui.enableNotes(self.frame_id,notesEnableButton)) #Use the same method to trigger an API Post whenever you switch the state of a dropdown.
        #keep going tomorrow, im burntout for the day
        notesEnableButton.grid(row=0,column=4,pady=5,padx=5)


if __name__=='__main__':
    app = gui()
import customtkinter as ct
from tkinter import *
import json

class gui:
    def __init__(self) -> None:
        self.window = ct.CTk()
        self.version = 1.0
        self.window.title(f'Smokr {self.version}')
        self.window.resizable(False,False)
        #self.window.iconbitmap(self.resourcePath('smokr.ico'))
        self.window.after(200,self.callJson())
        
        self.mainFrame = ct.CTkFrame(self.window)
        self.mainFrame.grid(row=0,column=0,padx=5,pady=5)
        
        self.window.mainloop()
    
    def callJson(self):
        with open('template.json', "r") as tcsuite:
            data = json.load(tcsuite)
        self.test_cases = []
        for item in data:
            test_case = TestCase(item["id"], item["name"], item.get("android_state", "Untested"), item.get("ios_state", "Untested"), item.get("android_comment", ""), item.get("ios_comment", ""), item.get("related_issues", []))
            self.test_cases.append(test_case)
        print(self.test_cases[32].name)


class TestCase:
    def __init__(self, id, name, android_state='Untested',ios_state="Untested", android_comment="", ios_comment="", related_issues=[]):
        self.id = id
        self.name = name
        self.android_state = android_state
        self.ios_state = ios_state
        self.android_comment = android_comment
        self.ios_comment = ios_comment
        self.related_issues = related_issues

if __name__=='__main__':
    app = gui()
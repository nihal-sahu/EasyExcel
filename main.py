from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
import pandas
from datetime import datetime, timezone
from pathlib import Path
import random
import os
import xlsxwriter
import xlwings
from tkinter import Tk    
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askopenfilename
from openpyxl import load_workbook

Builder.load_file('frontend.kv')

class StartScreen(Screen):
    def edit(self, filepath):
        if os.path.exists(filepath) and not (filepath.endswith(".xlsx") or filepath.endswith(".xls")):
            self.ids.wrong_file.text = "ERROR: This file is not an Excel file.\nYou can try changing the file extension to .xlsx or .xls in your file explorer."
        elif not os.path.exists(filepath): 
            self.ids.wrong_file.text = "ERROR: This file does not exist. Please try again."
        else: 
            self.manager.transition.direction = "left"
            self.manager.current = "sheet_editor"
            
    def create_new(self): 
        Tk().withdraw()
        global filepath
        filepath = asksaveasfilename(
                filetypes=(
                    ("Excel Workbook", "*.xlsx *.xls"),
                    ("All files", "*.*"),
                ),
                defaultextension = ".xlsx"
            )
        
        if filepath != "":
            self.ids.filepath.text = filepath

            filename = filepath[filepath.rfind("/") + 1:]

            workbook = xlsxwriter.Workbook(filepath)
            worksheet = workbook.add_worksheet()
            workbook.close()
        
        if os.path.exists(filepath):
            self.ids.wrong_file.text = f"{filename} was created successfully. Click edit."

    def browse(self):
        Tk().withdraw()
        global filepath
        filepath = askopenfilename() 
        self.ids.filepath.text = filepath

        filename = filepath[filepath.rfind("/") + 1:]
        if os.path.exists(filepath):
            self.ids.wrong_file.text = f"{filename} was loaded successfully. Click edit."

class SheetEditor(Screen):
    def previous_sheet(self):
        self.manager.transition.direction = "right"
        self.manager.current = "start_screen"
    def add(self, sheet_name, dollar_amount, comment, date):
        sheet_name = sheet_name.lower().title()

        current_sheet = pandas.read_excel(filepath, sheet_name)
        temp_sheet = pandas.read_excel(filepath, sheet_name)
        temp_sheet = temp_sheet.iloc[0:1, :]

        if "Unnamed: 0" in temp_sheet.columns:
            temp_sheet = temp_sheet.drop(columns = "Unnamed: 0")

        current_datetime = str(datetime.now())

        temp_sheet["Comment"] = [comment]
        temp_sheet["Amount($)"] = [dollar_amount]
        temp_sheet["Date"] = [date]
        temp_sheet["Date Added"] = [current_datetime]
        
        current_sheet = current_sheet.append(temp_sheet, ignore_index = True)
        
        if "Unnamed: 0" in current_sheet.columns:
            current_sheet = current_sheet.drop(columns = "Unnamed: 0")
        
        with pandas.ExcelWriter(filepath, engine="openpyxl", mode='a', if_sheet_exists = "replace") as writer:  
            current_sheet.to_excel(writer, sheet_name = sheet_name, )
        
        self.ids.error_message.text = f"Entry of ${dollar_amount} successfully added to {sheet_name}"


class RootWidget(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__ == "__main__":
    MainApp().run()
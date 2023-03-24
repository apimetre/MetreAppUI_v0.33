# Python imports
import os
import numpy as np
import datetime as datetime
import time
import json
from pytz import timezone

# Pythonista imports
import ui


class TData (ui.ListDataSource):
    def __init__(self, scale, items=None):
        ui.ListDataSource.__init__(self, items)
        self.xscale = scale
        
    def tableview_cell_for_row(self, tableview, section, row):
        cell = ui.TableViewCell()
        cell.text_label.text = str(self.items[row])
        scaled_size = round(self.xscale, 1) *1.5 + 12

        cell.text_label.font = ("Helvetica", scaled_size)
        cell.text_label.alignment = ui.ALIGN_CENTER
        return cell
    

class ResultsTable(object):
    def __init__(self, subview_, table_, xscale, yscale, cwd):
        self.subview = subview_
        self.table = table_      
        self.xscale = xscale
        self.yscale = yscale
        self.cwd = cwd
        self.log_src = (self.cwd + '/log/log_003.json')
        
        with open(self.log_src) as json_file:
            self.log = json.load(json_file)        
            
        if self.xscale > 2:
            self.spacer = '    '
        else:
            self.spacer = '  '
        with open(self.log_src) as json_file:
            self.log = json.load(json_file) 
            
        self.etime = self.log['Etime']   
        self.sorted_etime = sorted(list(self.etime))

        self.dt_etime = []
        for val in self.etime:
                tval = datetime.datetime.fromtimestamp(int(val))
                self.dt_etime.append(tval)     
        self.acetone = self.log['Acetone']
        
        ############### This is for displaying '< 2' for acetone values < 2 ##############
        self.acetone_str = []
        for val in self.acetone:
            if float(val) < 2:
                self.acetone_str.append("< 2")
            else:
                self.acetone_str.append(str(round(val,1)))
        ###################################################################################
        
        new_sorted_etime = sorted(list(self.etime)) # This is the sorted version of self.log['Etime']
        
        new_sorted_dt = sorted(self.dt_etime)
        
        self.rev_sort_etime = list(reversed(new_sorted_etime))         
        dt_list = []
        orig_dt_list = [] 
        for i in new_sorted_dt:
            dt_list.append(i.strftime("%b %d, %Y, %I:%M %p"))
        for i in self.dt_etime:
            orig_dt_list.append(i.strftime("%b %d, %Y, %I:%M %p"))
            
        results = []
        self.ref_list_inv = []
        for i in dt_list:
            results.append(i + self.spacer + self.acetone_str[np.where(np.array(orig_dt_list) == i)[0][0]] + ' ppm ' + np.array(self.log['Key'])[np.where(np.array(orig_dt_list) == i)[0][0]])
            self.ref_list_inv.append(np.where(np.array(orig_dt_list) == i)[0][0])
         
        self.ref_list = list(reversed(self.ref_list_inv))
        self.table.data_source =  TData(self.xscale, reversed(results))
        self.table.delegate.action = self.write_notes
        
    def update_table(self):
        self.table.reload()        
        with open(self.log_src) as json_file:
            self.log = json.load(json_file) 
            
        self.etime = self.log['Etime']   
        self.dt_etime = []
        for val in self.etime:
                tval = datetime.datetime.fromtimestamp(int(val))
                self.dt_etime.append(tval)     
        self.acetone = self.log['Acetone']
        
        ############### This is for displaying '< 2' for acetone values < 2 ##############
        self.acetone_str = []
        for val in self.acetone:
            if float(val) < 2:
                self.acetone_str.append("< 2")
            else:
                self.acetone_str.append(str(round(val,1)))
        ###################################################################################        
        
        new_sorted_etime = sorted(list(self.etime)) # This is the sorted version of self.log['Etime']
        new_sorted_dt = sorted(self.dt_etime)
        self.rev_sort_etime = list(reversed(new_sorted_etime)) 
        dt_list = []
        orig_dt_list = [] 
        for i in new_sorted_dt:
            dt_list.append(i.strftime("%b %d, %Y, %I:%M %p"))
        for i in self.dt_etime:
            orig_dt_list.append(i.strftime("%b %d, %Y, %I:%M %p"))
            
        results = []
        self.ref_list_inv = []
        for i in dt_list:
            results.append(i + self.spacer + self.acetone_str[np.where(np.array(orig_dt_list) == i)[0][0]] + ' ppm ' + np.array(self.log['Key'])[np.where(np.array(orig_dt_list) == i)[0][0]])
            self.ref_list_inv.append(np.where(np.array(orig_dt_list) == i)[0][0])
         
        self.ref_list = reversed(self.ref_list_inv)
                
        self.table.data_source =  TData(self.xscale, reversed(results))
        
    def write_notes(self, sender):
        with open(self.log_src) as json_file:
            self.log = json.load(json_file)        
        self.row_ix = sender.selected_row
        self.log_entry = self.log['Notes'][np.where(np.array(self.etime) == self.rev_sort_etime[self.row_ix])[0][0]]#self.log['Notes'][self.row_ix]
        
        self.tdialog = ui.load_view('tabledialog')
        self.tdialog.name = self.table.data_source.items[sender.selected_row]
        self.tdialog.frame = (0,0,600,150)
        update_button = self.tdialog['update']
        replace_button = self.tdialog['replace']
        self.tdialog['test_notes'].text = self.log_entry
        update_button.action = self.update_log_notes
        replace_button.action = self.replace_log_notes
        self.tdialog.frame = (0, 0, 600, 150)

        self.tdialog.present('Sheet')
        

    def update_log_notes(self, sender):
        self.update_table()

        current_entry = self.log_entry
        entry_to_add = self.tdialog['text_entry'].text
        try:
            if entry_to_add[0].isupper():
                try:
                    if current_entry[-1] != '.':
                        spacer = '. '
                    else:
                        spacer = '  '
                except:
                    spacer = ''
            
            
            elif entry_to_add[0].isdigit():
                try:
                    if current_entry[-1] != '.':
                        spacer = '. '
                    else:
                        spacer = ', '
                except:
                    spacer = ''
                    
            else:
                try:
                    if current_entry[-1] != ',':
                        spacer = ', '
                    else:
                        spacer = '  '
                except:
                    spacer = ''           

            new_entry = self.log_entry + spacer + entry_to_add 


            self.log['Notes'][np.where(np.array(self.etime) == self.rev_sort_etime[self.row_ix])[0][0]] = new_entry
                              
            
            self.log['Key'][np.where(np.array(self.etime) == self.rev_sort_etime[self.row_ix])[0][0]] = " *"
            with open(self.log_src, "w") as outfile:
                json.dump(self.log, outfile)
                    
            self.tdialog['test_notes'].text = self.log['Notes'][np.where(np.array(self.etime) == self.rev_sort_etime[self.row_ix])[0][0]]
            self.tdialog['text_entry'].text = ''
        except:
            self.tdialog['text_entry'].text = ''
        self.tdialog['text_entry'].end_editing()        
        self.update_table()
        self.table.delegate.action = self.write_notes                           
    def replace_log_notes(self, sender):
        self.update_table()
        current_entry = self.log_entry
        entry_to_add = self.tdialog['text_entry'].text           
        try:
            self.log['Notes'][np.where(np.array(self.etime) == self.rev_sort_etime[self.row_ix])[0][0]] = entry_to_add
            if entry_to_add != '':
                self.log['Key'][np.where(np.array(self.etime) == self.rev_sort_etime[self.row_ix])[0][0]] = " *"  
            else: 
                self.log['Key'][np.where(np.array(self.etime) == self.rev_sort_etime[self.row_ix])[0][0]] = ''          
            with open(self.log_src, "w") as outfile:
                json.dump(self.log, outfile)
                    
            self.tdialog['test_notes'].text = self.log['Notes'][np.where(np.array(self.etime) == self.rev_sort_etime[self.row_ix])[0][0]]
            self.tdialog['text_entry'].text = ''    
        except:
            self.tdialog['text_entry'].text = ''    
        self.tdialog['text_entry'].end_editing()   
        self.update_table()
        self.table.delegate.action = self.write_notes 

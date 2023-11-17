import os
import dearpygui.dearpygui as dpg
from enum import StrEnum, auto
import json


#CONFIG_PATH = os.path.join(os.path.expanduser('~'), '.txttable')
CONFIG_PATH = './conf.json'

class Element(StrEnum):
    PRIMARY_WINDOW = auto()
    TABLE = auto()
    MENU_BAR = auto()
    MENU_FILE = auto()
    TARGET_FILE_PATH_INPUT = auto()
    STATUS_BAR = auto()

class Table:
    def __init__(self, rows=10, columns=16):
        self.rows = rows
        self.columns = columns
        self.column_width = 200
        self.column_height = 54
        self._data = []
        self._table_wrapper_tag = f'{Element.TABLE}#wrapper'

    def _make_table(self):
        print('make table')
        with dpg.table(tag=Element.TABLE, parent=self._table_wrapper_tag,
            borders_outerH=True, borders_outerV=True,
            borders_innerV=True, borders_innerH=True,
            no_pad_innerX=True, no_pad_outerX=True,
            resizable=True, policy=dpg.mvTable_SizingFixedFit,
            header_row=False, scrollX=True):
            
            for i in range(self.columns):
                dpg.add_table_column()
            
            data_length = len(self._data)
            for i in range(self.rows):
                with dpg.table_row():
                    for j in range(self.columns):
                        index = i*self.columns + j
                        cell_value = self._data[index] if index < data_length else ''
                        #print(cell_value, sep=' ')
                        #dpg.add_text('kek')
                        with dpg.group(width=self.column_width) as g:
                            dpg.add_input_text(
                                tag=self.get_cell_tag(i, j), default_value=cell_value,
                                width=self.column_width, height=self.column_height, multiline=True)

    def make(self):
        dpg.add_child_window(label='Table window', tag=self._table_wrapper_tag,
            horizontal_scrollbar=True)
        self._make_table() 

    def _remake(self):
        '''delete table and create again'''
        dpg.delete_item(Element.TABLE)
        self._make_table()
    
    def _resize(self, rows, columns):
        self.rows = rows
        self.columns = columns
    
    def set_data(self, data: list[str]):
        print(data)
        self._data = data.copy()
        n = len(data)
        new_rows = max(self.rows, (n + self.columns - 1) // self.columns)
        self._resize(rows=new_rows, columns=self.columns)
        self._remake()
         
    def get_data(self):
        data = []
        for row in range(self.rows):
            for col in range(self.columns):
                tag = self.get_cell_tag(row, col)
                value = dpg.get_value(tag)
                data.append(value)
        return data
        
    def get_cell_tag(self, i, j):
        return f'{Element.TABLE}#{i}_{j}'


class Config:
    def __init__(self, path=CONFIG_PATH):
        self._path = path
        if not os.path.exists(path):
            with open(path, 'w') as f:
                json.dump(dict(), f)

        self.config = self.load_config_file()
    
    def set_target_file_path(self, file_path):
        self.config['target_file_path'] = file_path
        self.save_config_file()
   
    def get_target_file_path(self):
        return self.config.get('target_file_path', '')

    def load_config_file(self):
        with open(self._path) as f:
            return json.load(f)

    def save_config_file(self):
        with open(self._path, 'w') as f:
            json.dump(self.config, f)

class StatusBar:
    def __init__(self):
        pass 

    def make(self):
        dpg.add_text('Welcome!', tag=Element.STATUS_BAR)

    def set_status(self, text, bad=False, good=False):
        dpg.set_value(Element.STATUS_BAR, text)
        if bad:
            color = (255, 0, 0)
        elif good:
            color = (0, 255, 0)
        else:
            color = (255, 255, 255)

        dpg.configure_item(Element.STATUS_BAR, color=color)


def menu():
    with dpg.menu_bar(tag=Element.MENU_BAR):
        with dpg.menu(label='File', tag=Element.MENU_FILE):
            dpg.add_menu_item(label='test')


class App:
    def __init__(self, config):
        self.config = config
        self.table = Table()
        self.status_bar = StatusBar()

    def make_gui(self):
        with dpg.window(tag=Element.PRIMARY_WINDOW):
            #menu()
            self.status_bar.make()
            with dpg.group(horizontal=True):
                dpg.add_text('Target file path:')
                dpg.add_input_text(tag=Element.TARGET_FILE_PATH_INPUT, default_value=self.config.get_target_file_path(), width=250)
                dpg.add_button(label='Load', callback=self.on_load_file)
                dpg.add_button(label='Save', callback=self.on_save_file)
            self.table.make()

    def run_gui(self):
        self.on_load_file()
        dpg.set_primary_window(Element.PRIMARY_WINDOW, True)
        dpg.start_dearpygui()

    def on_load_file(self):
        target_file_path_value = self.get_target_file_path()
        self.load_file(target_file_path_value)

    def on_save_file(self):
        target_file_path_value = self.get_target_file_path()
        self.save_file(target_file_path_value)

    def load_file(self, file_path):
        file_path = os.path.expanduser(file_path)
        if os.path.exists(file_path):
            self.config.set_target_file_path(file_path)
            with open(file_path) as f:
                data = f.read().split('\n\n')
                self.table.set_data(data)
            self.status_bar.set_status(f'File {file_path} loaded')
        elif file_path == '':
            self.status_bar.set_status('Enter file name and press \'Load\'')
        else:
            self.status_bar.set_status(f'File {file_path} not found!', bad=True)
    
    def save_file(self, file_path):
        data = self.table.get_data()
        with open(file_path, 'w') as f:
            f.write('\n\n'.join(data))

    def get_target_file_path(self):
        return dpg.get_value(Element.TARGET_FILE_PATH_INPUT)


if __name__ == '__main__':
    dpg.create_context()
    with dpg.font_registry():
        default_font = dpg.add_font('fonts/OpenSans-Regular.ttf', 24)
    dpg.bind_font(default_font)
    config = Config()
    app = App(config)
    dpg.setup_dearpygui()
    dpg.create_viewport(title='TxT Table', width=1600, height=800)
    dpg.show_viewport()
    app.make_gui()
    app.run_gui()
    dpg.destroy_context()

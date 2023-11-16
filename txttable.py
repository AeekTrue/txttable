import os.path
from typing import List
import dearpygui.dearpygui as dpg
from dearpygui_ext.themes import create_theme_imgui_light
from itertools import repeat
from config import *
import json

dpg.create_context()
print(USER_DATA_DIR)
print(USER_CONFIG_PATH)

def init_user_data_dir():
    if not os.path.exists(USER_DATA_DIR):
        os.makedirs(USER_DATA_DIR)
    if not os.path.exists(USER_CONFIG_PATH):
        with open(USER_CONFIG_PATH, 'w') as f:
            json.dump(dict(), f)


def load_config() -> dict:
    if os.path.exists(USER_CONFIG_PATH):
        with open(USER_CONFIG_PATH, 'r') as f:
            return json.load(f)
    else:
        return dict()


def save_config(config: dict):
    with open(USER_CONFIG_PATH, 'w') as f:
        json.dump(config, f)


class App:
    def __init__(self):
        init_user_data_dir()
        self.config = load_config()
        if 'target_file_path' in self.config:
            self.target_file_path = self.config['target_file_path']
            dpg.set_value('path input', self.target_file_path)
            load_txt()
        else:
            self.target_file_path = None

    def set_target_file_path(self, file_path):
        self.target_file_path = file_path
        self.config['target_file_path'] = file_path
        save_config(self.config)


TABLE_ID = -1
TABLE_W = 16
TABLE_H = 10
app = App()


def set_target_file_path():
    pass


def _log(sender, app_data, user_data):
    print(f"sender: {sender}, \t app_data: {app_data}, \t user_data: {user_data}")


def get_filename() -> str:
    filename = os.path.expanduser(dpg.get_value('path input'))
    app.set_target_file_path(filename)
    return filename


def load_txt():
    filename = get_filename()
    text = ''
    with open(filename, 'r') as f:
        text = f.read()

    splitted_text = text.split('\n\n')
    matrix = []
    for row in range((len(splitted_text) + TABLE_W - 1) // TABLE_W):
        matrix.append(splitted_text[row * TABLE_W: (row + 1) * TABLE_W])
    set_table_content(matrix)


def save_txt():
    filename = get_filename()
    text = get_table_txt()
    with open(filename, 'w') as f:
        f.write(text)


def set_table_content(content: List[str]):
    for i in range(TABLE_H):
        if i >= len(content):
            break
        for j in range(TABLE_W):
            if j >= len(content[i]):
                break
            tag = f'##{i}_{j}'
            # print(tag)
            dpg.set_value(tag, content[i][j])


def get_table_content():
    content = []
    for i in range(TABLE_H):
        content.append([])
        for j in range(TABLE_W):
            tag = f'##{i}_{j}'
            # print(tag)
            content[i].append(dpg.get_value(tag))
    print(content)


def get_table_txt():
    text = []
    for row in range(TABLE_H):
        for col in range(TABLE_W):
            tag = f'##{row}_{col}'
            value = dpg.get_value(tag)
            text.append(value)
    return '\n\n'.join(text)


def on_save_txt():
    save_txt()


def on_load_txt():
    load_txt()


def menu_bar():
    with dpg.menu_bar(label="Menu bar"):
        with dpg.menu(label="File"):
            pass
        with dpg.menu(label="About"):
            pass


def table():
    global TABLE_ID
    column_width = 100
    with dpg.child_window(label='Table window', horizontal_scrollbar=True):
        with dpg.table(borders_outerH=True, borders_outerV=True,
                       borders_innerV=True, borders_innerH=True,
                       header_row=False, width=column_width * TABLE_W, no_pad_innerX=True,
                       no_pad_outerX=True, resizable=True, policy=dpg.mvTable_SizingStretchSame) as tbl:
            TABLE_ID = tbl
            for i in range(TABLE_W):
                dpg.add_table_column(label=str(i))

            for i in range(TABLE_H):
                with dpg.table_row():
                    for j in range(TABLE_W):
                        dpg.add_input_text(tag=f"##{i}_{j}", width=-1, height=40, multiline=True)


def ui():
    with dpg.window(label="", tag='pm'):
        menu_bar()
        dpg.add_button(label="Load from file", callback=on_load_txt)
        dpg.add_input_text(tag='path input')
        dpg.set_value('path input', '~/.txttable')
        dpg.add_button(label="Save to file", callback=on_save_txt)
        table()


def primary_window():
    ui()
    dpg.set_primary_window('pm', True)


def main():
    with dpg.font_registry():
        default_font = dpg.add_font('fonts/OpenSans-Regular.ttf', 24)
    with dpg.handler_registry():
        dpg.add_key_press_handler(dpg.mvKey_Escape, callback=lambda: print('lol'))

    dpg.bind_font(default_font)
    # light_theme = create_theme_imgui_light()
    # dpg.bind_theme(light_theme)

    # dpg.show_item_registry()
    dpg.create_viewport(title='TxT Table', width=1600, height=800)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    primary_window()
    dpg.start_dearpygui()
    dpg.destroy_context()

import dearpygui.dearpygui as dpg


dpg.create_context()


def _log(sender, app_data, user_data):
    print(f"sender: {sender}, \t app_data: {app_data}, \t user_data: {user_data}")

def menu_bar():
    with dpg.menu_bar(label="Menu bar"):
        with dpg.menu(label="File"):
            pass
        with dpg.menu(label="About"):
            pass

def table():
    columns, rows = 16, 10
    column_width = 100
    with dpg.child_window(label='Table window', horizontal_scrollbar=True):
        with dpg.table(borders_outerH=True, borders_outerV=True,
                       borders_innerV=True, borders_innerH=True,
                       header_row=False, width=column_width*columns, no_pad_innerX=True,
                       no_pad_outerX=True):
            for i in range(columns):
                dpg.add_table_column(label=str(i), width=100)

            for i in range(rows):
                with dpg.table_row():
                    for j in range(columns):
                        dpg.add_input_text(width=100, multiline=True)

def ui():
    with dpg.window(label="", tag='pm'):
        menu_bar()
        table()
        dpg.add_text('hello')


def primary_window():
    ui()
    dpg.set_primary_window('pm', True)

def main():
    with dpg.font_registry():
        default_font = dpg.add_font('fonts/OpenSans-Regular.ttf', 24)
    with dpg.handler_registry():
        dpg.add_key_press_handler(dpg.mvKey_Escape, callback=lambda: print('lol'))
    dpg.bind_font(default_font)

    dpg.create_viewport(title='TxT Table', width=600, height=600)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    primary_window()
    dpg.start_dearpygui()
    dpg.destroy_context()

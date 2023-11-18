#!/usr/bin/python
import dearpygui.dearpygui as dpg
import dearpygui.demo as demo

dpg.create_context()
with dpg.font_registry():
    default_font = dpg.add_font('data/fonts/OpenSans-Regular.ttf', 24)
dpg.bind_font(default_font)


dpg.create_viewport(title='Custom Title', width=800, height=1000)

demo.show_demo()
dpg.set_primary_window('__demo_id', value=True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
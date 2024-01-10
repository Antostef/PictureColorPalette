import asyncio

import PySimpleGUI as sg

from processing.processing import get_colors_from_picture
from utils.constants import STEP_PROMPT, STEP_DESC, COLORS_OUTPUT_PROMPT, COLORS_OUTPUT_DESC

use_custom_titlebar = True if sg.running_trinket() else False

def make_window(theme=None):
    NAME_SIZE = 23

    def name(name):
        dots = NAME_SIZE-len(name)-2
        return sg.Text(name + ' ' + '•'*dots, size=(NAME_SIZE,1), justification='r',pad=(0,0), font='Courier 10')

    sg.theme("Tan")

    # NOTE that we're using our own LOCAL Menu element
    if use_custom_titlebar:
        Menu = sg.MenubarCustom
    else:
        Menu = sg.Menu

    treedata = sg.TreeData()

    treedata.Insert("", '_A_', 'Tree Item 1', [1234], )
    treedata.Insert("", '_B_', 'B', [])
    treedata.Insert("_A_", '_A1_', 'Sub Item 1', ['can', 'be', 'anything'], )

    layout = [
            [sg.T('Color Palette Maker', font='_ 14', justification="l")]
            , [sg.FileBrowse('import your image', button_color="grey", font="_ 16", key="import_img", enable_events=True)],
            [sg.T(COLORS_OUTPUT_PROMPT, font="_ 16"), sg.InputText("", key="colors_out", s=(5,1))],
            [sg.T(COLORS_OUTPUT_DESC, font="_ 10")],
            [sg.T(STEP_PROMPT, font="_ 16"), sg.InputCombo(values=[1,2,4,8,16,32,64], key="step",)],
            [sg.T(STEP_DESC, font="_ 10")],
            [sg.Checkbox("Output as a file", key="as_a_file")],
            [sg.Graph(canvas_size=(500, 500), graph_bottom_left=(0, 0), graph_top_right=(500, 500), enable_events=True, drag_submits=True, key="graph", expand_x=True, expand_y=True, visible=False)],
            [sg.SaveAs(target=(None, None), key="file_path", enable_events=True)]            
    ]

    window = sg.Window('Color Palette', layout, size=(800, 800), finalize=True, right_click_menu=sg.MENU_RIGHT_CLICK_EDITME_VER_EXIT, keep_on_top=False, use_custom_titlebar=use_custom_titlebar)

    # window['-PBAR-'].update(30)                                                     # Show 30% complete on ProgressBar
    # window['-GRAPH-'].draw_image(data=sg.EMOJI_BASE64_HAPPY_JOY, location=(0,50))   # Draw something in the Graph Element

    return window


async def create_pcp(img_path, number_of_colors, step, as_a_file):
    await get_colors_from_picture(img_path, number_of_colors=number_of_colors, step=step, as_a_file=as_a_file)


window = make_window()

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Exit':
        break
        
    if event == "import_img":
        img_path = values.get("import_img")
        if img_path is not None:
            get_colors_from_picture(img_path, number_of_colors=int(values.get("colors_out", 5)), step=values.get("step", 16), as_a_file=values.get("as_a_file", False))
            window["graph"].update(visible=True)
            window["graph"].draw_image(filename=r"C:\Users\antod\code\PictureColorPalette\src\out\color_palette.png", location=(0, 500))
            print("comes here")
            values.update({"file_path": r"C:\Users\antod\code\PictureColorPalette\src\out\color_palette.png"}) 
            print(values)
        

window.close() 
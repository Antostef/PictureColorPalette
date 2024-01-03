import PySimpleGUI as sg

from processing.processing import get_colors_from_picture

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
            [sg.T('Color Palette Maker', font='_ 14', justification="l", expand_x=True)],
            [sg.FileBrowse('import your image', button_color="grey", font="_ 16", key="import_img", enable_events=True)],
            [sg.Graph(canvas_size=(500, 500), graph_bottom_left=(0, 0), graph_top_right=(500, 500), enable_events=True, drag_submits=True, key="graph", expand_x=True, expand_y=True, visible=False)],
            [sg.Button("Show image", key="btn")]
    ]

    window = sg.Window('Color Palette', layout, finalize=True, right_click_menu=sg.MENU_RIGHT_CLICK_EDITME_VER_EXIT, keep_on_top=False, use_custom_titlebar=use_custom_titlebar)

    # window['-PBAR-'].update(30)                                                     # Show 30% complete on ProgressBar
    # window['-GRAPH-'].draw_image(data=sg.EMOJI_BASE64_HAPPY_JOY, location=(0,50))   # Draw something in the Graph Element

    return window


window = make_window()

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    
    if event == "btn":
        window["graph"].update(visible=True)
        window["graph"].draw_image(filename=r"C:\Users\antod\code\PictureColorPalette\src\out\color_palette.png", location=(0, 500))
        
    if event == "import_img":
        img_path = values.get("import_img")
        if img_path is not None:
            get_colors_from_picture(img_path)
        

window.close()
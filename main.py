#!/bin/python3
import inspect
import os
import sys
import PySimpleGUI as sg


def get_script_dir(follow_symlinks=True):
    if getattr(sys, 'frozen', False):
        path = os.path.abspath(sys.executable)
    else:
        path = inspect.getabsfile(get_script_dir)
    if follow_symlinks:
        path = os.path.realpath(path)
    return os.path.dirname(path)


BK_COLOR = "#E8E36A"
BK_NUMS_COLOR = "#BCB62B"
BK_SHOP_COLOR = "#4ABCD3"
BK_WARNING_COLOR = "#9D26F4"

END_GAME_LAYOUT = [[sg.Text("Congratulations, you have earned 1000000000 "
                            "coins!!!", background_color="#FF5733",
                            size=(50, 5), font=('Helvetica', 15))],
                   [sg.Text("Now you can leave the game, or take "
                            "multiplicators for the next one",
                            background_color="#FF5733", size=(50, 5),
                            font=('Helvetica', 15))],
                   [sg.Button("Play next game", key="-Next-", size=(75, 5),
                              button_color="#31E858")],
                   [sg.Button("Leave the game", key="-Leave-", size=(75, 3),
                              button_color="#D51B1B")]]

END_GAME_WINDOW = sg.Window("", END_GAME_LAYOUT, no_titlebar=True,
                            keep_on_top=True, background_color="#FF5733")

WARNING_LAYOUT = [[sg.Text("Sorry, you don't have enough money",
                           background_color=BK_WARNING_COLOR,
                           font=('Helvetica', 12))],
                  [sg.Button("Back", key='-Back-', button_color="#394CEA",
                             size=(40, 2))]]

WARNING_WINDOW = sg.Window("Warning", WARNING_LAYOUT, no_titlebar=True,
                           keep_on_top=True, grab_anywhere=True,
                           background_color=BK_WARNING_COLOR)

SHOP_LAYOUT = [[sg.Text("Value:", size=(10, 1), pad=((10, 0), 0),
                        font=('Helvetica', 20),
                        background_color=BK_SHOP_COLOR),
                sg.Text("Cost:", size=(10, 1), pad=((10, 0), 0),
                        font=('Helvetica', 20),
                        background_color=BK_SHOP_COLOR)],
               [sg.Text("Per_sec:", size=(10, 1), pad=((10, 0), 0),
                        font=('Helvetica', 20),
                        background_color=BK_SHOP_COLOR),
                sg.OptionMenu(values=("0 0", "10 100", "20 200",
                                      "50 500", "100 10000", "200 20000",
                                      "500 50000"), size=(10, 1),
                              default_value="0 0",
                              tooltip="Buy multiplier for coins per second")],
               [sg.Text("Per_click:", size=(10, 1), pad=((10, 0), 0),
                        font=('Helvetica', 20),
                        background_color=BK_SHOP_COLOR),
                sg.OptionMenu(values=("0 0", "10 1000", "20 2000",
                                      "50 5000", "100 10000", "200 20000",
                                      "500 50000"), size=(10, 1),
                              default_value="0 0",
                              tooltip="Buy multiplier for coins per click")],
               [sg.Button("Exit", size=(15, 1),
                          button_color=('white', '#F0384B'), key='-Exit-'),
                sg.Button("Submit", size=(15, 1),
                          button_color=('white', '#3EE95D'), key='-Submit-')]]

SHOP_WINDOW = sg.Window("Shop Menu", SHOP_LAYOUT, no_titlebar=True,
                        keep_on_top=False, grab_anywhere=True,
                        background_color=BK_SHOP_COLOR)

MAIN_LAYOUT = [[sg.Text("Total:", size=(10, 1), pad=((10, 0), 0),
                        font=('Helvetica', 20),
                        background_color=BK_NUMS_COLOR),
                sg.Text('', size=(23, 1), font=('Helvetica', 20),
                        justification='center', tooltip="You total coins",
                        background_color=BK_NUMS_COLOR, key='total')],
               [sg.Text("Per_sec:", size=(10, 1), pad=((10, 0), 0),
                        font=('Helvetica', 20),
                        background_color=BK_NUMS_COLOR,),
                sg.Text('', size=(23, 1), font=('Helvetica', 20),
                        justification='center', key='per_sec',
                        tooltip="Coins, you earn per second",
                        background_color=BK_NUMS_COLOR)],
               [sg.Text("Per_click:", size=(10, 1), pad=((10, 0), 0),
                        font=('Helvetica', 20),
                        background_color=BK_NUMS_COLOR),
                sg.Text('', size=(23, 1), font=('Helvetica', 20),
                        justification='center', background_color=BK_NUMS_COLOR,
                        key='per_click', tooltip="Coins, you earn per click")],
               [sg.Button('', image_filename=f"{get_script_dir()}/cookie.png",
                          border_width=0, size=(5, 5),
                          button_color=BK_COLOR, key='-Click-')],
               [sg.Button("Shop", size=(20, 2), key='-Shop-',
                          button_color=('white', BK_NUMS_COLOR))]]

MAIN_WINDOW = sg.Window("Clicker", MAIN_LAYOUT, background_color=BK_COLOR)

if __name__ == "__main__":
    TOTAL = int(0)
    PROFIT_PER_SEC = int(1)
    PROFIT_PER_CLICK = int(10)

    MAIN_EVENT, MAIN_VALUES = MAIN_WINDOW.read(timeout=0)
    MAIN_WINDOW['total'].update(f'{TOTAL}')
    MAIN_WINDOW['per_sec'].update(f'{PROFIT_PER_SEC}')
    MAIN_WINDOW['per_click'].update(f'{PROFIT_PER_CLICK}')

    SHOP_EVENT, SHOP_VALUES = SHOP_WINDOW.read(timeout=0)
    FLAG_OPEN_SHOP = False
    FLAG_OPEN_WARNING = False

    while True:
        SHOP_WINDOW.hide()
        MAIN_EVENT, MAIN_VALUES = MAIN_WINDOW.read(timeout=1000)
        if TOTAL > 1000000000:
            while True:
                END_GAME_EVENT, END_GAME_VALUES = END_GAME_WINDOW.read()
                if END_GAME_EVENT == "-Leave-":
                    END_GAME_WINDOW.hide()
                    MAIN_EVENT = sg.WIN_CLOSED
                    break
                else:
                    PROFIT_PER_CLICK *= 100
                    PROFIT_PER_SEC *= 100
                    TOTAL = 0
                    END_GAME_WINDOW.close()
                    break

        if MAIN_EVENT == sg.WIN_CLOSED:
            SHOP_WINDOW.hide()
            FLAG_OPEN_SHOP = False
            break
        elif MAIN_EVENT == "-Click-":
            TOTAL += PROFIT_PER_CLICK
        elif MAIN_EVENT == "-Shop-" and not FLAG_OPEN_SHOP:
            FLAG_OPEN_SHOP = True
            SHOP_WINDOW.un_hide()
            SHOP_EVENT, SHOP_VALUES = SHOP_WINDOW.read(timeout=0)
            while True:
                SHOP_EVENT, SHOP = SHOP_WINDOW.read()
                SHOP_VALUES = {0: SHOP[0].split(' '), 1: SHOP[1].split(' ')}
                if MAIN_EVENT == sg.WIN_CLOSED:
                    SHOP_EVENT = ''
                    SHOP_WINDOW.hide()
                    FLAG_OPEN_SHOP = False
                    break
                if SHOP_EVENT == '-Submit-':
                    if int(SHOP_VALUES[0][1]) + int(SHOP_VALUES[1][1]) > TOTAL:
                        if FLAG_OPEN_WARNING:
                            WARNING_WINDOW.un_hide()
                        FLAG_OPEN_WARNING = True
                        WARNING_EVENT, WARNING_VALUES = WARNING_WINDOW.read()
                        if WARNING_EVENT == '-Back-':
                            WARNING_WINDOW.hide()
                    else:
                        TOTAL -= int(SHOP_VALUES[0][1])
                        PROFIT_PER_SEC += int(SHOP_VALUES[0][0])
                        TOTAL -= int(SHOP_VALUES[1][1])
                        PROFIT_PER_CLICK += int(SHOP_VALUES[1][0])
                        MAIN_WINDOW['total'].update(f'{TOTAL}')
                        MAIN_WINDOW['per_sec'].update(f'{PROFIT_PER_SEC}')
                        MAIN_WINDOW['per_click'].update(f'{PROFIT_PER_CLICK}')
                if SHOP_EVENT == '-Exit-':
                    SHOP_EVENT = ''
                    FLAG_OPEN_SHOP = False
                    SHOP_WINDOW.hide()
                    break

        TOTAL += PROFIT_PER_SEC
        MAIN_WINDOW['total'].update(f'{TOTAL}')
        MAIN_WINDOW['per_sec'].update(f'{PROFIT_PER_SEC}')
        MAIN_WINDOW['per_click'].update(f'{PROFIT_PER_CLICK}')

    WARNING_WINDOW.close()
    SHOP_WINDOW.close()
    MAIN_WINDOW.close()

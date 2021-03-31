#!/bin/bash
import PySimpleGUI as sg

warning_layout = [[sg.Text("Sorry, you don't have enough money")],
                  [sg.Button("Back", key='-Back-')]]

warning_window = sg.Window("Warning", warning_layout, no_titlebar=True,
                           keep_on_top=True, grab_anywhere=True)

shop_layout = [[sg.Text("Value:", size=(10, 1), pad=((10, 0), 0),
                        font=('Helvetica', 20)),
                sg.Text("Cost:", size=(10, 1), pad=((10, 0), 0),
                        font=('Helvetica', 20))],
               [sg.Text("Per_sec:", size=(10, 1), pad=((10, 0), 0),
                        font=('Helvetica', 20)),
                sg.OptionMenu(values=("0 0", "10 100", "20 200",
                                      "50 500", "100 10000", "200 20000",
                                      "500 50000"), size=(10, 1),
                              default_value="0 0")],
               [sg.Text("Per_click:", size=(10, 1), pad=((10, 0), 0),
                        font=('Helvetica', 20)),
                sg.OptionMenu(values=("0 0", "10 1000", "20 2000",
                                      "50 5000", "100 10000", "200 20000",
                                      "500 50000"), size=(10, 1),
                              default_value="0 0")],
               [sg.Button("Exit", size=(15, 1),
                          button_color=('white', '#A81D29'), key='-Exit-'),
                sg.Button("Submit", size=(15, 1),
                          button_color=('white', '#13B722'), key='-Submit-')]]
"""

shop_layout = [[sg.Text('Costs', pad=((10, 0), 0), font=('Helvetica', 10)),
                sg.Text('100'), sg.Text('200'), sg.Text('500'),
                sg.Text('1000'), sg.Text('2000'), sg.Text('5000')],
               [sg.Text("Per_click", pad=((10, 0), 0), font=('Helvetica', 10)),
                sg.Button('10' ), sg.Button('20'), sg.Button('50'),
                sg.Button('100'), sg.Button('200'), sg.Button('500')],
               [sg.Text("Per_sec", pad=((10, 0), 0), font=('Helvetica', 10)),
                sg.OptionMenu(values=('10', '20', '50', '100', '200', '500'))],
               [sg.Button("Exit", button_color=('white', 'black'),
                          key='-Exit-')]]
"""
shop_window = sg.Window("Shop Menu", shop_layout, no_titlebar=True,
                        grab_anywhere=True)

main_layout = [[sg.Text("Total:", size=(10, 1), pad=((10, 0), 0),
                        font=('Helvetica', 20)),
                sg.Text('', size=(20, 1), font=('Helvetica', 20),
                        justification='center', key='total')],
               [sg.Text("Per_sec:", size=(10, 1), pad=((10, 0), 0),
                        font=('Helvetica', 20)),
                sg.Text('', size=(20, 1), font=('Helvetica', 20),
                        justification='center', key='per_sec')],
               [sg.Text("Per_click:", size=(10, 1), pad=((10, 0), 0),
                        font=('Helvetica', 20)),
                sg.Text('', size=(20, 1), font=('Helvetica', 20),
                        justification='center', key='per_click')],
               [sg.Button("Click", size=(40, 2),
                          button_color=('white', '#29B898'), key='-Click-'),
                sg.Button("Shop", size=(20, 2),
                          button_color=('white', '#1828AE'), key='-Shop-')]]

main_window = sg.Window("Clicker", main_layout)  # margins=(100, 50))

total = int(0)
profit_per_sec = int(1)
profit_per_click = int(10)

main_event, main_values = main_window.read(timeout=0)
main_window['total'].update(f'{total}')
main_window['per_sec'].update(f'{profit_per_sec}')
main_window['per_click'].update(f'{profit_per_click}')

shop_event, shop_values = shop_window.read(timeout=0)
flag_open_shop = False
flag_open_warning = False
while True:
    shop_window.hide()
    main_event, main_values = main_window.read(timeout=1000)
    if main_event == sg.WIN_CLOSED:
        break
    elif main_event == "-Click-":
        total += profit_per_click
    elif main_event == "-Shop-" and flag_open_shop == False:
        flag_open_shop = True
        shop_window.un_hide()
        shop_event, shop_values = shop_window.read(timeout=0)
        while True:
            shop_event, shop = shop_window.read()
            shop_values = {0 : shop[0].split(' '), 1 : shop[1].split(' ')}
            if shop_event == '-Submit-':
                if int(shop_values[0][1]) + int(shop_values[1][1]) > total:
                    if flag_open_warning == True:
                        warning_window.un_hide()
                    flag_open_warning = True
                    warning_event, warning_values = warning_window.read()
                    if warning_event == '-Back-':
                        warning_window.hide()
                else:
                    total -= int(shop_values[0][1])
                    profit_per_sec += int(shop_values[0][0])
                    total -= int(shop_values[1][1])
                    profit_per_click += int(shop_values[1][0])
                    main_window['total'].update(f'{total}')
                    main_window['per_sec'].update(f'{profit_per_sec}')
                    main_window['per_click'].update(f'{profit_per_click}')

            if shop_event == '-Exit-':
                shop_event = ''
                flag_open_shop = False
                shop_window.hide()
                break

    total += profit_per_sec
    main_window['total'].update(f'{total}')
    main_window['per_sec'].update(f'{profit_per_sec}')
    main_window['per_click'].update(f'{profit_per_click}')

warning_window.close()
shop_window.close()
main_window.close()

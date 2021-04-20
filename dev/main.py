import PySimpleGUI as sg

bk_color = "#E8E36A"
bk_nums_color = "#BCB62B"
bk_shop_color = "#4ABCD3"
bk_warning_color = "#9D26F4"

end_game_layout = [[sg.Text("Congratulations, you have earned 1000000000 "
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

end_game_window = sg.Window("", end_game_layout, no_titlebar=True,
                            keep_on_top=True, background_color="#FF5733")

warning_layout = [[sg.Text("Sorry, you don't have enough money",
                           background_color=bk_warning_color)],
                  [sg.Button("Back", key='-Back-', button_color="#394CEA",
                             size=(40, 2))]]

warning_window = sg.Window("Warning", warning_layout, no_titlebar=True,
                           keep_on_top=True, grab_anywhere=True,
                           background_color=bk_warning_color)

shop_layout = [[sg.Text("Value:", size=(10, 1), pad=((10, 0), 0),
                        font=('Helvetica', 20),
                        background_color=bk_shop_color),
                sg.Text("Cost:", size=(10, 1), pad=((10, 0), 0),
                        font=('Helvetica', 20),
                        background_color=bk_shop_color)],
               [sg.Text("Per_sec:", size=(10, 1), pad=((10, 0), 0),
                        font=('Helvetica', 20),
                        background_color=bk_shop_color),
                sg.OptionMenu(values=("0 0", "10 100", "20 200",
                                      "50 500", "100 10000", "200 20000",
                                      "500 50000"), size=(10, 1),
                              default_value="0 0")],
               [sg.Text("Per_click:", size=(10, 1), pad=((10, 0), 0),
                        font=('Helvetica', 20),
                        background_color=bk_shop_color),
                sg.OptionMenu(values=("0 0", "10 1000", "20 2000",
                                      "50 5000", "100 10000", "200 20000",
                                      "500 50000"), size=(10, 1),
                              default_value="0 0")],
               [sg.Button("Exit", size=(15, 1),
                          button_color=('white', '#F0384B'), key='-Exit-'),
                sg.Button("Submit", size=(15, 1),
                          button_color=('white', '#3EE95D'), key='-Submit-')]]

shop_window = sg.Window("Shop Menu", shop_layout, no_titlebar=True,
                        keep_on_top=False, grab_anywhere=True,
                        background_color=bk_shop_color)

main_layout = [[sg.Text("Total:", size=(10, 1), pad=((10, 0), 0),
                        font=('Helvetica', 20),
                        background_color=bk_nums_color),
                sg.Text('', size=(23, 1), font=('Helvetica', 20),
                        justification='center',
                        background_color=bk_nums_color, key='total')],
               [sg.Text("Per_sec:", size=(10, 1), pad=((10, 0), 0),
                        font=('Helvetica', 20),
                        background_color=bk_nums_color),
                sg.Text('', size=(23, 1), font=('Helvetica', 20),
                        justification='center',
                        background_color=bk_nums_color, key='per_sec')],
               [sg.Text("Per_click:", size=(10, 1), pad=((10, 0), 0),
                        font=('Helvetica', 20),
                        background_color=bk_nums_color),
                sg.Text('', size=(23, 1), font=('Helvetica', 20),
                        justification='center', background_color=bk_nums_color,
                        key='per_click')],
               [sg.Button('', image_filename="cookie.png", border_width=0,
                          size=(5, 5), button_color=bk_color, key='-Click-')],
               [sg.Button("Shop", size=(20, 2), key='-Shop-',
                          button_color=('white', bk_nums_color))]]

main_window = sg.Window("Clicker", main_layout, background_color=bk_color)
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
    if total > 1000000000:
        while True:
            end_game_event, end_game_values = end_game_window.read()
            if end_game_event == "-Leave-":
                end_game_window.hide()
                main_event = sg.WIN_CLOSED
                break
            else:
                profit_per_click *= 100
                profit_per_sec *= 100
                total = 0
                end_game_window.close()
                break

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

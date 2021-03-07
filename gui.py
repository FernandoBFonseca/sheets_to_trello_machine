import tkinter as tk
import os
import json
# from sheets_to_trello import *


def update_command():
    SPREADSHEET_ID, KEY, TOKEN = get_inputs().values()
    # board_id = get_board_id(BOARD_NAME)
    # labels = get_labels(board_id)
    # list_id = get_list_id(board_id, LIST_NAME)

    # headers, values = get_from_sheets(SPREADSHEET_ID, RANGE_NAME)
    # data_from_sheets = pd.DataFrame(values, columns=headers)
    # data_from_sheets = filtragem(data_from_sheets, board_id)
    # pprint.pprint(data_from_sheets)
    print(SPREADSHEET_ID)
    print(KEY)
    print(TOKEN)


def get_previous():
    if os.path.exists('infos.json'):
        with open("infos.json", "r") as read_file:
            info_dict = json.load(read_file)

    return info_dict.values()


def get_inputs():
    info_dict = {}
    info_dict['spreadsheet_id'] = spreadsheet_id_entry.get()
    info_dict['key'] = trello_key_entry.get()
    info_dict['token'] = trello_token_entry.get()

    with open('infos.json', 'w') as write_file:
        json.dump(info_dict, write_file)

    return info_dict


_id, _key, _token = get_previous()

if __name__ == '__main__':

    mainWindow = tk.Tk()
    mainWindow.title("Sheets To Trello Machine")
    mainWindow.geometry('640x480')
    mainWindow['padx'] = 8

    spreadsheet_id_label = tk.Label(mainWindow, text="Spreadsheet ID", relief='sunken', borderwidth=2)
    spreadsheet_id_instructions = tk.Label(mainWindow,
                                           text="O ID do arquivo da planilha. É a longa sequência de números e letras no url.\nEncontrada logo após '/spreadsheets/d/', e não deve incluir os termos finais como 'edit'.", relief='sunken', borderwidth=2)
    spreadsheet_id_entry = tk.Entry(mainWindow, relief='sunken', borderwidth=2)
    spreadsheet_id_entry.insert(0, _id)

    spreadsheet_id_label.grid(row=0, column=0, sticky='nsew')
    spreadsheet_id_instructions.grid(row=0, column=1, sticky='nsew')
    spreadsheet_id_entry.grid(row=1, column=0, columnspan=2, sticky='nsew')

    trello_key_label = tk.Label(mainWindow, text="Trello Key", relief='sunken', borderwidth=2)
    trello_key_instructions = tk.Label(mainWindow, text="A chave de sua conta no Trello. Para encontrar acesse\n"
                                       "https://trello.com/app-key", relief='sunken', borderwidth=2)
    trello_key_entry = tk.Entry(mainWindow, relief='sunken', borderwidth=2)
    trello_key_entry.insert(0, _key)

    trello_key_label.grid(row=2, column=0, sticky='nsew')
    trello_key_instructions.grid(row=2, column=1, sticky='nswe')
    trello_key_entry.grid(row=3, column=0, columnspan=2, sticky='nsew')

    trello_token_label = tk.Label(mainWindow, text="Trello Token", relief='sunken', borderwidth=2)
    trello_token_instructions = tk.Label(
        mainWindow, text="O Token de sua conta no Trello. Para encontrar acesse https://trello.com/app-key,\n clique no hiperlink 'Token' e na página que irá se abrir clique em 'Permitir'.", relief='sunken', borderwidth=2)
    trello_token_entry = tk.Entry(mainWindow, relief='sunken', borderwidth=2)
    trello_token_entry.insert(0, _token)

    trello_token_label.grid(row=4, column=0, sticky='nsew')
    trello_token_instructions.grid(row=4, column=1, sticky='nsew')
    trello_token_entry.grid(row=5, column=0, columnspan=2, sticky='nsew')

    update_button = tk.Button(mainWindow, text='Update', command=update_command)
    update_button.grid(row=6, column=1, sticky='se')

    mainWindow.mainloop()

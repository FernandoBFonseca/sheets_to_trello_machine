import tkinter as tk
from sheets_to_trello import *


_id =
_key =
_token =


def update_command():
    SPREADSHEET_ID, KEY, TOKEN = get_infos()
    board_id = get_board_id(BOARD_NAME)
    labels = get_labels(board_id)
    list_id = get_list_id(board_id, LIST_NAME)

    headers, values = get_from_sheets(SPREADSHEET_ID, RANGE_NAME)
    data_from_sheets = pd.DataFrame(values, columns=headers)
    data_from_sheets = filtragem(data_from_sheets, board_id)
    pprint.pprint(data_from_sheets)


def get_infos():
    spreadsheet_id = spreadsheet_id_entry.get()
    key = trello_key_entry.get()
    token = trello_token_entry.get()
    return spreadsheet_id, key, token


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

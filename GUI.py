import tkinter
# from sheets_to_trello import *

mainWindow = tkinter.Tk()
mainWindow.title("Sheets To Trello Machine")
mainWindow.geometry('640x480')
mainWindow['padx'] = 8

# canvas = tk.Canvas(mainWindow, width=640, height=480)
# canvas.pack()

spreadsheet_id_label = tkinter.Label(mainWindow, text="Spreadsheet ID", relief='sunken', borderwidth=2)
spreadsheet_id_instructions = tkinter.Label(mainWindow,
                                            text="O ID do arquivo da planilha. É a longa sequência de números e letras no url.\nEncontrada logo após '/spreadsheets/d/', e não deve incluir os termos finais como 'edit'.", relief='sunken', borderwidth=2)
spreadsheet_id_box = tkinter.Entry(mainWindow, relief='sunken', borderwidth=2)


spreadsheet_id_label.grid(row=0, column=0, sticky='nsew')
spreadsheet_id_instructions.grid(row=0, column=1, sticky='nsew')
spreadsheet_id_box.grid(row=1, column=0, columnspan=2, sticky='nsew')


trello_key_label = tkinter.Label(mainWindow, text="Trello Key", relief='sunken', borderwidth=2)
trello_key_instructions = tkinter.Label(mainWindow, text="A chave de sua conta no Trello. Para encontrar acesse\n"
                                        "https://trello.com/app-key", relief='sunken', borderwidth=2)
trello_key_box = tkinter.Entry(mainWindow, relief='sunken', borderwidth=2)

trello_key_label.grid(row=2, column=0, sticky='nsew')
trello_key_instructions.grid(row=2, column=1, sticky='nswe')
trello_key_box.grid(row=3, column=0, columnspan=2, sticky='nsew')


trello_token_label = tkinter.Label(mainWindow, text="Trello Token", relief='sunken', borderwidth=2)
trello_token_instructions = tkinter.Label(
    mainWindow, text="O Token de sua conta no Trello. Para encontrar acesse https://trello.com/app-key,\n clique no hiperlink 'Token' e na página que irá se abrir clique em 'Permitir'.", relief='sunken', borderwidth=2)
trello_token_box = tkinter.Entry(mainWindow, relief='sunken', borderwidth=2)


trello_token_label.grid(row=4, column=0, sticky='nsew')
trello_token_instructions.grid(row=4, column=1, sticky='nsew')
trello_token_box.grid(row=5, column=0, columnspan=2, sticky='nsew')

mainWindow.mainloop()

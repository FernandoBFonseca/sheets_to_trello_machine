from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import datetime
import requests
import json
import pandas as pd
import pprint

# ----------------------------------------------------------------------------------------------------------------------------------------------------
# Aqui vão algumas variáveis cujos valores você deve preencher.

# O intervalo do qual os dados serão usados. O termo antes do ponto de exclamação é a planilha usada (dentro de um arquivo pode haver várias planilhas/abas). O termo após o ponto de exclamação pode ser um intervalo nomeado ou o intervalo tradicional do tipo "A2:E20".
RANGE_NAME = 'Página1!A1:D1000'

# O nome do Quadro em que as tarefas serão adicionadas.
BOARD_NAME = "Tarefas Elétrica"

# O nome da Lista que as tarefas serão adicionadas.
LIST_NAME = "BACKLOG"

subsistemas = {
    'Baterias': 'red',
    'Powertrain': 'yellow',
    'Hardware': 'green',
    'Software': 'sky'
}

# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Here are the functions responsible for pulling the information from Google Sheets
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


def get_from_sheets(spreadsheet_id, range_name):
    """Uses the Google Sheets API to get the data in a Spreadsheet and return it as a data structure.
    Takes the Spreadsheet's ID and range of the data within the Spreadsheet as arguments.
    The data structure is a list of lists. The internal lists are the rows, and each item in it is a cell.

    Args:
        spreadsheet_id (str): A sequence of characters that identifies the file. Can be copied from the URL of the Spreadsheet.
        range_name (str): The range in which the data is contained. Usually of the format 'A1:Z26', but can also be a named range.

    Returns:
        headers (list): A list containing the headers of the list. 
        values (list): A data structure containing the spreadsheet's contents.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    values = safe_read(sheet, spreadsheet_id, range_name)

    if not values:
        print('No data found.')
    else:
        headers = values.pop(0)
        for row in values:
            if row[3]:
                # converting the strings into correctly formatted datetime objects
                row[3] = datetime.datetime.strptime(row[3], "%d/%m/%Y").isoformat()
    return headers, values


def safe_read(sheet, spreadsheet_id, range_name):
    """ Reads and returns the data from the spreadsheet. The API ignores empty cells at the end of intervals, this function corrects that.
        Takes as arguments the connection to the sheet, the spreadsheet's id and the range of the data.

    Args:
        sheet (object): The sheet object returned by the method .spreadsheets() which was used on the build of the API .
        spreadsheet_id (str): A sequence of characters that identifies the file. Can be copied from the URL of the Spreadsheet.
        range_name (str): The range in which the data is contained. Usually of the format 'A1:Z26', but can also be a named range.

    Returns:
        list: The data on the sheet. Corrected to contain also the empty cells.
    """
    result = sheet.values().get(spreadsheetId=spreadsheet_id,
                                range=range_name, majorDimension='ROWS',
                                dateTimeRenderOption='FORMATTED_STRING').execute()
    crappy_data = result.get('values', [])
    cols = max(len(line) for line in crappy_data)
    rows = len(crappy_data)

    return [[_safe_read(crappy_data, r, c)
             for c in range(cols)]
            for r in range(rows)]


def _safe_read(data, r, c):
    """ Returns the correct value for a cell. Returns an empty value if the cell was not created.

    Args:
        data (object): The data structure (list of lists) created as taken from the API. It may contain errors such as ignoring empty cells.
        r (int): The row of the cell.
        c (int): The column of the cell.

    Returns:
        (object): The correct value a cell must have. Whether it is the same as in 'data' or an empty value.
    """
    try:
        return data[r][c]
    except IndexError:
        return ''

# ----------------------------------------------------------------------------------------------------------------------------------------------------
# Aqui estão as funções responsáveis por levar os dados até o Trello


def get_board_id(board_name) -> str:
    """Takes the name of the board whose id we wish to find as an argument, and returns the board's id. 

    Args:
        board_name (str): The name of the board. 

    Returns:
        str: A sequence of characters which uniquely identifies the board within a member's account.
    """
    params = {
        'modelTypes': 'boards',
        'key': KEY,
        'token': TOKEN,
        'query': {f'name:{BOARD_NAME}'}
    }

    url = f'https://api.trello.com/1/search'
    r = requests.get(url, params=params)
    return (r.json()['boards'][0]['id'])


def get_list_id(board_id, list_name) -> str:
    """ Takes the board in which the list is located on and the list's name as arguments, 
        and returns the list's id. 
        The Trello API does not support lists as searchable items, so this funtion gets all the
        lists in a board and then performs a brute force comparision of all the lists in order to 
        find the one with the correct name. If the API changes this in the future, it would be better
        to update the fucntion to work similarly to the get_board_id function.

    Args:
        board_id (str): The id of the board that contains the list whose id we are searching.
        list_name (str): The name of the list whose id we wish to find.

    Returns:
        str: A sequence of characters which uniquely identifies the list within a board. 
    """
    lists_dict = get_lists(board_id)

    return lists_dict[list_name]


def get_labels(board_id):
    url = f'https://api.trello.com/1/boards/{board_id}/labels'
    params = {
        'key': KEY,
        'token': TOKEN,
        'fields': 'name,color'
    }
    response = requests.get(url, params=params)

    label_list = json.loads(response.text)
    labels_dict = {}
    for label in label_list:
        if label['name']:
            labels_dict[label['name']] = label['color']
    return labels_dict


def post_card(list_id, name, due, macro, subsistema=None):
    """Creates a card within the selected list. 

    Args:
        list_id (str): A string that uniquely represents the list in which the card will be created. 
        name (str): The name of the card.
        due (datetime): A datetime object, that must be formatted correctly (ISO 8601, by the isoformat() method). It is the due date of the card.
        subsistema (string): The subsistema from which the task of the card will be part of. Will be used to color code the card by using a cover.
                            Defaults to None.
    """
    url = "https://api.trello.com/1/cards"
    headers = {
        "Accept": "application/json"
    }
    data = {
        'key': KEY,
        'token': TOKEN,
        'idList': list_id,
        'name': name,
        'due': due,
    }
    response = requests.post(url, data=data)
    card = json.loads(response.text)
    # Creating the cover by updating the card
    if subsistema:
        url = f"https://api.trello.com/1/cards/{card['id']}/cover"
        params = {
            'key': KEY,
            'token': TOKEN,
            'value': {
                'brightness': 'light',
                'color': subsistemas[subsistema],
                'idAttachment': None,
                'idPlugin': None,
                'idUploadedBackground': None,
                'size': 'normal'
            }
        }
        requests.put(url, headers=headers, json=params)
    if macro in labels:
        url = f"https://api.trello.com/1/cards/{card['id']}/labels"
        params = {
            'key': KEY,
            'token': TOKEN,
            'color': labels[macro]
        }
        requests.post(url, params=params)


def get_lists(id_board):
    url = f"https://api.trello.com/1/boards/{id_board}/lists"

    params = {
        'key': KEY,
        'token': TOKEN,
        'fields': 'name'
    }

    response = requests.get(url, params=params)
    lists = json.loads(response.text)

    lists_dict = {}
    for item in lists:
        lists_dict[item['name']] = item['id']

    return lists_dict


def get_cards(id_board):
    """Gets all the cards within a Trello board.

    Args:
        id_board (str): The sequence of characters that uniquely represents a Trello board.

    Returns:
        [type]: A list with all the names of the cards.
    """

    url = f"https://api.trello.com/1/boards/{id_board}/cards"

    params = {
        'key': KEY,
        'token': TOKEN,
        'fields': 'name,idList'
    }

    response = requests.get(url, params=params)
    cards = json.loads(response.text)
    cards_dict = {}
    lists = get_lists(id_board)

    for card in cards:
        if card['idList'] == lists['Informações e códigos'] or card['idList'] == lists['ORCs (OKRs) iniciados']:
            continue
        cards_dict[card['name']] = card['idList']

    return cards_dict


def filtragem(data_from_sheets, board_id):
    """Filters the data from the spreadsheet to only contain the tasks that haven't already been added to the Trello board.

    Args:
        data_from_sheets (DataFrame): A Pandas DataFrame object containing all the rows from the Spreadsheet.
        board_id (str): The sequence of characters that uniquely represents a Trello board.

    Returns:
        [type]: A Pandas DataFrame object which only contains the tasks that haven't already been added to the Trello board.
    """
    cards = list(get_cards(board_id).keys())
    # comentário teste
    return data_from_sheets[~data_from_sheets['Micro-tarefa'].isin(cards)]


if __name__ == '__main__':
    board_id = get_board_id(BOARD_NAME)
    labels = get_labels(board_id)
    list_id = get_list_id(board_id, LIST_NAME)

    SPREADSHEET_ID, _, _ = gui.get_infos()

    headers, values = get_from_sheets(SPREADSHEET_ID, RANGE_NAME)
    data_from_sheets = pd.DataFrame(values, columns=headers)
    data_from_sheets = filtragem(data_from_sheets, board_id)
    pprint.pprint(data_from_sheets)
    # data_from_sheets.apply(lambda row: post_card(list_id, name=row['Micro-tarefa'], due=row['Entrega'], macro=row['Macro-Tarefa'], subsistema=row['Subsistema']), axis=1)

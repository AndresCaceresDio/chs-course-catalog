# Program that converts a jsonl file to a google spreadsheet
# The user must indicate how many jsonl lines to fit into every cell (block_size)
# Service account credentials are required; Google Cloud must also have access to the spreadsheet

import gspread
from oauth2client.service_account import ServiceAccountCredentials

def authenticate_with_google():
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name('your_credentials.json', scope)
    client = gspread.authorize(creds)
    return client

def get_worksheet(client, spreadsheet_name, sheet_title):
    sheet = client.open(spreadsheet_name).worksheet(sheet_title)
    return sheet

def read_and_split_file(filename, block_size):
    with open(filename, 'r') as file:
        lines = []
        chunk = ""
        i = 0
        for line in file:
            i += 1
            chunk = chunk + str(line)
            if (i % block_size) == 0:
                lines.append(chunk)
                chunk = ""
        if chunk:
            lines.append(chunk)
    return lines

def write_blocks_to_sheet(sheet, blocks):
    batch_size = 3313
    for i in range(0, len(blocks), batch_size):
        end_index = i + batch_size
        values = [[block] for block in blocks[i:end_index]]
        cell_range = 'A{}:A{}'.format(i+1, i + len(values))
        sheet.update(values, cell_range)

def main():
    client = authenticate_with_google()
    sheet = get_worksheet(client, 'your_spreadsheet', 'your_sheet')
    blocks = read_and_split_file('your_file.txt', 10)
    write_blocks_to_sheet(sheet, blocks)

if __name__ == '__main__':
    main()


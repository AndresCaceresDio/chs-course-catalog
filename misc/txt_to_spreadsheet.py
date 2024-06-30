import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Function to authenticate with Google Sheets using OAuth2
def authenticate_with_google():
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name('your_credentials.json', scope)
    client = gspread.authorize(creds)
    return client

# Function to get the specified worksheet by its title
def get_worksheet(client, spreadsheet_name, sheet_title):
    sheet = client.open(spreadsheet_name).worksheet(sheet_title)
    return sheet

# Function to read the text file and split it into blocks
def read_and_split_file(filename, delimiter):
    with open(filename, 'r') as file:
        content = file.read()
        blocks = content.split(delimiter)
        if blocks[0] == '':
            blocks = blocks[1:]
        for i in range(len(blocks)):
            blocks[i] = blocks[i].strip()
        return blocks

# Function to write the blocks to the Google Sheet
def write_blocks_to_sheet(sheet, blocks):
    # Write in batches to avoid Google Sheets rate limit
    batch_size = 3313
    for i in range(0, len(blocks), batch_size):
        end_index = i + batch_size
        values = [[block] for block in blocks[i:end_index]]
        cell_range = 'A{}:A{}'.format(i+1, i + len(values))
        sheet.update(values, cell_range)

# Main function to execute the workflow
def main():
    client = authenticate_with_google()
    sheet = get_worksheet(client, 'your_spreadsheet', 'your_sheet')
    blocks = read_and_split_file('your_file.txt', ', ')
    write_blocks_to_sheet(sheet, blocks)

if __name__ == '__main__':
    main()

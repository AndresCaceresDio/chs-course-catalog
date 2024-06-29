import gspread
from oauth2client.service_account import ServiceAccountCredentials

def authenticate_with_google():
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    return client

def get_worksheet(client, spreadsheet_name, sheet_title):
    sheet = client.open(spreadsheet_name).worksheet(sheet_title)
    return sheet

def read_and_split_file(filename, delimiter):
    with open(filename, 'r') as file:
        phrase = """
Please make one more output based on this input:

{"input_text": "Generate a high quality MBE Civil Procedure practice question, in English, that reflects the complexity of questions found on the actual MBE. Please include the question stem, the call of the question, four answer choices (A, B, C, D), and clearly indicate the correct answer. Do not include an explanation for the answer.", "output_text": }"""
        lines = []
        chunk = ""
        i = 0
        for line in file:
            i += 1
            chunk = chunk + str(line)
            if (i % delimiter) == 0:
                chunk = chunk + phrase
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
    sheet = get_worksheet(client, 'GPT-4o', 'Sheet2')
    blocks = read_and_split_file('torts.txt', 230)
    write_blocks_to_sheet(sheet, blocks)

if __name__ == '__main__':
    main()


import argparse
import gspread
import regex
from oauth2client.service_account import ServiceAccountCredentials

# helpers
def convertTimeToSeconds(time):
    seconds = sum(x * int(t) for x, t in zip([60, 1], time.split(":")))
    print(seconds)
    return seconds

def convertSecondsToTime(seconds):
    s = seconds % 60
    m = seconds // 60
    timeString = f"{m}:{s}"
    print(timeString)
    return timeString

parser = argparse.ArgumentParser(description='Generates a bomb based on the arguments provided.')
parser.add_argument('-t', metavar='time', type=str, default='60:00',
                    help='Bomb timer. H:mm:ss or number of minutes. Default 60:00')
parser.add_argument('-s', metavar='strikes', type=int, default=5,
                    help='Number of strikes. Default 5')
parser.add_argument('-w', metavar='widgets', type=int, default=None,
                    help='Number of widgets. Default not set')
parser.add_argument('-fs', metavar='full solo', type=bool, default=False,
                    help='Create a bomb using all checked modules and calculates time based on average solves')
parser.add_argument('-bal', metavar='balanced', type=bool, default=False,
                    help='Create a balanced bomb using approximately 20% hard, 40% medium, 40% medium')
args = parser.parse_args()

# Replace with your own Google API credentials file
creds = ServiceAccountCredentials.from_json_keyfile_name('ktane-bomb-generator-d77ad124ab38.json', ['https://spreadsheets.google.com/feeds'])

# Replace with the URL of your Google Sheet
sheet_url = 'https://docs.google.com/spreadsheets/d/1ANxqDnh9PmeYpva1czavRQKYJw3DdbLsD0tw-OLvouc/edit#gid=0'

# Replace with the name of the worksheet you want to access
worksheet_name = 'Sheet1'

# Authenticate and open the worksheet
client = gspread.authorize(creds)
worksheet = client.open_by_url(sheet_url).worksheet(worksheet_name)

# Get all the rows in the worksheet
rows = worksheet.get_all_records()


# parse script arguments
time = args.t
strikes = f"{args.s}X"
widgets = '// widgets:5' if (args.w == None) else f'widgets:{args.w}'
fullSolo = args.fs
balanced = args.bal



# validate script arguments
# time should be correct format
time_regex = r'^\d{1,2}:[0-5][0-9]$'  # match MM:SS format with at least one digit in minutes
if not regex.match(time_regex, time): raise Exception(f"{time} is not a valid time string")

# bomb creation options can't conflict
# todo



    
# Open the output file for writing
with open('output.txt', 'w') as f:
    f.write('// Auto-generated bomb\n')
    
    # generate solo bomb with dynamic time based on average solve time
    if fullSolo:
        filteredRows = list(filter(lambda row: (row['Selected?'] == 'TRUE') and (row['Defuser / Expert'] == 'Defuser'), rows))

        print('create full solo')
        seconds = 0
        
        for row in filteredRows:
            if row['Module ID'] == 'iconic':
                seconds += len(filteredRows) * 3
                f.write(f"1*{row['Module ID']}\n")
            else:
                seconds += convertTimeToSeconds(row['Average Solve Time'])
                f.write(f"1*{row['Module ID']}\n")
            
        time = convertSecondsToTime(seconds)
        f.write(f"{time}\n")
        f.write(f"{strikes}\n")
        f.write(f"{widgets}\n")
    elif balanced:
        # todo
        f.write(f"//balanced\n")

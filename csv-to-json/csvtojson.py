import csv
import json
import os
import sys
​

def read_dict():
    if len(sys.argv) == 1 and not os.isatty(0):
        # If there are no provided arguments and the program is being piped to, read from stdin.
        return json.load(sys.stdin)
    elif len(sys.argv) == 2:
        # If an argument is provided, open the file pointed to and read that.
        json_file = open(sys.argv[1], 'r')

        return json.load(json_file)
    else:
        print('Missing filename')
        exit(0)
​
​
vals = read_dict()
fields = ['Name']
​
for row_key in vals.keys():
    row = vals[row_key]
    row['Name'] = row_key
    for col_key in row.keys():
        if col_key not in fields:
            fields.append(col_key)
​
with open('results.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    
    writer.writeheader()
    for row_key in vals.keys():
        writer.writerow(vals[row_key])

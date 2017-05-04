import sys
import os.path
import csv
import numpy as np
import matplotlib.pyplot as plt

# Usage: CSV_plotter.py filename.csv

# Start from index 1 because argv[0] is the python script itself.
argv = sys.argv[1:]

# Check if input file (first argument to script) exists and is valid.
# Returns filepath if successful, null if invalid.
def processArgs():
    filePath = None

    if len(argv) == 0:
        print("Error: No input file.")
    elif argv[0].lower() == '--help':
        print("Usage: CSV_plotter.py path...\n")
        print("Opens csv file and plots to the screen.")
        print("Automatically skips header rows, expects data in the form:")
        print("    <frequency (MHz)>, <power output level (dB)>\n")
    elif not os.path.isfile(argv[0]):
        print("Error: {} is not a file or does not exist.".format(argv[0]))
    else: # Input file exists:
        # Get and check file extension,
        # can only check once we've proven that user has input file that exists.
        inputFileExtension = os.path.splitext(argv[0])[1]
        if (inputFileExtension.lower() != '.csv'):
            print("Error: {} is not a csv file.".format(argv[0]))
        else:
            # File exists and has a .csv extension, opening will be successful
            filePath = argv[0]

    return filePath

def isNumber(inputString):
    try:
        float(inputString)
    except ValueError:
        return False 
    else:
        return True

def countHeaderRows(reader):
    headerRowsEnd = 0

    # Only need to check if first column is a string because our header format is
    #     <label (string), other info (*anything*)>
    # Data rows are always
    #     <frequency (float), power output level (float)>
    for row in reader:
        if not isNumber(row[0]): # Header row
            headerRowsEnd += 1
            '''
            print(headerRowsEnd)
        else: # Reached the data rows
            print(row)
            '''
    return headerRowsEnd

# Expects variable amount of header rows before data rows.
# Actual data format however is two columns per row,
# in the format <frequency (float), power output level (float)>
if __name__ == "__main__":
    filePath = None
    # Get the first row that the data starts at by counting the row that the
    #     headers finish on 
    headerRowsEnd = 0

    filePath = processArgs()

    if filePath != None: # input args were valid, filepath is csv that exists
        reader = csv.reader(open(filePath,"rt"))
        headerRowsEnd = countHeaderRows(reader)
        frequency, powerLevel = np.loadtxt(filePath, dtype='float', delimiter=',', skiprows=headerRowsEnd, usecols=(0,1), unpack=True)

        fig = plt.figure(figsize=(20,8)) # figsize is in inches
        fig.suptitle('RF Spectrum Analyser data', fontsize=22)
        plt.xlabel('Frequency (MHz)', fontsize=16)
        plt.ylabel('Power Level (dB)', fontsize=16)
        plt.grid(True)
        plt.plot(frequency, powerLevel, linewidth=2.0)
        plt.show()

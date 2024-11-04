import csv
from tempfile import NamedTemporaryFile
import shutil
import os


def fftMagToZero(folder_path):
    filenames = os.listdir(folder_path)
    
    for file in filenames:
        if file.endswith('.csv'):
            filepath = folder_path + '/' + file
            tempfile = NamedTemporaryFile('w+t', newline='', delete=False)

            with open(filepath, 'r', newline='') as infile, tempfile:
                reader = csv.reader(infile)
                writer = csv.writer(tempfile)
                for row in reader:
                    if row[0] == '0.0':
                        row[1] = '0.0'
                    writer.writerow(row)

            shutil.move(tempfile.name, filepath)
    
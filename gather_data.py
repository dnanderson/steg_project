import hash_embed
import lsb_embed
import lorem
import os
import csv
import subprocess
from functools import partial


"""
This script runs over a directory of images, and embeds random lorem text into them
After embedding the information into the images it runs the java StegExpose tool
on them, then it extracts the csv from the java software, and adds some additional
data that is gathered as the information is embedded into each file.
"""
longtext = [lorem.text() for x in range(1000)]
longtext = ''.join(longtext)
print(len(longtext))
this_path = os.path.dirname(os.path.realpath(__file__))


def run_embed(embed_method, method_identifier):
    os.chdir(this_path)
    os.chdir('img')
    embed_rate = {}
    for file in os.listdir('.'):
        filename = os.fsdecode(file)
        if filename.startswith('clean_'):
            newfilename = filename.replace('clean_', f'steg_{method_identifier}_')
            bits_embedded = embed_method(filename, newfilename, bytes(longtext, 'utf-8'))
            embed_rate[newfilename] = bits_embedded
            if bits_embedded is None:
                print('Embedded all bytes of message')
            else:
                print('Embedded ', bits_embedded)
    os.chdir(this_path)
    return embed_rate

def run_detect():
    os.chdir(this_path)
    os.chdir('StegExpose')
    process = subprocess.Popen(['java', '-jar', 'StegExpose.jar', '../img/', 'default', '0.2', '../data.csv'])
    stdout, stderr = process.communicate()
    process.wait()
    os.chdir(this_path)



r_lsb = run_embed(lsb_embed.main_bytes, 'lsb')
em = partial(hash_embed.main_bytes, rate=2)
r_hash2 = run_embed(em, 'hash2')
em = partial(hash_embed.main_bytes, rate=3)
r_hash3 = run_embed(em, 'hash3')
em = partial(hash_embed.main_bytes, rate=4)
r_hash4 = run_embed(em, 'hash4')
r_lsb.update(r_hash2)
r_lsb.update(r_hash3)
r_lsb.update(r_hash4)
run_detect()

# Read in the CSV, add in the embedding rates of each of the images
csvrows = []
with open('data.csv', newline='') as csvfile:
    csvread = csv.reader(csvfile)
    for row in csvread:
        if not row:
            continue
        csvrows.append(row)

import pdb; pdb.set_trace()
for row in csvrows[1:]:
    embedded = r_lsb.get(row[0], 0)
    if embedded != 0:
        embedded = embedded //  8
    row.insert(3, embedded)

csvrows[0].insert(3, 'Actual Bytes Embedded')
with open('added_data.csv', 'w', newline='') as csvfile:
    csvwrite = csv.writer(csvfile)
    for row in csvrows:
        csvwrite.writerow(row)





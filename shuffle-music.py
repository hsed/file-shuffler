# Gets first two chars from filename
# If NN e.g. 01, 22, 43... then remove them
# Next append random unique NN with space or no space if 3rd char is space

# Do this for all in folder but should be scalable so from 0-100 or 0-1000 etc

from numpy.random import randint
import sys
import argparse
import os
import time
import random

def main():
    parser = argparse.ArgumentParser(description='')
    
    parser.add_argument('dataDir', type=str, help='The dirname which contains all the music files (mp3 only)')
    parser.add_argument('-d', dest='debug', action='store_true', help='Specify this flag to turn on debug mode.')
    parser.add_argument('-df', '--debug_file', type=str, help='The filename where debug output of this script will be written to.')
    
    parser.set_defaults(debug=False)
    parser.set_defaults(debug_file="shuffle_results.txt")
    args = parser.parse_args()
    
    debug = args.debug
    debug_info = []

    # os.listdir gets all files and sub dir names in folder
    # then check if each item which is in that list is a file,
    # If true then add it to the filenames array 
    filenames = [item for item in os.listdir(args.dataDir) if os.path.isfile(os.path.join(args.dataDir, item))]


    
    tot_files = len(filenames) # total number of files

    #%02d so only works for 00-99
    
    # printProgressBar(_+1, tot_range, prefix = 'Progress:', suffix = '', bar_length = 30, start = start)

    rand_numbers = random.sample(range(tot_files), tot_files) # produces unique ints from 00-{TOT_FILE-1}

    # check/assert len (rand_numbers) == len(filenames)

    # string[start_index:{end_index+1}] starts at start_index (0 based) and ends at end_index

    if (debug): debug_info.append("Total Numbers: %d \tTotal Files: %d\n" % (len(rand_numbers), tot_files))

    start = time.time()

    for i in range(len(rand_numbers)):
        old_str = filenames[i]
        new_str =  ("%02d" % rand_numbers[i] + old_str) if not old_str[:2].isdigit() else ("%02d" % rand_numbers[i] + old_str[2:])

        # python strings are immutable (need to split and rejoin)
        new_str = (new_str[:2] + " - " + new_str[2:]) if not new_str[2].isspace() else (new_str)
        
        os.rename(os.path.join(args.dataDir, old_str), os.path.join(args.dataDir, new_str))
        
        if (debug): debug_info.append("Number: %02d \tOrig_Name: %s \tNew_Name: %s" % (rand_numbers[i], old_str[:20] + "(...)", new_str[:20] + "(...)"))

        printProgressBar(i+1, tot_files, prefix = 'Progress:', suffix = '', bar_length = 30, start = start)


    print("All done!")
    if (debug): debug_info.append("\nAll done!")


    if(debug):
        with open(args.debug_file, mode='wt', encoding='utf-8') as myfile:
            myfile.write('\r\n'.join(debug_info)) # "\r\n" for windows
    

# Print iterations progress
def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, bar_length=100, start = time.time()):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        bar_length  - Optional  : character length of bar (Int)
    """
    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '#' * filled_length + '-' * (bar_length - filled_length)

    elapsedTime = time.time() - start
    estimatedRemaining = int(elapsedTime * (1.0/max((iteration / float(total)),0.001)) - elapsedTime)

    sys.stdout.write('\r%s |%s| %s%s %s (ETA: %im %02is)' % (prefix, bar, percents, '%', suffix, estimatedRemaining/60, estimatedRemaining%60))

    if iteration == total:
        # Special routine to basically clear the progressbar
        sys.stdout.write('\r                                                                                             \r')
    sys.stdout.flush()


main()


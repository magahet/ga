import re
import subprocess

files = ["testCaseSmall.txt", "testCase3k.txt", "large.txt"]
alphas = [".75",".85",".95"]
flags = ["", "-s"]

for fileName in files:
    for alpha in alphas:
        for flag in flags:
            if(flag == ''):
                output = subprocess.check_output(["python", "pageRank.py", "-i", fileName, "-a", alpha])
            else:
                output = subprocess.check_output(["python", "pageRank.py", "-i", fileName, "-a", alpha, flag])
            match = re.search("Making.*", output, re.IGNORECASE)
            print match.group()
            match = re.search("PageRank object made\.  Elapsed time : ([0-9.]+) seconds", output, re.IGNORECASE)
            print match.group()
            match = re.search("PageRank vector calculated\.  Elapsed time : ([0-9.]+) seconds", output, re.IGNORECASE)
            print match.group()
            match = re.search("Your calculated PageRank vector matches the validation file", output, re.IGNORECASE)
            if(match):
                print "Succssfully matched"
            else:
                print "Match Failed"
            print "---------------------------------------------------------------------------"

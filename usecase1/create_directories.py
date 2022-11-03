import subprocess

#print("starting script...")
with open("directories.txt", "r") as directories:
    for dirs in directories:
        #print(dirs)
        subprocess.run("mkdir ./{0}".format(dirs),shell=True, capture_output=True)

#Use ls to make sure files were printed out
subprocess.run("ls",shell=True)


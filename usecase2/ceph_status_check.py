import subprocess
import argparse
import re
from os.path import exists


# If your shell script has shebang,
# you can omit shell=True argument.
#proc = subprocess.run(["../bash/check_ceph.sh"], shell=True,capture_output=True)
#output = proc.stdout.decode()

class health_check():

    def __init__(self,i,o,u):
        #self.outputf = output_file
        self.o = o
        self.u = u
        if i is not None:
            self.input_file = i[0]
        else:
            self.input_file = None
        self.health_status = None
        self.num_osds = None
        self.capacity = None
        self.num_pgs = None

        if self.input_file != None and exists(self.input_file):
            with open(self.input_file) as output:
                self.parse_output(output)
        else:
            print("running check_ceph.sh...")
            proc = subprocess.run(["../bash/check_ceph.sh"], shell=True,capture_output=True)
            output = proc.stdout.decode()
            print(output)
            self.parse_output(output)

        if all(var is not None for var in [self.health_status,self.num_osds,self.capacity,self.num_pgs, self.o, self.u]):
            self.check_expectations()

        else:
            print("Skipped diagnostic report. For report, please rerun with expected number of OSDs and PGs")
            #print([self.health_status,self.num_osds,self.capacity,self.num_pgs])

        self.print_final_report()

####### METHODS HERE #############################            

    def parse_output(self,output):
        for line in output:
            if "health" in line:
                self.health_status = re.search(r"health: \w+", line).group(0).replace("health: ", "")
                #print(health_status)
            if "osd:" in line:
                l_line = re.search(r"\d+\sosds\b",line)
                self.num_osds = int(l_line.group(0).replace(" osds", ""))
                #print(num_osds)
            if "usage:" in line:
                u_line = re.search(r"/ \d+\s+\w+", line)
                self.capacity = u_line.group(0).replace("/ ", "").replace(" ", "")
                #print(capacity)
            if "pgs:" in line:
                self.num_pgs = int(re.search(r"\d+", line).group(0))
                #print(pg)


    def check_expectations(self):
        o = self.o[0]
        u = self.u[0]
        osd_check = o == self.num_osds
        capacity_check = u == self.capacity

        if osd_check:
            print("expected number of OSDs detected ({0})".format(o))
        else:
            print("expected {0} OSDs, found {1}".format(o, self.num_osds))

        if capacity_check:
            print("expected usable capacity detected ({0})".format(u))
        else:
            print("expected {0}, detected {1}".format(u, self.capacity))

    def print_final_report(self):
        if self.health_status != None:
            print("Ceph health status: {0}".format(self.health_status))
        if self.capacity != None:
            print("Available capacity: {0}".format(self.capacity))
        if self.num_osds != None:
            print("Number of OSDs: {0}".format(self.num_osds))
        if self.num_pgs != None:
            print("Number of pgs: {0}".format(self.num_pgs))

#    def parse_pools(self):


    def pg_calculator(self):
        total_pgs = (osds*100)/pool_size
        return total_pgs


#####Add arg parser here for command line argumentsi
###Description of script
parser = argparse.ArgumentParser(description="Verify health status of Ceph cluster. You can use an input file from running ceph status, ceph osd tree, and ceph df - if you don't specify input file, this script will run a bash script that will obtain the output from the ceph commands.")

#required argument
#parser.add_argument('output_file', metavar='output_file', type=str, nargs=1, help='path and file name for output')

#optional arguments
parser.add_argument('-i', metavar='input_file', type=str, nargs=1, help='path to output.txt from ceph health check bash',default=None)
parser.add_argument('-o', metavar='num_osds', type=int, nargs=1, help ="input number of expected OSDs", default=None)
parser.add_argument('-u', metavar='cap', type=str, nargs=1, help="input expected usable capacity (i.e. 6TiB)", default=None)
args = parser.parse_args()

#turn arguments into dictionary to pass to class
args_dict = vars(args)

#call health check class
health_check(**args_dict)






import sys,time,subprocess

pids = []
for i in range(int(sys.argv[1])):
    pid = subprocess.Popen(["python", "sante.py"], stdout=sys.stdout, stderr=sys.stderr).pid
    pids.append(pid)
    time.sleep(3)

import pdb;pdb.set_trace()

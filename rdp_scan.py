import os
from Database.MongoDB import db

def rdpscan():
    c = 0
    fp = open('current_rdp.txt', 'r')
    prev = int(fp.read().strip())

    f = open('ipblocks.txt', 'r')
    for x in f:
        cmd = 'sudo masscan '+x.strip()+' -p3389 --wait 0 --max-rate 100000 >> ips.txt'
        print('Line Number ' + str(c))
        c +=1
        if c < prev:
            continue
        fp = open('current_rdp.txt', 'w')
        fp.write(str(c))
        os.system(cmd)

def produce_results():
    f = open('trimmed_result.txt', 'r')
    vul = 0
    safe = 0
    unknown = 0
    for x in f:
        x = x.strip()
        if 'VULNERABLE' in x:
            vul += 1
        elif 'UNKNOWN' in x:
            unknown += 1
        elif 'SAFE' in x:
            safe += 1
    return vul, unknown, safe


def save_db(v,u,s):
	rdp_c = db["RDP"]
	rdp_c.drop()
	rdp_c = db["RDP"]
	
	obj = {}
	obj['vulnerable'] = v
	obj['unknown'] = u
	obj['safe'] = s
	
	x = rdp_c.insert_one(obj)



rdpscan()
os.system('rdpscan --file ips.txt --workers 10000 >results.txt')
lines_seen = set() # holds lines already seen
outfile = open("trimmed_result.txt", "w")
for line in open("results.txt", "r"):
    if line not in lines_seen: # not a duplicate
        outfile.write(line)
        lines_seen.add(line)
outfile.close()
v,u,s = produce_results()

print(v)
print(u)
print(s)

save_db(v,u,s)

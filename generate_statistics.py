import os
from Database.MongoDB import db
from flask_table import Table, Col

# Declare your table
class ItemTable(Table):
    domain_name = Col('Doamin Name')
    failed_messages = Col('Fails')
    error_messages = Col('Errors')

# Get some objects
class Item(object):
    def __init__(self, domain_name, failed_messages, error_messages):
        self.domain_name = domain_name
        self.failed_messages = failed_messages
        self.error_messages = error_messages


command = 'sslyze --certinfo '

def get_cert_data(filename, type):
    f = open(filename, "r")
    for x in f:
        print(x)
        s = command + x.strip() + ' > ' + x.strip() + '_'+type+'_CERT.txt'
        os.system(s)


get_cert_data('banks.txt', 'BANKS')
get_cert_data('universities.txt', 'UNI')
get_cert_data('medicals.txt', 'MEDICAL')
get_cert_data('newspapers.txt', 'NEWS')



def print_cert_validity(type):
    items = []
    file = open( type+".html", "w")
    file.write("<table>")
    file.write("\n")
    file.write("<thead><tr><th>Doamin Name</th><th>Fails</th><th>Errors</th></tr></thead>")
    file.write("\n")
    file.write("<tbody>")
    file.write("\n")
    for filename in os.listdir(os.getcwd()):
        if filename.find("CERT")!=-1 and filename.find(type)!=-1:
            file.write("<tr><td>")
            n = filename[ : filename.find("_")]
            file.write(n.strip())
            file.write("</td><td>")
            e = "<ul>"
            fa = "<ul>"
            f = open(filename, "r")
            for x in f:
                if x.find("ERROR")!=-1 :
                    s = "ERROR - " +  x[0: x.find("ERROR")-1].strip() + " - " + x[x.find("ERROR") + 8 :].strip()
                    print(s)
                    e += "<li>"
                    e += s.strip()
                    e += "</li>"

                if x.find("FAILED")!=-1 :
                    s = "FAILED - " +  x[0: x.find("FAILED")-1].strip() + " - " + x[x.find("FAILED") + 9 :].strip()
                    print(s)
                    fa += "<li>"
                    fa += s.strip()
                    fa += "</li>"

            print(("#"*50))
            e += "</ul>"
            fa += "</ul>"
            if len(fa)<12:
                file.write("OK")
            else:
                file.write(fa)
            file.write("</td>")
            file.write("<td>")
            if len(e)<12:
                file.write("OK")
            else:
                file.write(e)
            file.write("</td></tr>")
            file.write("\n")
    file.write("</tbody>")
    file.write("\n")
    file.write("</table>")
    file.write("\n")
    file.close()

def print_cert_validity_2(type):
    er = set()
    fa = set()
    tot = set()
    for filename in os.listdir(os.getcwd()):
        if filename.find("CERT")!=-1 and filename.find(type)!=-1:
            tot.add(filename)
            f = open(filename, "r")
            for x in f:
                if x.find("ERROR")!=-1 :
                    er.add(filename)

                if x.find("FAILED")!=-1 :
                    fa.add(filename)
    return er, fa, tot
def save_db():
	ssly = db["SSLYZE"]
	ssly.drop()
	ssly = db["SSLYZE"]
	
	obj = {}

	
	err, fai, total = print_cert_validity_2("BANKS")
	ara = [err, fai, total]
	obj['banks'] = ara
	
	err, fai, total = print_cert_validity_2("NEWS")
	ara = [err, fai, total]
	obj['news'] = ara
	
	err, fai, total = print_cert_validity_2("MEDICAL")
	ara = [err, fai, total]
	obj['medical'] = ara
	
	err, fai, total  = print_cert_validity_2("UNI")
	ara = [err, fai, total]
	obj['uni'] = ara
	x = ssly.insert_one(obj)


print("BANKS")
print(len(err))
print(len(fai))
print(len(total))

print("NEWS")
print(len(err))
print(len(fai))
print(len(total))

print("MEDICAL")
print(len(err))
print(len(fai))
print(len(total))


print("UNI")
print(len(err))
print(len(fai))
print(len(total))

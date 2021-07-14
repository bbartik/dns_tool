import time
import subprocess
import textfsm



def resolve_name_subprocess():
    """ Resolve DNS name a bunch of times and time the query"""
    
    start_time = time.perf_counter()
    answer = subprocess.check_output(["nslookup", "dnspython.org", "8.8.8.8"]).decode("utf-8")
    #pdb.set_trace()
    end_time = time.perf_counter()

    with open("nslookup.template", "r") as template:
        re_table = textfsm.TextFSM(template)
        data = re_table.ParseText(answer)[0]
    qry_time = end_time - start_time
    print(f'{data[2]} resolved to {data[3][0]} by {data[1]} in {qry_time} seconds')

    return None



if __name__ == "__main__":

    counter = 10
    for x in range(1, counter):
        resolve_name_subprocess()
        #resolve_name()
        time.sleep(1)

        
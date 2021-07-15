import datetime
import time
import subprocess
import textfsm
import pandas as pd
import typer

import pdb

def main(host: str, dns_server: str, counter: int):
    """ Resolve DNS name set number of times and calculate delay stats"""
    
    # initialize the dns data list
    dns_data = []

    # main loop
    for x in range(1, counter):
        #intialize the dns dataset entry
        dns_entry = {}
        start_time = pd.Timestamp.now()
        answer = subprocess.check_output(["nslookup", host, dns_server]).decode("utf-8")
        end_time = pd.Timestamp.now()
        qry_delay = end_time - start_time

        # parse the nslookup output using custom textfsm template
        with open("nslookup.template", "r") as template:
            re_table = textfsm.TextFSM(template)
            data = re_table.ParseText(answer)[0]

        # populate dns dataset entry and then append to full list
        dns_entry.update({
            "dns_qry_time": pd.Timestamp.now(),
            "dns_qry_name": data[2],
            "dns_srv_addr": data[1],
            "dns_answer": data[3][0],
            "dns_delay": qry_delay,
        })
        dns_data.append(dns_entry)
        print(dns_entry)
        
        # set time between commands to 1 sec
        time.sleep(1)

    df = pd.DataFrame(dns_data)
    df.set_index(['dns_qry_time'])
    print(f"Mean time is {df['dns_delay'].mean()}")
    print(f"Max time is {df['dns_delay'].max()}")

    return None



if __name__ == "__main__":

    typer.run(main)

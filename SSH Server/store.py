
import json
import sys
import time
import matplotlib.pyplot as plt
from plotting import Plot


filename1 = "ip.json"
filename2 = "data.json"

class Store():
    
    def __init__(self, data):
        
        self.data = data
       
    def store_ip(self, data):
        
        if data:
            
            try:
                with open(filename1, 'a') as f:
                    
                    create = json.dumps({"IP":data[0],"PORT":int(data[1])},indent=4,seperators=(',',':'))
                    json.dump(create,f)
            
            except Exception as e:
                print("[-] Error : {}|".format(str(e)))
    def store_data(self, data):
        
        
        if data:
            
            #data_len = len(data)
            try:
                with open(filename2, 'a') as f:
                    
                    create = json.dumps({"data":len(data),"time":time.strftime("%M")},
                                        indent=4,
                                        separators=(',',':'))
                    json.dump(create,f)
                    print(len(data))
                    show = Plot(len(data),time.strftime("%M"))
                    show.graph()
            except Exception as s:
                print("[-] Error 2 : {}".format(str(s)))
                    

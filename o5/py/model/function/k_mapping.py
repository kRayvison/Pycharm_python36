
import time
import shutil
import os
import sys
class k_mapping():
    def __init__(self,B_path,mount):
        self.clean_network()
        
        self.mapping_network(mount)
        self.mapping_plugins(B_path)
        
    def clean_network(self):

        for j in range(3):
            if os.system("net use * /delete /y"):
                print ("clean mapping network failed.")
                time.sleep(2)
                print ("Wait 2 seconds...")
            else:
                print ("clean mapping network successfully.")
                break
        sys.stdout.flush()



    def mapping_network(self,mount):
        for i in mount:

            path = mount[i].replace("/", "\\")
            if os.path.exists(path):
                if path.startswith("\\"):
                    for j in range(3):
                        if os.system("net use %s %s" % (i, path)):
                            print ("can not mapping %s to %s" % (i, path))
                            time.sleep(5)
                            print ("Wait 5 seconds...")
                        else:
                            print ("Mapping %s to %s" % (i, path))
                            break

                elif path.lower().startswith("c:"):
                    path = r"\\127.0.0.1\c$" + path.split(":")[1]
                    if os.system("net use %s %s" % (i, path)):
                        print ("can not mapping %s to %s" % (i, path))
                    else:
                        print ("Mapping %s to %s" % (i, path))
                else:
                    self.create_virtua_drive(i, path)
            else:
                print ('[warn]The path is not exist:%s' % path)

            sys.stdout.flush()

        os.system("net use")
        os.system("subst")


    def mapping_plugins(self,B_path):
        drive = "B:"
        auto_plugins = B_path

        if os.system("net use %s %s" % (drive, auto_plugins)):
            print ("can not mapping %s to %s" % (drive, auto_plugins))
        else:
            print ("Mapping %s to %s" % (drive, auto_plugins))


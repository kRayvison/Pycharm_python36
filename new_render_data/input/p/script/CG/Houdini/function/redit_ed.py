import winreg
import os,sys

class RegEdit():

    ## eg. data_dict = {"name":"SYSTEM\CurrentControlSet\services\HoudiniLicenseServer",
    ##                  "value":{'ObjectName': 'LocalSystem', 
    ##                   'ImagePath': 'C:\\Windows\\System32\\sesinetd.exe', 
    ##                      'Start': 2, 'Type': 16, 'ErrorControl': 1, 
    ##                          'DisplayName': 'HoudiniLicenseServer'},}

    @classmethod
    def SetServer(cls,data_dict='',temp=""):
        base_key = winreg.HKEY_LOCAL_MACHINE
        server_name = r'%s'%data_dict['name']
        adict_new = data_dict['value']
        adict_temp ={}

        # ----------------------------------------------------------------------------------------------------
        # found whether if the key * is exist
        # ----------------------------------------------------------------------------------------------------
        it_exit = False
        upnode_exist = False
        try:
            if winreg.OpenKey(base_key,server_name):
                it_exit = True
        except:
            print("The %s reg key is not found."%server_name)
        
        print("%s key: %s" % (server_name,it_exit))
        if it_exit==False:
            up_node = cls.GetUpNode(server_name,2)
            try:
                if winreg.OpenKey(base_key,up_node):
                    upnode_exist = True
            except:
                print("services not exist.")

        if it_exit:
            print("[Back] Try to back the %s."%server_name)
            try:
                mainkey = winreg.OpenKey(base_key,server_name)
                i = 0 
                while 1: 
                    name, value, type = winreg.EnumValue(mainkey, i)
                    #print (name,value)
                    adict_temp[name] = value
                    i += 1
            except WindowsError:
                print("[Back] Search finished.")
            if len(adict_temp):
                # print(adict_temp)
                with open(temp,"w") as f:
                    f.write(str(adict_temp))
                    f.close()
                print("[Back] Back %s finished."%server_name)
            # ---------------------------------------------------------------------------------------------
            # try to  delete it 
            # ---------------------------------------------------------------------------------------------
            print("Try to delete %s."%server_name)
            try:
                cls.DeleteKeys(base_key,server_name)
                print("DeleteKey %s finished."%server_name)
            except:
                pass

        elif upnode_exist == False:
            print("Check 'therd up_node'")
            therd_up = cls.GetUpNode(server_name,3)
            therd_up_node = cls.GetUpNode(server_name,4)
            software_exist = False
            try:
                if winreg.OpenKey(base_key,therd_up):
                    software_exist = True
            except:
                print("%s key not exist."%therd_up)
            if software_exist == False:
                print("Creat '%s'"%therd_up)
                key_name = os.path.basename(therd_up)
                thiskey = winreg.OpenKey(base_key,therd_up_node)
                newKey_ks = winreg.CreateKey(thiskey, key_name)
            print("Creat '%s'"%therd_up)
            key_name = os.path.basename(cls.GetUpNode(server_name,2))
            thiskey = winreg.OpenKey(base_key,therd_up)
            newKey = winreg.CreateKey(thiskey,key_name)

        print("Creat new %s"%server_name)
        up_node = os.path.dirname(server_name)
        main_server = os.path.basename(server_name)
        mainkey = winreg.OpenKey(base_key,up_node)
        newKey_ks = winreg.CreateKey(mainkey,main_server)
        for elm in adict_new:
            print(elm)
            print(adict_new[elm])
            print()
            if isinstance(adict_new[elm],int):
                winreg.SetValueEx(newKey_ks,elm,0,winreg.REG_DWORD,cls.complement(adict_new[elm]))
                
            else:
                print(adict_new[elm])
                winreg.SetValueEx(newKey_ks,elm,0,1,adict_new[elm])
                
            
        print("Creat %s finished." % server_name)


    @staticmethod
    def DeleteKeys(base_key,nodekey):
        thiskey = winreg.OpenKey(base_key,nodekey)
        subkeys = []
        try:
            i = 0 
            while 1: 
                this_key = winreg.EnumKey(thiskey, i)
                print(this_key)
                subkeys.append(this_key)
                i += 1
        except WindowsError:
            pass
            #print("finished.")

        if len(subkeys)==0:
            thisNode = os.path.dirname(nodekey)
            ks_version = os.path.basename(nodekey)
            thiskey = winreg.OpenKey(winreg.HKEY_USERS,thisNode)
            winreg.DeleteKey(thiskey, ks_version)
        else:
            if len(subkeys):
                for elm in subkeys:
                    this_node_new = "%s\%s" % (nodekey,elm)
                    print(this_node_new)
                    DeleteKeys("%s"%this_node_new)
                    print("DeleteKeys: %s "%this_node_new)

            thisNode = os.path.dirname(nodekey)
            ks_version = os.path.basename(nodekey)
            thiskey = winreg.OpenKey(winreg.HKEY_USERS,thisNode)
            winreg.DeleteKey(thiskey, ks_version)

    @staticmethod
    def GetUpNode(keys,num):
        ## num from the end
        ## keys = "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\services\HoudiniLicenseServer"
        values = keys.replace("\\","/").split("/")
        return_val = ""
        for i in range(len(values)-int(num)+1):
            if i==0:
                return_val = values[i]
            else:
                return_val += "\\"+values[i]

        return return_val

    @staticmethod
    def complement(n,radix=32):
        ## https://stackoverflow.com
        ## /questions/2381205/python-2-6-i-can-not-write-dwords-greater-than-0x7fffffff-into-registry-using
        if n < (1<<(radix-1)) : return n
        else : return n - (1<<radix) 


data_dict1 = {"name":"SYSTEM\CurrentControlSet\services\HoudiniLicenseServer",
               "value":{'ObjectName': 'LocalSystem', 
                  'ImagePath': 'C:\\Windows\\System32\\sesinetd.exe', 
                     'Start': 2, 'Type': 16, 'ErrorControl': 1, 
                      'DisplayName': 'HoudiniLicenseServer'}}

aa = {'DisplayName': 'HoudiniServer', 'ObjectName': 'LocalSystem', 'ErrorControl': 0, 'Type': 16, 'Start': 2, 'ImagePath': 'C:\\Windows\\system32\\hserver.exe'}
data_dict={"name":"SYSTEM\CurrentControlSet\services\HoudiniServer","value":aa}
temp = "C:/temp/aaa.json"
RegEdit.SetServer(data_dict1,temp)
RegEdit.SetServer(data_dict1,temp)
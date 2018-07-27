import os,sys
import nuke
import RVNUKE

def changeval(pathin =''):
    path_arr=pathin.split("/")
    arr_elm=[]
    returnpath=''
    for i in range(0,len(path_arr)):
        if path_arr[i]=="..":
            arr_elm.append(i)

    if len(arr_elm)>0:
        bigen=arr_elm[0]-len(arr_elm)
        end=arr_elm[-1]
        for i in range(0,len(path_arr)):
            if i==0:
                returnpath=path_arr[i]
            elif i<bigen or i>end:
                returnpath+="/"+path_arr[i]
    else:
        returnpath=pathin
    return returnpath

def DOFILES(filepath='',visible=0):
    fileinfo=''    
    if not filepath=="":
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        F_path=filepath+"/filesinfo.txt"
    else:
        F_path="D:/"+"filesinfo.txt"


    readNodes = RVNUKE.RecursiveFindNodes( "Read", nuke.Root())
    readgeoNodes = RVNUKE.RecursiveFindNodes( "ReadGeo2", nuke.Root())
    readNodes.extend(readgeoNodes)

    read_adict={}
    readgeo_adict={}



    for nodes in readNodes:
        mpath = nuke.filename(nodes)
        nodefullname = nodes.fullName()

        print nodefullname + ':' + mpath
        print '-------------------------------------\n'
        nodename=nodes.Class()

        if nodename in ["Read","ReadGeo2"]:
            if nodename=="Read":
                read_adict[nodes]=nodes
            if nodename=="ReadGeo2":
                readgeo_adict[nodes]=nodes


    ### do files
    adict_files={}

    adict_files = dict(read_adict)
    adict_files.update(readgeo_adict)



    print "\nThe read files: %d " % (len(read_adict))
    print "\nThe readgeo files: %d " % (len(readgeo_adict))

    fileinfo+="\nThe readnode files: %d " % (len(read_adict)+len(readgeo_adict))+"\n"

    for elm in readNodes:
        mpath = nuke.filename(elm)
        nodefullname = elm.fullName()

        fileval=changeval(mpath)
        if not os.path.exists(fileval):
            print("\nWarning: %s" %fileval)
            print nodefullname
            print mpath
            fileinfo+="\nWarning: %s" %fileval+"\n"
        if visible:
            print nodefullname
            print mpath
            print fileval
        fileinfo+= mpath+"\n"+ fileval +"\n"

    with open(F_path,"w") as f:
        f.write(fileinfo)
        f.close()
# DOFILES()
if __name__=="__main__":
    DOFILES()
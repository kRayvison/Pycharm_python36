import os 
import datetime
import imghdr
import platform
import re               ## re part

class CheckFrame():
    def __init__(self,logObj):
        print ('init')
        self.LOG=logObj
        self.LOG.info('Check Frame')
        
    def checkoutframe(self,path1="",path2="",checkname = ''):

        returnA = 0
        returnB = 0
        bad_size=10
        Erro_size = 0
        if os.path.exists(path2):
            picturs_local=os.listdir(path1)
            picturs_server=os.listdir(path2)
            ##print("File's name: ",checkname)
            # print("Here the files number : local & server: ",len(picturs_local) ,' & ',len(picturs_server))
            # self.LOG.info("Here the files number : local & server: "+len(picturs_local) +' & '+len(picturs_server))            
            lenth = len(picturs_local)
            if lenth>0:

                fileN=checkname		

                with_numb = re.search(r'\d',fileN)               ### whether sequence 
                with_numb_end = re.search(r'\d',fileN.split('.')[-1])
                if with_numb_end:
                    # print("Waring: This file without any type in the end ! ")
                    self.LOG.info("Waring: This file without any type in the end ! ")

                if fileN in picturs_server :

                    pathN_L = path1+"\\"+fileN
                    pathN_S = path2+"\\"+fileN

                    fileSizi_local = os.path.getsize(pathN_L)
                    fileSizi_local = fileSizi_local/1024
                    fileSizi_server = os.path.getsize(pathN_S)
                    fileSizi_server = fileSizi_server/1024

                    if fileSizi_server==fileSizi_local :
                        if fileSizi_local>Erro_size:
                            ## do adjust
                            returnA = self.Itisimg(pathN_L)
                        else:                            
                            self.LOG.info("This file's size is less than "+str(Erro_size)+" KB")
                else:
                    ## do adjust
                    self.LOG.info(("This file \""+fileN+"\" not in server path !"))
                    returnA = 0
        else:
            # print("There is not dir path  \"",path2," \"")
            self.LOG.info("There is not dir path  \""+path2+" \"")
            returnA = 0
            returnB = 1
        return ([returnA,returnB])

    def IfWarning(self,wherein='',filein=''):
        returnA = 0
        returnB = 0
        bad_size=10
        Erro_size = 0
        path2 = wherein
        fileN = filein
        with_numb = re.search(r'\d',fileN)

        if os.path.exists(path2):
            picturs_server=os.listdir(path2)
            if fileN in picturs_server:
                pathN_S = path2+"\\"+fileN
                fileSizi_server = os.path.getsize(pathN_S)
                fileSizi_server = fileSizi_server/1024
                if fileSizi_server>Erro_size:
                    if fileSizi_server<bad_size:
                        returnA = 0
                        self.LOG.info("This file's size is less than "+str(bad_size)+" KB")
                        if with_numb:
                            returnB = self.Tojudgment(fileN,picturs_server,path2)                
                    else:
                        returnA = 1
                        if with_numb:
                            returnB = self.Tojudgment(fileN,picturs_server,path2)
                else:
                    self.LOG.info("This file's size is less than "+str(Erro_size)+" KB")
            else:
                self.LOG.info(("This file \""+fileN+"\" not in server path !"))
        else:
            self.LOG.info("There is not dir path  \""+path2+" \"")

        return ([returnA,returnB])


        

    def Itisimg(self,wherein=''):
        types_avil = ['bmp','gif','jpeg','pbm' , 'pgm' , 'png' , 'ppm' , 'rast', 'rgb','SGI', 'tiff','xbm']
        imgtype = imghdr.what(wherein)
        types = wherein.split(".")
        dig_arr = re.findall(r'\d+',wherein)[-1]
        dig_indt = 0
        arr_fileN = types
        for i in range(0,len(arr_fileN)):
            if dig_arr in arr_fileN[i]:
                dig_indt = i
                break			
        type_ind = dig_indt+1
        typepart = ''	
        for i in range(type_ind,len(arr_fileN)):
            if i==type_ind:
                typepart += arr_fileN[i]
            else:
                typepart += r'.'+arr_fileN[i]
    ###------------------------------------------------------------------------
        types = typepart
        if types=='jpg':
            types = types.replace("jpg","jpeg")            
        if types in types_avil:
            if imgtype==types:                
                self.LOG.info("This image's type: "+imgtype)
                return 1
            else:                
                self.LOG.info("This is not a \""+types+"\" type image ! && type:"+imgtype)
                return 0
        else:            
            #self.LOG.info("This file's type  \""+types+"\"  can't be read by imghder: passed")
            return 1


    ###------------------------------------------------------------------------------------------###
    ###                    aaa_123_0001.exr , aaa.1112.exr   with sequence 
    ###******************************************************************************************###

    def Tojudgment(self,filename="",arr_in=[],wherein=''):
        # print("----------------------------------------------------------------")
        # print("                   HERE TO DO THE JUDGMEENT                     ")
        path = wherein+"\\"
        fileN = filename        
        #self.LOG.info("The file's name which to do the judgment: "+fileN)

        fine_lever = 0.01                ## MB
        error_lever = 0.05
        bad_lever = 0.003
        ###--------------------------------------------------------------------------------------#
        # return_fine = 1
        # return_erro = 0
        # return_warn = 2
        ###--------------------------------------------------------------------------------------#
        return_final = 1
        
        arr_fileN = fileN.split('.')
        dig_arr = re.findall(r'\d+',fileN)[-1]

        name_arr = fileN.split(dig_arr)
        typepart = ''
        if len(name_arr)>2:
            for i in range(0,len(name_arr)-1):
                if i==0:
                    typepart = name_arr[i]
                else:
                    typepart += dig_arr+name_arr[i]
        else:
            typepart = name_arr[0]            

            ##	get types eg. exr, bgeo.sc
    ###------------------------------------------------------------------------------

        indts = dig_arr
        typeN = name_arr[-1]        
        rename= typepart        
        
        if len(arr_in)>=4:
            
            indt_1= str(int(indts)-3)         ## file_1 file_2 file_3 file file_4 file_5 file_6
            num_1 = indt_1.zfill(len(indts))
            
            indt_2= str(int(indts)-2)
            num_2 = indt_2.zfill(len(indts))

            indt_3= str(int(indts)-1)
            num_3 = indt_3.zfill(len(indts))

            file_1 = rename+num_1+typeN
            file_2 = rename+num_2+typeN
            file_3 = rename+num_3+typeN
            
            ture_bef = 0
            ture_aft = 0
            if file_3 in arr_in:
                ture_bef+=1
                if file_2 in arr_in:
                    ture_bef+=1
                    if file_1 in arr_in:
                        ture_bef+=1
            ##self.LOG.info(file_1+"  "+file_2+"  "+file_3)		

            if ture_bef==3:
                k_1 = float(os.path.getsize(path+file_2))/pow(1024,2)-float(os.path.getsize(path+file_1))/pow(1024,2)
                k_2 = float(os.path.getsize(path+file_3))/pow(1024,2)-float(os.path.getsize(path+file_2))/pow(1024,2)
                k_3 = float(os.path.getsize(path+fileN))/pow(1024,2)-float(os.path.getsize(path+file_3))/pow(1024,2)			
                # print ("Change level's diffrence: ","%.3f"%((k_3-k_2)-(k_2-k_1)))
                ##self.LOG.info("Change level's diffrence: "+str("%.3f"%((k_3-k_2)-(k_2-k_1))))                
                if abs((k_3-k_2)-(k_2-k_1))>fine_lever:
                    if abs((k_3-k_2)-(k_2-k_1))>error_lever:
                        return_final=0
                        # print("bad pictures: ","picture \"",fileN,"\"  in  ",path)
                        self.LOG.info("Warning: bad picture \""+fileN+"\"  in  "+path)
                    else:
                        return_final=2					

                indt_4= str(int(indts)+1)
                num_4 = indt_4.zfill(len(indts))

                indt_5= str(int(indts)+2)
                num_5 = indt_5.zfill(len(indts))

                indt_6= str(int(indts)+3)
                num_6 = indt_6.zfill(len(indts))

                file_4 = rename+num_4+typeN
                file_5 = rename+num_5+typeN
                file_6 = rename+num_6+typeN

                if file_4 in arr_in:
                    ture_aft+=1
                    if file_5 in arr_in:
                        ture_aft+=1
                        if file_6 in arr_in:
                            ture_aft+=1

                if ture_aft==3 and return_final==2:
                    k_4 = float(os.path.getsize(path+file_4))/pow(1024,2)-float(os.path.getsize(path+fileN))/pow(1024,2)
                    k_5 = float(os.path.getsize(path+file_5))/pow(1024,2)-float(os.path.getsize(path+file_4))/pow(1024,2)
                    k_6 = float(os.path.getsize(path+file_6))/pow(1024,2)-float(os.path.getsize(path+file_5))/pow(1024,2)
                    if (abs((k_4-k_5)-(k_5-k_6))-abs((k_3-k_2)-(k_2-k_1)))<bad_lever:
                        return_final=1
                        print("Normal*************************************")
                    else:
                        # print("Warning: \n","pictur: ",fileN,"in",path)
                        self.LOG.info("Warning: bad picture \""+fileN+"\"  in  "+path)
        else:
            # print("With out any judgment because there less than 4 picturs in the server ***** ")
            # self.LOG.info("Without any judgment because there less than 4 picturs in the server ***** ")
            return_final = 1

        return return_final



    def checkFrames(self,pathin1 = '',pathin2 = '',checkturn='checkcopy'):
        # pathin1 = r'C:\work\render\5117480\output'
        python_ver=platform.python_version()
        self.LOG.info("Python ver: "+python_ver)
        # if '.' in python_ver:
        #     _arr=python_ver.split('.')
        # if int(_arr[0])<3:
        #     pathin1=unicode(pathin1, 'utf8').encode('gbk')
        #     pathin2=unicode(pathin2, 'utf8').encode('gbk')

        pathin1=pathin1
        pathin2=pathin2

        pathin_arr= []
        path_fine = pathin1
        if '/' in pathin1:
            pathin_arr = pathin1.split('/')
            length_pathin_arr=len(pathin_arr)
            for i in range(0,length_pathin_arr):
                if i==0:
                    path_fine=pathin_arr[i]
                else:
                    path_fine += '\\'+pathin_arr[i]
            pathin1 = path_fine        

        return_final = 0
        judgment_times = 0
        cunnt_files = 0
        if os.path.exists(pathin1):
            for dirpath, dirnames, filenames in os.walk(pathin1):
                for files in filenames:
                    cunnt_files +=1

            if cunnt_files>0:
                for dirpath, dirnames, filenames in os.walk(pathin1):
                    for file in filenames:
                        path_in1 = pathin1
                        path_in2 = pathin2
                                                
                        if not dirpath == path_in1:
                            path_arr = dirpath.split('\\')
                            path_in1_arr = path_in1.split('\\')

                            diff_inde = len(path_in1_arr)
                            
                            path_end = ""
                            for inde in range(diff_inde,len(path_arr)):
                                path_end +="\\"+path_arr[inde]
                            path_in1 = dirpath
                            path_in2 = path_in2+path_end

                        self.LOG.info("Find files in the local here: "+path_in1)
                        self.LOG.info("Find files in the server here: "+path_in2)

                        if not "db" in file.split('.')[-1]:
                            if checkturn=='checkcopy':
                                am=self.checkoutframe(path_in1,path_in2,file)
                                return_final += am[0]
                                judgment_times +=1
                                # print("checkoutframe returned: ",am)                            
                                self.LOG.info("checkoutframe returned: "+str(am))
                            elif checkturn=='checkwarning':
                                ##do something checks
                                am=self.IfWarning(path_in2,file)
                                return_final += am[0]
                                judgment_times +=1
                                self.LOG.info("IfWarning returned: "+str(am))
                            else:
                                print("take a modle!")

            else:
                judgment_times=1
                self.LOG.info("The local folder is empty!")
        else:
            judgment_times=1
            # print("The path not exists: ",pathin1)
            self.LOG.info("The path not exists: "+pathin1)        

        if return_final==judgment_times:
            self.LOG.info("Final check result: 0")
            return 0
        else:
            self.LOG.info("Final check result: 1")
            return 1


###----------------------------------------------------------------------------------------------------###
###                                        DO TEST:  checkFrames()

'''
path_local=r"F:\123"
path_server=r"D:\work\render\597777\outputbak"
checkObj=CheckFrame()
print("\nFinal check result: ",checkObj.checkFrames(path_local,path_server,"checkcopy" ))
print("\nFinal warning result: ",checkObj.checkFrames(path_local,path_server,"checkwarning"))
'''
###---------------------------------------------------------------------------------------------------###



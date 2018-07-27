import os,sys,subprocess,string,logging,time,shutil

import logging
import json
from CommonUtil import RBCommon as CLASS_COMMON_UTIL
from CommonUtil import RBKafka as CLASS_KAFKA

class AnalyzeBase():

    def __init__(self,**paramDict):
        print '[BASE.init.start.....]'
        
        #self.G_DOPY_NAME='do.py'
        self.G_RENDER_CORE_TYPE = 'cpu'
        self.G_JOB_ID=paramDict['G_JOB_ID']
        self.G_USER_ID=paramDict['G_USER_ID']
        self.G_USER_ID_PARENT=paramDict['G_USER_ID_PARENT']
        self.G_TASK_ID=paramDict['G_TASK_ID']
        self.G_SCRIPT_POOL=paramDict['G_SCRIPT_POOL']
        self.G_ACTION=paramDict['G_ACTION']

        self.G_SYS_ARGVS=paramDict['G_SYS_ARGVS']#taskid,jobindex,jobid,nodeid,nodename
        self.G_JOB_NAME=self.G_SYS_ARGVS[3].replace('"','')
        self.G_NODE_NAME=self.G_SYS_ARGVS[5]
        
        #self.G_HELPER_WORK='C:/WORK/helper'
        
        self.G_WORK='c:/work'
        self.G_LOG_RENDER='C:/LOG/render'
        self.G_RENDER_OS = paramDict['G_RENDER_OS']
        if self.G_RENDER_OS=='Linux':
            self.G_LOG_RENDER='/tmp/nzs-data/log/render'
            #self.G_HELPER_WORK='/tmp/nzs-data/work/helper'
            self.G_WORK='/tmp/nzs-data/work'
            
        self.G_WORK_RENDER=os.path.normpath(os.path.join(self.G_WORK,'render'))
        self.G_WORK_RENDER_TASK=os.path.normpath(os.path.join(self.G_WORK_RENDER,self.G_TASK_ID))
        self.G_WORK_RENDER_TASK_CFG=os.path.normpath(os.path.join(self.G_WORK_RENDER_TASK,'cfg'))
        
        
            
        #-----------------------------------------init log-----------------------------------------------
        self.G_ANALYZE_LOG=logging.getLogger('analyse_log')
        
        fm=logging.Formatter("%(asctime)s  %(levelname)s - %(message)s","%Y-%m-%d %H:%M:%S")
        analyseLogPath = os.path.join(self.G_LOG_RENDER,self.G_TASK_ID)
        analyseLog=os.path.join(analyseLogPath,(self.G_JOB_NAME+'.txt'))
        if not os.path.exists(analyseLogPath):
            os.makedirs(analyseLogPath)
        self.G_ANALYZE_LOG.setLevel(logging.DEBUG)
        renderLogHandler=logging.FileHandler(analyseLog)
        renderLogHandler.setFormatter(fm)
        self.G_ANALYZE_LOG.addHandler(renderLogHandler)
        console = logging.StreamHandler()  
        console.setLevel(logging.INFO)  
        self.G_ANALYZE_LOG.addHandler(console)
        
        #-----------------------------------------kafka-----------------------------------------------
        self.G_KAFKA_HOST='10.60.96.142'
        self.G_KAFKA_PORT=9092
        self.G_KAFKA_TOPIC= 'dev-munu-topic-01'

        #-----------------------------------------task.json-----------------------------------------------
        self.G_TASK_JSON=paramDict['G_TASK_JSON']
        self.G_ANALYZE_LOG.info(self.G_TASK_JSON)
        if not os.path.exists(self.G_TASK_JSON):
            CLASS_COMMON_UTIL.error_exit_log(self.G_ANALYZE_LOG,'task.json not exists')
            
            
        self.G_TASK_JSON_DICT=eval(open(self.G_TASK_JSON, "r").read())
        #jsonStr = (open(self.G_TASK_JSON, "r").read())
        #self.G_TASK_JSON_DICT=json.load(jsonStr)
        self.G_ZONE=self.G_TASK_JSON_DICT['system_info']['common']["zone"]
        self.G_PLATFORM=self.G_TASK_JSON_DICT['system_info']['common']["platform"]
        self.G_TILES_PATH=os.path.normpath(self.G_TASK_JSON_DICT['system_info']['common']["tiles_path"])
        self.G_INPUT_CG_FILE=os.path.normpath(self.G_TASK_JSON_DICT['system_info']['common']["input_cg_file"])
        self.G_CHANNEL=self.G_TASK_JSON_DICT['system_info']['common']["channel"]
        self.G_INPUT_PROJECT_PATH=os.path.normpath(self.G_TASK_JSON_DICT['system_info']['common']["input_project_path"])
        self.G_CONFIG_PATH=os.path.normpath(self.G_TASK_JSON_DICT['system_info']['common']["config_path"]+'/')
        self.G_SMALL_PATH=os.path.normpath(self.G_TASK_JSON_DICT['system_info']['common']["small_Path"])
        self.G_OUTPUT_USER_PATH=os.path.normpath(self.G_TASK_JSON_DICT['system_info']['common']["output_user_path"])
        self.G_INPUT_USER_PATH=os.path.normpath(self.G_TASK_JSON_DICT['system_info']['common']["input_user_path"])
        self.G_PLUGIN_PATH=os.path.normpath(self.G_TASK_JSON_DICT['system_info']['common']["plugin_path"])
        
        
        
        self.G_PRE_PY=os.path.join(self.G_WORK_RENDER_TASK_CFG,'pre.py')
        self.G_POST_PY=os.path.join(self.G_WORK_RENDER_TASK_CFG,'post.py')
        
        print '[BASE.init.end.....]'
        

        

    def RB_MAKE_DIR(self):#1
        print '[BASE.RBmakeDir.start.....]'
                    
        #renderwork
        if not os.path.exists(self.G_WORK_RENDER_TASK):
            os.makedirs(self.G_WORK_RENDER_TASK)
        print '[BASE.RBmakeDir.end.....]'

    def RB_PRE_PY(self):#pre custom
        self.G_ANALYZE_LOG.info('[BASE.RBprePy.start.....]')
        self.G_ANALYZE_LOG.info(self.G_PRE_PY)
        if os.path.exists(self.G_PRE_PY):
            sys.argv=[self.G_USER_ID,self.G_TASK_ID]
            execfile(self.G_PRE_PY)
        self.G_ANALYZE_LOG.info('[BASE.RBprePy.end.....]')
        
    def RB_HAN_FILE(self):#3 copy script,copy from pool,#unpack
        self.G_ANALYZE_LOG.info('[BASE.RBhanFile.start.....]')
        self.G_ANALYZE_LOG.info('[BASE.RBhanFile.end.....]')
    
    
    def RB_CONFIG(self):#5
        self.G_ANALYZE_LOG.info('[BASE.RBconfig.start.....]')
        self.G_ANALYZE_LOG.info('[BASE.RBconfig.end.....]')
    
    def RB_ANALYZE(self):#7
        self.G_ANALYZE_LOG.info('[BASE.RB_ANALYZE.start.....]')
        self.G_ANALYZE_LOG.info('[BASE.RB_ANALYZE.end.....]')
        
    def RB_HAN_RESULT(self):#8
        self.G_ANALYZE_LOG.info('[BASE.RBhanResult.start.....]')
        #nodeTaskJson = os.path.join(self.G_WORK_RENDER_TASK,'task.json')
        
        self.G_ANALYZE_LOG.info('[BASE.RBhanResult.end.....]')

    def RB_KAFKA_NOTIFY(self):
    
        
        
        start_time = time.time()
        params = {}
        params["messageKey"] = self.G_ACTION
        params['platform']=self.G_PLATFORM
        params['messageTime']=str(int(start_time))
        params['messageId']=self.G_TASK_ID+'_'+params["messageKey"]+'_'+self.G_JOB_ID
        message_body_dict={}
        message_body_dict['zone']=self.G_ZONE
        message_body_dict['nodeName']=self.G_NODE_NAME
        message_body_dict['jobId']=self.G_JOB_ID
        message_body_dict['taskId']=self.G_TASK_ID
        params['messageBody']=message_body_dict
        
        kafka_result=CLASS_KAFKA.produce(params,self.G_KAFKA_HOST, self.G_KAFKA_PORT,self.G_KAFKA_TOPIC)
        print ('kafka_result='+str(kafka_result))

    def RB_POST_PY(self):#post custom
        self.G_ANALYZE_LOG.info('[BASE.RBpostPy.start.....]')
        if os.path.exists(self.G_POST_PY):
            sys.argv=[self.G_USER_ID,self.G_TASK_ID]
            execfile(self.G_POST_PY)
        self.G_ANALYZE_LOG.info('[BASE.RBpostPy.end.....]')
    

            
    def RB_DEL_MAP_DRIVER(self):
        CLASS_COMMON_UTIL.del_net_use()
        CLASS_COMMON_UTIL.del_subst()
        
    def RB_EXECUTE(self):#total
        print 'BASE.execute.....'
        
        self.G_ANALYZE_LOG.info('[BASE.RBexecute.start.....]')
        self.RB_PRE_PY()
        self.RB_MAKE_DIR()
        self.RB_HAN_FILE()
        self.RB_DEL_MAP_DRIVER()
        self.RB_CONFIG()
        self.RB_ANALYZE()
        self.RB_HAN_RESULT()
        self.RB_POST_PY()
        self.RB_KAFKA_NOTIFY()
        self.G_ANALYZE_LOG.info('[BASE.RBexecute.end.....]')
        
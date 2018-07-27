import c4d
from c4d import gui, documents
#Welcome to the world of Python


def main():
    doc = c4d.documents.GetActiveDocument()
    rd = doc.GetActiveRenderData()
    
    RI_save_click = int(rd[c4d.RDATA_SAVEIMAGE])
    RI_saveimage_path = rd[c4d.RDATA_PATH]
    RI_saveimage_path.decode('gbk','ignore').encode('utf-8')
    print RI_save_click, RI_saveimage_path
    _save_data = {}
    _save_data['RI_save_click'] = RI_save_click
    _save_data['RI_saveimage_path'] = RI_saveimage_path
       
    
    
    MP_save_click = int(rd[c4d.RDATA_MULTIPASS_SAVEIMAGE])
    MP_saveimage_path = rd[c4d.RDATA_MULTIPASS_FILENAME]
    #MP_saveonefile = rd[c4d.RDATA_MULTIPASS_SAVEONEFILE]
    
    
    MP_saveimage_path.decode('gbk','ignore').encode('utf-8')

    print MP_save_click, MP_saveimage_path

    _save_data = {}
    _save_data['MP_save_click'] = MP_save_click
    _save_data['MP_saveimage_path'] = MP_saveimage_path
    #_save_data['MP_saveonefile'] = MP_saveonefile

if __name__=='__main__':
    main()

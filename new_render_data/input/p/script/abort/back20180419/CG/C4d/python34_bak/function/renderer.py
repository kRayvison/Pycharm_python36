import c4d
from c4d import gui,documents
#Welcome to the world of Python


def main():
    doc = documents.GetActiveDocument()
    rd = doc.GetActiveRenderData()
    vp = rd.GetFirstVideoPost()
    renderer_setting = {0:'Standard', 1:'Software OpenGL', 1023342:'Physical', 1016630:'CineMan'}
    print renderer_setting[int(rd[c4d.RDATA_RENDERENGINE])]
    #phy = renderer_setting.get(1023342)
    #print phy
 
 
    _physical_sampler = []
    _physical_sampler = {0:'Fixed', 1:'Adaptive', 2:'Progressive'}
    print _physical_sampler[int(vp[c4d.VP_XMB_RAYTRACING_SAMPLER])]
    
    _physical_sampler_mode = []
    _physical_sampler_mode = {0:'Infinite', 1:'Pass Count', 2:'Time Limit'}
    print _physical_sampler_mode[int(vp[c4d.VP_XMB_RAYTRACING_INTERACTIVE_MODE])]
        

if __name__=='__main__':
    main()

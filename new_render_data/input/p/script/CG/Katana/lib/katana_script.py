from Katana import KatanaFile, version, FarmAPI,Nodes3DAPI
import NodegraphAPI,sys,json,os

katana_scene = sys.argv[1]
anal_txt = sys.argv[2]
#_tid_from_cmd = sys.argv[2]
#_inf_from_cmd = sys.argv[3]


def kanana_analyse(katana_scene,anal_txt):

    print katana_scene
    print anal_txt
    #yourKatanaScene = "/home/ladaojeiang/yes/demos/katana_files/aovs_prman.katana"
    KatanaFile.Load( katana_scene ) # Loading scene /yourDirectory/yourFile.katana

    render_info_dict={}
    
    render_nodes = NodegraphAPI.GetAllNodesByType("Render")
    if len(render_nodes) != 0:
        print len(render_nodes)
        print render_nodes    
        for render_node in render_nodes:
            if render_node.isBypassed()==False:
                render_outputs={}
                Source_list=[]
                Variance_list=[]
                Final_list=[]

                render_name=render_node.getName() 
                print render_name
                render_node_info=Nodes3DAPI.RenderNodeUtil.GetRenderNodeInfo(render_node)

                for render_output_name in render_node_info.getAllOutputNames():

                    render_output=render_node_info.getOutputInfoByName(render_output_name,0)['outputFile']
                    #print render_output
                    
                    if render_output.find('tmp')==1:
                        #print render_output
                        pass            
                    elif render_output.find('Source')>0:
                        Source_list.append(render_output)
                    elif render_output.find('Variance')>0:
                        Variance_list.append(render_output)
                    elif render_output.find('Final')>0:
                        Final_list.append(render_output)


                render_outputs['Source']=Source_list
                render_outputs['Variance']=Variance_list
                render_outputs['Final']=Final_list
                render_info_dict[render_name]=render_outputs
            else:
                render_name=render_node.getName() 
                print render_name +"  is  not render , this node is disabled"
        print len(render_info_dict.keys())
        #print render_info_dict
        anal_txt_handle = file(anal_txt, 'w')
        anal_txt_handle.write(json.dumps(render_info_dict))
        anal_txt_handle.close()
    else:
        print 'the render node 0, analysis failed!'
        if  os.path.exists(anal_txt):
            os.remove(anal_txt)
            sys.exit(1)

kanana_analyse(katana_scene,anal_txt)


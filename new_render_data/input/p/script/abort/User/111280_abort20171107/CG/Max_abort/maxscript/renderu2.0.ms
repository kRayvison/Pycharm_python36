








/**



-----------kg------------

*/

--(DotNetClass "System.Windows.Forms.Application").CurrentCulture = dotnetObject "System.Globalization.CultureInfo" "zh-cn"


dotnetcode = "
using System;
 
class StdOutPrinter {
    static public bool print(string txt) {
        Console.WriteLine(txt);
        return true;
    }
}
 
class StdErrPrinter {
    static public bool print(string txt) {
        Console.Error.WriteLine(txt);
        return true;
    }
}
class WriteToFile{
	static public bool write(string txt) {
        Console.Error.WriteLine(txt);
        return true;
    }

}
"
 
fn createAssembly dotnetcode className = (
    provider = dotNetObject "Microsoft.CSharp.CSharpCodeProvider"
    param = dotNetObject "System.CodeDom.Compiler.CompilerParameters"
    param.GenerateInMemory = on
    compiled = provider.CompileAssemblyFromSource param #(dotnetcode)
    compiled.CompiledAssembly.CreateInstance className
)
G_STDOUT = createAssembly dotnetcode "StdOutPrinter"

fn RB_MontiorDialog =
(


	local WindowHandle = DialogMonitorOPS.GetWindowHandle()

	local dialogName = UIAccessor.GetWindowText WindowHandle
--DOSCommand ("echo dialogName... " +dialogName+">>c:/dialogName.txt") 
	if  dialogName!=undefined and dialogName!="" and dialogName=="About Hot4MAX" then (

		format "Dialog Name: %\n" (UIAccessor.GetWindowText WindowHandle)
		 
		
		local hwnd_children = uiAccessor.getChildWindows WindowHandle
		for i = 1 to hwnd_children.count do (
			format "% = \"%\"\n" i (uiAccessor.getWindowText hwnd_children[i])
		)
		UIAccessor.pressButtonByName WindowHandle "OK"
	--UIAccessor.PressDefaultButton()
	--UIAccessor.CloseDialog WindowHandle
	--UIAccessor.SendMessageID WindowHandle #IDOK
	)



	if  dialogName!=undefined and dialogName!="" and dialogName=="Proxy System" then (

		format "Dialog Name: %\n" (UIAccessor.GetWindowText WindowHandle)
		 
		
		local hwnd_children = uiAccessor.getChildWindows WindowHandle
		for i = 1 to hwnd_children.count do (
			format "% = \"%\"\n" i (uiAccessor.getWindowText hwnd_children[i])
		)

		--UIAccessor.PressDefaultButton()
		
		--UIAccessor.CloseDialog WindowHandle
		UIAccessor.pressButtonByName WindowHandle "&No"
		--UIAccessor.SendMessageID WindowHandle #IDOK
	)
    
    if  dialogName!=undefined and dialogName!="" and (matchpattern dialogName pattern:"vue xstream*" ignoreCase:true) then (

		format "Dialog Name: %\n" (UIAccessor.GetWindowText WindowHandle)
		 
		
		UIAccessor.PressDefaultButton()
		UIAccessor.CloseDialog WindowHandle
		UIAccessor.pressButtonByName WindowHandle "&No"
		UIAccessor.pressButtonByName WindowHandle "&Cancel"
		UIAccessor.SendMessageID WindowHandle #IDOK
        format "Dialog NameXXXXXXX\n" 
		
	)
	true
)

-----------------------------------------------------



struct STUtil(
	fn dotnetLog logStr=(
		if (maxversion())[1] < 18000 then(--2015,2014,2013,2012,2011,2010
			dotnetOut = DotNetClass "System.Console"
			dotnetOut.WriteLine ((localTime as string)+logStr)
		
		)else(
			G_STDOUT.print logStr
		)
		
		format "% %\n"localTime logStr
	),
	fn cmdLog logStr = (
		format "%\n" logStr
		DOSCommand ("echo "+logStr)
	),
	

	fn fillLeftZero sourceStr count= (
		if sourceStr ==undefined or sourceStr =="" then return sourceStr
		
		local str =sourceStr as string
		
		if  (matchPattern  str pattern:"-*" ) then(
			str=substring str 2 -1
			format "line......%\n" str
			while str.count<(count-1) do (
				str = "0" + str
			)
			str = "-"+str
		)else(
			while str.count<count do (
				str = "0" + str
			)
		)
		
		str
	),

	fn getFileNameFN file= (
		local ext = getFilenameType file
		local bname = getFileNameFile file
		local result = bname + ext
		result
	),
	
	
	fn replaceFN sourceStr oldStr newStr  = (
		
		if sourceStr ==undefined then return sourceStr
		local resultArr = #()
		for i=1 to sourceStr.count do (
			local index = findString sourceStr oldStr
			if index!=undefined then (
				local startStr = substring sourceStr 1 (index-1) 
				sourceStr = substring sourceStr (index+oldStr.count) sourceStr.count				
				append resultArr (startStr + newStr)
				
			)
		)
		append resultArr sourceStr
		local result = ""	
		for  rr in resultArr do (			
			append result rr
			
		)
		
		result
	),
	
	fn isStandardName myName= (
		allowed = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_-. "
		if myName==undefined or myName=="" then (
			return false
		)
		for i = 1 to myName.count do(
			if (findstring allowed myName[i]) == undefined then(			
				return false
			)
		)
		true
	),
	
	fn toStanderName myName=(
		local allowed = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_-. "
		local result = ""
		if myName==undefined or myName=="" then (
			
			result=undefined 
		)else(
			for i = 1 to myName.count do(
				if (findstring allowed myName[i]) != undefined then(
					result = result+myName[i]
				)
			)
			
			
			--check  all is space
			myName=result
			local spaceStr=" "
			local spaceCount=0
			format "myName....%\n" myName
			for i = 1 to myName.count do(
				if (findstring spaceStr myName[i]) != undefined then(
					spaceCount=spaceCount+1
				)
			)
			
			if spaceCount==myName.count then (
				result =undefined
			)
			
			if result=="" then (
				result=undefined
			)
		)
		
		result
	
	),
	fn get_json_val json_parser key_list value_type:"string" =(
		--local my_val = (((json_parser.GetValue  "system_info").GetValue "common").GetValue "channel").Value
		local json_temp =undefined
		for key in key_list do (
			if json_temp==undefined then (
				json_temp=(json_parser.GetValue  key)
			)else(
				json_temp=(json_temp.GetValue  key)
			)
			
		)
        if value_type=="list" then (
            json_temp
        )else(
            json_temp.Value
        )
		
	)
	
	
	
)
G_OBJ_UTIL = STUtil()




struct STConst (
	
	WORK_PATH="d:/work/render/",
	USER_ID,
	TASK_ID,
	MY_ACTION,
	
	SCRIPT_UPDATE,
	DEFAULT_DRIVER="A:",
	RENDER_FRAME,
	RENDER_FRAME_START,
	RENDER_FRAME_END,
	RENDER_FRAME_BY,
	RENDER_FRAME_SERIAL, 
	BLOCK_NUMBER,
	TOTAL_BLOCK,
	OVER_LAP=5,
	REGION_ARR,
	MAXFILE,
	NOT_RENDER,
	MYKG,
	MYPLATFORM,
	STEP_COUNT="7",
	PROJECT_SYMBOL="default",
	GUY_VERSION,
	OUTPUT_NAME="renderbus.jpg",
	ELEMENT_ACTIVE,
	RENDER_ELEMENT,
	ELEM_TYPE,
	VRAY_GI,
	VRAY_PRIMARY_GIENGINE,
	VRAY_SECONDARY_GIENGINE,
	VRAY_IRRADIANCEMAP_MODE,
	VRAY_IRRMAP_FILE,
	VRAY_LIGHTCACHE_MODE,
	VRAY_LIGHTCACHE_FILE,
	VRAY_IMAGE_SAMPLE_TYPE,
	VRAY_FILTER_ON,
	VRAY_FILTER_KERNEL,
	VRAY_DISTRIBUTE,
	JOB_ID,
	OUTPUT_PATH,
	OUTPUT_FILE,
	OUTPUT_SERIAL_FILE,
	RENDER_WORK="",
	LOG_PATH="c:/log/render/",
	CACHE_PATH,
	TEXTURE_PATH,
	PHOTON_PATH,
    MERGE_PATH,
	RENDERER_OBJECT,
	RENDERER_STR,
	RENDER_CFG_FILE="c:/rayvision/render/render.cfg",
	MAX_GAMMA,
	MAX_GAMMAVAL,
	MAX_INGAMMA,
	MAX_OUTGAMMA,
	ACTIVE_CAMERA,
	RENDERABLE_CAMERA,
	SKIP_UPLOAD="0",
	MYWIDTH,
	MYHEIGHT,
	MYCURRENTTASK,--picture/photon
	PLUGINS_MAX="B:/plugins/max/script/user/",
	SUB_FROM,
	IS_PICTURE="false",
	IS_BAKERENDER="false",		
	BAKERENDERID,
	CUSTOM_CLIENT="",
    MAX_QUICK_RENDER=true,
	PARAM_ARRAY=#(),
	ASSET_WEB_COOLECT_BY_PATH=false,
	PHOTON_DISPLACEMENT,
	PHOTON_REFLE_REFRA,
	MAX_USER_PATH=#(),
	MAX_XREF_PATH=#(),
	JSON_PARSER,
	
	fn bcdPath myDriver myPath=(
		local pathArr = filterString myPath ":"
		myDriver = pathArr[1]
		mySubPath= pathArr[2]
		
		local resultPath = (RENDER_WORK+myDriver+mySubPath)
		G_OBJ_UTIL.dotnetLog (" [bcdPath.resultPath]="+resultPath)
		resultPath
		
	),
	
	fn analyseRenderFrame =(
		local myStartFrame = undefined 
		local myEndFrame=undefined 
		local myByFrame=undefined
		
		if RENDER_FRAME !=undefined then (
			local frameArr1 = filterString RENDER_FRAME  "-"
			if frameArr1!=undefined and frameArr1.count==2 then (--11-113[6]
				myStartFrame = ""
				myEndFrame = ""
				if RENDER_FRAME[1] == "-" then(
					myStartFrame = "-"
				)
				if (findString RENDER_FRAME "--") != undefined then(
					myEndFrame = "-"
				)
			
				myStartFrame=myStartFrame+frameArr1[1]
				
				local frameArr2 = filterString frameArr1[2] "["
				
				if frameArr2!=undefined and frameArr2.count==2 then (
					myEndFrame=myEndFrame+frameArr2[1]
					
					myByFrame=G_OBJ_UTIL.replaceFN frameArr2[2] "]" ""
					
				)else if frameArr2!=undefined and frameArr2.count==1 then (--11-113
					myEndFrame=myEndFrame+frameArr2[1]
					
					myByFrame="1"
				)
				
			)
		)
		if myStartFrame!=undefined and myEndFrame!=undefined and myByFrame!=undefined then(--kg=100
			RENDER_FRAME_START= myStartFrame
			RENDER_FRAME_END=myEndFrame
			RENDER_FRAME_BY=myByFrame
		)
		if MYKG == "100" then(
			RENDER_FRAME_START= RENDER_FRAME
			RENDER_FRAME_END=RENDER_FRAME
			RENDER_FRAME_BY="1"
		)
		
	),
	
	fn getMaxFile=(
		--local maxFile=getINISetting RENDER_CFG_FILE "max" "max"
        local maxFile = (((json_parser.GetValue  "system_info").GetValue "common").GetValue "input_cg_file").Value
		maxFile=substituteString maxFile "\\" "/"
		format "maxfile............%\n" maxFile
		
		if VRAY_DISTRIBUTE!=undefined and VRAY_DISTRIBUTE=="true" then (
			
			local resultPath =RENDER_WORK+TASK_ID+".max"
			G_OBJ_UTIL.dotnetLog (" [getMaxFile.resultPath]="+resultPath)
			return resultPath
			
		)else(
			local netRenderTxt=PLUGINS_MAX+USER_ID+"/netrender.txt"
			if  doesFileExist netRenderTxt  then (-- net render
				local resultPath =(RENDER_WORK+(getfilenamefile maxFile)+(getfilenametype maxFile))
				G_OBJ_UTIL.dotnetLog (" [getMaxFile.resultPath]="+resultPath)
				return resultPath
			)
			
			if SKIP_UPLOAD=="1" then (
				local resultPath =(RENDER_WORK+(getfilenamefile maxFile)+(getfilenametype maxFile))
				G_OBJ_UTIL.dotnetLog (" [getMaxFile.resultPath]="+resultPath)
				return resultPath
			)else(
				if (findstring maxFile "/")==1 then (--\\serverA\bbgg\gg\abdd.pic>>/neta/bbgg/gg/abdd.pic
					local pathArr = filterString maxFile "/"
					mySubPath=""
					for i=1 to pathArr.count do (
						if i==pathArr.count then (
							mySubPath=mySubPath+pathArr[i]
						)else(
							mySubPath=mySubPath+pathArr[i]+"/"
						)
					)
					local resultPath = (RENDER_WORK+"net/"+mySubPath)
					if SUB_FROM=="1" or SUB_FROM=="2" then (
						resultPath = (RENDER_WORK+"__"+mySubPath)
					)
					G_OBJ_UTIL.dotnetLog (" [getMaxFile.resultPath]="+resultPath)
					return resultPath
				)
				
				local lowerMaxFile = toLower maxFile
				
				if (findstring lowerMaxFile "b:")==1 then (--c:/img/feee.jpg>>e/img/feee.jpg
					return bcdPath "b" maxFile
				)
				if (findstring lowerMaxFile "c:")==1 then (--c:/img/feee.jpg>>e/img/feee.jpg
					return bcdPath "c" maxFile
				)
				
				if (findstring lowerMaxFile "d:")==1 then (--c:/img/feee.jpg>>e/img/feee.jpg
					return bcdPath "d" maxFile
				)
				
				if (findstring maxFile ":")==2 then (--e:/img/feee.jpg>>e/img/feee.jpg
					G_OBJ_UTIL.dotnetLog (" [getMaxFile.resultPath]=undefined2")
					
					return maxFile 
				)
				
				local resultPath =("/default/"+maxFile)
				G_OBJ_UTIL.dotnetLog (" [getMaxFile.resultPath]="+resultPath)
				return resultPath
			)
			
		)
			
		
        
        
	),
	
	fn readRenderCfg =(
		
		if doesFileExist RENDER_CFG_FILE then (
            
			local renderSettingsOptionName="renderSettings"
			if SUB_FROM=="1" or SUB_FROM=="2" then (
				renderSettingsOptionName="common"
				local outputBaseName=getINISetting RENDER_CFG_FILE renderSettingsOptionName "rendoutputfilebasename"
				local outputType=getINISetting RENDER_CFG_FILE renderSettingsOptionName "rendoutputfiletype"
				OUTPUT_NAME=outputBaseName+outputType
			)else(
				renderSettingsOptionName="renderSettings"
				
				OUTPUT_NAME=getINISetting RENDER_CFG_FILE renderSettingsOptionName "output"
			)
			
			
			
			
			--RENDERABLE_CAMERA = getINISetting RENDER_CFG_FILE renderSettingsOptionName "renderableCamera"
			MAX_GAMMA = getINISetting RENDER_CFG_FILE renderSettingsOptionName "gamma"
			MAX_GAMMAVAL = getINISetting RENDER_CFG_FILE renderSettingsOptionName "gammaval"
			MAX_INGAMMA = getINISetting RENDER_CFG_FILE renderSettingsOptionName "ingamma"
			MAX_OUTGAMMA = getINISetting RENDER_CFG_FILE renderSettingsOptionName "outgamma"
			GUY_VERSION= getINISetting RENDER_CFG_FILE "common" "guyVersion"
			PROJECT_SYMBOL= getINISetting RENDER_CFG_FILE "common" "projectSymbol"
			
			scriptUpdateStr= getINISetting RENDER_CFG_FILE "common" "update"
			SCRIPT_UPDATE=scriptUpdateStr as integer
			
			--if G_OBJ_UTIL.isBigVersion GUY_VERSION "3.0.1.17" then(
			
			
			ELEMENT_ACTIVE=getINISetting RENDER_CFG_FILE renderSettingsOptionName "ElementActive"
			RENDER_ELEMENT=getINISetting RENDER_CFG_FILE renderSettingsOptionName "RenderElement"
			ELEM_TYPE=getINISetting RENDER_CFG_FILE renderSettingsOptionName "elemType"
			
			
			VRAY_GI=getINISetting RENDER_CFG_FILE "vray" "gi"
			VRAY_PRIMARY_GIENGINE=getINISetting RENDER_CFG_FILE "vray" "PrimaryGIEngine"
			VRAY_SECONDARY_GIENGINE=getINISetting RENDER_CFG_FILE "vray" "SecondaryGIEngine"
			VRAY_IRRADIANCEMAP_MODE=getINISetting RENDER_CFG_FILE "vray" "irradianceMapMode"
			VRAY_IRRMAP_FILE=getINISetting RENDER_CFG_FILE "vray" "irrmapfile"
			VRAY_LIGHTCACHE_MODE=getINISetting RENDER_CFG_FILE "vray" "lightcacheMode"
			VRAY_LIGHTCACHE_FILE=getINISetting RENDER_CFG_FILE "vray" "lightcacheFile"
			VRAY_IMAGE_SAMPLE_TYPE=getINISetting RENDER_CFG_FILE "vray" "imageSamplerType"
			VRAY_FILTER_ON=getINISetting RENDER_CFG_FILE "vray" "filterOn"
			VRAY_FILTER_KERNEL=getINISetting RENDER_CFG_FILE "vray" "filterKernel"
			VRAY_DISTRIBUTE=getINISetting RENDER_CFG_FILE "vray" "distribute"
			--VRAY_DISTRIBUTE="3"
			PHOTON_DISPLACEMENT= getINISetting RENDER_CFG_FILE "vray" "displacement"
			PHOTON_REFLE_REFRA= getINISetting RENDER_CFG_FILE "vray" "reflectionRefraction"
			
            CUSTOM_CLIENT= getINISetting RENDER_CFG_FILE "common" "customclient"
            
			--if MYCURRENTTASK!=undefined and MYCURRENTTASK=="photon" then (
            if MY_ACTION!=undefined and MY_ACTION=="RenderPhoton" then (
				MYWIDTH=getINISetting RENDER_CFG_FILE "vray" "giwidth"
				MYHEIGHT=getINISetting RENDER_CFG_FILE "vray" "giheight"
                if CUSTOM_CLIENT!=undefined and CUSTOM_CLIENT=="yunwu" then (
                    MYWIDTH="1800"
                    MYHEIGHT="900"
                )
				renderWidth=MYWIDTH as integer
				renderHeight=MYHEIGHT  as integer
			)else(
				MYWIDTH=getINISetting RENDER_CFG_FILE renderSettingsOptionName "width"
				MYHEIGHT=getINISetting RENDER_CFG_FILE renderSettingsOptionName "height"
				renderWidth=MYWIDTH as integer
				renderHeight=MYHEIGHT  as integer
			)
			
			
			IS_PICTURE= getINISetting RENDER_CFG_FILE "common" "ispicture"
			if IS_PICTURE==undefined or IS_PICTURE=="" then (
				IS_PICTURE="false"
				
			)
			
			IS_BAKERENDER= getINISetting RENDER_CFG_FILE "common" "isbakerender"
			if IS_BAKERENDER==undefined or IS_BAKERENDER=="" then (
				IS_BAKERENDER="false" 
			)
			BAKERENDERID= getINISetting RENDER_CFG_FILE "renderSettings" "bakeobjectids"
			 
            
			 
			--multipler camera output folder with camera label
            local myRenderCameras= getINISetting RENDER_CFG_FILE renderSettingsOptionName "renderablecamera"
            local myRenderCameras2= getINISetting RENDER_CFG_FILE renderSettingsOptionName "renderablecameras"
			myRenderCameras=trimRight myRenderCameras "[,]"
            myRenderCameras2=trimRight myRenderCameras2 "[,]"
            if myRenderCameras!=undefined and ( matchPattern  myRenderCameras pattern:"*[,]*" ) then(
				local myCameraFolder=substituteString RENDERABLE_CAMERA "/" "_"
				myCameraFolder=substituteString RENDERABLE_CAMERA "\\" "_"
				--OUTPUT_PATH=OUTPUT_PATH+myCameraFolder+"/"
                PHOTON_PATH=PHOTON_PATH+myCameraFolder+"/"
                MERGE_PATH=MERGE_PATH+myCameraFolder+"/"
                
			)else if myRenderCameras2!=undefined and ( matchPattern  myRenderCameras2 pattern:"*[,]*" ) then(
				local myCameraFolder=substituteString RENDERABLE_CAMERA "/" "_"
				myCameraFolder=substituteString RENDERABLE_CAMERA "\\" "_"
				--OUTPUT_PATH=OUTPUT_PATH+myCameraFolder+"/"
                PHOTON_PATH=PHOTON_PATH+myCameraFolder+"/"
                MERGE_PATH=MERGE_PATH+myCameraFolder+"/"
			)
			
			SKIP_UPLOAD=getINISetting RENDER_CFG_FILE "common" "skipUpload"
			format "*****[%].....\n" OUTPUT_NAME
			if OUTPUT_NAME!=undefined then (
				if OUTPUT_NAME=="" then (
					OUTPUT_NAME="rayvision.tga"
				)
				local baseName=getfilenamefile OUTPUT_NAME
				if baseName!=undefined and (not matchPattern  baseName pattern:"*_" ) then(
					OUTPUT_NAME=baseName+"_"+(getfilenametype OUTPUT_NAME)
				)
			)
			
			
			--if CUSTOM_CLIENT!=undefined and CUSTOM_CLIENT=="yunwu" then (
			--	RENDERABLE_CAMERA=PARAM_ARRAY[11]
			--)				
			
		)
		
	),
	

	
	fn myLoadAssembly dllFile =(
		local assemblyStr=((dotnetClass "System.IO.File").ReadAllBytes dllFile)
		(dotnetClass "System.Reflection.Assembly").Load assemblyStr
	),
	
	fn get_json_parser task_json=(
		
		format "task_json-------------------%\n" task_json
		local json_dll=@"B:\plugins\max\newtonsoftJson\3.5\Newtonsoft.Json.dll" 
		myLoadAssembly json_dll
		local json_str = ""  
		local json_file = openFile task_json  
		while not eof json_file do(  
			json_str += readchar json_file  
		)  
		close json_file
		--(dotnetClass "System.Reflection.assembly").Load ((dotnetClass "System.IO.File").ReadAllBytes(json_dll))  
	
		JSON_PARSER = (dotNetObject "Newtonsoft.Json.Linq.JObject").parse json_str  
	),
    
	fn readTaskJson task_json=(
		
		if doesFileExist task_json then (
            
			--local renderSettingsOptionName="renderSettings"
			
			if SUB_FROM=="1" or SUB_FROM=="2" then (
				--renderSettingsOptionName="common"
				local outputBaseName=G_OBJ_UTIL.get_json_val JSON_PARSER #("scene_info_render","common", "output_file_basename")
				local outputType=G_OBJ_UTIL.get_json_val JSON_PARSER #("scene_info_render","common", "output_file_type")
				if (findString outputType ".")==undefined then(
					OUTPUT_NAME=outputBaseName+"."+outputType
				)else(
					OUTPUT_NAME=outputBaseName+outputType
				)
			)else(
				--renderSettingsOptionName="renderSettings"
				
				--OUTPUT_NAME=getINISetting RENDER_CFG_FILE renderSettingsOptionName "output"
			)
			
			
			--MYKG = G_OBJ_UTIL.get_json_val JSON_PARSER #("scene_info_render","common", "kg")
			
			--RENDERABLE_CAMERA = getINISetting RENDER_CFG_FILE renderSettingsOptionName "renderableCamera"
			MAX_GAMMA = G_OBJ_UTIL.get_json_val JSON_PARSER #("scene_info_render","common", "gamma")
			MAX_GAMMAVAL = G_OBJ_UTIL.get_json_val JSON_PARSER #("scene_info_render","common", "gamma_val")
			MAX_INGAMMA = G_OBJ_UTIL.get_json_val JSON_PARSER #("scene_info_render","common", "in_gamma")
			MAX_OUTGAMMA = G_OBJ_UTIL.get_json_val JSON_PARSER #("scene_info_render","common", "out_gamma")
			--GUY_VERSION= getINISetting RENDER_CFG_FILE "common" "guyVersion"
			--PROJECT_SYMBOL= getINISetting RENDER_CFG_FILE "common" "projectSymbol"
			
			--scriptUpdateStr= getINISetting RENDER_CFG_FILE "common" "update"
			--SCRIPT_UPDATE=scriptUpdateStr as integer
			
			--if G_OBJ_UTIL.isBigVersion GUY_VERSION "3.0.1.17" then(
			
			
			ELEMENT_ACTIVE=G_OBJ_UTIL.get_json_val JSON_PARSER #("scene_info_render","common", "element_active")
			RENDER_ELEMENT=G_OBJ_UTIL.get_json_val JSON_PARSER #("scene_info_render","common", "all_element")
			ELEM_TYPE=G_OBJ_UTIL.get_json_val JSON_PARSER #("scene_info_render","common", "element_type")
			
			local renderer_name_yes = true
			try
			(
				local renderer_name = G_OBJ_UTIL.get_json_val JSON_PARSER #("scene_info_render","renderer", "name")
				format "renderer_name:%\n" renderer_name
			)
			catch
			(
					print "json file have no scene_info_render.renderer.name"
					renderer_name_yes = false
			)
			
			if renderer_name_yes == true and (G_OBJ_UTIL.get_json_val JSON_PARSER #("scene_info_render","renderer", "name")) == "vray" then
			(
				VRAY_GI=G_OBJ_UTIL.get_json_val JSON_PARSER #("scene_info_render","renderer", "gi")
				VRAY_PRIMARY_GIENGINE=G_OBJ_UTIL.get_json_val JSON_PARSER #("scene_info_render","renderer", "primary_gi_engine")
				VRAY_SECONDARY_GIENGINE=G_OBJ_UTIL.get_json_val JSON_PARSER #("scene_info_render","renderer", "secondary_gi_engine")
				VRAY_IRRADIANCEMAP_MODE=G_OBJ_UTIL.get_json_val JSON_PARSER #("scene_info_render","renderer", "irradiance_map_mode")
				VRAY_IRRMAP_FILE=G_OBJ_UTIL.get_json_val JSON_PARSER #("scene_info_render","renderer", "irrmap_file")
				VRAY_LIGHTCACHE_MODE=G_OBJ_UTIL.get_json_val JSON_PARSER #("scene_info_render","renderer", "light_cache_mode")
				VRAY_LIGHTCACHE_FILE=G_OBJ_UTIL.get_json_val JSON_PARSER #("scene_info_render","renderer", "light_cache_file")
				VRAY_IMAGE_SAMPLE_TYPE=G_OBJ_UTIL.get_json_val JSON_PARSER #("scene_info_render","renderer", "image_sampler_type")
				VRAY_FILTER_ON=G_OBJ_UTIL.get_json_val JSON_PARSER #("scene_info_render","renderer", "filter_on")
				VRAY_FILTER_KERNEL=G_OBJ_UTIL.get_json_val JSON_PARSER #("scene_info_render","renderer", "filter_kernel")
				VRAY_DISTRIBUTE=G_OBJ_UTIL.get_json_val JSON_PARSER #("system_info","common", "distribute_node")
				--VRAY_DISTRIBUTE="3"
				PHOTON_DISPLACEMENT= G_OBJ_UTIL.get_json_val JSON_PARSER #("scene_info_render","renderer", "displacement")
				PHOTON_REFLE_REFRA= G_OBJ_UTIL.get_json_val JSON_PARSER #("scene_info_render","renderer", "reflection_refraction")

			)
            --CUSTOM_CLIENT= getINISetting RENDER_CFG_FILE "common" "customclient"
            
			if MY_ACTION!=undefined and MY_ACTION=="RenderPhoton" then (
				MYWIDTH=G_OBJ_UTIL.get_json_val JSON_PARSER #("scene_info_render","renderer", "gi_width")
				MYHEIGHT=G_OBJ_UTIL.get_json_val JSON_PARSER #("scene_info_render","renderer", "gi_height")
                --if CUSTOM_CLIENT!=undefined and CUSTOM_CLIENT=="yunwu" then (
                --    MYWIDTH="1800"
                --   MYHEIGHT="900"
                --)
				renderWidth=MYWIDTH as integer
				renderHeight=MYHEIGHT  as integer
			)else(
				MYWIDTH=G_OBJ_UTIL.get_json_val JSON_PARSER #("scene_info_render","common", "width")
				MYHEIGHT=G_OBJ_UTIL.get_json_val JSON_PARSER #("scene_info_render","common", "height")
				renderWidth=MYWIDTH as integer
				renderHeight=MYHEIGHT  as integer
			)
			
			/*
			IS_PICTURE= getINISetting RENDER_CFG_FILE "common" "ispicture"
			if IS_PICTURE==undefined or IS_PICTURE=="" then (
				IS_PICTURE="false"
				
			)
			
			IS_BAKERENDER= getINISetting RENDER_CFG_FILE "common" "isbakerender"
			if IS_BAKERENDER==undefined or IS_BAKERENDER=="" then (
				IS_BAKERENDER="false" 
			)
			BAKERENDERID= getINISetting RENDER_CFG_FILE "renderSettings" "bakeobjectids"
			*/ 
            
			 
			--multipler camera output folder with camera label
            local myRenderCameras= G_OBJ_UTIL.get_json_val JSON_PARSER #("scene_info_render","common", "renderable_camera") value_type:"list"
            --local myRenderCameras2= getINISetting RENDER_CFG_FILE renderSettingsOptionName "renderablecameras"
			--myRenderCameras=trimRight myRenderCameras "[,]"
            --myRenderCameras2=trimRight myRenderCameras2 "[,]"
			--if myRenderCameras!=undefined and ( matchPattern  myRenderCameras pattern:"*[,]*" ) then(
            if myRenderCameras!=undefined and myRenderCameras.count > 1 then(
				local myCameraFolder=substituteString RENDERABLE_CAMERA "/" "_"
				myCameraFolder=substituteString RENDERABLE_CAMERA "\\" "_"
				--OUTPUT_PATH=OUTPUT_PATH+myCameraFolder+"/"
                PHOTON_PATH=PHOTON_PATH+myCameraFolder+"/"
                MERGE_PATH=MERGE_PATH+myCameraFolder+"/"
               
			)
			/* 
			else if myRenderCameras2!=undefined and ( matchPattern  myRenderCameras2 pattern:"*[,]*" ) then(
				local myCameraFolder=substituteString RENDERABLE_CAMERA "/" "_"
				myCameraFolder=substituteString RENDERABLE_CAMERA "\\" "_"
				--OUTPUT_PATH=OUTPUT_PATH+myCameraFolder+"/"
                PHOTON_PATH=PHOTON_PATH+myCameraFolder+"/"
                MERGE_PATH=MERGE_PATH+myCameraFolder+"/"
			)
			*/
			--SKIP_UPLOAD=getINISetting RENDER_CFG_FILE "common" "skipUpload"
			format "*****[%].....\n" OUTPUT_NAME
			if OUTPUT_NAME!=undefined then (
				if OUTPUT_NAME=="" then (
					OUTPUT_NAME="rayvision.tga"
				)
				local baseName=getfilenamefile OUTPUT_NAME
				if baseName!=undefined and (not matchPattern  baseName pattern:"*_" ) then(
					OUTPUT_NAME=baseName+"_"+(getfilenametype OUTPUT_NAME)
				)
			)
			
			
			--if CUSTOM_CLIENT!=undefined and CUSTOM_CLIENT=="yunwu" then (
			--	RENDERABLE_CAMERA=PARAM_ARRAY[11]
			--)				
			
		)
		
	),    
    
    
	--fn init u t notRender f blockNumber totalBlock kg j  outputPath myplatfrom cgOption  currenttask subFrom myMaxFile =(
	fn init paramArray=(
		PARAM_ARRAY=paramArray
		USER_ID = PARAM_ARRAY[1]
		TASK_ID = PARAM_ARRAY[2]
		NOT_RENDER=PARAM_ARRAY[3]
		RENDER_FRAME = PARAM_ARRAY[4]
		RENDER_FRAME_START= PARAM_ARRAY[4]
		RENDER_FRAME_END =PARAM_ARRAY[4]
		JOB_ID=PARAM_ARRAY[5]
		
        RENDERABLE_CAMERA=PARAM_ARRAY[6]
		MY_ACTION=PARAM_ARRAY[7]
		OUTPUT_PATH=PARAM_ARRAY[8]
		MAXFILE =PARAM_ARRAY[9]
		
		
		
        task_json=PARAM_ARRAY[10]
		MYKG = PARAM_ARRAY[11]
        
		LOG_PATH=LOG_PATH+USER_ID+"/"+TASK_ID+"/"
		
		analyseRenderFrame()
		RENDER_FRAME_SERIAL  = ""
		if RENDER_FRAME_START==RENDER_FRAME_END then(
			RENDER_FRAME_SERIAL  = G_OBJ_UTIL.fillLeftZero RENDER_FRAME 4
		)
		
		RENDER_WORK =WORK_PATH+TASK_ID+"/max/"--( pathConfig.removePathLeaf MAXFILE)+"/"
		
		PHOTON_PATH=RENDER_WORK+"/photon/"
        MERGE_PATH=WORK_PATH+TASK_ID+"/block/frame_"+RENDER_FRAME+"/"
		--RENDER_WORK=G_OBJ_UTIL.replaceFN RENDER_WORK "\\" "/"
		CACHE_PATH=RENDER_WORK
		TEXTURE_PATH=RENDER_WORK
		
		MYWIDTH=renderWidth as string
		MYHEIGHT=renderHeight as string
		
		get_json_parser(task_json)
		--local sys_info = (((JSON_PARSER.GetValue  "system_info").GetValue "common").GetValue "channel").Value
		SUB_FROM=G_OBJ_UTIL.get_json_val JSON_PARSER #("system_info","common", "channel")
		MYPLATFORM=G_OBJ_UTIL.get_json_val JSON_PARSER #("system_info","common", "platform")
		readTaskJson(task_json)
		
		
		
		G_OBJ_UTIL.dotnetLog (" [init]MYPLATFORM="+MYPLATFORM)
		G_OBJ_UTIL.dotnetLog (" [init]RENDER_CFG_FILE="+RENDER_CFG_FILE)
		G_OBJ_UTIL.dotnetLog (" [init]USER_ID="+USER_ID)
		G_OBJ_UTIL.dotnetLog (" [init]TASK_ID="+TASK_ID)
		G_OBJ_UTIL.dotnetLog (" [init]NOT_RENDER="+NOT_RENDER)
		G_OBJ_UTIL.dotnetLog (" [init]BLOCK_NUMBER="+(BLOCK_NUMBER as string))
		G_OBJ_UTIL.dotnetLog (" [init]TOTAL_BLOCK="+(TOTAL_BLOCK as string))
		G_OBJ_UTIL.dotnetLog (" [init]RENDER_FRAME="+RENDER_FRAME)
		G_OBJ_UTIL.dotnetLog (" [init]RENDER_FRAME_START="+RENDER_FRAME_START)
		G_OBJ_UTIL.dotnetLog (" [init]RENDER_FRAME_END="+RENDER_FRAME_END)
		G_OBJ_UTIL.dotnetLog (" [init]RENDER_FRAME_BY="+(RENDER_FRAME_BY as string))
		G_OBJ_UTIL.dotnetLog (" [init]MY_ACTION="+MY_ACTION)
		G_OBJ_UTIL.dotnetLog (" [init]SUB_FROM="+SUB_FROM)
		G_OBJ_UTIL.dotnetLog (" [init]CUSTOM_CLIENT="+CUSTOM_CLIENT)	
		G_OBJ_UTIL.dotnetLog (" [init]MAX_QUICK_RENDER="+(MAX_QUICK_RENDER as string))	
			
			
		G_OBJ_UTIL.dotnetLog (" [init]JOB_ID="+JOB_ID)
		G_OBJ_UTIL.dotnetLog (" [init]MAXFILE="+MAXFILE)
		G_OBJ_UTIL.dotnetLog (" [init]OUTPUT_PATH="+OUTPUT_PATH)
		G_OBJ_UTIL.dotnetLog (" [init]MYWIDTH="+MYWIDTH)
		G_OBJ_UTIL.dotnetLog (" [init]MYHEIGHT="+MYHEIGHT)
		
		G_OBJ_UTIL.dotnetLog (" [init]RENDER_WORK="+RENDER_WORK)
		G_OBJ_UTIL.dotnetLog (" [init]RENDER_FRAME_SERIAL="+RENDER_FRAME_SERIAL)
		
		G_OBJ_UTIL.dotnetLog (" [init]RENDERABLE_CAMERA="+(RENDERABLE_CAMERA as string))
			
			
		G_OBJ_UTIL.dotnetLog (" [init]OUTPUT_NAME="+(OUTPUT_NAME as string))
			
			
		makeDir OUTPUT_PATH all:true
			
	)
	
)
G_STCON=STConst()






struct STConfigMax(
	
	fn delAllUserPath = (
		
		local cc =mapPaths.count()
		for i in cc to 1 by -1 do (
			try(
				mapPaths.delete i
			)catch()
		)
		
	),

	fn getAllUserPath=(
		
		local userPathArr = #()
		for i=1 to mapPaths.count() do (
			local myPath = mapPaths.get i
			append userPathArr myPath
		)
		userPathArr
	),

	fn addUserPath userPathArr = (
		
		for i=1 to userPathArr.count do (
			local mpath = userPathArr[i]
			if mpath!=undefined then (
				mapPaths.add mpath
			)
			
		)
		
		
	),

	
	fn delAllXrefPath = (
		
		local cc =xrefPaths.count()
		for i in cc to 1 by -1 do (
			try(
				xrefPaths.delete i
			)catch()
		)
		
	),

	fn getAllXrefPath=(
		
		local xrefPathArr = #()
		for i=1 to xrefPaths.count() do (
			local myPath = xrefPaths.get i
			append xrefPathArr myPath
		)
		xrefPathArr
	),

	fn addXrefPath xrefPathArr = (
		
		for i=1 to xrefPathArr.count do (
			local mpath = xrefPathArr[i]
			if mpath!=undefined then (
				xrefPaths.add mpath
			)
			
		)
		
		
	),
	
	
	fn initMaxFN = (
		G_OBJ_UTIL.dotnetLog (" [initMaxFN].Start ")
		/*
		if (maxversion())[1] == 12000 then(
			try(
				(DotNetClass "System.Windows.Forms.Application").CurrentCulture = dotnetObject "System.Globalization.CultureInfo" "zh-cn"
				
			)catch()
		)
		*/
		try(
			useFileUnits=true 
			quiet=true 
		)catch()
		try(setVRaySilentMode() )catch()
	
		local pathArr = getAllUserPath()
		G_STCON.MAX_USER_PATH=pathArr
		local userPathArr=#(G_STCON.RENDER_WORK,G_STCON.TEXTURE_PATH,G_STCON.CACHE_PATH)
		addUserPath userPathArr
		
		local xrefPathArr =getAllXrefPath()
		G_STCON.MAX_XREF_PATH=xrefPathArr
		local xrefPathArr=#(G_STCON.RENDER_WORK,G_STCON.TEXTURE_PATH,G_STCON.CACHE_PATH)
		addUserPath xrefPathArr
		G_OBJ_UTIL.dotnetLog (" [initMaxFN].End \n")
		
	),
	
	
	fn resetMaxFN =(
		G_OBJ_UTIL.dotnetLog (" [resetMaxFN].Start ")
		try(
			delAllUserPath()
			addUserPath G_STCON.MAX_USER_PATH
		)catch()
		
		try(
			delAllXrefPath()
			addXrefPath G_STCON.MAX_XREF_PATH
		)catch()
			
		G_OBJ_UTIL.dotnetLog (" [resetMaxFN].End \n")
		
	)
	
	
)



struct STFileUtil (
	
	fn abcdPath myDriver myPath=(
		local pathArr = filterString myPath ":"
		myDriver = pathArr[1]
		mySubPath= pathArr[2]
		
		local resultPath = (G_STCON.RENDER_WORK+myDriver+mySubPath)
		G_OBJ_UTIL.dotnetLog (" [NEW] "+resultPath)
		resultPath
		
	),
	
	

	fn analysePath myPath=(
		
		G_OBJ_UTIL.dotnetLog (" [OLD] "+(myPath as string))
			
		if G_STCON.VRAY_DISTRIBUTE!=undefined and G_STCON.VRAY_DISTRIBUTE=="true" then (
			G_OBJ_UTIL.dotnetLog ("vray distribute")
			return undefined
		)else(
			local netRenderTxt=G_STCON.PLUGINS_MAX+G_STCON.USER_ID+"/netrender.txt"
			if  doesFileExist netRenderTxt  then (-- net render
				return undefined
			)
			--if G_STCON.MYPLATFORM=="1005" or G_STCON.MYPLATFORM=="1004" or G_STCON.MYPLATFORM=="1002" then (
			--if G_STCON.MYPLATFORM=="1004"  then (
			--local scriptUpdate = getINISetting G_STCON.RENDER_CFG_FILE "common" "update"
			if G_STCON.MYPLATFORM=="1007"  then (
				local myFile=undefined 
				if myPath!=undefined and  myPath !="" then (
					local myFilename =getfilenamefile myPath+getfilenametype myPath
					local myFile = G_STCON.TEXTURE_PATH+myFilename
				)
				G_OBJ_UTIL.dotnetLog (" [NEW] "+(myFile as string))
				return myFile
				
			)else(
				if myPath==undefined or myPath=="" then (
					G_OBJ_UTIL.dotnetLog (" [NEW] "+(myPath as string))--("undefined")
					return undefined
				)
				myPath=G_OBJ_UTIL.replaceFN myPath "\\" "/"
				
				local myName =getfilenamefile myPath
				local myType= getfilenametype myPath
				local myFile = myName+myType
				if G_STCON.SUB_FROM=="1" or G_STCON.SUB_FROM=="2" then(
					------------------------by path-----------------------
					if G_STCON.ASSET_WEB_COOLECT_BY_PATH then (
						
						if myType==".max" then (
							local resultPath = (G_STCON.RENDER_WORK+myFile)
							return resultPath
						)
						------------net path
						if (findstring myPath "/")==1 then (--\\serverA\bbgg\gg\abdd.pic>>/neta/bbgg/gg/abdd.pic
							local pathArr = filterString myPath "/"
							mySubPath=""
							for i=1 to pathArr.count do (
								if i==pathArr.count then (
									mySubPath=mySubPath+pathArr[i]
								)else(
									mySubPath=mySubPath+pathArr[i]+"/"
								)
							)
							local resultPath = (G_STCON.RENDER_WORK+"__"+mySubPath)
							
							G_OBJ_UTIL.dotnetLog ("NEW="+(resultPath as string))
							return resultPath
						)
						
						lowerMyPath = toLower myPath
						if (findstring lowerMyPath "a:")==1 then (--c:/img/feee.jpg>>e/img/feee.jpg
							return abcdPath "a" myPath
						)
						if (findstring lowerMyPath "b:")==1 then (--c:/img/feee.jpg>>e/img/feee.jpg
							return abcdPath "b" myPath
						)
						if (findstring lowerMyPath "c:")==1 then (--c:/img/feee.jpg>>e/img/feee.jpg
							return abcdPath "c" myPath
						)
						
						if (findstring lowerMyPath "d:")==1 then (--c:/img/feee.jpg>>e/img/feee.jpg
							return abcdPath "d" myPath
						)
						
						if (findstring myPath ":")==2 then (--e:/img/feee.jpg>>e/img/feee.jpg
							G_OBJ_UTIL.dotnetLog (" [NEW] "+(myPath as string))--(" undefined2")
							
							local resultPath=undefined
							--G_OBJ_UTIL.dotnetLog (" [analysePath.type]="+ (myType as string))
							if myType==".vrmap" or myType==".vrlmap" then (
								resultPath= myPath 
							)
							
							return resultPath 
						)
						
						local resultPath =(G_STCON.RENDER_WORK+"/default/"+myFile)
						G_OBJ_UTIL.dotnetLog (" [NEW] "+(resultPath as string))
						return resultPath
						
					)else(-----------------------------------------------by name----------------------
						local resultPath =(G_STCON.RENDER_WORK+myFile)
						G_OBJ_UTIL.dotnetLog (" [NEW] "+(resultPath as string))
						return resultPath
						
					)
					
				)else(
					---------------------------------client-------------------------------------------
					if G_STCON.SKIP_UPLOAD=="1" then (
						local resultPath =(G_STCON.RENDER_WORK+myFile)
						G_OBJ_UTIL.dotnetLog (" [NEW] "+(resultPath as string))
						return resultPath
					)else(
						--max file
						if myType==".max" then (
							local resultPath = (G_STCON.RENDER_WORK+myFile)
							return resultPath
						)
						------------net path
						if (findstring myPath "/")==1 then (--\\serverA\bbgg\gg\abdd.pic>>/neta/bbgg/gg/abdd.pic
							local pathArr = filterString myPath "/"
							mySubPath=""
							for i=1 to pathArr.count do (
								if i==pathArr.count then (
									mySubPath=mySubPath+pathArr[i]
								)else(
									mySubPath=mySubPath+pathArr[i]+"/"
								)
							)
							local resultPath = (G_STCON.RENDER_WORK+"net/"+mySubPath)
							
							G_OBJ_UTIL.dotnetLog (" [NEW] "+(resultPath as string))
							return resultPath
						)
						
						lowerMyPath = toLower myPath
						if (findstring lowerMyPath "a:")==1 then (--c:/img/feee.jpg>>e/img/feee.jpg
							return abcdPath "a" myPath
						)
						if (findstring lowerMyPath "b:")==1 then (--c:/img/feee.jpg>>e/img/feee.jpg
							return abcdPath "b" myPath
						)
						if (findstring lowerMyPath "c:")==1 then (--c:/img/feee.jpg>>e/img/feee.jpg
							return abcdPath "c" myPath
						)
						
						if (findstring lowerMyPath "d:")==1 then (--c:/img/feee.jpg>>e/img/feee.jpg
							return abcdPath "d" myPath
						)
						
						if (findstring myPath ":")==2 then (--e:/img/feee.jpg>>e/img/feee.jpg
							--G_OBJ_UTIL.dotnetLog (" undefined2")
							
							local resultPath=undefined
							--G_OBJ_UTIL.dotnetLog (" [analysePath.type]="+ (myType as string))
							if myType==".vrmap" or myType==".vrlmap" then (
								resultPath= myPath 
							)
							G_OBJ_UTIL.dotnetLog (" [NEW] "+(myPath as string))
							return resultPath 
						)
						
						if not pathConfig.isAbsolutePath myPath then (
								
							local resultPath =(maxfilepath+myPath)
							--G_OBJ_UTIL.dotnetLog (resultPath)
							G_OBJ_UTIL.dotnetLog (" [NEW] "+(resultPath as string))
							return resultPath
						)
						
						local resultPath =(G_STCON.RENDER_WORK+"default/"+myFile)
						--G_OBJ_UTIL.dotnetLog (resultPath)
						G_OBJ_UTIL.dotnetLog (" [NEW] "+(resultPath as string))
						return resultPath
					
					)
				)
				
				
				
			)
		)

		
	)
	



-----------????,?????,?????????
/*
usedMapsArr= usedMaps()
for i=1 to usedMapsArr.count do (
format "%\n" usedMapsArr[i]
)




--VM = VRayMtl()
--show VM
--currentMaterialLibrary
show sceneMaterials
--currentMaterialLibrary 

=======================================================

vmtl = getClassInstances VrayMtl



for i=1 to vmtl.count do (
if i<5 do (
format "---%\n" vmtl[i]
format "-===%-\n" vmtl[i].texmap_diffuse
format "-===%-\n" vmtl[i].texmap_reflection
format "-===%-\n" vmtl[i].texmap_refraction
format "-===%-\n" vmtl[i].texmap_bump
format "-===%-\n" vmtl[i].texmap_reflectionGlossiness
format "-===%-\n" vmtl[i].texmap_refractionGlossiness
--format "-%-\n" vmtl[i].texmap_diffuse.bitmap
)
 
)

 p=getPropNames VrayMtl
format "----------line----------------------"
--show sceneMaterials

for t=1 to sceneMaterials.count do (
sm = sceneMaterials[t]
if t==1 do (
format "--%\n" sm.texmap_diffuse.bitmap 
)
)
	
*/
	
)
G_OBJ_FILEUTIL=STFileUtil()





struct STAsset (
	
	fn bitmapFN=(
		G_OBJ_UTIL.dotnetLog (" [STAsset.bitmapFN.start].... ")
		local allBitmaps = #()
		try(
			local allBitmaps1 = getClassInstances bitmapTex processChildren:True
			join allBitmaps allBitmaps1
			
		)catch(
			G_OBJ_UTIL.dotnetLog ("NO_bitmapTex")
			--G_OBJ_UTIL.dotnetLog (getcurrentException() as string)	
		)
		
		try(
			local allBitmaps2 = getClassInstances bitmapHDR processChildren:True 
			join allBitmaps allBitmaps2
		)catch(
			G_OBJ_UTIL.dotnetLog ("NO_bitmapHDR")
			--G_OBJ_UTIL.dotnetLog (getcurrentException() as string)	
		)
		
		try(
			local allBitmaps3 = getClassInstances CoronaBitmap processChildren:True 
			join allBitmaps allBitmaps3
		)catch(
			G_OBJ_UTIL.dotnetLog ("NO_CoronaBitmap")
			--G_OBJ_UTIL.dotnetLog (getcurrentException() as string)	
		)
		
		for myObj in allBitmaps do (
			local resultBitmapName=G_OBJ_FILEUTIL.analysePath myObj.filename
			if resultBitmapName!=undefined then (
				myObj.filename=resultBitmapName
				
			)
			
		)
		G_OBJ_UTIL.dotnetLog (" [STAsset.bitmapFN.end]\n")
	),
	
	fn iesFN=(
		local allInstanceArr= #()
		for mylight in lights do (
			try(
				local tempArr=#()
				InstanceMgr.GetInstances mylight &tempArr
				if findItem allInstanceArr mylight==0 then (
					format "%[not found]...\n" mylight.name
					local resultIes = G_OBJ_FILEUTIL.analysePath mylight.webfile
					if resultIes!=undefined then (
						--InstanceMgr.MakeObjectsUnique mylight #individual
						local oldIntensity = mylight.intensity
						local oldtype = mylight.type
						local olduseMultiplier =mylight.useMultiplier
						local oldmultiplier = mylight.multiplier
						mylight.webfile=resultIes
						mylight.intensity=oldIntensity
						mylight.type=oldtype
						mylight.useMultiplier =olduseMultiplier
						mylight.multiplier=oldmultiplier
						
						
					)
				)else(
					format "% [found]\n" mylight.name
				)
				if tempArr.count>0 then (
					join allInstanceArr tempArr
					
				)
			)catch()
		)
		
	try(
			local Cories = getClassInstances CoronaLight
			for i in Cories do(
				local resultIesfile=G_OBJ_FILEUTIL.analysePath i.iesFile
				if resultIesfile!=undefined then (
					i.iesFile=resultIesfile
				)
				
			)
	)catch(
			G_OBJ_UTIL.dotnetLog ("NO_CoronaIES")	
	)	
	
	),
	fn vrayFileFN = (
		G_OBJ_UTIL.dotnetLog (" [STAsset.vrayFileFN.start].... ")	
		
		
	
		try
		(
			local hdris = getClassInstances VRayHDRI
			for hd in hdris do	(
				local resultHDRIMapName=G_OBJ_FILEUTIL.analysePath hd.HDRIMapName
				if resultHDRIMapName!=undefined then (
					hd.HDRIMapName=resultHDRIMapName
					
				)
			)
		)catch(
			G_OBJ_UTIL.dotnetLog (" NO_VRayHDRI")
			--G_OBJ_UTIL.dotnetLog (getcurrentException() as string)	
		)
		
			
		try
		(
			local cams = getClassInstances VRayStereoscopic
			for cam in cams do(
				
				if  cam.enabled == true and cam.shademap_mode == 2 then(
					local resultShademapfile=G_OBJ_FILEUTIL.analysePath  cam.shademap_file
					if resultShademapfile!=undefined then (
						cam.shademap_file=resultShademapfile
					)
				)
			)
		)catch(
			G_OBJ_UTIL.dotnetLog ("NO_VRayStereoscopic")
			--G_OBJ_UTIL.dotnetLog (getcurrentException() as string)		
		)
			
		--VRayPhysicalCamera
		try(
			local cams = getClassInstances VRayPhysicalCamera
			for cam in cams do(
				if cam.distortion_type == 2 then(
					local resultLensfile=G_OBJ_FILEUTIL.analysePath  cam.lens_file
					if resultLensfile!=undefined then (
						cam.lens_file=resultLensfile
					)
				)
			)
		)catch()

		
		
		try(
			local ies = getClassInstances VRayIES
			for i in ies do(
				local resultIesfile=G_OBJ_FILEUTIL.analysePath i.ies_file
				if resultIesfile!=undefined then (
					i.ies_file=resultIesfile
				)
				
			)
		)catch(
			G_OBJ_UTIL.dotnetLog ("NO_VRayIES")
			--G_OBJ_UTIL.dotnetLog (getcurrentException() as string)		
		)
			
			
		try(
			local vrayBmpArr = getClassInstances VRayBmpFilter
			for myObj in vrayBmpArr do (
				local resultBitmapName=G_OBJ_FILEUTIL.analysePath myObj.filename
				if resultBitmapName!=undefined then (
					myObj.filename=resultBitmapName
					
				)
			)
		)catch(
			G_OBJ_UTIL.dotnetLog ("NO_VRayBmpFilter")
			--G_OBJ_UTIL.dotnetLog (getcurrentException() as string)	
		)
		
		try(
			local vrMeshArr=getclassinstances vrayproxy
			for myMesh in vrMeshArr do (
				local resultBitmapName=G_OBJ_FILEUTIL.analysePath myMesh.filename
				if resultBitmapName!=undefined then (
					myMesh.filename=resultBitmapName
					
				)
				
			)
		)catch(
			G_OBJ_UTIL.dotnetLog ("NO_vrayproxy")
			--G_OBJ_UTIL.dotnetLog (getcurrentException() as string)		
		)
		
		try(
			local vRayVolumeGridArr=getclassinstances VRayVolumeGrid
			for volumeGrid in vRayVolumeGridArr do (
				local resultVRayVolumeGrid=G_OBJ_FILEUTIL.analysePath volumeGrid.rendinput
				if resultVRayVolumeGrid!=undefined then (
					volumeGrid.rendinput=resultVRayVolumeGrid
					volumeGrid.prv_dwnsmp = 0
					volumeGrid.usrchmap = "2,density;"
				)
				
			)
		)catch(
			G_OBJ_UTIL.dotnetLog ("NO_VRayVolumeGrid")
			--G_OBJ_UTIL.dotnetLog (getcurrentException() as string)		
		)
		G_OBJ_UTIL.dotnetLog (" [STAsset.vrayFileFN.end]\n")
	),
	fn pointCacheFN=(
		G_OBJ_UTIL.dotnetLog (" [STAsset.pointCacheFN.start].... ")
		local pcArr = #()
		
		try(
			pcArr = getClassInstances  Point_Cache
		)catch(
			G_OBJ_UTIL.dotnetLog ("NO_Point_Cache")
			--G_OBJ_UTIL.dotnetLog (getcurrentException() as string)
		)
		try(
			
			local pcwsmArr =  getClassInstances Point_CacheSpacewarpModifier
			join pcArr pcwsmArr
		)catch(
			G_OBJ_UTIL.dotnetLog ("NO_Point_CacheSpacewarpModifier")
			--G_OBJ_UTIL.dotnetLog (getcurrentException() as string)
		)			
		for myFile in pcArr do (
			local resultFile=G_OBJ_FILEUTIL.analysePath myFile.filename
			if resultFile!=undefined then (
				local oldPlaybackType=undefined
				local oldPlaybackStart=undefined
				local oldPlaybackEnd=undefined
				try(
					oldPlaybackType=myFile.playbackType
					oldPlaybackStart=myFile.playbackStart
					oldPlaybackEnd=myFile.playbackEnd
				)catch()
				
				myFile.filename=resultFile
				
				try(
					myFile.playbackType=oldPlaybackType
					myFile.playbackStart=oldPlaybackStart
					myFile.playbackEnd=oldPlaybackEnd
				)catch()
				
			)
		)
		G_OBJ_UTIL.dotnetLog (" [STAsset.pointCacheFN.end]\n")
	),

-------------------------------------------------------------Alembic-------------------------------------------------st
	fn AlembicFN = (
		G_OBJ_UTIL.dotnetLog (" [Alembic_Mesh_Geometry].Start ")
		try(
			local arr = getclassinstances Alembic_Mesh_Geometry 
			for a in arr do (
				local AlembicFile = a.path
				local resultAlembicName=G_OBJ_FILEUTIL.analysePath AlembicFile
				if resultAlembicName!=undefined then (
					a.path=resultAlembicName
				)
				
			)
		)catch(
			G_OBJ_UTIL.dotnetLog ("NO_Alembic_Mesh_Geometry")
			--G_OBJ_UTIL.dotnetLog (getcurrentException() as string)	
		)
		G_OBJ_UTIL.dotnetLog (" [AlembicFN_Alembic_Mesh_Geometry].End\n")
		
		
		G_OBJ_UTIL.dotnetLog (" [AlembicFN_AlembicObject].Start ")
		try(
			local arr = getclassinstances AlembicObject
			for a in arr do (
				local AlembicFile = a.source
				local resultAlembicName=G_OBJ_FILEUTIL.analysePath AlembicFile
				if resultAlembicName!=undefined then (
					a.source=resultAlembicName
				)
				
			)
		)catch(
			G_OBJ_UTIL.dotnetLog ("NO_AlembicObject")
			--G_OBJ_UTIL.dotnetLog (getcurrentException() as string)	
		)
		G_OBJ_UTIL.dotnetLog (" [AlembicObject].End\n")
	),
-------------------------------------------------------------Alembic-------------------------------------------------end

-------------------------------------------------------------KrakatoaPRTLoader---------------------------------------st
		fn KrakatoaPRTLoaderFN = (
		G_OBJ_UTIL.dotnetLog (" [KrakatoaPRTLoader].Start ")
		try(
			local krakatoaPRTLoaderList = getclassinstances KrakatoaPRTLoader
			for myKrakatora in krakatoaPRTLoaderList do 
				(
				for ii = 1 to myKrakatora.fileList.count do 
					(
						format "a1...%\n" myKrakatora.fileList[ii]
				local PRTLoaderFile = myKrakatora.fileList[ii]
				local resultPRTLoaderName=G_OBJ_FILEUTIL.analysePath PRTLoaderFile
				if resultPRTLoaderName!=undefined then (
					myKrakatora.fileList[ii]=resultPRTLoaderName
					format "a2...%\n" myKrakatora.fileList[ii]
				)
					)
				)
		)catch(
			G_OBJ_UTIL.dotnetLog ("NO_KrakatoaPRTLoader")
			--G_OBJ_UTIL.dotnetLog (getcurrentException() as string)	
		)
		G_OBJ_UTIL.dotnetLog (" [KrakatoaPRTLoader].End\n")
		
	),
-------------------------------------------------------------KrakatoaPRTLoader---------------------------------------end
	
-------------------------------------------------------------phoenixFN-----------------------------------------------st
	fn phoenixFN = (
		
		-------------------------PHXSimulator-------------------------
		G_OBJ_UTIL.dotnetLog (" [phoenixFN_PHXSimulator].Start ")
		try(
			
			local arr = getclassinstances PHXSimulator
			for a in arr do (
				-------------------------input
				local phoenixFile = a.rendinput
				if  phoenixFile!=undefined and not (matchPattern  phoenixFile pattern:"$*" ) then(
					local resultPhoenixName=G_OBJ_FILEUTIL.analysePath phoenixFile
					if resultPhoenixName!=undefined then (
						a.rendinput=resultPhoenixName
					)
				)
				-------------------------output
				local phoenixFileOut = a.simoutput
				if  phoenixFileOut!=undefined and not (matchPattern  phoenixFileOut pattern:"$*" ) then(
					local resultPhoenixFileOut=G_OBJ_FILEUTIL.analysePath phoenixFileOut
					if resultPhoenixFileOut!=undefined then (
						a.simoutput=resultPhoenixFileOut
					)
				)
				
			)
		)catch(
			G_OBJ_UTIL.dotnetLog ("NO_PHXSimulator")
			--G_OBJ_UTIL.dotnetLog (getcurrentException() as string)	
		)
		G_OBJ_UTIL.dotnetLog (" [phoenixFN_PHXSimulator].End\n")
		
		
		-------------------------FireSmokeSim-------------------------
		G_OBJ_UTIL.dotnetLog (" [phoenixFN_FireSmokeSim].Start ")
		try(
			local arr = getclassinstances FireSmokeSim
			for a in arr do (
				-------------------------input
				local phoenixFile = a.rendinput
				if  phoenixFile!=undefined and not (matchPattern  phoenixFile pattern:"$*" ) then(
					local resultPhoenixName=G_OBJ_FILEUTIL.analysePath phoenixFile
					if resultPhoenixName!=undefined then (
						a.rendinput=resultPhoenixName
					)
				)
				
				-------------------------output
				local phoenixFileOutput = a.simoutput
				if  phoenixFileOutput!=undefined and not (matchPattern  phoenixFileOutput pattern:"$*" ) then(
					local resultPhoenixFileOutput=G_OBJ_FILEUTIL.analysePath phoenixFileOutput
					if resultPhoenixFileOutput!=undefined then (
						a.simoutput=resultPhoenixFileOutput
					)
				)
			)
		)catch(
			G_OBJ_UTIL.dotnetLog ("NO_FireSmokeSim")
			--G_OBJ_UTIL.dotnetLog (getcurrentException() as string)	
		)
		G_OBJ_UTIL.dotnetLog (" [phoenixFN_FireSmokeSim].End\n")
		
		
		-------------------------LiquidSim-------------------------
		G_OBJ_UTIL.dotnetLog (" [phoenixFN_LiquidSim].Start ")
		try(
			local arr = getclassinstances LiquidSim
			for a in arr do (
				-------------------------input
				local phoenixFile = a.simoutput
				local resultPhoenixName=G_OBJ_FILEUTIL.analysePath phoenixFile
				if resultPhoenixName!=undefined then (
					a.simoutput=resultPhoenixName
				)
				
				-------------------------output
				local phoenixFileOutput = a.simoutput
				if  phoenixFileOutput!=undefined and not (matchPattern  phoenixFileOutput pattern:"$*" ) then(
					local resultPhoenixFileOutput=G_OBJ_FILEUTIL.analysePath phoenixFileOutput
					if resultPhoenixFileOutput!=undefined then (
						a.simoutput=resultPhoenixFileOutput
					)
				)
			)
		)catch(
			G_OBJ_UTIL.dotnetLog ("NO_LiquidSim")
			--G_OBJ_UTIL.dotnetLog (getcurrentException() as string)	
		)
		G_OBJ_UTIL.dotnetLog (" [phoenixFN_LiquidSim].End\n")
	),
-------------------------------------------------------------phoenixFN-----------------------------------------------end
    
   
	 
    fn fumefxFN=(
		G_OBJ_UTIL.dotnetLog (" [fumefxFN].Start ")
		try(
			local arr = getclassinstances FumeFX
			for a in arr do(
				local defaultPath = a.GetPath "default"
				local waveletPath = a.GetPath "wavelet"
				local retimerPath = a.GetPath "retimer"
				G_OBJ_UTIL.dotnetLog (G_STCON.OUTPUT_PATH +"/" +"preview.avi")
				local previewPath=a.GetPath "preview"
				G_OBJ_UTIL.dotnetLog (previewPath)
				
				if previewPath!=undefined and previewPath!="" then (
					a.SetPath (G_STCON.OUTPUT_PATH +"/" +"preview.avi") #("preview")
				)
				
				local resultDefaultFile=G_OBJ_FILEUTIL.analysePath defaultPath
				local resultDefaultFileFolder=getFilenamePath resultDefaultFile
				if doesfileexist resultDefaultFileFolder and  resultDefaultFile!=undefined then (
					a.SetPath (resultDefaultFile+".fxd") #("default")
				)
				
				local resultWaveletFile=G_OBJ_FILEUTIL.analysePath waveletPath
				local resultWaveletFileFolder=getFilenamePath resultWaveletFile
				if doesfileexist resultWaveletFileFolder and resultWaveletFile!=undefined then(
					a.SetPath (resultWaveletFile+".fxd") #("wavelet")
					
				)
				
				local resultRetimerFile=G_OBJ_FILEUTIL.analysePath retimerPath
				local resultRetimerFileFolder=getFilenamePath resultRetimerFile
				if doesfileexist resultRetimerFileFolder and resultRetimerFile!=undefined then (
					a.SetPath (resultRetimerFile+".fxd") #("retimer")
				)
				
				
				
				
			)
			
		)catch()
		G_OBJ_UTIL.dotnetLog (" [fumefxFN].end\n")
		
	),
	
	
	fn realflowFN = (
		G_OBJ_UTIL.dotnetLog (" [realflowFN].Start ")
		
		
		try(
			local rfMeshes = getClassInstances RFMeshLoader		
			for rfMesh in rfMeshes do(
				local meshPath = rfMesh.path
				local oldstart = rfMesh.start
				local oldoffset = rfMesh.offset
				local resultMeshPath=G_OBJ_FILEUTIL.analysePath meshPath
				if resultMeshPath!=undefined then (
					if not (matchpattern resultMeshPath pattern:"*/" ignoreCase:true) then (
						resultMeshPath=resultMeshPath+"/"
					)
					G_OBJ_UTIL.dotnetLog (" [realflowFN].resultMeshPath="+resultMeshPath)
					rfMesh.path=resultMeshPath
					rfMesh.start = oldstart
					rfMesh.offset = oldoffset

				)
				
			)
		)catch	(
			G_OBJ_UTIL.dotnetLog ("NO_RFMeshLoader")	
		)
			
			
		try(
			local rfParticles = getClassInstances ParticleLoader
			if rfParticles.count > 0 and  hasProperty rfParticles[1] "binPath" then(
				for rfp in rfParticles do (
					
					local myBinPath= rfp.binPath
					local resultBinPath=G_OBJ_FILEUTIL.analysePath myBinPath
					if resultBinPath!=undefined then (
						if not (matchpattern resultBinPath pattern:"*/" ignoreCase:true) then (
							resultBinPath=resultBinPath+"/"
						)
						G_OBJ_UTIL.dotnetLog (" [NEW] "+resultBinPath)
						rfp.binPath=resultBinPath
						
					)
				)
			)
			
			
		)catch(
				G_OBJ_UTIL.dotnetLog ("NO_ParticleLoader")
		)
			
			
		try(
			
			local rfEditableMeshPaths = getClassInstances RFSoftBody
			if rfEditableMeshPaths.count>0  and  hasProperty rfEditableMeshPaths[1] "SD_Filename" then (
						
				for rfMesh in rfEditableMeshPaths do(
					local rfMeshPath = rfMesh.SD_Filename
					local resultRfMeshPath=G_OBJ_FILEUTIL.analysePath rfMeshPath
					if resultRfMeshPath!=undefined  then (
						if not (matchpattern resultRfMeshPath pattern:"*/" ignoreCase:true) then (
							resultRfMeshPath=resultRfMeshPath+"/"
						)
						G_OBJ_UTIL.dotnetLog (" [NEW] "+resultRfMeshPath)
						rfMesh.SD_Filename =resultRfMeshPath						
					)
				)
			)
			
			
		)catch(
			G_OBJ_UTIL.dotnetLog ("NO_RFSoftBody")
		)
		G_OBJ_UTIL.dotnetLog (" [realflowFN].End\n")
	),
	
	fn xmeshFN=(
		G_OBJ_UTIL.dotnetLog (" [xmeshFN].Start ")
		try(
			local cacheArr = getclassinstances XMeshLoader
			for mycache in cacheArr do (
				
				--showproperties mycache
				
				local renderSequencePath = mycache.renderSequence
				local proxySequencePath = mycache.proxySequence
				
				local resultRenderSequencePath=G_OBJ_FILEUTIL.analysePath renderSequencePath
				if resultRenderSequencePath!=undefined  then (
					mycache.renderSequence = resultRenderSequencePath
					
				)
				local resultProxySequencePath=G_OBJ_FILEUTIL.analysePath proxySequencePath
				if resultProxySequencePath!=undefined  then (
					mycache.proxySequence = resultProxySequencePath
					
				)
				
				
				
			)
		)catch()
		G_OBJ_UTIL.dotnetLog (" [xmeshFN].End\n")
	),
	
	fn runFN =(
		
		if G_STCON.VRAY_DISTRIBUTE!=undefined and G_STCON.VRAY_DISTRIBUTE=="true" then (
			
		)else(
			
			bitmapFN()
			iesFN()
			pointCacheFN()
			vrayFileFN()
			KrakatoaPRTLoaderFN()
			AlembicFN()
			phoenixFN()
			fumefxFN()
			realflowFN()
			xmeshFN()
		)
	)
	
	
)


struct STRender(
	
	
	
	fn getMyCamera=(
		
		local myCamera = getActiveCamera()
		local renderView
		try(
			if (rendUseActiveView) then ( 
				renderView = viewport.activeViewport 
			)else ( 
				renderView = rendViewIndex 
			)
			myCamera =  (viewport.getCamera index:renderView)
			G_STCON.ACTIVE_CAMERA=myCamera
			G_OBJ_UTIL.dotnetLog (" [getMyCamera]G_STCON.ACTIVE_CAMERA="+G_STCON.ACTIVE_CAMERA)
		)catch()
		
		myCamera
	),
	
	

    fn setImageInfo imageInfoArr=(
		G_OBJ_UTIL.dotnetLog ("-----get output file info-----")
		

		
		G_OBJ_UTIL.dotnetLog ("-----set output file info-----")
		if imageInfoArr!=undefined and imageInfoArr.count>0 then (
			
			if imageInfoArr[1]=="type:jpg" then (
				for imageInfo in imageInfoArr do (
					if imageInfo!=undefined and matchPattern imageInfo pattern:"quality:*" ignoreCase:true then (
						local myQuality = (substring imageInfo 9 -1) as integer
						jpeg.setQuality myQuality
						G_OBJ_UTIL.dotnetLog  ("[setImageInfo]setQuality..."+myQuality as string)
					)else if imageInfo!=undefined and matchPattern imageInfo pattern:"smooth:*" ignoreCase:true then (
						local mySmooth = (substring imageInfo 8 -1) as integer
						jpeg.setSmoothing mySmooth
						G_OBJ_UTIL.dotnetLog  ("[setImageInfo]setSmoothing..."+mySmooth as string)
					)
				)
			)else if imageInfoArr[1]=="type:bmp" then (
				for imageInfo in imageInfoArr do (
					if imageInfo!=undefined and  imageInfo=="colors:2" then (
						bmp.setType #paletted
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]BMP_setTyp 8 Bit Optimized palette"
					)else if imageInfo!=undefined and  imageInfo=="colors:8" then (
						bmp.setType #true24
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]BMP_setTyp RGB 24 bit"
					)
				)
			)else if imageInfoArr[1]=="type:png" then (
				for imageInfo in imageInfoArr do (
					if imageInfo!=undefined and  imageInfo=="colors:2" then (
						pngio.setType #paletted
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]PNG_colors Optimized palette(256)"
					)else if imageInfo!=undefined and  imageInfo=="colors:8" then (
						pngio.setType #true24
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]PNG_colors RGB 24bit(16.7Million)"
					)else if imageInfo!=undefined and  imageInfo=="colors:9" then (
						pngio.setType #true48
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]PNG_colors RGB 48 bit(281 Trillion)"
					)else if imageInfo!=undefined and  imageInfo=="colors:3" then (
						pngio.setType #gray8
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]PNG_colors Grayscale 8 bit (256)"
					)else if imageInfo!=undefined and  imageInfo=="colors:4" then (
						pngio.setType #gray16
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]PNG_colors Grayscale 16 bit (65,536)"
					)else if imageInfo!=undefined and  imageInfo=="alphachannel:1" then (
						pngio.setAlpha true
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]setAlpha_true..." 
					)else if imageInfo!=undefined and  imageInfo=="alphachannel:0" then (
						pngio.setAlpha false
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]setAlpha_false..." 
					)else if imageInfo!=undefined and  imageInfo=="interlaced:1" then (
						pngio.setInterlaced true
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]setInterlaced_true..." 
					)else if imageInfo!=undefined and  imageInfo=="interlaced:0" then (
						pngio.setInterlaced false
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]setInterlaced_false..." 
					)
				)
			)else if imageInfoArr[1]=="type:rla" then (
				for imageInfo in imageInfoArr do (
					if imageInfo!=undefined and  imageInfo=="bitsperchannel:0" then (
						rla.colorDepth =8
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]RLA.Bits per channel 8"
					)else if imageInfo!=undefined and  imageInfo=="bitsperchannel:1" then (
						rla.colorDepth =16
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]RLA.Bits per channel 16"
					)else if imageInfo!=undefined and  imageInfo=="bitsperchannel:2" then (
						rla.colorDepth =32
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]RLA.Bits per channel 32"
					)else if imageInfo!=undefined and  imageInfo=="storealphachannel:0" then (
						rla.alpha =false
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]RLA.storealphachannel false"
					)else if imageInfo!=undefined and  imageInfo=="storealphachannel:1" then (
						rla.alpha =true
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]RLA.storealphachannel true"
					)else if imageInfo!=undefined and  imageInfo=="premultalpha:0" then (
						rla.premultAlpha =false
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]RLA_premultAlpha false"
					)else if imageInfo!=undefined and  imageInfo=="premultalpha:1" then (
						rla.premultAlpha =true
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]RLA_premultAlpha true"
					)else if imageInfo!=undefined and  imageInfo=="zchannel:0" then (
						rla.zChannel =false
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]RLA_ZChannel false"
					)else if imageInfo!=undefined and  imageInfo=="zchannel:1" then (
						rla.zChannel =true
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]RLA_ZChannel true"
					)else if imageInfo!=undefined and  imageInfo=="mtlidchannel:0" then (
						rla.mtlIDChannel =false
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]RLA_MtlIDChannel false"
					)else if imageInfo!=undefined and  imageInfo=="mtlidchannel:1" then (
						rla.mtlIDChannel =true
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]RLA_MtlIDChannel true"
					)else if imageInfo!=undefined and  imageInfo=="objectidchannel:0" then (
						rla.nodeIDChannel =false
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]RLA_ObjectChannel false"
					)else if imageInfo!=undefined and  imageInfo=="objectidchannel:1" then (
						rla.nodeIDChannel =true
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]RLA_ObjectChannel true"
					)else if imageInfo!=undefined and  imageInfo=="uvchannel:0" then (
						rla.uvChannel =false
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]RLA.UVChannel false"
					)else if imageInfo!=undefined and  imageInfo=="uvchannel:1" then (
						rla.uvChannel =true
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]RLA.UVChannel true"
					)else if imageInfo!=undefined and  imageInfo=="normalchannel:0" then (
						rla.normalChannel =false
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]RLA.NormalChannel false"
					)else if imageInfo!=undefined and  imageInfo=="normalchannel:1" then (
						rla.normalChannel =true
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]RLA.NormalChannel true"
					)else if imageInfo!=undefined and  imageInfo=="non-clampedchannel:0" then (
						rla.realpixChannel =false
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]RLA.Non-ClampedChannel false"
					)else if imageInfo!=undefined and  imageInfo=="non-clampedchannel:1" then (
						rla.realpixChannel =true
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]RLA.Non-ClampedChannel true"
					)else if imageInfo!=undefined and  imageInfo=="coveragechannel:0" then (
						rla.coverageChannel =false
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]RLA.coveragechannel false"
					)else if imageInfo!=undefined and  imageInfo=="coveragechannel:1" then (
						rla.coverageChannel =true
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]RLA.coveragechannel true"
					)
				)
			)else if imageInfoArr[1]=="type:tga" then (
				for imageInfo in imageInfoArr do (
					if imageInfo!=undefined and  imageInfo=="bitsperpixel:0" then (
						Targa.setColorDepth 16
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]TGA.Image bitsperpixel 16"
					)else if imageInfo!=undefined and  imageInfo=="bitsperpixel:1" then (
						Targa.setColorDepth 24
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]TGA.Image bitsperpixel 24"
					)else if imageInfo!=undefined and  imageInfo=="bitsperpixel:2" then (
						Targa.setColorDepth 32
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]TGA.Image bitsperpixel 32"
					)else if imageInfo!=undefined and  imageInfo=="compressed:0" then (
						Targa.setCompressed false
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]TGA.compressed false"
					)else if imageInfo!=undefined and  imageInfo=="compressed:1" then (
						Targa.setCompressed true
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]TGA.compressed true"
					)else if imageInfo!=undefined and  imageInfo=="alphasplit:0" then (
						Targa.setAlphaSplit false
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]TGA.alphaSplit false"
					)else if imageInfo!=undefined and  imageInfo=="alphasplit:1" then (
						Targa.setAlphaSplit true
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]TGA.alphaSplit true"
					)else if imageInfo!=undefined and  imageInfo=="premultalpha:0" then (
						Targa.setPreMultAlpha false
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]TGA.preMultAlpha false"
					)else if imageInfo!=undefined and  imageInfo=="premultalpha:1" then (
						Targa.setPreMultAlpha true
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]TGA.preMultAlpha true"
					)
				)
			)else if imageInfoArr[1]=="type:tif" then (
				for imageInfo in imageInfoArr do (
					if imageInfo!=undefined and  imageInfo=="imagetype:0" then (
						TIF.setType #mono
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]TIF.imagetype 8-bit Greyscale"
					)else if imageInfo!=undefined and  imageInfo=="imagetype:1" then (
						TIF.setType #color
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]TIF.imagetype 8-bit Color"
					)else if imageInfo!=undefined and  imageInfo=="imagetype:2" then (
						TIF.setType #logL
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]TIF.imagetype 16-bit Color"
					)else if imageInfo!=undefined and  imageInfo=="imagetype:3" then (
						TIF.setType #logLUV
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]TIF.imagetype 16-bit SGI Logl"
					)else if imageInfo!=undefined and  imageInfo=="imagetype:4" then (
						TIF.setType #color16
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]TIF.imagetype 32-bit SGI LogLUV"
					)else if imageInfo!=undefined and  imageInfo=="compressiontype:0" then (
						TIF.setCompression #none
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]TIF.Compression Type No Compression"
					)else if imageInfo!=undefined and  imageInfo=="compressiontype:1" then (
						TIF.setCompression #packBits
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]TIF.Compression Type PackBits"
					)else if imageInfo!=undefined and  imageInfo=="storealphachannel:0" then (
						TIF.setAlpha #false
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]TIF.storealphachannel 0"
					)else if imageInfo!=undefined and  imageInfo=="storealphachannel:1" then (
						TIF.setAlpha #true
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]TIF.storealphachannel 1"
					)else if imageInfo!=undefined and  (matchpattern imageInfo pattern:"dotsperinch:*" ignoreCase:true) then (
						local dotsperinch = (substring imageInfo 13 -1) as float
						TIF.setDPI dotsperinch
						G_OBJ_UTIL.dotnetLog  ("[setImageInfo]TIF. "+ dotsperinch as string)
					)
				)
			)else if imageInfoArr[1]=="type:rpf" then (
				for imageInfo in imageInfoArr do (
					if imageInfo!=undefined and  imageInfo=="bitsperchannel:0" then (
						rpf.colorDepth =8
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]rpf.Bits per channel 8"
					)else if imageInfo!=undefined and  imageInfo=="bitsperchannel:1" then (
						rpf.colorDepth =16
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]RPF.Bits per channel 16"
					)else if imageInfo!=undefined and  imageInfo=="bitsperchannel:2" then (
						rpf.colorDepth =32
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]RPF.Bits per channel 32"
					)else if imageInfo!=undefined and  imageInfo=="storealphachannel:0" then (
						rpf.alpha =false
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]RPF.StoreAlphaChannel false"
					)else if imageInfo!=undefined and  imageInfo=="storealphachannel:1" then (
						rpf.alpha =true
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]RPF.StoreAlphaChannel true"
					)else if imageInfo!=undefined and  imageInfo=="premultalpha:0" then (
						rpf.premultAlpha =false
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]RPF.premultalpha false"
					)else if imageInfo!=undefined and  imageInfo=="premultalpha:1" then (
						rpf.premultAlpha =true
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]RPF.premultalpha true"
					)else if imageInfo!=undefined and  imageInfo=="zchannel:0" then (
						rpf.zChannel =false
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]RPF.zchannel false"
					)else if imageInfo!=undefined and  imageInfo=="zchannel:1" then (
						rpf.zChannel =true
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]RPF.zchannel true"
					)else if imageInfo!=undefined and  imageInfo=="mtlidchannel:0" then (
						rpf.mtlIDChannel =false
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]RPF.mtlidchannel false"
					)else if imageInfo!=undefined and  imageInfo=="mtlidchannel:1" then (
						rpf.mtlIDChannel =true
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]RPF.mtlidchannel true"
					)else if imageInfo!=undefined and  imageInfo=="objectidchannel:0" then (
						rpf.nodeIDChannel =false
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]RPF.objectidchannel false"
					)else if imageInfo!=undefined and  imageInfo=="objectidchannel:1" then (
						rpf.nodeIDChannel =true
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]RPF.objectidchannel true"
					)else if imageInfo!=undefined and  imageInfo=="uvchannel:0" then (
						rpf.uvChannel =false
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]RPF.uvchannel false"
					)else if imageInfo!=undefined and  imageInfo=="uvchannel:1" then (
						rpf.uvChannel =true
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]RPF.uvchannel true"
					)else if imageInfo!=undefined and  imageInfo=="normalchannel:0" then (
						rpf.normalChannel =false
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]RPF.normalchannel false"
					)else if imageInfo!=undefined and  imageInfo=="normalchannel:1" then (
						rpf.normalChannel =true
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]RPF.normalchannel true"
					)else if imageInfo!=undefined and  imageInfo=="non-clampedchannel:0" then (
						rpf.realpixChannel =false
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]RPF.non-clampedchannel false"
					)else if imageInfo!=undefined and  imageInfo=="non-clampedchannel:1" then (
						rpf.realpixChannel =true
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]RPF.non-clampedchannel true"
					)else if imageInfo!=undefined and  imageInfo=="coveragechannel:0" then (
						rpf.coverageChannel =false
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]RPF.coveragechannel false"
					)else if imageInfo!=undefined and  imageInfo=="coveragechannel:1" then (
						rpf.coverageChannel =true
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]RPF.coveragechannel true"
					)else if imageInfo!=undefined and  imageInfo=="noderenderidchannel:0" then (
						rpf.nodeRenderIDChannel =false
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]RPF.noderenderidchannel false"
					)else if imageInfo!=undefined and  imageInfo=="noderenderidchannel:1" then (
						rpf.nodeRenderIDChannel =true
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]RPF.noderenderidchannel true"
					)else if imageInfo!=undefined and  imageInfo=="colorchannel:0" then (
						rpf.colorChannel =false
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]RPF.colorchannel false"
					)else if imageInfo!=undefined and  imageInfo=="colorchannel:1" then (
						rpf.colorChannel =true
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]RPF.colorchannel true"
					)else if imageInfo!=undefined and  imageInfo=="transpchannel:0" then (
						rpf.transpChannel =false
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]RPF.transpchannel false"
					)else if imageInfo!=undefined and  imageInfo=="transpchannel:1" then (
						rpf.transpChannel =true
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]RPF.transpchannel true"
					)else if imageInfo!=undefined and  imageInfo=="velocchannel:0" then (
						rpf.velocChannel =false
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]RPF.velocchannel false"
					)else if imageInfo!=undefined and  imageInfo=="velocchannel:1" then (
						rpf.velocChannel =true
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]RPF.velocchannel true"
					)else if imageInfo!=undefined and  imageInfo=="weightchannel:0" then (
						rpf.weightChannel =false
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]RPF.weightchannel false"
					)else if imageInfo!=undefined and  imageInfo=="weightchannel:1" then (
						rpf.weightChannel =true
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]RPF.weightchannel true"
					)else if imageInfo!=undefined and  imageInfo=="maskchannel:0" then (
						rpf.maskChannel =false
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]RPF.maskchannel false"
					)else if imageInfo!=undefined and  imageInfo=="maskchannel:1" then (
						rpf.maskChannel =true
						G_OBJ_UTIL.dotnetLog  "[setImageInfo]RPF.maskchannel true"
					)
				)
			)else if imageInfoArr[1]=="type:exr" then (
				
			)
		
		)
		
		
		
		
		if G_STCON.USER_ID=="1301008" then (
			try(
				G_OBJ_UTIL.dotnetLog  "[setImageInfo]RPF.custom.1301008"
				rpf.colorDepth =16
				rpf.nodeIDChannel =true
				rpf.zChannel =true
			)catch(
				G_OBJ_UTIL.dotnetLog  "[setImageInfo]RPF.custom.1301008__exception"
			)
		)
		
		
	),
	

	fn getImageInfo=(
		local imageInfoArr = #()
		
		local rendOutputFilenameTemp=rendOutputFilename
		if rendOutputFilenameTemp!=undefined and rendOutputFilenameTemp!="" then(
			
			local outputTypeScene=getFilenametype rendOutputFilenameTemp
			local outputTypeRender=getFilenametype G_STCON.OUTPUT_NAME
			G_OBJ_UTIL.dotnetLog ("outputTypeScene="+outputTypeScene)
			G_OBJ_UTIL.dotnetLog ("outputTypeRender="+outputTypeRender)
			if outputTypeScene==outputTypeRender then (
				
				try(
					imageInfoArr=getBitmapInfoRayvision()
				)catch(
					G_OBJ_UTIL.dotnetLog (" [setImageInfo]_get output file info failed")	
				)
				G_OBJ_UTIL.dotnetLog  ("imageInfoArr___"+ (imageInfoArr as string))
			)
		)
		imageInfoArr
	),
	
	fn setMaxOutputNameFN =(
		G_OBJ_UTIL.dotnetLog (" [setMaxOutputNameFN].Start ")
		
		
		--20151001
		G_STCON.OUTPUT_FILE = (G_STCON.OUTPUT_PATH +"/" +"/"+G_STCON.OUTPUT_NAME)
		
		G_STCON.OUTPUT_SERIAL_FILE=G_STCON.OUTPUT_PATH +"/" +(getfilenamefile G_STCON.OUTPUT_NAME)+G_STCON.RENDER_FRAME_SERIAL+(getfilenametype G_STCON.OUTPUT_NAME)
		
		
		local imageInfoArr=getImageInfo()
		
		rendSaveFile=true
        if   G_STCON.MAX_QUICK_RENDER  then(
			
			rendOutputFilename=G_STCON.OUTPUT_SERIAL_FILE
		)else(
            rendOutputFilename=G_STCON.OUTPUT_FILE
        )
		
		setImageInfo imageInfoArr
		
		
		if G_STCON.USER_ID=="964684" or G_STCON.USER_ID=="962712"  then (
				G_OBJ_UTIL.dotnetLog (" [run].customScript ")
				if matchPattern G_STCON.OUTPUT_NAME pattern:"*.exr" then (
					G_OBJ_UTIL.dotnetLog (" [runFN].Exr")
					fopenexr.setLayerOutputFormat 0 1
					fopenexr.setLayerOutputType 0 0 
					fopenexr.SetCompression 3
					fopenexr.setSaveScanline true
					fopenexr.setSaveRegion false

					fopenexr.delAllGBufferLayers()
					fopenexr.addGBufferChannelLayer 0 "zDepth" 2 1
					fopenexr.addGBufferChannelLayer 11 "Velocity" 3 1
				
				
					G_OBJ_UTIL.dotnetLog (" [runFN].Exr_setAutoAddRenderElements ")
					fopenexr.setAutoAddRenderElements true
					/*
					if fopenexr.isAutoAddRenderElements() then (
						G_OBJ_UTIL.dotnetLog (" [runFN].Exr_Elements_xxx ")
						G_STCON.ELEM_TYPE="xxx"
					)
					*/
				)
				
			) else if  G_STCON.USER_ID=="120106" or  G_STCON.USER_ID=="1822156"  or G_STCON.USER_ID=="965342" then (
				G_OBJ_UTIL.dotnetLog (" [run].customScript ")
				if matchPattern G_STCON.OUTPUT_NAME pattern:"*.exr" then (
					G_OBJ_UTIL.dotnetLog (" [runFN].Exr")
					
				
				
					G_OBJ_UTIL.dotnetLog (" [runFN].Exr_setAutoAddRenderElements ")
					fopenexr.setAutoAddRenderElements true
					/*
					if fopenexr.isAutoAddRenderElements() then (
						G_OBJ_UTIL.dotnetLog (" [runFN].Exr_Elements_xxx ")
						G_STCON.ELEM_TYPE="xxx"
					)
					*/
				)
				
			) else if  G_STCON.USER_ID=="1814686"  then (
				G_OBJ_UTIL.dotnetLog (" [run].customScript ")
				if matchPattern G_STCON.OUTPUT_NAME pattern:"*.exr" then (
					G_OBJ_UTIL.dotnetLog (" [1814686_runFN].Exr")
					
                    fopenexr.setLayerOutputFormat 0 2
				)
				
			)else if  G_STCON.USER_ID=="962276" or  G_STCON.USER_ID=="1841984"  then (
				G_OBJ_UTIL.dotnetLog (" [run].customScript ")
				if matchPattern G_STCON.OUTPUT_NAME pattern:"*.exr" then (
					G_OBJ_UTIL.dotnetLog (" [runFN].962276_1841984_Exr")
					
				
				
					G_OBJ_UTIL.dotnetLog (" [runFN].Exr_setAutoAddRenderElements ")
					fopenexr.setAutoAddRenderElements true
					
				)
				
			)else if  G_STCON.USER_ID=="961404"  then (
				G_OBJ_UTIL.dotnetLog (" [run].customScript ")
				if matchPattern G_STCON.OUTPUT_NAME pattern:"*.exr" then (
					G_OBJ_UTIL.dotnetLog (" [runFN].961404EXR")
					
					fopenexr.setLayerOutputFormat 0 1
					fopenexr.setLayerOutputType 0 0 
					fopenexr.SetCompression 3
					fopenexr.setSaveScanline true
				
					
				)
				
			)else(
				G_OBJ_UTIL.dotnetLog (" [run].customScript ")
				if matchPattern G_STCON.OUTPUT_NAME pattern:"*.exr" then (
					fopenexr.setAutoAddRenderElements false
					
				)
			)
		
		G_OBJ_UTIL.dotnetLog (" [setMaxOutputNameFN].G_STCON.OUTPUT_FILE="+G_STCON.OUTPUT_FILE)
		G_OBJ_UTIL.dotnetLog (" [setMaxOutputNameFN].End\n")
		outPath
	),
	
	fn elementFN =(
		G_OBJ_UTIL.dotnetLog (" [elementFN].Start ")
		
		if G_STCON.ELEM_TYPE==undefined or G_STCON.ELEM_TYPE=="" then (
			G_STCON.ELEM_TYPE="tga"
		)
		re = maxOps.GetCurRenderElementMgr() 
		theManager = maxOps.GetRenderElementMgr #Production
		theManager.SetDisplayElements false
		--20151001
		if G_STCON.ELEMENT_ACTIVE=="on" or G_STCON.ELEMENT_ACTIVE=="true" then(
			re.SetElementsActive true
			for n = 0 to (theManager.numrenderelements()- 1) do(
			
				local el = re.getrenderelement n	
				el.enabled=true
				local elName = re.GetRenderElementFilename n
				local elType = el.elementname
				
				local resultName = ""
				if elName==undefined or elName=="" then(				
					resultName = elType+"_"+G_STCON.RENDER_FRAME_SERIAL+"."+G_STCON.ELEM_TYPE
				)else(	
					local elBasename = getFilenameFile elname
					resultName = elBasename +"_"+G_STCON.RENDER_FRAME_SERIAL+ "."+G_STCON.ELEM_TYPE
				)
				re.SetRenderElementFilename n (G_STCON.OUTPUT_PATH +"/" + resultName )
				
			)
		)else(
			re.SetElementsActive false
		)
			
		
		
		
		
		G_OBJ_UTIL.dotnetLog (" [elementFN].End\n")
	),
	

	fn commonFN=(--run after load max file
		G_OBJ_UTIL.dotnetLog (" [commonFN].Start ")
		
		/*
		if (maxversion())[1] >= 16000 then(--is and more then 2014
			if G_STCON.MAX_GAMMA!=undefined and G_STCON.MAX_GAMMA=="on" then (
					IDisplayGamma.colorCorrectionMode == #gamma
					IDisplayGamma.gamma=G_STCON.MAX_GAMMAVAL as float
					fileInGamma=G_STCON.MAX_INGAMMA as float
					fileOutGamma=G_STCON.MAX_GAMMAVAL as float
					
			)else(
					IDisplayGamma.colorCorrectionMode == #none
			)
		
		)*/
		
		
		renderWidth = G_STCON.MYWIDTH as integer
		renderHeight= G_STCON.MYHEIGHT as integer
		
		try(
			G_OBJ_UTIL.dotnetLog (" [commonFN].BitmapProxyMgr.start ")
		
			BitmapProxyMgr.globalProxyEnable=false
			G_OBJ_UTIL.dotnetLog (" [commonFN].BitmapProxyMgr.end\n")
		
		)catch(
			G_OBJ_UTIL.dotnetLog (" [commonFN].BitmapProxyMgrexception ")
			G_OBJ_UTIL.dotnetLog (getcurrentexception() as string)
		)
		
		try(
			G_OBJ_UTIL.dotnetLog (" [commonFN].IBitmapPager.start ")
		
			IBitmapPager.enabled=false
			G_OBJ_UTIL.dotnetLog (" [commonFN].IBitmapPager.end\n")
		
		)catch(
			G_OBJ_UTIL.dotnetLog (" [commonFN].IBitmapPagerexception ")
			G_OBJ_UTIL.dotnetLog (getcurrentexception() as string)
		)
		
		G_OBJ_UTIL.dotnetLog (" [commonFN].End\n")
		
		
	),
	
	fn photonOption=(
		rendSaveFile=false
		G_STCON.RENDERER_OBJECT.options_dontRenderImage=true
		G_STCON.RENDERER_OBJECT.gi_irradmap_showCalcPhase=true
		G_STCON.RENDERER_OBJECT.gi_primary_type=G_STCON.VRAY_PRIMARY_GIENGINE as integer
		G_STCON.RENDERER_OBJECT.gi_secondary_type=G_STCON.VRAY_SECONDARY_GIENGINE as integer
		
	
				
		if G_STCON.PHOTON_DISPLACEMENT=="1" then (
			G_STCON.RENDERER_OBJECT.options_displacement=true
		)else(
			G_STCON.RENDERER_OBJECT.options_displacement=false
		)
		if G_STCON.PHOTON_REFLE_REFRA=="1" then (
			G_STCON.RENDERER_OBJECT.options_reflectionRefraction=true
		)else(
			G_STCON.RENDERER_OBJECT.options_reflectionRefraction=false
		)
		--20151001
		G_STCON.RENDERER_OBJECT.imageSampler_type=G_STCON.VRAY_IMAGE_SAMPLE_TYPE as integer
		if G_STCON.VRAY_FILTER_ON=="true" then (
			G_STCON.RENDERER_OBJECT.filter_on=true
		)else(
			G_STCON.RENDERER_OBJECT.filter_on=false
		)
		
		if G_STCON.VRAY_FILTER_KERNEL!=undefined and G_STCON.VRAY_FILTER_KERNEL!="" then (
			
			G_OBJ_UTIL.dotnetLog (" filter_kernel= "+G_STCON.VRAY_FILTER_KERNEL)
			local clientfilter=G_STCON.VRAY_FILTER_KERNEL
			if clientfilter ==	"Area"	then(	
				renderers.production.filter_kernel =	Area()
			)else if clientfilter ==	"Sharp Quadratic" 	then(	
				renderers.production.filter_kernel =	Sharp_Quadratic()
			)else if clientfilter ==	"Catmull-Rom"	then(	
				renderers.production.filter_kernel =	Catmull_Rom()
			)else if clientfilter ==	"Plate Match/MAX R2"	then(	
				renderers.production.filter_kernel =	Plate_Match_MAX_R2()
			)else if clientfilter ==	"Quadratic"	then(	
				renderers.production.filter_kernel =	Quadratic()
			)else if clientfilter ==	"cubic"	then(	
				renderers.production.filter_kernel =	cubic()
			)else if clientfilter ==	"Video"	then(	
				renderers.production.filter_kernel =	Video()
			)else if clientfilter ==	"Soften"	then(	
				renderers.production.filter_kernel =	Soften()
			)else if clientfilter ==	"Cook Variable"	then(	
				renderers.production.filter_kernel =	Cook_Variable()
			)else if clientfilter ==	"Blend"	then(	
				renderers.production.filter_kernel =	Blendfilter()
			)else if clientfilter ==	"Blackman"	then(	
				renderers.production.filter_kernel =	Blackman()
			)else if clientfilter ==	"Mitchell-Netravali"	then(	
				renderers.production.filter_kernel =	Mitchell_Netravali()
			)else if clientfilter ==	"VRayLanczosFilter" 	then(	
				renderers.production.filter_kernel =	VRayLanczosFilter()
			)else if clientfilter ==	"VRaySincFilter"	then(	
				renderers.production.filter_kernel =	VRaySincFilter()
			)else if clientfilter ==	"VRayBoxFilter"	then(	
				renderers.production.filter_kernel =	VRayBoxFilter()
			)else if clientfilter ==	"VRayTriangleFilter"	then(	
				renderers.production.filter_kernel =	VRayTriangleFilter()

			)
			
			--execute  ("renderers.production.filter_kernel= "+ myfileter+"()")
			--execute  ("renderers.production.filter_kernel= "+ G_STCON.VRAY_FILTER_KERNEL+"()")
		)
			
		
	),
	
	fn flyThrough=(
		if G_STCON.VRAY_LIGHTCACHE_MODE=="1" or G_STCON.IS_PICTURE=="true" then (--Fly-through
			G_OBJ_UTIL.dotnetLog (" lightcache_flyThrough ")
			G_STCON.RENDERER_OBJECT.lightcache_mode=1
			G_STCON.RENDERER_OBJECT.lightcache_autoSave=true
			G_STCON.RENDERER_OBJECT.lightcache_autoSaveFileName=G_STCON.OUTPUT_PATH +"/"+G_STCON.TASK_ID+"_lightcache.vrlmap"
		)
		
	),
	
	fn flyThroughFromFile=(
		if G_STCON.VRAY_LIGHTCACHE_MODE=="1"  or G_STCON.IS_PICTURE=="true" then (--Fly-through convert to from file
			G_OBJ_UTIL.dotnetLog (" lightcache_from file ")
			G_STCON.RENDERER_OBJECT.lightcache_mode=2
			G_STCON.RENDERER_OBJECT.lightcache_loadFileName=G_STCON.PHOTON_PATH+G_STCON.TASK_ID+"_lightcache.vrlmap"
		)
		
	),
	
	fn vrayFN = (
		
		G_OBJ_UTIL.dotnetLog (" [vrayFN].Start ")
		
		
		if G_STCON.VRAY_DISTRIBUTE!=undefined and G_STCON.VRAY_DISTRIBUTE=="true" then (
			G_STCON.RENDERER_OBJECT.system_distributedRender=true
		)
		
		
		try(
				--G_STCON.RENDERER_OBJECT.system_vrayLog_show=true
				--G_STCON.RENDERER_OBJECT.system_vrayLog_level=4
				--G_STCON.RENDERER_OBJECT.system_vrayLog_file=@"c:/vraylog.txt"
				memLimit_USER = G_STCON.RENDERER_OBJECT.system_raycaster_memLimit
				if memLimit_USER<16000 then 
				(
						sysIN=sysinfo.getSystemMemoryInfo()
						s_N =((sysIN[3] /= (1024.*1024.)) as integer) as string
						sysout=(replace s_N 2 4 "0000") as integer
						if sysout > 30000 then
						(	
						G_STCON.RENDERER_OBJECT.system_raycaster_memLimit = sysout-18000
						NEW_NCs=G_STCON.RENDERER_OBJECT.system_raycaster_memLimit
						G_OBJ_UTIL.dotnetLog ("------"+"New_dynamic memory limit:"+NEW_NCs as string +"MB------")			
						)
						else
						(
						G_STCON.RENDERER_OBJECT.system_raycaster_memLimit =16000
						NEW_NC=G_STCON.RENDERER_OBJECT.system_raycaster_memLimit
						G_OBJ_UTIL.dotnetLog ("------"+"New_dynamic memory limit:"+NEW_NC as string +"MB------")

						)
				)	
				else()	
			RaytraceGlobalSettings.showMessages = false
		)catch()

		try(
			
			if G_STCON.RENDERER_OBJECT.system_region_x <= 32 then (
				G_OBJ_UTIL.dotnetLog ("------System region------48")
				G_STCON.RENDERER_OBJECT.system_region_x = G_STCON.RENDERER_OBJECT.system_region_y = 48
				G_STCON.RENDERER_OBJECT.system_region_sequence = 0
				G_STCON.RENDERER_OBJECT.system_region_meaning = 0	
			)
			
		)catch()

		G_STCON.RENDERER_OBJECT.output_width = G_STCON.MYWIDTH as integer
		G_STCON.RENDERER_OBJECT.output_height = G_STCON.MYHEIGHT as integer
		
		G_STCON.RENDERER_OBJECT.options_dontRenderImage=false
		
		if G_STCON.CUSTOM_CLIENT!=undefined and G_STCON.CUSTOM_CLIENT=="yunwu" then (
			try(
				G_STCON.RENDERER_OBJECT.camera_type=1
				G_STCON.RENDERER_OBJECT.camera_overrideFOV=true
				G_STCON.RENDERER_OBJECT.camera_fov=360.0
				
				G_STCON.RENDERER_OBJECT.camera_cyl_height=400.0
				G_STCON.RENDERER_OBJECT.camera_fish_autoDistance=true
				G_STCON.RENDERER_OBJECT.camera_fish_distance=2.0
				G_STCON.RENDERER_OBJECT.camera_fish_curve=1.0
			)catch()
		)
		
		--------------------------------vfb-----------------------------
		local enableFrameBuffer = G_STCON.RENDERER_OBJECT.output_on
		local renderToRwFile = G_STCON.RENDERER_OBJECT.output_saveRawFile			
		local splitBuffer = G_STCON.RENDERER_OBJECT.output_splitgbuffer
		if(enableFrameBuffer==true) then (--vray frame buffer
			local outputRawFile = G_STCON.RENDERER_OBJECT.output_rawFileName
			if renderToRwFile==true and outputRawFile!=undefined and outputRawFile!=""  then (					
				local outputRawFileT = getFilenameType outputRawFile
				local outputRawFileN = getFileNameFile outputRawFile
				G_STCON.RENDERER_OBJECT.output_rawFileName =G_STCON.OUTPUT_PATH +"/" + outputRawFileN + outputRawFileT
			)
				
			local splitFileName = G_STCON.RENDERER_OBJECT.output_splitfilename
			if splitBuffer==true and splitFileName!=undefined and splitFileName != "" then (					
				local splitFileT = getFilenameType splitFileName
				local splitFileN = getFileNameFile splitFileName					
				G_STCON.RENDERER_OBJECT.output_splitfilename = G_STCON.OUTPUT_PATH +"/" + splitFileN + splitFileT
				
			)
            try(
				rendShowVFB=FALSE
			)catch()
            
		)else(
			try(
				G_STCON.RENDERER_OBJECT.output_saveRawFile=false		
				G_STCON.RENDERER_OBJECT.output_splitgbuffer=false
			)catch()
            try(
				rendShowVFB=TRUE
			)catch()
		)
		
		
		if G_STCON.MYKG=="0"  then (
			
			if G_STCON.VRAY_GI=="on" or G_STCON.VRAY_GI=="true" or G_STCON.VRAY_GI=="1" then (
				G_STCON.RENDERER_OBJECT.gi_primary_type=G_STCON.VRAY_PRIMARY_GIENGINE as integer
				G_STCON.RENDERER_OBJECT.gi_secondary_type=G_STCON.VRAY_SECONDARY_GIENGINE as integer
				
				if G_STCON.VRAY_IRRADIANCEMAP_MODE!=undefined and G_STCON.VRAY_IRRADIANCEMAP_MODE!="" then (
					G_STCON.RENDERER_OBJECT.adv_irradmap_mode=G_STCON.VRAY_IRRADIANCEMAP_MODE as integer
				)
				if G_STCON.VRAY_LIGHTCACHE_MODE!=undefined and G_STCON.VRAY_LIGHTCACHE_MODE!="" then (
					G_STCON.RENDERER_OBJECT.lightcache_mode=G_STCON.VRAY_LIGHTCACHE_MODE as integer
				)
				
				if G_STCON.RENDERER_OBJECT.lightcache_mode==1 then (
					G_STCON.RENDERER_OBJECT.lightcache_autoSave=true
					G_STCON.RENDERER_OBJECT.lightcache_autoSaveFileName=G_STCON.OUTPUT_PATH +"/"+G_STCON.TASK_ID+"_lightcache.vrlmap"
				)
				
				local irrLoadFileInscenePath=G_OBJ_FILEUTIL.analysePath G_STCON.VRAY_IRRMAP_FILE
				if G_STCON.RENDER_WORK!=undefined and irrLoadFileInscenePath!=undefined then (
					G_STCON.RENDERER_OBJECT.adv_irradmap_loadFileName=G_STCON.RENDER_WORK+(filenameFromPath irrLoadFileInscenePath)
					
				)
				local ligLoadFileInscenePath=G_OBJ_FILEUTIL.analysePath G_STCON.VRAY_LIGHTCACHE_FILE
				if G_STCON.RENDER_WORK!=undefined and ligLoadFileInscenePath!=undefined then (
					G_STCON.RENDERER_OBJECT.lightcache_loadFileName=G_STCON.RENDER_WORK+(filenameFromPath ligLoadFileInscenePath)
					
				)
				
			)
			else if G_STCON.VRAY_GI=="off" or G_STCON.VRAY_GI=="false" or G_STCON.VRAY_GI=="0" then(
				G_STCON.RENDERER_OBJECT.gi_on = false
			)
			
		)else if G_STCON.MYKG=="100" then (--incremental add to current map
			G_STCON.RENDERER_OBJECT.gi_on=True 
			--if  G_STCON.MYCURRENTTASK=="photon"  then (
            if G_STCON.MY_ACTION=="RenderPhoton" then (
				G_STCON.RENDERER_OBJECT.adv_irradmap_mode=4
				G_STCON.RENDERER_OBJECT.adv_irradmap_autoSave=true
				G_STCON.RENDERER_OBJECT.adv_irradmap_autoSaveFileName=G_STCON.OUTPUT_PATH +"/"+G_STCON.TASK_ID+"_irrmap.vrmap"
				
				photonOption()
				flyThrough()
				
			)else(
				G_STCON.RENDERER_OBJECT.adv_irradmap_mode=2
				G_STCON.RENDERER_OBJECT.adv_irradmap_loadFileName=G_STCON.PHOTON_PATH+G_STCON.TASK_ID+"_irrmap.vrmap"
				flyThroughFromFile()
				
			)
			
		) else if G_STCON.MYKG=="101" then (--animation (prepass) rend map
			G_STCON.RENDERER_OBJECT.gi_on=True 
			--if  G_STCON.MYCURRENTTASK=="photon"  then (
            if G_STCON.MY_ACTION=="RenderPhoton" then (
				G_STCON.RENDERER_OBJECT.adv_irradmap_mode=6
				G_STCON.RENDERER_OBJECT.adv_irradmap_autoSave=true
				G_STCON.RENDERER_OBJECT.adv_irradmap_autoSaveFileName=G_STCON.OUTPUT_PATH +"/"+G_STCON.TASK_ID+"_animation.vrmap"
				
				photonOption()
				flyThrough()
			)else(
				G_STCON.RENDERER_OBJECT.adv_irradmap_mode=7
				G_STCON.RENDERER_OBJECT.adv_irradmap_loadFileName=G_STCON.PHOTON_PATH+G_STCON.TASK_ID+"_animation.vrmap"
				flyThroughFromFile()
			)
		
			
		) else if  G_STCON.MYKG=="102" then (--fast rend map
			G_STCON.RENDERER_OBJECT.gi_on=True 
			--if  G_STCON.MYCURRENTTASK=="photon"  then (
            if G_STCON.MY_ACTION=="RenderPhoton" then (
				G_STCON.RENDERER_OBJECT.adv_irradmap_autoSave=true
				G_STCON.RENDERER_OBJECT.adv_irradmap_mode=4
				G_STCON.RENDERER_OBJECT.adv_irradmap_autoSaveFileName=G_STCON.OUTPUT_PATH +"/"+G_STCON.TASK_ID+"_irrmap"+ G_STCON.RENDER_FRAME_SERIAL+".vrmap"
				photonOption()
				flyThrough()
			)else(
				G_STCON.RENDERER_OBJECT.adv_irradmap_mode=2
				G_STCON.RENDERER_OBJECT.adv_irradmap_loadFileName=G_STCON.PHOTON_PATH+G_STCON.TASK_ID+"_irrmap.vrmap"
				flyThroughFromFile()
			)
		
			
		)			
		
		

		G_OBJ_UTIL.dotnetLog (" [vrayFN].End\n")
	),
	

	
	fn rendererFN=(
		
		if (G_STCON.RENDERER_STR == (vray as string)) then (
			vrayFN()
		) else if (G_STCON.RENDERER_STR == (default_scanline_renderer as string)) then (
			
		) else if G_STCON.RENDERER_STR == (finalRender_stage_1 as string) then (
			--finalRenderFN()
		) else if (G_STCON.RENDERER_STR == (MaxwellRenderer as string)) then (
			
		) else if (G_STCON.RENDERER_STR == (mental_ray_renderer as string)) then (
			
		) else if (G_STCON.RENDERER_STR == (mental_ray_iray_Renderer as string)) then (
			
		) else if (G_STCON.RENDERER_STR == (Quicksilver_Hardware_Renderer as string)) then (
			
		) 
		
		
	),
	
	

	
	fn saveExrToJpg myBitmap=(
		
		try(
			local myBitmapName=myBitmap.filename
			local bitmapType = getFilenameType myBitmapName
			
			if bitmapType==".exr" then (
				
				if (maxversion())[1] < 16000 then(--2013,2012,2011,2010
					if G_STCON.MAX_GAMMA!=undefined and G_STCON.MAX_GAMMA=="on" and G_STCON.MAX_OUTGAMMA!=undefined then (
						myBitmap.gamma=G_STCON.MAX_OUTGAMMA as float
					)
				
				)
				local bitmapFileBaseName=getFilenameFile myBitmapName
				local exrToJpgDir=G_OBJ_UTIL.replaceFN G_STCON.OUTPUT_PATH +"/" "output" "exr2jpg"
				makedir exrToJpgDir all:true
				exrToJpg=exrToJpgDir+bitmapFileBaseName+bitmapType+".jpg"
				myBitmap.filename=exrToJpg
				save myBitmap --frame:(G_STCON.RENDER_FRAME as integer) 
			)
		)catch(
			G_OBJ_UTIL.dotnetLog "[saveExrToJpg].save exr failed"
			G_OBJ_UTIL.dotnetLog (getcurrentException() as string)
		)
	),
	
	/*
	fn analyseRenderFrame=(
		local myStartFrame = undefined 
		local myEndFrame=undefined 
		local myByFrame=undefined
		if G_STCON.RENDER_FRAME !=undefined then (
			local frameArr1 = filterString G_STCON.RENDER_FRAME  "-"
			if frameArr1!=undefined and frameArr1.count==2 then (--11-113[6]
				myStartFrame=frameArr1[1]
				
				local frameArr2 = filterString frameArr1[2] "["
				
				if frameArr2!=undefined and frameArr2.count==2 then (
					myEndFrame=frameArr2[1]
					
					myByFrame=G_OBJ_UTIL.replaceFN frameArr2[2] "]" ""
					
				)else if frameArr2!=undefined and frameArr2.count==1 then (--11-113
					myEndFrame=frameArr2[1]
					
					myByFrame="1"
				)
				
			)
		)
		local frameArr=#()
		if myStartFrame!=undefined and myEndFrame!=undefined and myByFrame!=undefined then(--kg=100
			append frameArr myStartFrame
			append frameArr myEndFrame
			append frameArr myByFrame
		)
		frameArr
	),
	*/

	fn calcRegion  =(
		G_OBJ_UTIL.dotnetLog (" [calcRegion].Start ")
		local sqrtBlock=(sqrt G_STCON.TOTAL_BLOCK) as integer
		local blockWidth=(G_STCON.MYWIDTH as integer)/sqrtBlock
		local blockHeight=(G_STCON.MYHEIGHT as integer)/sqrtBlock
		
		G_OBJ_UTIL.dotnetLog (" [calcRegion].sqrtBlock= "+(sqrtBlock as string))
		G_OBJ_UTIL.dotnetLog (" [calcRegion].blockWidth= "+(blockWidth as string))
		G_OBJ_UTIL.dotnetLog (" [calcRegion].blockHeight= "+(blockHeight as string))
		
		local row=G_STCON.BLOCK_NUMBER/sqrtBlock
		local col=(mod G_STCON.BLOCK_NUMBER sqrtBlock) as integer
		
		local leftTopX=col*blockWidth
		local leftTopY=row*blockHeight
		local rightBottomX=(col+1)*blockWidth+G_STCON.OVER_LAP
		local rightBottomY=(row+1)*blockHeight+G_STCON.OVER_LAP
		local str = " [calcRegion]["+(row as string)+","+(col as string)+"] ("+(leftTopX as string)+","+(leftTopY as string)+","+(rightBottomX as string)+","+(rightBottomY as string)+")"
		G_OBJ_UTIL.dotnetLog (str)
		G_STCON.REGION_ARR=#(leftTopX,leftTopY,rightBottomX,rightBottomY)
		G_OBJ_UTIL.dotnetLog (" [calcRegion].end\n")
	),
    
    fn saveOutputGamma=(
        if (maxversion())[1] < 16000 then(--2013,2012,2011,2010
			--(getfilenametype G_STCON.OUTPUT_NAME)
			format "111...\n"
			if not (matchPattern G_STCON.OUTPUT_NAME pattern:"*.tif" ignoreCase:true) then (
			format "1112...\n"
				if G_STCON.MAX_GAMMA!=undefined and (G_STCON.MAX_GAMMA=="on" or G_STCON.MAX_GAMMA=="gamma" )and G_STCON.MAX_OUTGAMMA!=undefined then (
					G_OBJ_UTIL.dotnetLog (" [renderExecuteFN].gammaStart ")
					format "1113...\n"
					try(
						G_OBJ_UTIL.dotnetLog (" [renderExecuteFN].setgamma")
						local bm=openBitMap G_STCON.OUTPUT_SERIAL_FILE
						local bmm = copy bm
						format "1114...\n"
						bmm.filename=G_STCON.OUTPUT_SERIAL_FILE
						bmm.gamma=G_STCON.MAX_OUTGAMMA as float
						save bmm
					)catch(
						G_OBJ_UTIL.dotnetLog (getcurrentException() as string)	
					)
					G_OBJ_UTIL.dotnetLog (" [renderExecuteFN].GammaEnd ")
				)
			)
			
			
		)
		
    ),
	
	fn renderExecuteFN=(
		
		G_OBJ_UTIL.dotnetLog (" [renderExecuteFN].Start ")

		/*
		rla.alpha=true
		rla.premultAlpha=true
		rla.zChannel=true
		rla.mtlIDChannel=true
		rla.nodeIDChannel=true
		rla.uvChannel=true
		rla.normalChannel=true
		rla.realpixChannel=true
		rla.coverageChannel=true
		*/
		
		/*
		
		/*
			0. #zDepth 
			1. #matID 
			2. #objectID 
			3. #UVCoords 
			4. #normal 
			5. #unClamped 
			6. #coverage 
			7. #node 
			8. #mask 
			9. #shaderColor 
			10. #shaderTransparency 
			11. #velocity 
			12. #weight 

			fopenexr.addGBufferChannelLayer 6 "Coverage" 2 2
			fopenexr.addGBufferChannelLayer 2 "Object ID" 2 2
			fopenexr.addGBufferChannelLayer 11 "Velocity" 4 0

		*/
		
		
		/*
		global REND_START_FRAME=undefined
		global REND_END_FRAME=undefined
		global REND_BY_FRAME=undefined
		*/
		local elemArr=#()
		
		
		global myRenderCamera=undefined
		G_OBJ_UTIL.dotnetLog (" [renderExecuteFN].myRenderCamera__ ")
		for c in cameras do (
			local cameraNameStr=trimright (trimleft c.name)
			G_OBJ_UTIL.dotnetLog (" [renderExecuteFN].cameraNameStr__ "+cameraNameStr)
			if (classof c)!=Targetobject and cameraNameStr==G_STCON.RENDERABLE_CAMERA then (
				try(
                    --viewport.ResetAllViews() 
                    viewport.setCamera c
					
					
					local viewId=viewport.activeViewport
	
					local viewType =viewport.getType index:viewId --viewport.getType()
					G_OBJ_UTIL.dotnetLog ("ViewPort="+(viewId as string)+"..."+(viewType as string))
                )catch()
                myRenderCamera=c
			)
			
		)
		G_OBJ_UTIL.dotnetLog (" [renderExecuteFN].myRenderCamera... "+(myRenderCamera as string))
		
		local renderCmd="render quiet:true    outputwidth:(G_STCON.MYWIDTH as number) outputheight:(G_STCON.MYHEIGHT as number) outputfile:G_STCON.OUTPUT_SERIAL_FILE "
		
		-----------frame
		if G_STCON.RENDER_FRAME_START==G_STCON.RENDER_FRAME_END then(
			renderCmd=renderCmd+" frame:(G_STCON.RENDER_FRAME as time) "
			try(-----------sliderTime
				sliderTime=(G_STCON.RENDER_FRAME as time)
			)catch()
		)else(
			renderCmd=renderCmd+" fromframe:(G_STCON.RENDER_FRAME_START as time)  toframe:(G_STCON.RENDER_FRAME_END as time)  nthframe:(G_STCON.RENDER_FRAME_BY as time) "
		)
		/*
		local frameArr=analyseRenderFrame()
		if frameArr.count>0 then (--
			REND_START_FRAME=frameArr[1]
			REND_END_FRAME=frameArr[2]
			REND_BY_FRAME=frameArr[3]
			renderCmd=renderCmd+" fromframe:(REND_START_FRAME as time)  toframe:(REND_END_FRAME as time)  nthframe:(REND_BY_FRAME as time) "
		)else(
			renderCmd=renderCmd+" frame:(G_STCON.RENDER_FRAME as time) "
		)
		*/
		
		-----------camera
		if myRenderCamera!=undefined then (
			renderCmd=renderCmd+" camera:myRenderCamera"
		)
		
		G_OBJ_UTIL.dotnetLog (" [renderExecuteFN].RenderType... "+(getRenderType() as string))
		local myRenderType=toLower (getRenderType() as string)
		----------------block
		if G_STCON.TOTAL_BLOCK>1 then(
			calcRegion()
			renderCmd=renderCmd+" renderType:#regionCrop region:G_STCON.REGION_ARR "
		)else(
			
			if myRenderType=="region" then (
				renderCmd=renderCmd+" renderType:#region "
			)else if myRenderType =="selected" then(
				renderCmd=renderCmd+" renderType:#selected "
			)
			else if myRenderType =="selection" then (
				renderCmd=renderCmd+" renderType:#selection "
			)else if myRenderType =="blowup" then (
				renderCmd=renderCmd+" renderType:#blowup "
			)else if myRenderType =="crop" then (
				renderCmd=renderCmd+" renderType:#crop "
			)
		)
		-----------elements
		--if (G_STCON.MYKG=="100" or G_STCON.MYKG=="101" or G_STCON.MYKG=="102" ) and G_STCON.MYCURRENTTASK=="photon" then (--incremental add to current map
        if (G_STCON.MYKG=="100" or G_STCON.MYKG=="101" or G_STCON.MYKG=="102" ) and G_STCON.MY_ACTION=="RenderPhoton" then (--incremental add to current map
			
		)else(
			
		)
		
		
		if G_STCON.USER_ID=="961404"  then (
			renderCmd=renderCmd+" outputHDRbitmap:true "
		)
		
		-----------execute
		G_OBJ_UTIL.dotnetLog (" [renderExecuteFN].rendercmd___"+renderCmd)
		if G_STCON.NOT_RENDER=="true" then (
			
		)else(
			execute(renderCmd)
		)
		
		G_OBJ_UTIL.dotnetLog (" [renderExecuteFN].End\n")
		
        saveOutputGamma()
        
        /*
		if (maxversion())[1] < 16000 then(--2013,2012,2011,2010
			--(getfilenametype G_STCON.OUTPUT_NAME)
			if not (matchPattern G_STCON.OUTPUT_NAME pattern:"*.tif" ignoreCase:true) then (
			
				if G_STCON.MAX_GAMMA!=undefined and G_STCON.MAX_GAMMA=="on" and G_STCON.MAX_OUTGAMMA!=undefined then (
					G_OBJ_UTIL.dotnetLog (" [renderExecuteFN].gammaStart ")
					try(
						G_OBJ_UTIL.dotnetLog (" [renderExecuteFN].setgamma")
						local bm=openBitMap G_STCON.OUTPUT_SERIAL_FILE
						local bmm = copy bm
						bmm.filename=G_STCON.OUTPUT_SERIAL_FILE
						bmm.gamma=G_STCON.MAX_OUTGAMMA as float
						save bmm
					)catch(
						G_OBJ_UTIL.dotnetLog (getcurrentException() as string)	
					)
					G_OBJ_UTIL.dotnetLog (" [renderExecuteFN].GammaEnd ")
				)
			)
			
			
		)
		
		
		
		
		G_OBJ_UTIL.dotnetLog (" [renderExecuteFN].elem.start ")
		
			--renderCmd=renderCmd+" renderElements:false "
			G_OBJ_UTIL.dotnetLog (" [renderExecuteFN].saveelem ")
			try(
				if elemArr != undefined then (
					for elem in elemArr do (					
						save elem		
					)
				)
			)catch()
		
		G_OBJ_UTIL.dotnetLog (" [renderExecuteFN].elem.end ")

		*/
		
		
		
		
		/*
		--render frame:(G_STCON.RENDER_FRAME as time) camera:c quiet:true progressbar:true  renderMultiPassEffects:true  outputwidth:(G_STCON.MYWIDTH as number) outputheight:(G_STCON.MYHEIGHT as number)
							
		--local imgBitmap = render  frame:(G_STCON.RENDER_FRAME as time) camera:c quiet:true   progressbar:true  renderElements:true renderElementBitmaps:&elemArr  outputwidth:(G_STCON.MYWIDTH as number) outputheight:(G_STCON.MYHEIGHT as number)--"E:/inputData/53/TEST/tex/scene/TT_2011.max"			
							
		local imgBitmap = render  fromframe:(myStartFrame as time)  toframe:(myEndFrame as time)  nthframe:(myByFrame as time) quiet:true   progressbar:true    outputwidth:(G_STCON.MYWIDTH as number) outputheight:(G_STCON.MYHEIGHT as number)--"E:/inputData/53/TEST/tex/scene/TT_2011.max"			
		*/						
							
	),
	
	
	
	fn maxQuickRenderFn=(
		
		G_OBJ_UTIL.dotnetLog (" [maxQuickRenderFn].Start ")

		
		----------------------camera----------------------
		global myRenderCamera=undefined
		G_OBJ_UTIL.dotnetLog (" [maxQuickRenderFn].myRenderCamera__ ")
		for c in cameras do (
			local cameraNameStr=trimright (trimleft c.name)
			G_OBJ_UTIL.dotnetLog (" [maxQuickRenderFn].cameraNameStr__ "+cameraNameStr)
			if (classof c)!=Targetobject and cameraNameStr==G_STCON.RENDERABLE_CAMERA then (
				try(
                    --viewport.ResetAllViews() 
                    viewport.setCamera c
					
					
					local viewId=viewport.activeViewport
	
					local viewType =viewport.getType index:viewId --viewport.getType()
					G_OBJ_UTIL.dotnetLog ("ViewPort="+(viewId as string)+"..."+(viewType as string))
                )catch()
                myRenderCamera=c
			)
			
		)
		G_OBJ_UTIL.dotnetLog (" [maxQuickRenderFn].myRenderCamera... "+(myRenderCamera as string))
		
		
		----------------------frame----------------------
		if G_STCON.RENDER_FRAME_START==G_STCON.RENDER_FRAME_END then(
			rendTimeType = 1 
			try(-----------sliderTime
				sliderTime=(G_STCON.RENDER_FRAME as time)
			)catch()
		)else(
			rendTimeType = 3 
			--rendPickupFrames=G_STCON.RENDER_FRAME_START +"-"+G_STCON.RENDER_FRAME_END --+"["+G_STCON.RENDER_FRAME_BY+"]"
			rendSaveFile=true
			rendNThFrame=G_STCON.RENDER_FRAME_BY as integer
			rendStart=G_STCON.RENDER_FRAME_START as integer
			rendEnd=G_STCON.RENDER_FRAME_END as integer
		)
		sleep 1
        if G_STCON.NOT_RENDER=="true" then (
			
		)else(
            renderSceneDialog.open()
            renderSceneDialog.commit()
            if (maxversion())[1] < 17000 then(
                try(
                    renderSceneDialog.update()
                )catch()
            )
            
            renderSceneDialog.close()
			max quick render
		)
		
        
        saveOutputGamma()
	),
	
	fn loadMaxFN=(
		G_OBJ_UTIL.dotnetLog (" [loadMaxFN].Start ")
		
		DialogMonitorOPS.unRegisterNotification id:#RB_Monitor_Dialog 
		DialogMonitorOPS.RegisterNotification RB_MontiorDialog id:#RB_Monitor_Dialog
		DialogMonitorOPS.Enabled = true
		
		G_OBJ_UTIL.dotnetLog G_STCON.MAXFILE
		local loadResult = loadMaxFile G_STCON.MAXFILE useFileUnits:true quiet:true 
        try(callbacks.removeScripts #preRender id:#ID_CRP_preRenderP )catch() 
        try(callbacks.removeScripts #filePostOpen id:#ID_CRP_filePostOpenP )catch()
        try(callbacks.removeScripts #viewportChange id:#ID_CRP_viewportChangeP )catch() 
        try(callbacks.removeScripts #filePostOpen id:#ID_CRP_filePostOpen )catch() 
        try(callbacks.removeScripts #filePostMerge id:#ID_CRP_filePostMerge )catch()
        try(callbacks.removeScripts #postImport id:#ID_CRP_postImport )catch()
		G_OBJ_UTIL.dotnetLog (" [loadMaxFN].End\n")
		
		G_STCON.RENDERER_OBJECT=renderers.production 
		G_STCON.RENDERER_STR = ( classof G_STCON.RENDERER_OBJECT ) as string
		
		
		
		G_OBJ_UTIL.dotnetLog(" [loadMaxFN].G_STCON.RENDERER_STR="+G_STCON.RENDERER_STR)
		
		try(
			local gammaFu=IDisplayGamma.colorCorrectionMode as string
			G_OBJ_UTIL.dotnetLog ("------Gamma after load max is"+gammaFu+"--------")
		)catch()
		
		try(
			rendUseNet=false
		)catch()
		
		loadResult
		
	),
	
	fn saveMaxFn=(
		local tempMax=G_STCON.WORK_PATH+G_STCON.TASK_ID+"/"+maxFileName
		saveMaxFile tempMax useNewFile:true quiet:true
	),
	
	fn cpuSet=(
        try(
            local cpuCount = SysInfo.CPUCount
            G_OBJ_UTIL.dotnetLog ( "cpuCount="+(cpuCount as string))
            local TargetAffinity=0
            local targetAffinity = 0
            for coreID = 2 to SysInfo.CPUCount do(
                targetAffinity = (Bit.Set targetAffinity coreID true)
            )
            SysInfo.ProcessAffinity = targetAffinity
        )catch()
		
		try(
			sysInfo.MAXPriority=#low
		)catch()
	),
	
    fn bakeRenders=(
		G_OBJ_UTIL.dotnetLog ("\n\n-------------------[Render to Texture]-------------------\n")
		local Allgeo =  filterString G_STCON.BAKERENDERID "," 
		select (maxOps.getNodeByHandle (Allgeo[G_STCON.RENDER_FRAME_START as integer] as integer))
		G_OBJ_UTIL.dotnetLog ("___Geoname::"+($.name as string) +"    Modcount::"+ ($.modifiers.count as string))
			for  i = 1 to $.NumBakeElements() do 
				(
					local enname = $.GetBakeElement i
					format "%__%\n" enname (classof enmame as string)
					local newPath=G_STCON.OUTPUT_PATH +"/" +(getfilenamefile enname.filename)+(getfilenametype G_STCON.OUTPUT_NAME)
					local filetype= G_STCON.OUTPUT_PATH +"/" +(getfilenamefile enname.filename)+(getfilenametype G_STCON.OUTPUT_NAME)
					format "newPath.....%\n" newPath
					enname.filename = (getfilenamefile enname.filename)+(getfilenametype G_STCON.OUTPUT_NAME)
					enname.filetype = newPath
					renderWidth  = enname.outputSzX as integer
					renderHeight = enname.outputSzY as integer
				)
			render rendertype:#bakeselected
    ),
	
	fn custombakeRenders=(
		G_OBJ_UTIL.dotnetLog ("\n\n-------------------[Custom_Render to Texture]-------------------\n")
		max select all
		G_OBJ_UTIL.dotnetLog ("___ALLselectGeo::"+$.count as string)		
		select selection[G_STCON.RENDER_FRAME_START as integer]
		G_OBJ_UTIL.dotnetLog ("___Geoname::"+($.name as string) +"    Modcount::"+ ($.modifiers.count as string))
		for  i = 1 to $.NumBakeElements() do 
			(
				local enname = $.GetBakeElement i
				format "%__%\n" enname (classof enmame as string)
				local newPath=G_STCON.OUTPUT_PATH +"/" +(getfilenamefile enname.filename)+(getfilenametype G_STCON.OUTPUT_NAME)
				local filetype= G_STCON.OUTPUT_PATH +"/" +(getfilenamefile enname.filename)+(getfilenametype G_STCON.OUTPUT_NAME)
				format "newPath.....%\n" newPath
				enname.filename = (getfilenamefile enname.filename)+(getfilenametype G_STCON.OUTPUT_NAME)
				enname.filetype = newPath
				renderWidth  = enname.outputSzX as integer
				renderHeight = enname.outputSzY as integer
			)
		render rendertype:#bakeselected
    ),
	
	fn runFN=(
		
		G_OBJ_UTIL.dotnetLog (" [runFN].Start ")
		
		G_OBJ_UTIL.dotnetLog ("\n\n-------------------[2/"+G_STCON.STEP_COUNT+"][Load Max File]-------------------\n")
		local loadResult=loadMaxFN()
		
		if loadResult==true then (
			G_OBJ_UTIL.dotnetLog ("\n\n-------------------[3/"+G_STCON.STEP_COUNT+"][Max File Common Info]-------------------\n")
			
			if  G_STCON.USER_ID=="1820634" then (
				try(
					IDisplayGamma.colorCorrectionMode = #none
				)catch()
			)
			if  G_STCON.USER_ID=="963733" then (
				try(
					IDisplayGamma.colorCorrectionMode = #none
				)catch()
			)


		
			commonFN()
			setMaxOutputNameFN()
			
			
			
			elementFN()
			G_OBJ_UTIL.dotnetLog ("\n\n-------------------[4/"+G_STCON.STEP_COUNT+"][Max File Renderer Info]-------------------\n")
			rendererFN()
			G_OBJ_UTIL.dotnetLog ("\n\n-------------------[5/"+G_STCON.STEP_COUNT+"][Max File Asset Info]-------------------\n")
			local myAsset=STAsset()
			myAsset.runFN()
			G_OBJ_UTIL.dotnetLog ("\n\n-------------------[6/"+G_STCON.STEP_COUNT+"][Start Render]-------------------\n")
			
			
			if G_STCON.MYPLATFORM!="1007" and matchPattern G_STCON.PROJECT_SYMBOL pattern:"*_savemaxfile" then (
				saveMaxFn()
			)
			
			cpuSet()
			
			--renderExecuteFN()
			
			/*
			if G_STCON.SUB_FROM=="1"or G_STCON.SUB_FROM=="2" or G_STCON.CUSTOM_CLIENT=="yunwu" or G_STCON.MAX_QUICK_RENDER then(
				G_OBJ_UTIL.dotnetLog ("\n\n-------------------[[Start Max Quick Render]-------------------\n")
			
				renderSceneDialog.open()
				renderSceneDialog.commit()
				if (maxversion())[1] < 17000 then(
                    try(
                        renderSceneDialog.update()
                    )catch()
				)
				
				renderSceneDialog.close()
				
				
				if G_STCON.TOTAL_BLOCK>1 then(
					renderExecuteFN()
				)else(
					maxQuickRenderFn()
				)
				
			)else(
				renderExecuteFN()
			)
			
			*/
		if G_STCON.IS_BAKERENDER == "true" then(
			bakeRenders())
		else(
			if (G_STCON.USER_ID=="1821496" or G_STCON.USER_ID=="1819964" or G_STCON.USER_ID=="1840720" or G_STCON.USER_ID=="1844686") and (getRenderType() == #selected) then(
			   custombakeRenders())
			else(
				if  G_STCON.MAX_QUICK_RENDER  then (
					G_OBJ_UTIL.dotnetLog ("\n\n-------------------[[Start Max Quick Render]-------------------\n")
					renderSceneDialog.open()
					renderSceneDialog.commit()
					if (maxversion())[1] < 17000 then(
						try(
							renderSceneDialog.update()
						)catch()
					)
					
					renderSceneDialog.close()
					maxQuickRenderFn()
				)else(
					renderExecuteFN()
				)
			)
			
		)	
			
		)else(
			G_OBJ_UTIL.dotnetLog (" [runFN].load max file failed ")
		)
		
		
		G_OBJ_UTIL.dotnetLog (" [runFN].End \n")
	
	
		
		
		
	)

	
	
)


fn mergeImg  =(
	G_OBJ_UTIL.dotnetLog (" [mergeImg].Start ")
	
	local oldGamma=IDisplayGamma.colorCorrectionMode
	try(
		IDisplayGamma.colorCorrectionMode = #none
	)catch()
	
	local blockPre="block_"
	local sqrtBlock=(sqrt G_STCON.TOTAL_BLOCK) as integer
	local blockWidth=(G_STCON.MYWIDTH as integer)/sqrtBlock
	local blockHeight=(G_STCON.MYHEIGHT as integer)/sqrtBlock

	
	G_OBJ_UTIL.dotnetLog (" [mergeImg].sqrtBlock= "+(sqrtBlock as string))
	G_OBJ_UTIL.dotnetLog (" [mergeImg].blockWidth= "+(blockWidth as string))
	G_OBJ_UTIL.dotnetLog (" [mergeImg].blockHeight= "+(blockHeight as string))
	
	--local mergePath=G_STCON.WORK_PATH+G_STCON.TASK_ID+"/block/frame_"+G_STCON.RENDER_FRAME+"/"
	
	G_OBJ_UTIL.dotnetLog (" [mergeImg].mergePath= "+G_STCON.MERGE_PATH)
	local mergePathArr=getDirectories (G_STCON.MERGE_PATH+"*")
	local block0Arr=getfiles (G_STCON.MERGE_PATH+blockPre+"0/*.*")
	for blockFile in block0Arr do (
		local blockFileName = getFilenameFile blockFile
		local blockFileType = getFilenameType blockFile
		if blockFileType!=".db" then(
			try(
				freeSceneBitmaps() 
			)catch()
			
			try(
				gc() 
			)catch()
			
			
			local resultBitmap=bitmap (G_STCON.MYWIDTH as integer) (G_STCON.MYHEIGHT as integer)
			
			local myGamma=undefined
			local blockFile=blockFileName+blockFileType
			G_OBJ_UTIL.dotnetLog (" [mergeImg].blockFile= "+blockFile)
			for blockNumber=0 to (G_STCON.TOTAL_BLOCK-1) do(
				local blockFilePath=G_STCON.MERGE_PATH+blockPre+(blockNumber as string)+"/"+blockFile
				
				
				local row=blockNumber/sqrtBlock
				local col=(mod blockNumber sqrtBlock) as integer
				local leftTopX=col*blockWidth
				local leftTopY=row*blockHeight
				
				local str = " [mergeImg] "+(blockNumber as string)+ "["+(row as string)+","+(col as string)+"] ("+(leftTopX as string)+","+(leftTopY as string)+") "
				G_OBJ_UTIL.dotnetLog (str+blockFilePath)
				format "block......%\n" blockFilePath
				local tempBitmap=openBitMap blockFilePath
				myGamma=tempBitmap.gamma
				try(
					G_OBJ_UTIL.dotnetLog ("Gamma is "+(myGamma as string))
				)catch()
				pastebitmap tempBitmap resultBitmap [0,0] [leftTopX,leftTopY] 
				--display resultBitmap
				close tempBitmap
				free tempBitmap
				
			)
			resultBitmap.filename=G_STCON.OUTPUT_PATH +"/"+blockFile
			if myGamma!=undefined then (
				save resultBitmap gamma:myGamma
			)else(
				save resultBitmap
			)
			close resultBitmap
			free resultBitmap
			
		)
	)
		
		
	try(
		IDisplayGamma.colorCorrectionMode = oldGamma
	)catch()
	
	
)


--fn rvRender userId taskId notRender renderFrame blockNumber totalBlock  kg jobName   outputPath optionArray currenttask  = (
fn rvRender paramArray deleteModel:#() rendModel:#()  = (

	
	
	G_OBJ_UTIL.dotnetLog "\n\n------------------------------------------------------------[Start maxscript render]--------------------------------------------------------\n\n"
	
	try(
		local gammaFu=IDisplayGamma.colorCorrectionMode as string
		G_OBJ_UTIL.dotnetLog ("------Gamma before load max is"+gammaFu+"--------")
	)catch()
	--G_STCON.init userId taskId notRender renderFrame blockNumber totalBlock  kg jobName   outputPath optionArray currenttask "client" "" 
	G_STCON.init  paramArray
	
	
	if G_STCON.TOTAL_BLOCK>1 and G_STCON.BLOCK_NUMBER==G_STCON.TOTAL_BLOCK then(
		mergeImg()
	)else(
		G_OBJ_UTIL.dotnetLog ("\n\n-------------------[1/"+G_STCON.STEP_COUNT+"][Config 3ds Max]-------------------\n")
		local configMaxObject=STConfigMax()
		configMaxObject.initMaxFN()
		
		local myrender=STRender()
		myrender.runFN()
		
		G_OBJ_UTIL.dotnetLog ("\n\n-------------------[7/"+G_STCON.STEP_COUNT+"][Reset 3ds Max And exit]-------------------\n")
		configMaxObject.resetMaxFN()
		G_OBJ_UTIL.dotnetLog "\n\n------------------------------------------------------------[End maxscript render]--------------------------------------------------------\n\n"
		
	)
	

	sleep 5
	

	G_OBJ_UTIL.dotnetLog " --------------rvRender.end---------------"
	
)

--fn fastRender userId taskId  notRender renderFrame blockNumber totalBlock  kg jobName   outputPath optionArray currenttask subFrom maxfile = (
fn web_render paramArray deleteModel:#() rendModel:#() =(
	
	G_OBJ_UTIL.dotnetLog "\n\n------------------------------------------------------------[Start maxscript render]--------------------------------------------------------\n\n"
	try(
		local gammaFu=IDisplayGamma.colorCorrectionMode as string
		G_OBJ_UTIL.dotnetLog ("------Gamma before load max is"+gammaFu+"--------")
	)catch()
	--G_STCON.init userId taskId notRender renderFrame blockNumber totalBlock  kg jobName   outputPath optionArray currenttask subFrom maxfile 
	G_STCON.init paramArray
	
	
	
	
	G_OBJ_UTIL.dotnetLog ("\n\n-------------------[1/"+G_STCON.STEP_COUNT+"][Config 3ds Max]-------------------\n")
	local configMaxObject=STConfigMax()
	configMaxObject.initMaxFN()
	
	local myrender=STRender()
	myrender.runFN()
	
	G_OBJ_UTIL.dotnetLog ("\n\n-------------------[7/"+G_STCON.STEP_COUNT+"][Reset 3ds Max And exit]-------------------\n")
	configMaxObject.resetMaxFN()
	G_OBJ_UTIL.dotnetLog "\n\n------------------------------------------------------------[End maxscript render]--------------------------------------------------------\n\n"
	
	
	

	sleep 5

	G_OBJ_UTIL.dotnetLog " --------------rvRender.end---------------"
	
)



--clearlistener()
        try(callbacks.removeScripts #preRender id:#ID_CRP_preRenderP )catch() 
        try(callbacks.removeScripts #filePostOpen id:#ID_CRP_filePostOpenP )catch()
        try(callbacks.removeScripts #viewportChange id:#ID_CRP_viewportChangeP )catch() 
        try(callbacks.removeScripts #filePostOpen id:#ID_CRP_filePostOpen )catch() 
        try(callbacks.removeScripts #filePostMerge id:#ID_CRP_filePostMerge )catch()
        try(callbacks.removeScripts #postImport id:#ID_CRP_postImport )catch()


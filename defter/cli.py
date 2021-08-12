import os
import re
import sys
import eel
import brython
import platform
import argparse
import warnings
import subprocess

bv = brython.__version__
IS_WIN32 = 'win32' in str(sys.platform).lower()


def main():
    def js2py(path=None):
        def subString(w1, w2, template):
            pat = re.compile(w1 + '(.*?)' + w2, re.S)
            return pat.findall(template)

        if path is None:
            path = os.getcwd()
        with open(path + '/AppResources/app.html', 'r', encoding='UTF-8') as code:
            codes = code.read()
            pos = codes.find("</html>") + 7
            codes = codes[0:pos]

        functions_py = []
        expose_js = []
        functions = subString("expose\\(", "\\)", codes)

        if functions:
            for function in functions:
                var_s = subString("function " + function + "\\(", "\\)", codes)[0]
                functions_py.append("def " + function + "(" + var_s + "):\n    eel." + function + "(" + var_s + ")")
                expose_js.append("<!--eel.expose(" + function + ");-->")
            codes_py = "import eel\n\n\n"
            for func in functions_py:
                codes_py += func + "\n\n\n"
            codes_py = codes_py[:-2]
            new_codes = codes + "\n\n\n"
            for expose in expose_js:
                new_codes += expose + '\n'

            with open(path + '/AppResources/app.html', 'w+', encoding='UTF-8') as code:
                code.write(new_codes)

            with open(path + '/js.py', 'w+', encoding='UTF-8') as code:
                code.write(codes_py)

    # Resources ⬇

    main_demo = """from defter import backend

backend.init(python_in_web=True)


@backend.expose
def py_fun(x):
    print('Hello World!' + ' -> From: ' + x)


backend.start()
"""

    html_demo = """<!DOCTYPE html>

<head>
    <meta charset="UTF-8">
    <title>Defter App</title>
    <script type="text/javascript" src="core.js"></script>
</head>

<body>

    <h1>Hello World!</h1>

    <script type="text/javascript">py_fun('JavaScript')</script>

    <script type="text/python">
    from browser import window
    window.py_fun('Python')
    </script>

</body>

</html>
"""

    electron_js_demo = """// Modules to control application life and create native browser window
const {app, BrowserWindow} = require('electron')
const path = require('path')

function createWindow () {
  // Create the browser window.
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    autoHideMenuBar: true,
    icon: __dirname + '/icon.ico',
    webPreferences: {
      nodeIntegration: false,
      webSecurity: false
    }
  })
  // and load the index.html of the app.
  // mainWindow.loadFile('app.html')
  mainWindow.loadURL('http://localhost:8080/app.html') // Add your app URL.

  // Open the DevTools.
  // mainWindow.webContents.openDevTools()
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(() => {
  createWindow()
  
  app.on('activate', function () {
    // On macOS it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit()
})

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.
"""

    electron_package_demo = """{
  "name": "electron-defter-app",
  "productName": "Defter App",
  "version": "1.0.0",
  "description": "A minimal Electron application",
  "main": "main.js",
  "scripts": {
    "start": "electron ."
  },
  "author": "Anonymous",
  "license": "-",
  "devDependencies": {
    "electron": "^13.1.4"
  }
}
"""

    # Parser options ⬇

    parser = argparse.ArgumentParser(description='manual to defter')
    parser.add_argument("-create", type=str)
    parser.add_argument("-update", type=str)
    parser.add_argument("-js2py", type=str)
    parser.add_argument("-package", type=str)
    args = parser.parse_args()

    def subprocess_call(*args, **kwargs):
        # It creates a new *hidden* window, so it will work in frozen apps (.exe).
        if IS_WIN32:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags = subprocess.CREATE_NEW_CONSOLE | subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            kwargs['startupinfo'] = startupinfo
        retcode = subprocess.call(*args, **kwargs)
        return retcode

    if args.create is not None:
        if args.create == "here":
            args.create = os.getcwd()
        if not os.path.exists(args.create + "/AppResources"):
            os.mkdir(args.create + "/AppResources")
        else:
            if os.path.exists(args.create + '/AppResources' + '/brython.js'):
                os.remove(args.create + '/AppResources' + '/brython.js')
            if os.path.exists(args.create + '/AppResources' + '/brython_stdlib.js'):
                os.remove(args.create + '/AppResources' + '/brython_stdlib.js')
        with open(args.create + '/main.py', 'w+') as demo_py:
            demo_py.write(main_demo)
        with open(args.create + '/AppResources' + '/app.html', 'w+') as html:
            html.write(html_demo)
        with open(args.create + '/AppResources' + '/main.js', 'w+') as ele_js_demo:
            ele_js_demo.write(electron_js_demo)
        with open(args.create + '/AppResources' + '/package.json', 'w+') as ele_package_demo:
            ele_package_demo.write(electron_package_demo)
        with open(args.create + '/AppResources' + '/core.js', 'w+') as core:
            core.write(
                """document.write("<script src='eel.js'></script>","<script src='brython.js'></script>","<script src='brython_stdlib.js'></script>");window.onload=function(){brython();};function expose(f){eel.expose(f);}""")
        with open(args.create + '/AppResources' + '/eel.js', 'w+') as eel_core:
            eel_core.write(
                """eel={_host:window.location.origin,set_host:function(hostname){eel._host=hostname},expose:function(f,name){if(name===undefined){name=f.toString();let i='function '.length,j=name.indexOf('(');name=name.substring(i,j).trim();}eel._exposed_functions[name]=f;},guid:function(){return eel._guid;},_guid:([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g,c=>(c^crypto.getRandomValues(new Uint8Array(1))[0]&15>>c/4).toString(16)),_exposed_functions:{},_mock_queue:[],_mock_py_functions:function(){for(let i=0;i<eel._py_functions.length;i++){let name=eel._py_functions[i];eel[name]=function(){let call_object=eel._call_object(name,arguments);eel._mock_queue.push(call_object);return eel._call_return(call_object);}}},_import_py_function:function(name){let func_name=name;eel[name]=function(){let call_object=eel._call_object(func_name,arguments);eel._websocket.send(eel._toJSON(call_object));return eel._call_return(call_object);}},_call_number:0,_call_return_callbacks:{},_call_object:function(name,args){let arg_array=[];for(let i=0;i<args.length;i++){arg_array.push(args[i]);}let call_id=(eel._call_number+=1)+Math.random();return{'call':call_id,'name':name,'args':arg_array};},_sleep:function(ms){return new Promise(resolve=>setTimeout(resolve,ms));},_toJSON:function(obj){return JSON.stringify(obj,(k,v)=>v===undefined?null:v);},_call_return:function(call){return function(callback=null){if(callback!=null){eel._call_return_callbacks[call.call]={resolve:callback};}else{return new Promise(function(resolve,reject){eel._call_return_callbacks[call.call]={resolve:resolve,reject:reject};});}}},_position_window:function(page){let size=eel._start_geometry['default'].size;let position=eel._start_geometry['default'].position;if(page in eel._start_geometry.pages){size=eel._start_geometry.pages[page].size;position=eel._start_geometry.pages[page].position;}if(size!=null){window.resizeTo(size[0],size[1]);}if(position!=null){window.moveTo(position[0],position[1]);}},_init:function(){eel._mock_py_functions();document.addEventListener("DOMContentLoaded",function(event){let page=window.location.pathname.substring(1);eel._position_window(page);let websocket_addr=(eel._host+'/eel').replace('http','ws');websocket_addr+=('?page='+page);eel._websocket=new WebSocket(websocket_addr);eel._websocket.onopen=function(){for(let i=0;i<eel._py_functions.length;i++){let py_function=eel._py_functions[i];eel._import_py_function(py_function);}while(eel._mock_queue.length>0){let call=eel._mock_queue.shift();eel._websocket.send(eel._toJSON(call));}};eel._websocket.onmessage=function(e){let message=JSON.parse(e.data);if(message.hasOwnProperty('call')){if(message.name in eel._exposed_functions){try{let return_val=eel._exposed_functions[message.name](...message.args);eel._websocket.send(eel._toJSON({'return':message.call,'status':'ok','value':return_val}));}catch(err){debugger;eel._websocket.send(eel._toJSON({'return':message.call,'status':'error','error':err.message,'stack':err.stack}));}}}else if(message.hasOwnProperty('return')){if(message['return']in eel._call_return_callbacks){if(message['status']==='ok'){eel._call_return_callbacks[message['return']].resolve(message.value);}else if(message['status']==='error'&&eel._call_return_callbacks[message['return']].reject){eel._call_return_callbacks[message['return']].reject(message['error']);}}}else{throw'Invalid message '+message;}};});}};eel._init();if(typeof require!=='undefined'){window.nodeRequire=require;delete window.require;delete window.exports;delete window.module;}""")
        if platform.system().lower() == 'windows':
            subprocess_call("cd " + args.create + "/AppResources" + " && python -m brython --install", shell=True,
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        elif platform.system().lower() == 'linux':
            subprocess_call("cd " + args.create + "/AppResources" + " && python3 -m brython --install", shell=True,
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            warnings.warn('This system is not supported!', RuntimeWarning)
            sys.exit(1)
        del_list = [args.create + "/AppResources/demo.html", args.create + "/AppResources/index.html",
                    args.create + "/AppResources/README.txt"]
        for i in del_list:
            os.remove(i)
        print('Creating...')
        print('Done.')

    if args.update is not None:
        if args.update == "here":
            args.update = os.getcwd()
        try:
            with open(args.update + '/AppResources' + '/core.js', 'w+') as core:
                core.write(
                    """document.write("<script src='eel.js'></script>","<script src='brython.js'></script>","<script src='brython_stdlib.js'></script>");window.onload=function(){brython();};function expose(f){eel.expose(f);}""")
            with open(args.update + '/AppResources' + '/eel.js', 'w+') as eel_core:
                eel_core.write(
                    """eel={_host:window.location.origin,set_host:function(hostname){eel._host=hostname},expose:function(f,name){if(name===undefined){name=f.toString();let i='function '.length,j=name.indexOf('(');name=name.substring(i,j).trim();}eel._exposed_functions[name]=f;},guid:function(){return eel._guid;},_guid:([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g,c=>(c^crypto.getRandomValues(new Uint8Array(1))[0]&15>>c/4).toString(16)),_exposed_functions:{},_mock_queue:[],_mock_py_functions:function(){for(let i=0;i<eel._py_functions.length;i++){let name=eel._py_functions[i];eel[name]=function(){let call_object=eel._call_object(name,arguments);eel._mock_queue.push(call_object);return eel._call_return(call_object);}}},_import_py_function:function(name){let func_name=name;eel[name]=function(){let call_object=eel._call_object(func_name,arguments);eel._websocket.send(eel._toJSON(call_object));return eel._call_return(call_object);}},_call_number:0,_call_return_callbacks:{},_call_object:function(name,args){let arg_array=[];for(let i=0;i<args.length;i++){arg_array.push(args[i]);}let call_id=(eel._call_number+=1)+Math.random();return{'call':call_id,'name':name,'args':arg_array};},_sleep:function(ms){return new Promise(resolve=>setTimeout(resolve,ms));},_toJSON:function(obj){return JSON.stringify(obj,(k,v)=>v===undefined?null:v);},_call_return:function(call){return function(callback=null){if(callback!=null){eel._call_return_callbacks[call.call]={resolve:callback};}else{return new Promise(function(resolve,reject){eel._call_return_callbacks[call.call]={resolve:resolve,reject:reject};});}}},_position_window:function(page){let size=eel._start_geometry['default'].size;let position=eel._start_geometry['default'].position;if(page in eel._start_geometry.pages){size=eel._start_geometry.pages[page].size;position=eel._start_geometry.pages[page].position;}if(size!=null){window.resizeTo(size[0],size[1]);}if(position!=null){window.moveTo(position[0],position[1]);}},_init:function(){eel._mock_py_functions();document.addEventListener("DOMContentLoaded",function(event){let page=window.location.pathname.substring(1);eel._position_window(page);let websocket_addr=(eel._host+'/eel').replace('http','ws');websocket_addr+=('?page='+page);eel._websocket=new WebSocket(websocket_addr);eel._websocket.onopen=function(){for(let i=0;i<eel._py_functions.length;i++){let py_function=eel._py_functions[i];eel._import_py_function(py_function);}while(eel._mock_queue.length>0){let call=eel._mock_queue.shift();eel._websocket.send(eel._toJSON(call));}};eel._websocket.onmessage=function(e){let message=JSON.parse(e.data);if(message.hasOwnProperty('call')){if(message.name in eel._exposed_functions){try{let return_val=eel._exposed_functions[message.name](...message.args);eel._websocket.send(eel._toJSON({'return':message.call,'status':'ok','value':return_val}));}catch(err){debugger;eel._websocket.send(eel._toJSON({'return':message.call,'status':'error','error':err.message,'stack':err.stack}));}}}else if(message.hasOwnProperty('return')){if(message['return']in eel._call_return_callbacks){if(message['status']==='ok'){eel._call_return_callbacks[message['return']].resolve(message.value);}else if(message['status']==='error'&&eel._call_return_callbacks[message['return']].reject){eel._call_return_callbacks[message['return']].reject(message['error']);}}}else{throw'Invalid message '+message;}};});}};eel._init();if(typeof require!=='undefined'){window.nodeRequire=require;delete window.require;delete window.exports;delete window.module;}""")
            if platform.system().lower() == 'windows':
                subprocess_call("cd " + args.update + "/AppResources" + " && python -m brython --update", shell=True,
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            elif platform.system().lower() == 'linux':
                subprocess_call("cd " + args.update + "/AppResources" + " && python3 -m brython --update", shell=True,
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
                warnings.warn('This system is not supported!', RuntimeWarning)
                sys.exit(1)
            del_list = [args.update + "/AppResources/demo.html", args.update + "/AppResources/index.html",
                        args.update + "/AppResources/README.txt"]
            for i in del_list:
                os.remove(i)
            print('Updating...')
            print('Done.')
        except:
            warnings.warn('Path "AppResources" not found!', RuntimeWarning)
            sys.exit(1)

    if args.js2py is not None:
        if args.js2py == "here":
            args.js2py = os.getcwd()
        print('Converting...')
        js2py(args.js2py)
        print('Done.')
        print(
            'Tip: js.py has been generated, please import the js module in Python and use js.your_function_name() to use the javascript program in Python.')

    if args.package is not None:
        with open(os.getcwd() + '/main.py', 'r', encoding='UTF-8') as code:
            codes = code.read()
            mirror_codes = 'selfcode = """' + codes + '"""' + '\n\n' + codes.rstrip()[0:-1] + ", selfcode=selfcode)\n"
        with open(os.getcwd() + '/main_mirror.py', 'w+', encoding='UTF-8') as code_mirror:
            code_mirror.write(mirror_codes)

        if platform.system().lower() == 'windows':
            if os.path.exists(os.path.dirname(args.package) + "AppResources" + "\\icon.ico"):
                subprocess_call("cd " + os.path.dirname(
                    args.package) + " && python -m eel " + "main_mirror.py" + " " + "AppResources" + "--onefile "
                                                                                                     "--noconsole "
                                                                                                     "--icon=" +
                                "AppResources" + "\\icon.ico",
                                shell=True)
            else:
                subprocess_call("cd " + os.path.dirname(
                    args.package) + " && python -m eel " + "main_mirror.py" + " " + "AppResources" + "--onefile "
                                                                                                     "--noconsole",
                                shell=True)
        elif platform.system().lower() == 'linux':
            if os.path.exists(os.path.dirname(args.package) + "AppResources" + "/icon.ico"):
                subprocess_call("cd " + os.path.dirname(
                    args.package) + " && python3 -m eel " + "main_mirror.py" + " " + "AppResources" + "--onefile "
                                                                                                      "--noconsole "
                                                                                                      "--icon=" +
                                "AppResources" + "/icon.ico",
                                shell=True)
            else:
                subprocess_call("cd " + os.path.dirname(
                    args.package) + " && python3 -ms eel " + "main_mirror.py" + " " + "AppResources" + "--onefile "
                                                                                                       "--noconsole",
                                shell=True)
        else:
            warnings.warn('This system is not supported!', RuntimeWarning)
            sys.exit(1)


# TODO 上次更新 2021/8/12 15:30
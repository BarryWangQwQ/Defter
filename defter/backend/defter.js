frontend = {
    _host: window.location.origin,

    set_host: function (hostname) {
        frontend._host = hostname
    },

    expose: function(f, name) {
        if(name === undefined){
            name = f.toString();
            let i = 'function '.length, j = name.indexOf('(');
            name = name.substring(i, j).trim();
        }

        frontend._exposed_functions[name] = f;
    },

    guid: function() {
        return frontend._guid;
    },

    // These get dynamically added by library when file is served
    /** _py_functions **/
    /** _start_geometry **/

    _guid: ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
            (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
        ),

    _exposed_functions: {},

    _mock_queue: [],

    _mock_py_functions: function() {
        for(let i = 0; i < frontend._py_functions.length; i++) {
            let name = frontend._py_functions[i];
            frontend[name] = function() {
                let call_object = frontend._call_object(name, arguments);
                frontend._mock_queue.push(call_object);
                return frontend._call_return(call_object);
            }
        }
    },

    _import_py_function: function(name) {
        let func_name = name;
        frontend[name] = function() {
            let call_object = frontend._call_object(func_name, arguments);
            frontend._websocket.send(frontend._toJSON(call_object));
            return frontend._call_return(call_object);
        }
    },

    _call_number: 0,

    _call_return_callbacks: {},

    _call_object: function(name, args) {
        let arg_array = [];
        for(let i = 0; i < args.length; i++){
            arg_array.push(args[i]);
        }

        let call_id = (frontend._call_number += 1) + Math.random();
        return {'call': call_id, 'name': name, 'args': arg_array};
    },

    _sleep: function(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    },

    _toJSON: function(obj) {
        return JSON.stringify(obj, (k, v) => v === undefined ? null : v);
    },

    _call_return: function(call) {
        return function(callback = null) {
            if(callback != null) {
                frontend._call_return_callbacks[call.call] = {resolve: callback};
            } else {
                return new Promise(function(resolve, reject) {
                    frontend._call_return_callbacks[call.call] = {resolve: resolve, reject: reject};
                });
            }
        }
    },

    _position_window: function(page) {
        let size = frontend._start_geometry['default'].size;
        let position = frontend._start_geometry['default'].position;

        if(page in frontend._start_geometry.pages) {
            size = frontend._start_geometry.pages[page].size;
            position = frontend._start_geometry.pages[page].position;
        }

        if(size != null){
            window.resizeTo(size[0], size[1]);
        }

        if(position != null){
            window.moveTo(position[0], position[1]);
        }
    },

    _init: function() {
        frontend._mock_py_functions();

        document.addEventListener("DOMContentLoaded", function(event) {
            let page = window.location.pathname.substring(1);
            frontend._position_window(page);

            let websocket_addr = (frontend._host + '/frontend').replace('http', 'ws');
            websocket_addr += ('?page=' + page);
            frontend._websocket = new WebSocket(websocket_addr);

            frontend._websocket.onopen = function() {
                for(let i = 0; i < frontend._py_functions.length; i++){
                    let py_function = frontend._py_functions[i];
                    frontend._import_py_function(py_function);
                }

                while(frontend._mock_queue.length > 0) {
                    let call = frontend._mock_queue.shift();
                    frontend._websocket.send(frontend._toJSON(call));
                }
            };

            frontend._websocket.onmessage = function (e) {
                let message = JSON.parse(e.data);
                if(message.hasOwnProperty('call') ) {
                    // Python making a function call into us
                    if(message.name in frontend._exposed_functions) {
                        try {
                            let return_val = frontend._exposed_functions[message.name](...message.args);
                            frontend._websocket.send(frontend._toJSON({'return': message.call, 'status':'ok', 'value': return_val}));
                        } catch(err) {
                            debugger
                            frontend._websocket.send(frontend._toJSON(
                                {'return': message.call,
                                'status':'error',
                                'error': err.message,
                                'stack': err.stack}));
                        }
                    }
                } else if(message.hasOwnProperty('return')) {
                    // Python returning a value to us
                    if(message['return'] in frontend._call_return_callbacks) {
                        if(message['status']==='ok'){
                            frontend._call_return_callbacks[message['return']].resolve(message.value);
                        }
                        else if(message['status']==='error' &&  frontend._call_return_callbacks[message['return']].reject) {
                                frontend._call_return_callbacks[message['return']].reject(message['error']);
                        }
                    }
                } else {
                    throw 'Invalid message ' + message;
                }

            };
        });
    }
};

frontend._init();

if(typeof require !== 'undefined'){
    // Avoid name collisions when using Electron, so jQuery etc work normally
    window.nodeRequire = require;
    delete window.require;
    delete window.exports;
    delete window.module;
}

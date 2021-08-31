from defter import backend


backend.init(path='src', extensions=['frontend-demo.js'])   # Back-end initialization.


@backend.expose    # Expose back-end function.
def py_fun(x):
    return "Hello " + x


backend.start('frontend-demo.html')    # Set up front-end portal and start back-end.

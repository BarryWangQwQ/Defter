document.title = "Hello Defter App"    # Set front-end title.

ele = document.createElement("h1")     # Create an html element.
document.body.appendChild(ele)         # Adding elements to the body.


def change(x):                         # Set a function that can change the element.
    ele.innerHTML = x


frontend.py_fun("World")(change)       # Calling back-end functions and using callbacks to get the return value.

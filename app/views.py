import random
from app import app
from flask import render_template, flash, redirect, url_for, Markup
from .get_docs import get_all_modules, get_function_list, format_function

@app.route('/')
@app.route('/index')
def index():
    py_version = 3.6

    # Scrape all the modules for that given python version
    modules = get_all_modules(py_version)

    # Get all the functions in that module
    # Keep trying until you get a module with functions
    while True:
        module = random.choice(modules)
        mod_functions = get_function_list(module, py_version)
        print(len(mod_functions))
        if mod_functions:
            break

    function = random.choice(mod_functions)
    function = format_function(function, py_version)
    function = Markup(str(function))

    return render_template('index.html', function=function)

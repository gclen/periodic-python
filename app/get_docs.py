import requests
from bs4 import BeautifulSoup


def replace_links(function, py_version):
    """Replace the internal links with external ones"""

    for a in function.find_all(class_='reference internal'):
        if '../' in a['href']:
            a['href'] = a['href'].lstrip('../')
            a['href'] = 'https://docs.python.org/{}/{}'.format(py_version, a['href'])
        else:
            a['href'] = 'https://docs.python.org/{}/library/{}'.format(py_version, a['href'])

    return function


def get_function_list(module, py_version):
    """Get the list of functions for the desired module taking
       python version into account
    """
    docs_url = 'https://docs.python.org/{}/library/{}.html'.format(py_version, module)
    page = requests.get(docs_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    functions = soup.find_all(class_='function')
    return functions


def is_deprecated(row):
    if row.find('strong'):
        if 'Deprecated' in row.find('strong').get_text():
            return True


def format_function(function, py_version):
    function = replace_links(function, py_version)

    # Remove the permalink
    permalink = function.find('a', class_='headerlink')
    permalink.decompose()

    return function


def get_all_modules(py_version):
    """Find all the non deprecated modules for the given python version"""
    page = requests.get('https://docs.python.org/{}/py-modindex.html'.format(py_version))
    soup = BeautifulSoup(page.content, 'html.parser')

    mod_links = soup.find_all('table')
    table_rows = mod_links[0].find_all('tr')

    modules = [tr.find('a').get_text() for tr in table_rows if not is_deprecated(tr) and tr.find('a') ]
    modules = sorted(list(set([m.split('.')[0] for m in modules])))

    return modules






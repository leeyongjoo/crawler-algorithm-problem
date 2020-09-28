langs = ['python3', 'java', 'javascript', 'kotlin', 'go', 'c', 'cpp', 'csharp', 'ruby', 'swift', 'scala',
         'mysql', 'oracle']
extensions = {
    'python3': 'py',
    'java': 'java',
    'javascript': 'js',
    'kotlin': 'kt',
    'go': 'go',
    'c': 'c',
    'cpp': 'cpp',
    'csharp': 'cs',
    'ruby': 'rb',
    'swift': 'swift',
    'scala': 'scala',
    'mysql': 'sql',
    'oracle': 'sql',
}


def get_extension(lang):
    return f'.{extensions[lang]}'


codeup_language_code = {
    'c': 0,
    'c++': 1,
    'java': 3,
    'python': 6,
}


def get_codeup_languages():
    return list(extensions.keys())

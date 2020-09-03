extensions = {
    'python': '.py',
    'c': '.c',
    'c++': '.cpp',
    'java': '.java',
}


def get_extension(language):
    return extensions[language]


codeup_language_code = {
    'c': 0,
    'c++': 1,
    'java': 3,
    'python': 6,
}


def get_codeup_languages():
    return list(extensions.keys())

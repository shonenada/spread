from setuptools import setup, find_packages


install_required = [l.strip() for l in open("requirements.txt", "r")]


metadata = {'name': 'spread',
            'version': '0.1',
            'packages': find_packages(),
            'author': 'shonenada',
            'author_email': 'shonenada@gmail.com',
            'url': "https://github.com/shonenada/spread",
            'zip_safe': False,
            'platforms': ['all'],
            'install_required': install_required}

if __name__ == '__main__':
    setup(**metadata)

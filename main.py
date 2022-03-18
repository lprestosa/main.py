project_name = "medium.com"
project_description = """
    App to process medium.com articles using various software stack technologies
"""
import config


def welcome():
    print(f'Project    : {project_name}')
    print('Script      : ' , __file__)
    print(f'Description: {project_description}')


if __name__ == '__main__':
    welcome()

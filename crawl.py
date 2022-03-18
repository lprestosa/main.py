# beautifulsoup_app.py
# beautiful soup application

import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import string
from os import listdir
from os.path import isfile, join
import config  # contains all the variables
import sys

DATADIR = config.datadir
CSVFILE = config.csvfile


def main():
    # Get links

    print(DATADIR)
    file_list = list_files(DATADIR, '.html')  # list all html files on this path
    #file_list = ['Medium-220314.html']
    df3 = pd.DataFrame()
    for html_file in file_list:
        print(html_file)
        links = get_links(DATADIR + html_file)  # scrape urls on this html file
        print('Number of URLs found: ', len(links))  # number of items in a list
        dict = {'url': links}
        df1 = pd.DataFrame(dict)  # create df containing url column
        df2 = parse_links(df1)  # add links to the dataframe
        df3 = df3.append(df2, ignore_index=True)  # accummulate

    # remove duplicate rows in df
    df3.drop_duplicates(subset='id', keep='last', inplace=True)

    # save df to csv
    df3.to_csv(CSVFILE)
    csvfile_info(CSVFILE)
    create_md_file(df3)


def create_md_file(df3):
    orig_stdout = sys.stdout
    with open('medium.md', 'w') as f:
        sys.stdout = f
        for index, row in df3.iterrows():
            id = row['id']
            title = row['title']
            url = row['url']
            print(f'+ {id} [{title}]({url})')
        sys.stdout = orig_stdout
    print('medium.md')

def list_files(mypath, search_str):
    """
    list filtered files on a path
    :return: file_list
    """
    f_list = []  # init file list
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for f in onlyfiles:
        if f.endswith(search_str):
            f_list.append(f)
    return f_list


def csvfile_info(file):
    print(file)
    handle = open(file)
    reader = csv.reader(handle)
    print("No of lines :", len(list(reader)))


def show_dataframe_info(df):
    print("df.shape", df.shape)
    print("df.columns", df.columns)
    # print("df.index", df.index)
    # print("df.describe()", df.describe())


def parse_links(df):
    # split url with '-' delimiter
    data = []
    df1 = pd.DataFrame(data, columns=['id', 'title'])

    for index, row in df.iterrows():
        split_url = row['url'].split('/')  # slice url by '/'
        title = (split_url[len(split_url) - 1])  # last node of url is the title
        words = title.split('-')  # slice title by '-'
        id = (words[len(words) - 1])  # last word of title is the id
        title = "-".join(words[0:len(words) - 1])  # remove id (last word) from title
        if all(c in string.hexdigits for c in id) and len(id) > 10 and "%" not in title:
            newrow = {'id': id, 'title': title, 'url': row['url']}
            df1 = df1.append(newrow, ignore_index=True)

    return df1


def get_links(html_file):
    with open(html_file, encoding="utf-8") as hf:
        soup = BeautifulSoup(hf, 'html.parser')
        links = []
        link1 = []
        link2 = []
        for item in soup.find_all('a'):  # get items from the soup
            link = item.get('href')  # get href links
            words = link.split('?')  # split link into words
            links.append(words[0])  # get first word and add to linklist
        links = sorted(set(links))  # sort links, remove dups

    for link in links:  # filter links that contain hyphen
        if '-' in link:
            link1.append(link)
    for link in link1:  # filter links with no third node.
        words = link.split('/')
        if len(words[3]) > 0:
            link2.append(link)

    ## print('\n'.join(link2))  # print list with \n delimiter
    ## print('Count: ', len(link2))  # number of items in a list
    return link2

def main2():
    """
    Navigate through a list of URL
    :return:
    """

if __name__ == '__main__':
    main()
    # main2()

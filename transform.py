# pandas_app.py
#
#  article dataframe
# prime ta dataframe
#
import pandas as pd

import config

CSV = config.articles_csv



def main():
    init()

    # read article csv to dataframe
    df_articles = pd.read_csv(CSV,index_col=None,header=None)
    df_articles = df_articles[df_articles['id'] != 'id']
    df_articles.set_index('id',inplace=True)      # reindex
    df_articles['rank'] = 1  # add new column with init value

    # drop first row
    #df_articles = df_articles[df_articles.id != 'id']
    #df_articles = df_articles.iloc()

    print(df_articles)
    exit(0)


    # create tag dataframe and populate
    cols = ['tag']
    df_tags = pd.DataFrame(columns=cols)
    tags = ['django', 'pandas', 'streamlit', 'python', 'django', 'sqlite', 'postgres', 'tkinter']
    df_tags['tag'] = tags

    df_tags.to_csv(config.tags_csv)

    # create idtag dataframe
    cols = ['id', 'tag']
    df_idtags = pd.DataFrame(columns=cols)
    df_temp = pd.DataFrame()

    for tag in df_tags['tag']:
        df_temp = pd.DataFrame()
        print('Tagging ', tag)
        df_temp['id'] = (df_article['id'][df_article['title'].str.contains(tag)])
        df_temp['tag'] = tag
        print('Row_count: ', len(df_temp))
        df_temp.reset_index(drop=True, inplace=True)
        df_idtags = df_idtags.append(df_temp)
    print('Row_count of df_idtags', len(df_idtags))
    df_idtags.to_csv(config.idtags_csv)

    for id in df_idtags['id']:
        df_articles['rank'] = df_articles['rank'] + 1

    #print("df_idtag", df_idtag)
    exit()

    # Create new rank dataframe
    cols = ['id', 'rank']
    df_rank = pd.DataFrame(columns=cols)
    print("df_rank", df_rank)

    # Save dataframe to csv
    df_url.to_csv(CSV)


def init():
    pd.set_option('display.max_colwidth', 200)
    pd.set_option('display.max_columns', 10)


if __name__ == '__main__':
    main()
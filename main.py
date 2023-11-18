import pandas as pd
import numpy as np


#Platform each song is most popular on
def find_most_played_platform(df):
    df['in_deezer_playlists'] = df['in_deezer_playlists'].str.strip().replace(',', '', regex=True)
    df['in_deezer_playlists'] = df['in_deezer_playlists'].astype(int)
    df['most_played_platform'] = df[['in_apple_playlists', 'in_deezer_playlists', 'in_spotify_playlists']].idxmax(axis=1)
    #print(df[['track_name','most_played_platform']].head())
    return df

#The most played song across each platform
def most_played_song(df):

    popular_song = df[['track_name','in_apple_playlists', 'in_deezer_playlists', 'in_spotify_playlists']]
    popular_song = popular_song.set_index('track_name')
    popular_song = popular_song.T
    #converting column data type to numeric
    popular_song = popular_song.replace(',', '', regex=True)
    popular_song = popular_song.apply(pd.to_numeric)
    #creating column with the most popular song on each platform
    popular_song['pop_song'] = popular_song.idxmax(axis = 1)
    return popular_song
 
def spotify_popular_streams(df):
    
    df = df.sort_values(by = 'streams', ascending=False).head(3) 
    return df

#Trends across the years
def popular_across_year(df):
    df = df[['track_name', 'year', 'streams']]
    
    df = df.groupby(['year','track_name'])['streams'].sum().reset_index()
    df = df.rename(columns={'streams':'total_streams'})
    df = df.sort_values(by='total_streams',ascending = False)
    return df

#Correlation of track attributes with number of streams
def attribute_correlation(df):
    df = spotify_popular_streams(df).head(10)
    df = df[['streams','valence_%', 'danceability_%', 'acousticness_%', 'instrumentalness_%', 'liveness_%', 'speechiness_%', 'energy_%']]
   
    df = df.corrwith(df['streams'])
    return df

#Correlation between number of playlist a song is included in and its average rank on spotify and shazam charts
def playlist_charts_correlation(df):
    df = df[['in_spotify_playlists', 'in_deezer_playlists', 'in_apple_playlists', 'in_spotify_charts', 'in_shazam_charts', 'in_deezer_charts', 'in_apple_charts']]
    df = df[(df!=0).all(1)]
    df['playlists'] = df[['in_spotify_playlists', 'in_deezer_playlists', 'in_apple_playlists']].mean(axis = 1)
    print(df['playlists'])
    df['charts'] = df[['in_spotify_charts', 'in_shazam_charts', 'in_deezer_charts', 'in_apple_charts']].replace(',' , '', regex=True).apply(pd.to_numeric).mean(axis = 1)
    print(df['charts'])
    correlation = df[['playlists', 'charts']].corr()
    return correlation


#separating artists into different columns
def artist_number_effect(df):
    df = df[['track_name', 'artist_count', 'artist(s)_name','streams']]
    df = df.sort_values(by = 'streams')
    name_expanded = df['artist(s)_name'].str.split(',', expand = True)
    name_expanded.columns = ['Artist'+str(i) for i in name_expanded.columns]

    
    name_expanded_concat = pd.concat([df, name_expanded], axis = 1)
    #final_df = pd.melt(name_expanded_concat, id_vars = ['track_name', 'artist_count'], value_vars = name_expanded.columns, )
    print(f"The artist1 column is: \n\n {name_expanded_concat['Artist1'].head(10)}")
    return name_expanded_concat

#Do songs with greater number of contributing artists tend to perform better?
def artist_number_impact(df):
    df = df[['artist_count', 'streams']]
    correlation = df.corr()
    return correlation


#Analyzing trends across the years
def year_trends(df):
    df = df[['track_name', 'year','Release_date','valence_%', 'danceability_%', 'acousticness_%', 'instrumentalness_%', 'liveness_%', 'speechiness_%', 'energy_%']]
    df = df.sort_values(by='Release_date', ascending=True)
    split_df = np.array_split(df, 4)
    df_dict = {}
    calculated_mean = list()
    for i, dfs in enumerate(split_df):
        df_dict[i] = dfs
    for i, small_df in df_dict.items():
        attribute_mean = small_df.iloc[:, 3:].mean(axis = 0)
        calculated_mean.append(attribute_mean)

    #print(f"The first set of split dataset is {calculated_mean[2]}")
    return calculated_mean


#most common keys and mode for most streamed song
def key_mode(df):
    df = spotify_popular_streams(df).head(100)
    trending_mode = df.mode()
    trending_key = df['key'].mode()
    print(f"The most common mode is {trending_mode}\n The most common key is {trending_key}\n")
    #return trending_key, trending_mode
df = pd.read_csv("spotify-2023.csv", encoding='latin1')
df.fillna(0, inplace=True)
x = df.isnull().sum().sum()
df = df.rename(columns= {'released_year':'year', 'released_month':'month', 'released_day':'day'})
print(df.index)
df['Release_date'] = pd.to_datetime(df[['year','month','day']])
print((f"The date column is \n {df['Release_date'].head()}"))
print(df.dtypes)
print(f"number of missing data is {x}")
print('On deezer charts\n\n')
print(df['day'].sort_values())
#print(df.count())

print('******The platform that each song is most popular on******\n\n')
print(find_most_played_platform(df).head())
print('******The most  popular song on each platform is******')
print(most_played_song(df).head())
print(f"Top most popular songs streamed on spotify is:\n\n {spotify_popular_streams(df)}")
print(f'\n\n\nThe most popular song across the years is:\n\n {popular_across_year(df)}')
print(df[['streams']].head(20))
print(f"troublesome at {df.columns}")
df = df.replace('MajorDanceability53Va', 345677654, regex=True)
print(f"streams data type is {df['streams'].dtype}")
df['streams'] = df['streams'].apply(pd.to_numeric)
print(f"The after streams data type is {df['streams'].dtype}")
print(f'\n\n\nThe correlation between different attributes with streams:\n\n{attribute_correlation(df)}')
print("charts data\n\n")
print(df[['track_name','in_shazam_charts', 'in_spotify_charts']].head(50))
print(df.dtypes)
print("\n\n\n correlation between playlists and charts\n\n\n")
print(playlist_charts_correlation(df))
print("\n\n\n Artists separated\n\n\n")
print(artist_number_effect(df))
print(f'Impact of number of artists on song popularity:\n\n {artist_number_impact(df)}')
print("\n\n\nYearly trends\n\n\n")
print(year_trends(df))
key_mode(df)
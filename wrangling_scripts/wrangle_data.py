import pandas as pd
import plotly.graph_objs as go

# Use this file to read in your data and prepare the plotly visualizations. The path to the data files are in
# `data/file_name.csv`


def prepare_data(weekdays_only = False):
    df = pd.read_csv('./data/daily_readings_sites.csv', parse_dates=[4])
    authority_df = pd.read_csv('./data/authority_df.csv')
    authority_dict = authority_df[['authority_id',
                                   'authority_name']].drop_duplicates().set_index(
                                       'authority_id').to_dict()['authority_name']
    
    df = df.merge(authority_df[['site_code','authority_id',
                                'authority_name']], 
                  on='site_code')
    df['day'] = df.date.dt.dayofweek
    if weekdays_only:
        df = df[~df.day.isin([5,6])]
    agg_df = df.groupby(
        ['authority_id','date'])[['NO2','O3','PM10','PM25']].agg(
            ['median','max','min']).reset_index()
    agg_df.columns = ['_'.join(tup) if tup[1] != '' else tup[0] 
                      for tup in list(agg_df.columns)]
    return agg_df, authority_dict



def return_figure(species):
    """Creates four plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """

    
    df, authority_dict = prepare_data(weekdays_only=True)
    
    col = species + '_median'
    
    fig = go.Figure()
    
    authorities_full = df.isnull().groupby(
        df['authority_id'])[col].sum() < df.date.nunique()-10
    
    authority_ls = pd.Series(authorities_full.index[authorities_full])

    fig.add_trace(
        go.Scatter(
            x = df.date,
            y = df[df.authority_id == authority_ls[0]][col].rolling(3,
                                                                    center=True).mean(),
            name = authority_dict[authority_ls[0]],
            visible=True))


    for authority_id in authority_ls[1:]:
         fig.add_trace(
            go.Scatter(
                x = df.date,
                y = df[df.authority_id == authority_id][col].rolling(3,
                                                                     center=True).mean(),
                name = authority_dict[authority_id],
                visible=False
            ))

    def create_layout_button(authority_id):
        return dict(label = authority_dict[authority_id],
                    method = 'update',
                    args = [{'visible': authority_ls.isin([authority_id]),
                             'title': authority_dict[authority_id],
                             'showlegend': True}])

    fig.update_layout(
        xaxis = dict(
            title_text = "Date",
            title_font = {"size": 20},
            title_standoff = 25),
        yaxis = dict(
            title_text = species + ' Levels',
            title_standoff = 25),
        title_text=species + " Pollution Rates in London Districts",
        height=400, width = 1000,
        updatemenus=[go.layout.Updatemenu(
            active = 0,
            buttons = list(authority_ls.map(
                lambda auth: create_layout_button(auth)))
            )
        ])
    return fig


# def return_figure():
#     species_ls = ['NO2','O3','PM10','PM25']
#     figures = [return_figure(species) for species in species_ls]
    

    # return figures
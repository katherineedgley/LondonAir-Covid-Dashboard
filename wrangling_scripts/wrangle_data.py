import pandas as pd
import plotly.graph_objs as go
import numpy as np

# Use this file to read in your data and prepare the plotly visualizations. The path to the data files are in
# `data/file_name.csv`


def prepare_data(weekdays_only = False):
    df = pd.read_csv('./data/daily_readings_sites_large.csv', parse_dates=[0])
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
            ['median']).reset_index()
    agg_df.columns = ['_'.join(tup) if tup[1] != '' else tup[0] 
                      for tup in list(agg_df.columns)]
    return agg_df, authority_dict



def get_diff_plot(df, authority_dict, col, species_name, species):
    
    df['before_lockdown'] = (df.date < pd.to_datetime('2020-03-23'))
    diff_df = df.groupby(['authority_id',
                              'before_lockdown'])[[col]].mean().unstack()
    diff_df.columns = ['rate_after','rate_before']
    diff_df['change'] = (diff_df.rate_after - diff_df.rate_before)/diff_df.rate_before.abs()
    diff_df['abs_change'] = diff_df.change.abs()
    diff_df = diff_df.sort_values(by='abs_change',
                                  ascending=False)[['change']].head(10).reset_index()
    diff_df['authority_name'] = diff_df.authority_id.apply(lambda x: authority_dict[x])
    
    max_val = np.max(diff_df.change.abs())
    
    fig = go.Figure(data=[
        go.Bar(y=diff_df['authority_name'], x=diff_df['change'],
               orientation='h')])

    fig.update_layout(
        width = 1000, height = 400,
        title_text = "Districts with greatest change in "+species_name+
        " after lockdown (March 23)",
        xaxis=dict(
            title='Average percent change in ' + species,
            titlefont_size=16,
            tickfont_size=14,
            range=(-max_val, max_val)
        ))
    return fig
    

def return_figures(species):
    """Creates four plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """
    def get_species_name(species, short=False):
        if species == "PM25":
            return "PM2.5" if short else "PM2.5 Particles"
        elif species == "PM10":
            return species if short else "PM10 Particles"
        elif species == "NO2":
            return species if short else "Nitrogen Dioxide (NO2)"
        else:
            return species if short else "Ozone (O3)"
        
    species_name = get_species_name(species)
    
    df, authority_dict = prepare_data(weekdays_only=False)
    
    col = species + '_median'
    
    
    barplot = get_diff_plot(df, authority_dict, col, species_name,
                            species)

    
    
    fig = go.Figure()
    authorities_full = df.isnull().groupby(
        df['authority_id'])[col].sum() < df.date.nunique()-10
    
    authority_ls = pd.Series(authorities_full.index[authorities_full])



    for authority_id in authority_ls:
         fig.add_trace(
            go.Scatter(
                x = df.date,
                y = df[df.authority_id == authority_id][col].rolling(5,
                                                                     center=True).mean(),
                name = authority_dict[authority_id],
                visible=True
            ))

    def create_layout_button(authority_id):
        return dict(label = authority_dict[authority_id],
                    method = 'update',
                    args = [{'visible': authority_ls.isin([authority_id]),
                             'title': authority_dict[authority_id],
                             'showlegend': True}])
    
    # button_all = dict(label = 'All',
    #                   method = 'update',
    #                   args = [{'visible': authority_ls.isin(authority_ls),
    #                            'title': 'All London Districts',
    #                            'showlegend':True}])

    fig.update_layout(
        title = dict(
            text=species_name + " Levels",
            y = 0.84,
            x = 0.5,
            xanchor = 'center',
            yanchor = 'top'),
        xaxis = dict(
            title_text = "Date",
            title_font = {"size": 15},
            title_standoff = 20),
        yaxis = dict(
            title_text = get_species_name(species, short=True) + " (µg/m³)",
            title_standoff = 25,
            title_font={"size":20}),
        height=400, width = 1000,
        updatemenus=[go.layout.Updatemenu(
            active = 0,
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.1,
            xanchor="left",
            y=1.25,
            yanchor="top",
            buttons =  list(authority_ls.map(
                lambda auth: create_layout_button(auth)))
            )
        ],
        annotations=[
        dict(text="District:", showarrow=False,
        x=0, y=1.18, xref='paper', yref='paper')
    ])
    
    figures= [fig, barplot]
        
    return figures


# def return_figure():
#     species_ls = ['NO2','O3','PM10','PM25']
#     figures = [return_figure(species) for species in species_ls]
    

    # return figures
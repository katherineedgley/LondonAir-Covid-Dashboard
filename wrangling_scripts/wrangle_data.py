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

agg_df, authority_dict = prepare_data()


def return_figures():
    """Creates four plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """

    # first chart plots arable land from 1990 to 2015 in top 10 economies 
    # as a line chart
    
    df, authority_dict = prepare_data()
    
    
    fig = go.Figure()
    authority_ls = pd.Series(df.authority_id.unique())
    fig.add_trace(
        go.Scatter(
            x = df.date,
            y = df[df.authority_id == authority_ls[0]]['NO2_median'],
            name = authority_dict[authority_ls[0]],
            visible=True))

    for authority_id in authority_ls[1:]:
        fig.add_trace(
            go.Scatter(
                x = df.date,
                y = df[df.authority_id == authority_id]['NO2_median'],
                name = authority_dict[authority_id],
                visible=False
            ))

    # button_all = dict(label = 'All',
    #                   method = 'update',
    #                   args = [{'visible': df.columns.isin(df.columns),
    #                            'title': 'All',
    #                            'showlegend':True}])

    def create_layout_button(authority_id):
        return dict(label = authority_dict[authority_id],
                    method = 'update',
                    args = [{'visible': authority_ls.isin([authority_id]),
                             'title': authority_dict[authority_id],
                             'showlegend': True}])

    fig.update_layout(
        height=400, width = 1000,
        updatemenus=[go.layout.Updatemenu(
            active = 0,
            buttons = list(authority_ls.map(
                lambda auth: create_layout_button(auth)))
            )
        ])
    
    # graph_one = []    
    # graph_one.append(
    #   go.Scatter(
    #   x = df['date'],
    #   y = df['NO2_median'],
    #   mode = 'lines'
    #   )
    # )

    # layout_one = dict(title = 'NO2',
    #             xaxis = dict(title = 'Date'),
    #             yaxis = dict(title = 'NO2'),
    #             updatemenus = [
    #                 dict(
    #                     buttons=list([
    #                         dict(
    #                             args=[])]))]
    #             )


# second chart plots ararble land for 2015 as a bar chart    
#     graph_two = []

#     graph_two.append(
#       go.Bar(
#       x = ['a', 'b', 'c', 'd', 'e'],
#       y = [12, 9, 7, 5, 1],
#       )
#     )

#     layout_two = dict(title = 'Chart Two',
#                 xaxis = dict(title = 'x-axis label',),
#                 yaxis = dict(title = 'y-axis label'),
#                 )


# # third chart plots percent of population that is rural from 1990 to 2015
#     graph_three = []
#     graph_three.append(
#       go.Scatter(
#       x = [5, 4, 3, 2, 1, 0],
#       y = [0, 2, 4, 6, 8, 10],
#       mode = 'lines'
#       )
#     )

#     layout_three = dict(title = 'Chart Three',
#                 xaxis = dict(title = 'x-axis label'),
#                 yaxis = dict(title = 'y-axis label')
#                        )
    
# # fourth chart shows rural population vs arable land
#     graph_four = []
    
#     graph_four.append(
#       go.Scatter(
#       x = [20, 40, 60, 80],
#       y = [10, 20, 30, 40],
#       mode = 'markers'
#       )
#     )

#     layout_four = dict(title = 'Chart Four',
#                 xaxis = dict(title = 'x-axis label'),
#                 yaxis = dict(title = 'y-axis label'),
#                 )
    
    # append all charts to the figures list
    figures = []
    figures.append(fig)
    # figures.append(dict(data=graph_two, layout=layout_two))
    # figures.append(dict(data=graph_three, layout=layout_three))
    # figures.append(dict(data=graph_four, layout=layout_four))

    return figures
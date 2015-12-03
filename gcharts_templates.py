'''
Created on Dec 1, 2015

@author: T-o-DD
'''

def monthly_checkin_combo (array_data, chartrow, chartcol):
    fn_txt= """

        var monthly_checkin_combo_data = new google.visualization.arrayToDataTable(%s , false);

        var monthly_checkin_combo_options = {'title':'Monthly Overall Checkins and New Users',
                  vAxis: {title: 'Checkins and New Users'},
                  hAxis: {title: 'Month'},
                  seriesType: 'bars',
                  series: {1: {type: 'line'}},
                  'width':700,
                  'height':400,
                  legend: { position: 'bottom', maxLines: 1 }
                    };

        var monthly_checkin_combo_chart = new google.visualization.ComboChart(document.getElementById('chart_div%d%d'));
        monthly_checkin_combo_chart.draw(monthly_checkin_combo_data, monthly_checkin_combo_options);


    """ % (array_data, chartrow, chartcol)

    return fn_txt


def checkins_per_location_bar (array_data, chartrow, chartcol):
    fn_txt= """

        var checkins_per_location_bar_data = new google.visualization.arrayToDataTable(%s , false);

        var checkins_per_location_bar_options = {'title':'Checkins per Location',
                  vAxis: {title: 'Location'},
                  hAxis: {title: 'Checkins'},
                  bar: {groupWidth: "80%"},
                  'width':700,
                  'height':400,
                  legend: { position: 'bottom', maxLines: 1 }
                    };

        var checkins_per_location_chart = new google.visualization.BarChart(document.getElementById('chart_div%d%d'));
        checkins_per_location_chart.draw(checkins_per_location_bar_data, checkins_per_location_bar_options);


    """ % (array_data, chartrow, chartcol)

    return fn_txt

def users_per_location_bar (array_data, chartrow, chartcol):
    fn_txt= """

        var users_per_location_bar_data = new google.visualization.arrayToDataTable(%s , false);

        var users_per_location_bar_options = {'title':'Users per Location',
                  vAxis: {title: 'Location'},
                  hAxis: {title: 'Users'},
                  bar: {groupWidth: "80%%"},
                  'width':700,
                  'height':400,
                  legend: { position: 'bottom', maxLines: 1 }
                    };

        var users_per_location_chart = new google.visualization.BarChart(document.getElementById('chart_div%d%d'));
        users_per_location_chart.draw(users_per_location_bar_data, users_per_location_bar_options);


    """ % (array_data, chartrow, chartcol)

    return fn_txt

def users_and_checkins_per_location_column (array_data, chartrow, chartcol):
    fn_txt= """

        var users_and_checkins_per_location_column_data = new google.visualization.arrayToDataTable( %s , false);

        var users_and_checkins_per_location_column_options = {'title':'Total Users and Checkins per Location',
                  vAxis: {title: 'Users and Checkins'},
                  hAxis: {title: 'Location'},
                  bar: {groupWidth: '80%%'},
                  'width':700,
                  'height':400,
                  legend: { position: 'bottom', maxLines: 1 }
                    };



        var users_and_checkins_per_location_column_chart = new google.visualization.ColumnChart(document.getElementById('chart_div%d%d'));
        users_and_checkins_per_location_column_chart.draw(users_and_checkins_per_location_column_data, users_and_checkins_per_location_column_options);


    """ % (array_data, chartrow, chartcol)

    return fn_txt

def time_between_visits_column (array_data, chartrow, chartcol):
    fn_txt= """

        var time_between_visits_column_data = new google.visualization.arrayToDataTable(%s , false);

        var time_between_visits_column_options = {'title':'Time Between Visits',
                  subtitle: 'From Loyal Members with 11 or more Visits',
                  vAxis: {title: 'Average Days Between Visits'},
                  hAxis: {title: 'Visit Number'},
                  'width':700,
                  'height':400,
                  legend: 'none'
                    };

        var time_between_visits_column_chart = new google.visualization.ColumnChart(document.getElementById('chart_div%d%d'));
        time_between_visits_column_chart.draw(time_between_visits_column_data, time_between_visits_column_options);


    """ % (array_data, chartrow, chartcol)

    return fn_txt

def avg_monthly_users_and_checkins_bubble (array_data, chartrow, chartcol):
    fn_txt= """

        var avg_monthly_users_and_checkins_bubble_data = new google.visualization.arrayToDataTable(%s , false);

        var avg_monthly_users_and_checkins_bubble_options = {'title':'Location Success: Average Monthly New Users and Checkins',
                  vAxis: {title: 'Average Monthly New Users'},
                  hAxis: {title: 'Average Monthly Checkins'},
                  'width':700,
                  'height':400,
                  bubble: {textStyle: {fontSize: 11}},
                  legend: 'none'
                    };

        var avg_monthly_users_and_checkins_bubble_chart = new google.visualization.BubbleChart(document.getElementById('chart_div%d%d'));
        avg_monthly_users_and_checkins_bubble_chart.draw(avg_monthly_users_and_checkins_bubble_data, avg_monthly_users_and_checkins_bubble_options);


    """ % (array_data, chartrow, chartcol)

    return fn_txt


def rewards_table (array_data, chartrow, chartcol):
    fn_txt= """

        var rewards_table_data = new google.visualization.arrayToDataTable(%s , false);

        var rewards_table_options = {'title':'Location Success: Average Monthly New Users and Checkins',
                  vAxis: {title: 'Average Monthly New Users'},
                  hAxis: {title: 'Average Monthly Checkins'},
                  'width':700,
                  'height':400,
                  bubble: {textStyle: {fontSize: 11}},
                  legend: 'none'
                    };

        var rewards_table_chart = new google.visualization.Table(document.getElementById('chart_div%d%d'));
        rewards_table_chart.draw(rewards_table_data, rewards_table_options);


    """ % (array_data, chartrow, chartcol)

    return fn_txt


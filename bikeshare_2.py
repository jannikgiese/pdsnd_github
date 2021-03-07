import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
WEEKDAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
filter_message = 'The analysed dataset consists of data from: \nCity: {} \nMonth: {} \nDay: {} \n'


def get_filter():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('\nWould you like to see data for Chicago, New York, or Washington?\n').strip().lower()
    if city == 'new york':
        city = 'new york city'

    while city not in CITY_DATA.keys():
        print('\nThe city you have entered is not in our list!')
        city = input('Please enter another one:\n').strip().lower()
        if city == 'new york':
            city = 'new york city' 

    # get user input for month (all, january, february, ... , june)
    month = input('\nThe data of which month would you like to analyze? (There is only data from January to June available) Type "all" if you don\'t want to filter on month.\n').strip().lower()
    
    while month not in MONTHS:
        print('\nThe month you have entered is not in our list!')
        month = input('Please enter another one:\n').strip().lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('\nThe data of which weekday would you like to analyze? Type "all" if you don\'t want to filter on weekday.\n').strip().lower()
    
    while day not in WEEKDAYS:
        print('\nThe day you have entered is not in our list!')
        day = input('Please enter another one:\n').strip().lower()

    print('-'*40)
    return city, month, day


def load_data(data_filter):
    """
    Loads data for the specified city, filters by month and day if applicable and 
    displays a dataset of 5 rows at a time if demanded by user.

    Args:
        (tuple) data_filter consisting of: 
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    city, month, day = data_filter

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTHS.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    

    new_dframe = df
    pd.set_option('display.max_columns',200)
    
    while True:
        show = input('\nWould you like to show the (next) 5 rows of the dataset? Enter yes or no.\n')
        if show.lower() == 'yes':
            print()
            print(new_dframe.head())
            new_dframe = new_dframe.drop(new_dframe.head().index)
        else:
            break

    print('-'*40)        
    return df

    
def time_stats(df, data_filter):
    """Displays statistics on the most frequent times of travel."""

    city, month, day = data_filter

    print('\nCalculating The Most Frequent Times of Travel...\n')
    print(filter_message.format(city.title(), month.title(), day.title()))
    start_time = time.time()

    # display the most common month
    # calcualtion only makes sense if data is not filtered on specific month
    if month == 'all':
        most_popular_month = df['month'].mode()[0]
        month_count = df['month'][df['month'] == most_popular_month].count()
        most_popular_month = MONTHS[df['month'].mode()[0] - 1].title()
        print('Most popular month: {}, Count: {}'.format(most_popular_month, month_count)) 
    
    # display the most common day of week
    # calcualtion only makes sense if data is not filtered on specific weekday
    if day == 'all':
        most_popular_weekday = df['day_of_week'].mode()[0]
        weekday_count = df['day_of_week'][df['day_of_week'] == most_popular_weekday].count()
        print('Most popular day: {}, Count: {}'.format(most_popular_weekday, weekday_count))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_popular_hour = df['hour'].mode()[0]
    hour_count = df['hour'][df['hour'] == most_popular_hour].count()
    print('Most popular hour: {}, Count: {}'.format(most_popular_hour, hour_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df, data_filter):
    """Displays statistics on the most popular stations and trip."""

    city, month, day = data_filter

    print('\nCalculating The Most Popular Stations and Trip...\n')
    print(filter_message.format(city.title(), month.title(), day.title()))
    start_time = time.time()

    # display most commonly used start station
    most_popular_start = df['Start Station'].mode()[0]
    start_count = df['Start Station'][df['Start Station'] == most_popular_start].count()
    print('Most popular start station: {}, Count: {}'.format(most_popular_start, start_count))

    # display most commonly used end station
    most_popular_end = df['End Station'].mode()[0]
    end_count = df['End Station'][df['End Station'] == most_popular_end].count()
    print('Most popular end station: {}, Count: {}'.format(most_popular_end, end_count))

    # display most frequent combination of start station and end station trip
    df['Trips'] = 'From ' + df['Start Station'] + ' to ' + df['End Station']
    most_popular_trip = df['Trips'].mode()[0]
    trip_count = df['Trips'][df['Trips'] == most_popular_trip].count()
    print('Most popular trip: {}, Count: {}'.format(most_popular_trip, trip_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df, data_filter):
    """Displays statistics on the total and average trip duration."""

    city, month, day = data_filter

    print('\nCalculating Trip Duration...\n')
    print(filter_message.format(city.title(), month.title(), day.title()))
    start_time = time.time()

    # display total travel time
    # new calculation as values in 'Trip Duration' are partly incorrect.
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Travel Time'] = df['End Time'] - df['Start Time']
    total_travel_time = df['Travel Time'].sum()
    print('Total travel time: {}'.format(total_travel_time))

    # display mean travel time
    mean_travel_time = df['Travel Time'].mean()
    print('Mean travel time: {}'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, data_filter):
    """Displays statistics on bikeshare users."""

    city, month, day = data_filter

    print('\nCalculating User Stats...\n')
    print(filter_message.format(city.title(), month.title(), day.title()))
    start_time = time.time()

    # Display counts of user types
    print('Breakdown of user types:')
    print(df['User Type'].value_counts())
    print()

    # Display counts of gender
    print('Breakdown of gender:')
    if 'Gender' in df.columns: 
        print(df['Gender'].value_counts())
        print()
    else:
        print('No gender information in dataset!')
        print()

    # Display earliest, most recent, and most common year of birth
    print('Birth year analysis:')
    if 'Birth Year' in df.columns:
        earliest_byear = int(df['Birth Year'].min())
        latest_byear = int(df['Birth Year'].max())
        most_common_byear = int(df['Birth Year'].mode()[0])
        print('Earliest year of birth: {} \nMost recent year of birth: {} \nMost common year of birth: {}'.format(earliest_byear, latest_byear, most_common_byear))
    else:
        print('No birth year information in dataset!')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        data_filter = get_filter()
        df = load_data(data_filter)

        time_stats(df, data_filter)
        station_stats(df, data_filter)
        trip_duration_stats(df, data_filter)
        user_stats(df, data_filter)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

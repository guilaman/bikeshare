import time
import sys
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Includes the option to close the program by inputting the keyword 'exit'.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data! You will be asked to input \
your\nchoices for the city and time period for which you want to display the data.\n\
You can close the program any time during the input questions by typing "exit".\n\
Once you have defined these filters, you will have the choice to first\n\
display some raw data, or to directly skip to the statistics summary.\n\n')
    # get user input for city (chicago, new york city, washington).
    # Use while loop to handle invalid inputs
    while True:
        city = input('Which city do you want to display data for?\nPlease type your \
choice among Chicago, New York City or Washington: \n').lower()
        if city == 'new york' or city == 'nyc':
            city = 'new york city'
        if city == 'exit':
            sys.exit()
        if city not in ['chicago', 'new york city', 'washington', 'new york', 'nyc']:
            print('It looks like the CITY NAME you entered isn\'t valid, please \
check \nthat the name you entered didn\'t contain any typos or abbreviations.')
        else:
            print('Got it, thanks!\n')
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('If you want to see data only for a particular month, \
please type which month between January and June,\notherwise type "all":\n').lower()
        if month == 'exit':
            sys.exit()
        if month not in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
            print('It looks like the MONTH NAME you entered isn\'t valid, please \
check \nthat the name you entered didn\'t contain any typos or abbreviations.')
        else:
            print('Got it, thanks!\n')
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('If you want to see data only for a particular day of the week, \
please type which day, otherwise type "all":\n').lower()
        if day == 'exit':
            sys.exit()
        if day not in ['monday', 'tuesday', 'wednesday', 'thursday',
        'friday', 'saturday', 'sunday', 'all']:
            print('It looks like the WEEKDAY NAME you entered isn\'t valid, please \
check \nthat the name you entered didn\'t contain any typos or abbreviations.')
        else:
            print('Got it, thanks!\n')
            break

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # use the input city to load the corresponing .csv file:
    df = pd.read_csv(CITY_DATA[city])
    # in order to apply the month and weekday filters, first convert the relevant time
    # column to datetime format and then extract month, weekday and hour to new columns:
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['weekday'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    '''TODO: CHECK THAT FILTERS ARE CORRECT'''
    # define the month and weekday filters:
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['weekday'] == day.title()]

    return df


def raw_data(df):
    while True:
        raw_choice = input('Would you like to display some raw data on the city and time period \
chosen?\nIf you do, please type "raw"; if instead you want to see statistics, type\
 "stats":\n').lower()
        if raw_choice == 'exit':
            sys.exit()
        if raw_choice == 'stats':
            break
        if raw_choice == 'raw':
            print_rows = 5
            last_row = print_rows
            print('\n', df.head(print_rows))
            while True:
                keep_printing = input('Type "more" to display more raw data, or "stats" to \
continue to the summaries:\n')
                if keep_printing == 'exit':
                    sys.exit()
                if keep_printing == 'stats':
                    break
                if keep_printing == 'more':
                    print(df[last_row : last_row + print_rows])
                    last_row += print_rows
                else:
                    print('Please make sure you typed the command correctly.')
            break
        else:
            print('Please make sure you typed the command correctly.')
    print('-'*40)

    
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    '''I refine the results for month and weekday when the user inputs "all"'''
    # display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    if len(df['month'].value_counts().index) > 1:
        print('The most common month of travel is {}.'
                .format(months[(df['month'].mode()[0]) - 1].title()))
    else:
        print('Filtering data for {}.'
                .format(months[(df['month'].mode()[0]) - 1].title()))
    # display the most common day of week
    if len(df['weekday'].value_counts().index) > 1:
        print('The most common day of travel in the week is {}.'
                .format(df['weekday'].mode()[0]))
    else:
        print('Filtering data for {}s.'
                .format(df['weekday'].mode()[0]))
    # display the most common start hour
    print('The most common hour of travel is {}.'.format(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most common start station is {}.'.format(df['Start Station'].mode()[0]))
    # display most commonly used end station
    print('The most common end station is {}.\n'.format(df['End Station'].mode()[0]))
    # display most frequent combination of start station and end station trip
    print('The most common combination of start and end stations is\n{};\n\n\
with the top fifteen most common start-to-end-trip combinations of stations \
in the selected time being:\n{}'
            .format((df['Start Station'] + ' to ' + df['End Station']).mode()[0],
            (df['Start Station'] + ' to ' + df['End Station']).value_counts().head(15)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    def secs_to_hrs(seconds):
        mins, secs = divmod(seconds, 60)
        hrs, mins = divmod(mins, 60)
        return '{} hours, {} minutes and {} seconds'.format(hrs, mins, secs)

    # display total travel time
    print('Total travel time of users of the service in the selected period was {},'
            .format(secs_to_hrs(int(df['Trip Duration'].sum().sum()))))
    print('and the total number of trips was {}.'
            .format(int(df['Trip Duration'].count())))
    # display mean travel time
    print('The mean travel time in the selected period was {}.\n'
            .format(secs_to_hrs(int(df['Trip Duration'].mean()))))

    # below is a filter for when the user chooses all months
    # and all weekdays that I choose not to use:
    # if len(df['month'].value_counts().index) > 1 and len(df['weekday'].value_counts().index) > 1:
        # Here I wanted to display the top fifteen longest trips in correct order,
        # the way I did it seems to work but I know there must be a better, cleaner way.
        # There seems to still be an issue with the sorting where two-digit numbers
        # appear always on top of the rest, but frankly I'm ok with this and
        # I have to keep moving foward with the course.
    print('It appears the longest travel time in the selected period was {};'
            .format(secs_to_hrs(int(df['Trip Duration'].max()))))
    print('the top fifteen longest trips being:\n{}'
            .format('\n'.join(sorted([secs_to_hrs(int(x))
                    for x in (np.sort(df['Trip Duration'])[-15:])], reverse=True))))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    df['User Type'].fillna('Other', inplace=True)
    print('The user type breakdown is the following:\n{}\n'
            .format(df['User Type'].value_counts()))
    # Display counts of gender
    '''Put gender & age filters inside if block to avoid crashing when city == washington'''
    if 'Gender' in df.columns:
        df['Gender'].fillna('Unknown', inplace=True)
        print('The breakdown by gender is the following:\n{}\n'
            .format(df['Gender'].value_counts()))
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('Some age statistics are:\n'
            '* earliest year of birth: {}\n'
            '* latest year of birth: {}\n'
            '* most common year of birth: {}'
            .format(int(df['Birth Year'].min()), int(df['Birth Year'].max()),
                int(df['Birth Year'].mode()[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if (restart.lower() != 'yes' and not restart.lower() == 'y'):
            break


if __name__ == "__main__":
	main()

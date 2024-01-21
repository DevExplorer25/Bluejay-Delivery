import pandas as pd

"""
Assumptions:
1. Shift refers to each row in the csv file
"""


def get_data(file_name: str) -> pd.DataFrame:
    """Reads in the data from the csv file and returns a pandas dataframe"""
    df = pd.read_csv('Assignment_Timecard.xlsx - Sheet1.csv')
    df = df.iloc[:, :-2]
    df.dropna(inplace=True)
    return df


def pretty_print(func):
    """Decorator function to print the name of the function"""
    def wrapper(*args, **kwargs):
        print('-'*50)
        print(func.__name__.replace('_', ' ').title() + ':\n')
        func(*args, **kwargs)
        print('-'*50)
    return wrapper


@pretty_print
def seven_consecutive_days(df: pd.DataFrame) -> pd.DataFrame:
    """Returns a dataframe of employees who have worked 7 consecutive days"""
    # group by `Employee Name` and `Position ID`
    df = df.groupby(['Employee Name', 'Position ID'])
    # iterate through each group
    for (name, position), group in df:
        # iterate through each row in the group
        set_of_dates = set()
        for i in range(len(group)):
            # add all the dates in the group to a list
            # group.iloc[i]['Time'] get only the date from the timestamp
            set_of_dates.add(
                int(group.iloc[i]['Time'].split()[0].split('/')[1]))

        # sort the list of dates
        sorted_dates = sorted(set_of_dates)

        has_worked = False
        consecutive_days = 1
        # iterate through the list of dates
        for i in range(1, len(sorted_dates)):
            # if the employee has worked 7 consecutive days
            if consecutive_days == 7:
                has_worked = True
                break
            # if the current date is one day after the previous date
            if sorted_dates[i] == sorted_dates[i-1] + 1:
                consecutive_days += 1
            else:
                consecutive_days = 0

        # if the employee has worked 7 consecutive days
        if has_worked:
            print(name, position)


# Who has worked for more than 14 hours in a single shift
@pretty_print
def more_than_14_hours(df: pd.DataFrame) -> pd.DataFrame:
    """Returns a dataframe of employees who have worked more than 14 hours in a single shift"""
    # group by `Employee Name` and `Position ID`
    df = df.groupby(['Employee Name', 'Position ID'])
    # iterate through each group
    for (name, position), group in df:

        has_worked_more_than_14_hours = False
        # iterate through each row in the group
        for i in range(len(group)):
            # if the employee has worked more than 14 hours in a single shift
            if int(group.iloc[i]['Timecard Hours (as Time)'].split(':')[0]) > 14:
                has_worked_more_than_14_hours = True
                break

        # if the employee has worked more than 14 hours in a single shift
        if has_worked_more_than_14_hours:
            print(name, position)


# who have less than 10 hours of time between shifts but greater than 1 hour
@pretty_print
def less_than_10_hours_but_greater_than_1(df: pd.DataFrame) -> pd.DataFrame:
    """Returns a dataframe of employees who have less than 10 hours of time between shifts but greater than 1 hour"""
    # group by `Employee Name` and `Position ID`
    df = df.groupby(['Employee Name', 'Position ID'])
    # iterate through each group
    for (name, position), group in df:

        has_less_than_10_hours = False
        # iterate through each row in the group
        for i in range(len(group)-1):
            # get the difference in hours between the current row and the next row
            difference = pd.to_datetime(
                group.iloc[i+1]['Time']) - pd.to_datetime(group.iloc[i]['Time Out'])
            # if the difference is less than 10 hours but greater than 1 hour
            if difference.seconds/3600 < 10 and difference.seconds/3600 > 1:
                has_less_than_10_hours = True
                break

        # if the employee has less than 10 hours of time between shifts but greater than 1 hour
        if has_less_than_10_hours:
            print(name, position)


if __name__ == '__main__':
    df = get_data('Assignment_Timecard.xlsx - Sheet1.csv')
    seven_consecutive_days(df)
    less_than_10_hours_but_greater_than_1(df)
    more_than_14_hours(df)

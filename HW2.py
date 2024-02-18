"""
Nalika Palayoor
Homework #2
Due 2/17
"""

import csv
import os
import seaborn as sns
import matplotlib.pyplot as plt
import re
import statistics
from scipy import stats



folder_path = "/Users/nalikapalayoor/Documents/S2 classes/DS2500/marathon_hw_data/"
FILES = [file for file in os.listdir(folder_path) if file.endswith('.csv')]


def read_csv(filename):
    ''' 
    given the name of a csv file, return its contents as a 2d list,
    including the header.
    '''
    data = []
    with open(filename, "r") as infile:
        csvfile = csv.reader(infile)
        for row in csvfile:
            data.append(row)
    
    return data

def remove_letters(lst):
    '''
    given a list of strings, return each element
    without the letters
    '''
    formatted = ['__' + re.sub(r'[^0-9]', '', i) for i in lst]
    
    return formatted


def col_to_lst(lst,col):
    
    ''' 
    given a 2D list (lst) and an integer column numnber (col),
    return a list containing all the values of the specified
    column number from each element of lst
    '''
    
    col_lst = []
    for element in lst:
        col_lst.append(element[col])
        
    return col_lst

def lst_of_cols(lst):
    '''
    given a 2D list, reorganize into 
    lists organized by column 
    (helper function for sums_cols)
    '''
    
    col = 0
    newlst = []
    while col < len(lst[0]):
        newlst.append(col_to_lst(lst,col))
        col += 1
        
    return newlst

def list_to_dict(lst):
    ''' 
    given a 2d list, create and return a dictionary
    where col 0 from each row is the key,
    and rest of row is the value
    '''
    dct = {}
    for row in lst:
        dct[row[0]] = row[1:]
    
    return dct


def time_string_to_list(time_str):
    '''
    given an H:MM:SS time, convert it to a list
    in the format [H,MM,SS]
    '''
    hours, minutes, seconds = [int(part) for part in time_str.split(':')]
    
    return [hours, minutes, seconds]


def convert_time_lst_to_sec(lst):
    '''
    works with time_string_to_list function to convert
    a [H, MM, SS] list to a  total number of seconds
    '''
    total_seconds = (3600 * lst[0]) + (60 * lst[1]) + (lst[2])
    
    return total_seconds

def find_avg(lst):
    '''
    given a list, return the average
    value of the list
    '''
    
    total = 0
    num_elements = 0
    
    for i in lst:
        total += i
        num_elements += 1
    
    avg = total / num_elements
    
    return avg

def seconds_to_clocktime(seconds):
    '''
    given an amount of seconds, return a time
    in the format H:MM:SS
    '''
    hours = seconds // 3600
    hours_remainder = seconds - hours * 3600
    minutes = hours_remainder // 60
    minutes_remainder = hours_remainder - minutes * 60
    seconds = round(minutes_remainder,2)
    
    return(str(int(hours)) + ":" + str(int(minutes)) + ":" + str(seconds)) 
    
def find_avg_time(lst):
    '''
    given a list of times, 
    calculate and return the mean time
    '''
    new_time_lst = []
    for time in lst:
        new_time_lst.append(time_string_to_list(time))
        
    # Initalize a new list where each of these elements will be converted to seconds
    seconds_lst = []
    for time_lst in new_time_lst:
        convert_time_lst_to_sec(time_lst)
        seconds_lst.append(convert_time_lst_to_sec(time_lst))
    
    # Find the average of all these elements
    seconds = find_avg(seconds_lst)
    
    return seconds_to_clocktime(seconds)

def which_year():
    '''
    Based on the year the user inputs, define "i"
    so that we can acsess the correct dictionary
    '''
    year = input("Which year do you want to know about?\n")  
    string = "__" + year 
    
    return string 

def find_dict(i):
    '''
    iterate through the given files a specified amount of times
    to get the dictionary in question
    '''
        
    twod_lst = read_csv(FILES[i])
    rearranged_list = lst_of_cols(twod_lst)
    dct = list_to_dict(rearranged_list)
    
    return dct
            
def remove_values_from_list(lst, val):
    '''
    Given a list and a specified value, 
    return the list with all occurences of the 
    value removed
    '''
    return [value for value in lst if value != val]    

def count_num_occur(lst,value):
    '''
    given a list and specified value, count 
    the number of occurences of the value in
    the list
    '''
    num = 0
    for i in lst:
        if i == value:
            num += 1
    
    return num
  
def years_and_sec_lst(column,string,FILES):
    '''
    given a column number and string to look for in
    that column, find the average time for all the rows
    that have the string. Create a list of years. return
    the list of seconds and the list of years as a dictionary. 
    '''
    seconds_lst = []
    years = remove_letters(FILES)


    for file in FILES:
        data = read_csv(file)
        total_seconds = 0
        count = 0
        
        for i in data:
            
            if i[column] == string:
                count += 1
                time_lst_format = time_string_to_list(i[13])
                time_seconds_format = convert_time_lst_to_sec(time_lst_format)
                total_seconds += time_seconds_format
        mean = total_seconds / count
        seconds_lst.append(mean)
    
    year_lst = [e[2:] for e in years]
    year_lst = [int(x) for x in year_lst]
    
    return {"year": year_lst, "seconds": seconds_lst}

 
def lin_regression(x_lst,y_lst):
    '''
    Given two lists, return the linear regression
    of the two lists
    '''

    lr = stats.linregress(x_lst,y_lst)
    
    # given an x value, compute the y value, using y = mx+b
    x = int(input("Enter the year you want a prediction for\n"))
    y = lr.slope * x + lr.intercept
    
    return y

def make_sec_list(num,string):
    '''
    given an index and string to look
    for in files, return a lst of the 
    times for only the specified string

    '''
    seconds_lst = []
    for file in FILES:
        data = read_csv(file)
        total_seconds = 0
        count = 0
        for i in data:
            
            if i[num] == string:
                count += 1
                time_lst_format = time_string_to_list(i[13])
                time_seconds_format = convert_time_lst_to_sec(time_lst_format)
                total_seconds += time_seconds_format
        mean = total_seconds / count
        seconds_lst.append(mean)
    
    return seconds_lst

def normalize(lst):
    '''
    given a list of numbers, return 
    a list of normalized numbers
    '''
    normal_lst = []
    maximum = max(lst)
    minimum = min(lst)
    for i in lst:
        new_num = (i-minimum)/(maximum-minimum)
        normal_lst.append(new_num)
        
    return normal_lst

def create_ln_chart(lst1,lst2,label1,label2):
    '''
    given 2 lists, create a double line graph with
    those 2 graphs over time
    '''
    years = remove_letters(FILES) 
    years_sorted = years.sort()
    print(years_sorted)
    y1 = lst1
    y2 = lst2
    
    
    plt.plot(years, y1, label = label1)
    plt.plot(years, y2, '-.', label = label2)
    plt.xticks(rotation=90)

    plt.xlabel("Year")
    plt.legend()
    plt.title(label1 + " and " + label2 + " over time")
    plt.show()

def mean_of_time_col():
    '''
    calculate the mean time for every year
    and return a list of each mean (in seconds)
    '''
    mean_finish_time = []
    
    # Iterate through each file
    for file in FILES:
    # Open the file using the csv module
        with open(file, 'r', newline='') as file:
            csv_reader = csv.reader(file)
        
            # Skip the header by advancing to the next row
            next(csv_reader)

            # Extract values from the specified column
            values = [row[13] for row in csv_reader]
            
            seconds_lst = []
            for i in values:
                lst = time_string_to_list(i)
                seconds = convert_time_lst_to_sec(lst)
                seconds_lst.append(seconds)

            # Calculate the median and append to the list
            mean = statistics.mean(seconds_lst)
            mean_finish_time.append(mean) 
        
    return mean_finish_time

def mean_lst():
    '''
    create a list of the mean finish time
    for every year
    '''
    mean_finish_time = []
    
    # Iterate through each file
    for file in FILES:
    # Open the file using the csv module
        with open(file, 'r', newline='') as file:
            csv_reader = csv.reader(file)
        
            # Skip the header by advancing to the next row
            next(csv_reader)

            # Extract values from the specified column
            values = [row[13] for row in csv_reader]
            
            seconds_lst = []
            for i in values:
                lst = time_string_to_list(i)
                seconds = convert_time_lst_to_sec(lst)
                seconds_lst.append(seconds)

            # Calculate the median and append to the list
            mean = statistics.mean(seconds_lst)
            mean_finish_time.append(mean)
            
    return mean_finish_time

def median_lst(column):
    '''
    given a column number, find the median value of
    that column for every file, and return the list
    of these values
    '''
    # create a list of the median age for each year
    median_ages = []

    # Iterate through each file
    for file in FILES:
    # Open the file using the csv module
        with open(file, 'r', newline='') as file:
            csv_reader = csv.reader(file)
        
            # Skip the header by advancing to the next row
            next(csv_reader)

            # Extract values from the specified column
            values = [float(row[column]) for row in csv_reader]

            # Calculate the median and append to the list
            median = statistics.median(values)
            median_ages.append(median)
    
    return median_ages
    

def main():
    
    # Create a 2D list with each runners information as a separate list in the list
    years = remove_letters(FILES)


# QUESTION 1: The average time for 2013 top 1000

    # Ask the user which year they want to know about
    print("1. In 2013, what was the mean finish time of the top 1000 runners?\n")
    i = years.index(which_year())
    
    # Get the dictionary based on the year provided
    thirteen_dct = find_dict(i)
    
    # creates a list of all the times from 2013
    thirteen_times = thirteen_dct['OfficialTime']
    
    # find the avg time
    print(find_avg_time(thirteen_times) + "\n")
    
    
# QUESTION 2: median age of the top 1000 runners in 2010
    
    # Ask the user which year they want to know about
    print("2. What is the median age of the top 1000 runners in 2010? \n")
    i = years.index(which_year())
    
    # Get the dictionary based on the year provided
    ten_dict = find_dict(i)
    
    # create a list of all the ages from 2010
    ten_ages = ten_dict['AgeOnRaceDay']
    
    # convert each element of the list to an int
    ten_ages_ints = []
    for i in ten_ages:
        ten_ages_ints.append(int(i))
    
    # find the average of all the elements in the ten_ages list
    #print(ten_ages_ints)
    print(str(int(statistics.median(ten_ages_ints))) + "\n")
    
    
# QUESTION 3: Country with most runners in 2023
    # Ask the user which year they want to know about
    print("3. Apart from the US, which country had the most runners in 2023?\n")
    i = years.index(which_year())
    
    # Get the dictionary based on the year provided
    twenthree_dict = find_dict(i)
    
    # Create a list of all the countrys from 2023
    twenthree_countries = twenthree_dict['CountryOfResName']
    
    # Remove all US from list
    new_lst = remove_values_from_list(twenthree_countries, "United States of America")
    mode = statistics.mode(new_lst)
    print(str(mode) + "\n")
    

# QUESTION 4: Women in top 1000 for 2021
    # Ask the user which year they want to know about
    print("4. How many women finished in the top 1000 in 2021?\n")
    i = years.index(which_year())
    
    # Get the dictionary based on the year provided
    twentyone_dict = find_dict(i)
    
    # Create a list of all the genders from 2021
    twentyone_genders = twentyone_dict['Gender']
    num_females = count_num_occur(twentyone_genders,'F')
    print(str(num_females) + "\n")
    
    
# QUESTION 5: R value for year vs mean finish time for women 
    print("5. What is the correlation (r-value) of year vs. the mean finish time of women in the top 1000?")
    women_dict = years_and_sec_lst(4,'F',FILES)
    women_years = women_dict["year"]
    women_seconds = women_dict["seconds"]
    R_women = statistics.correlation(women_years,women_seconds)

    print(str(round(R_women,4)) + "\n")
    

# QUESTION 6: R value for year vs mean finish of americans in top 1000
    print("6. What is the correlation (r-value) of year vs. the mean finish time of American runners in the top 1000?")
    usa_dict = years_and_sec_lst(9,'USA',FILES)
    usa_years = usa_dict["year"]
    usa_seconds = usa_dict["seconds"]
    R_usa = statistics.correlation(usa_years,usa_seconds)

    print(str(round(R_usa,4)) + "\n")
    
 
# QUESTION 7: 2020 race prediciton
    print("7. If the 2020 race had actually happened, what would you predict to be the mean finish time of Americans in the top 1000?")
    
    year_lst = [e[2:] for e in years]
    year_lst = [int(x) for x in year_lst]
    seconds_lst = make_sec_list(9,'USA')

    y = lin_regression(year_lst,seconds_lst)
    
    time_predict = seconds_to_clocktime(y)
    print("The predicted average finish time for that year would be " + str(time_predict))

# Plot 1: linear regression of year vs mean finish times of American runners in the top 1000
    
    # create a list of the mean USA finish time in hours
    usa_hours = [x/3600 for x in usa_seconds]
    
    # visualize the plot
    plot = sns.regplot(x = usa_years,y = usa_hours)
    plot.set_title('Year vs Mean USA Finish Time (Hours)')
    plot.set_xlabel('Year')
    plot.set_ylabel('Time in Hours')
    
# Plot 2: how median age and average finish times have changed over time
    
    mean_finish_time = mean_lst()  
    mean_finish_time_normal = normalize(mean_finish_time)

    median_ages = median_lst(3)  
    median_ages_normal = normalize(median_ages)
        
    sorted_median_ages_normal = [x for _,x in sorted(zip(years,median_ages_normal))]
    sorted_mean_finish_time_normal = [x for _,x in sorted(zip(years,mean_finish_time_normal))]
    create_ln_chart(sorted_mean_finish_time_normal,sorted_median_ages_normal,'Mean Finish Time','Median Age')   
    
if __name__ == "__main__":
    main()
    
    


    


import os
import filecmp
from dateutil.relativedelta import *
from datetime import date


def getData(file):
# get a list of dictionary objects from the file
# Input: file name
# Output: return a list of dictionary objects where
# the keys are from the first row in the data. and the values are each of the other rows
    input_file = open(file, "r")
    output = []

    headings = input_file.readline().split(",")

    num_columns = len(headings)
    line = input_file.readline()

    while line:
        row_dict = {}
        row = line.split(",")
        for i in range(num_columns):
            row_dict[headings[i].strip("\n")] = row[i].strip("\n")
        output.append(row_dict)
        line = input_file.readline()

    input_file.close()
    return output


def mySort(data,col):
# Sort based on key/column
# Input: list of dictionaries and col (key) to sort on
# Output: Return the first item in the sorted list as a string of just: firstName lastName
    sorted_list = sorted(data, key=lambda k: k[col])
    return sorted_list[0].get("First") + " " + sorted_list[0].get("Last")


def classSizes(data):
# Create a histogram
# Input: list of dictionaries
# Output: Return a list of tuples sorted by the number of students in that class in
# descending order
# [('Senior', 26), ('Junior', 25), ('Freshman', 21), ('Sophomore', 18)]
    class_dict = {}
    for row in data:
        class_name = row.get("Class")
        if class_name in class_dict:
            class_dict[class_name] += 1
        else:
            class_dict[class_name] = 1

    return sorted(list(class_dict.items()), key=lambda k: k[1], reverse=True)


def findMonth(a):
# Find the most common birth month form this data
# Input: list of dictionaries
# Output: Return the month (1-12) that had the most births in the data
    month_dict = {}
    for row in a:
        date = row.get("DOB")
        # Assumes m/d/y date format
        month = date.split("/")[0]

        if month in month_dict:
            month_dict[month] += 1
        else:
            month_dict[month] = 1

    return int(max(month_dict, key=month_dict.get))


def mySortPrint(a,col,fileName):
#Similar to mySort, but instead of returning single
#Student, the sorted data is saved to a csv file.
# as fist,last,email
#Input: list of dictionaries, col (key) to sort by and output file name
#Output: No return value, but the file is written
    sorted_list = sorted(a, key=lambda k: k[col])
    file = open(fileName, "w", newline="")

    for row in sorted_list:
        file.write(row.get("First"))
        file.write(",")
        file.write(row.get("Last"))
        file.write(",")
        file.write(row.get("Email"))
        file.write("\n")

    file.close()


def findAge(a):
# def findAge(a):
# Input: list of dictionaries
# Output: Return the average age of the students and round that age to the nearest
# integer.  You will need to work with the DOB and the current date to find the current
# age in years.
    ages = []
    today = date.today()
    for row in a:
        birthday = row.get("DOB").split("/")
        #birthday = datetime.date(date_list[2], date_list[0], date_list[1])
        ages.append(today.year - int(birthday[2]) - ((today.month, today.day) < (int(birthday[0]), int(birthday[1]))))

    total = 0
    for age in ages:
        total += age
    return int(round(float(total)/float(len(ages))))


################################################################
## DO NOT MODIFY ANY CODE BELOW THIS
################################################################

## We have provided simple test() function used in main() to print what each function returns vs. what it's supposed to return.
def test(got, expected, pts):
  score = 0;
  if got == expected:
    score = pts
    print(" OK ", end=" ")
  else:
    print (" XX ", end=" ")
  print("Got: ",got, "Expected: ",expected)
  return score


# Provided main() calls the above functions with interesting inputs, using test() to check if each result is correct or not.
def main():
    total = 0
    print("Read in Test data and store as a list of dictionaries")
    data = getData('P1DataA.csv')
    data2 = getData('P1DataB.csv')
    total += test(type(data),type([]),50)

    print()
    print("First student sorted by First name:")
    total += test(mySort(data,'First'),'Abbot Le',25)
    total += test(mySort(data2,'First'),'Adam Rocha',25)

    print("First student sorted by Last name:")
    total += test(mySort(data,'Last'),'Elijah Adams',25)
    total += test(mySort(data2,'Last'),'Elijah Adams',25)

    print("First student sorted by Email:")
    total += test(mySort(data,'Email'),'Hope Craft',25)
    total += test(mySort(data2,'Email'),'Orli Humphrey',25)

    print("\nEach grade ordered by size:")
    total += test(classSizes(data),[('Junior', 28), ('Senior', 27), ('Freshman', 23), ('Sophomore', 22)],25)
    total += test(classSizes(data2),[('Senior', 26), ('Junior', 25), ('Freshman', 21), ('Sophomore', 18)],25)

    print("\nThe most common month of the year to be born is:")
    total += test(findMonth(data),3,15)
    total += test(findMonth(data2),3,15)

    print("\nSuccessful sort and print to file:")
    mySortPrint(data,'Last','results.csv')
    if os.path.exists('results.csv'):
        total += test(filecmp.cmp('outfile.csv', 'results.csv'),True,20)

    print("\nTest of extra credit: Calcuate average age")
    total += test(findAge(data), 40, 5)
    total += test(findAge(data2), 42, 5)

    print("Your final score is " + str(total))

# Standard boilerplate to call the main() function that tests all your code
if __name__ == '__main__':
    main()

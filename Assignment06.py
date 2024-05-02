# -----------------------------------------------------------------
#
# Title: Assignment06.py
# Desc: This assignment demonstrates assignment05 and builds on it to use
#       functions, classes, and the separation of concerns pattern.
# Change Log: (Who, When, What)
# TMcGrew, 2024-04-26, Created script reusing code from my Assignment05
# TMcGrew, 2024-04-27, Put where it initially reads the json file into a function, breaks
#       where it shows menu and inputs menu choice into 2 functions instead of one
#       input statement, slightly changed how menu presents with more \n for spacing,
#       presenting current data in menu choice 2 now calls a function to display it,
#       registering a student and saving to file also now in a function
# TMcGrew, 2024-04-28, reconfigured functions to now have parameters and take arguments
#       instead of using only global variables.
# TMcGrew, 2024-04-29, reconfigured to use classes and methods and better separation of concerns
# TMcGrew, 2024-05-02, moved the data above the classes and added some missing params in docstrings
#       to some functions
# ------------------------------------------------------------------

# imports

import json
from json import JSONDecodeError

# -- data -- #

# constants

MENU: str = "\n --- Course Registration Program --- \n"
MENU += "Select from the following menu: \n"
MENU += "1. Register a Student for a Course \n"
MENU += "2. Show current data \n"
MENU += "3. Save data to a file \n"
MENU += "4. Exit the program \n"
MENU += "-------------------------------\n"

FILE_NAME: str = "Enrollments.json"

# variables

menu_choice: str = ""
students: list[dict[str, str]] = []  # table of student data (list of dictionaries)

# Presentation --------------------------------------- #
class IO:
    """
    A collection of presentation layer functions that manage user input and output

    ChangeLog: (Who, When, What)
    TMcGrew,04.29.2024,Created Class
    """

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        ''' This function displays a custom error messages to the user

        ChangeLog: (Who, When, What)
        TMcGrew,04.29.2024,Created function

        :param message: string with message data to display
        :param error: Exception object with technical message to display

        :return: None
        '''
        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message -- ")
            print(error, error.__doc__, type(error), sep='\n')

    @staticmethod
    def output_menu(menu: str):
        ''' This function displays a menu of choices to the user

        ChangeLog: (Who, When, What)
        TMcGrew,04.29.2024,Created function
        :param menu: string with menu of choices to display

        :return: None
        '''
        # Present the menu of choices
        print(menu)

    @staticmethod
    def input_menu_choice():
        ''' This function takes input from the user as to menu choice and sets the global
        menu_choice variable

        ChangeLog: (Who, When, What)
        TMcGrew,04.29.2024,Created function

        :return: None
        '''
        global menu_choice

        menu_choice = input('Your selection?: ')

    @staticmethod
    def output_student_courses(student_data: list):
        ''' This function takes a list of dictionaries and presents them formatted to the user

        ChangeLog: (Who, When, What)
        TMcGrew,04.29.2024,Created function
        :param student_data: list of dictionaries to display

        :return: None
        '''
        # Present the current data
        for student in students:
            print(f"{student['FirstName']} {student['LastName']} is registered for {student['CourseName']}.")


    @staticmethod
    def input_student_data(student_data=list):
        ''' This function takes a list of dictionaries and gets input from the user, formats
        it into a dictionary row and appends that list that was passed in

        ChangeLog: (Who, When, What)
        TMcGrew,04.29.2024,Created function

        :param student_data: list of dictionaries to input student data to by appending it

        :return: None
        '''
        student_first_name: str = ""
        student_last_name: str = ""
        course_name: str = ""
        student_row: dict[str, str] = {}  # one row of student data as a dictionary

        # variables capturing the input asked from the user
        try:
            student_first_name = input("Please enter your first name: ")
            if not student_first_name.isalpha():
                raise ValueError("The first name should not contain numbers.")

            student_last_name = input("Please enter your last name: ")
            if not student_last_name.isalpha():
                raise ValueError("The last name should not contain numbers.")

            course_name = input("Please enter the course name: ")

            # Add the student info to a dictionary using the student_row variable,
            # then add that dictionary to the student_data list to create a table of data
            # (a dictionary inside of a list).
            student_row = \
                {"FirstName": student_first_name, "LastName": student_last_name, "CourseName": course_name}
            student_data.append(student_row)  # important use .append here so gets passed in and not local reference

            # notify user to pick '3' now to fully register by saving it to a file
            print("\nThank you! Please now select '3' to save the registration to a file.\n")

        except ValueError as e:
            IO.output_error_messages(e)  # Prints the custom message

        except Exception as e:
            IO.output_error_messages("There was a non-specific error!\n",e)

# Processing --------------------------------------- #
class FileProcessor:
    """
    A collection of processing layer functions that work with Json files

    ChangeLog: (Who, When, What)
    TMcGrew,04.29.2024,Created Class
    """

    @staticmethod
    def read_data_from_file(file_name: str, student_data: list):
        """ This function reads a json file and loads it into a list
        both of which are passed in when called

         ChangeLog: (Who, When, What)
         TMcGrew,04.29.2024,Created function

        :param file_name: string data with name of file to read from
        :param student_data: list of dictionary rows to be filled with file data

        :return: None
         """

        file: TextIO = None

        try:

            # When the program starts, read the file data into a list of dictionaries (table)
            file = open(file_name, "r")
            # Extract the data from the file
            student_data += json.load(file)  # must import json above ###### here students? or student_data?
            # now student_data contains the parsed JSON data as a Python list of dictionaries
            # since passing in not just student_data = but += or could do loop through and append
            # it's a reference issue

        except FileNotFoundError as e:
            IO.output_error_messages("Text file must exist before running this script!\n",e)
            IO.output_error_messages("Creating file since it doesn't exist",e)
            file = open(file_name, "w")
            json.dump(student_data, file)  # putting empty list in upon creation
        except JSONDecodeError as e:
            IO.output_error_messages("Data in file isn't valid. Resetting it...",e)
            file = open(file_name, "w")
            json.dump(student_data, file)  # putting empty list in upon creation
        except Exception as e:
            IO.output_error_messages("There was a non-specific error!\n",e)
        finally:
            if file.closed == False:
                file.close()


    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        """ This function writes to a list of dictionaries to a json file both of which
        are passed in

         ChangeLog: (Who, When, What)
         TMcGrew,04.29.2024,Created function

        :param file_name: string data with name of file to write to
        :param student_data: list of dictionary rows to be writen to the file

        :return: None
         """

        file: TextIO = None

        try:
            # Save the data to a file
            # open() function to open a file in the desired mode ("w" for writing, "a' to append).
            file = open(file_name, "w")
            json.dump(student_data, file)
            # closes the file to save the information
            file.close()

            # shows user what it just wrote to the file
            for student in student_data:
                print(f"{student['FirstName']} {student['LastName']} is fully registered for {student['CourseName']}.")

            # print a line to get space after printing info and before menu again
            print('\n')

        except TypeError as e:
            IO.output_error_messages("Please check that the data is a valid JSON format\n",e)
        except Exception as e:
            IO.output_error_messages("Built-In Python error info: ",e)
        finally:
            if file.closed == False:
                file.close()



# Beginning of the main body of this script

# When the program starts, read the file data into a list of dictionaries (table)
FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=students)

# -- present and process the data -- #

# repeat the following tasks
while (menu_choice != "4"):
    # # Present the menu of choices
    IO.output_menu(menu=MENU)  # now in two different functions instead of MENU and input on one line
    IO.input_menu_choice()

    if (menu_choice == '1'):
        IO.input_student_data(student_data=students)
        continue

    elif (menu_choice == '2'):
        # Present the current data
        IO.output_student_courses(students)
        print("\nPlease now select '3' to save the registrations you entered to a file.\n")
        continue

    elif (menu_choice == '3'):
        FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students)
        continue

    # Stop the loop
    elif (menu_choice == '4'):
        exit()
        # break? or continue? or exit()?

    else:
        # spacing
        print()
        # They they picked something other than the options given
        print("Please pick one of the options.")
        # spacing
        print()
        continue

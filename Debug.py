import os, shutil
import ntpath
from ProblemSet import *
from Problem import *
from Figure import *
from Object import *


def delete_files_in_folder(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

def recheck_incorrect_global_images(list_of_paths,inc_same = False,inc_diff = False):
    if inc_diff:
        files = list_of_paths
        actual_directory = 'cs7637_project3/Test/global_diff/'
        error_directory = 'cs7637_project3/Test/global_diff_should_same/'
    elif inc_same:
        files = list_of_paths
        actual_directory = 'cs7637_project3/Test/global_same/'
        error_directory = 'cs7637_project3/Test/global_same_should_diff/'

    delete_files_in_folder(error_directory)

    not_found_paths = get_files_not_found(files)

    incorrect = []
    for path in not_found_paths:
        filename = get_filename_from_path(path)
        incorrect.append(get_problem_fig_obj_info_from_filename(filename))

        # move incorrect image to separate folder for analysis
        move_file_to_folder(actual_directory + filename,error_directory)

    return incorrect,not_found_paths

def get_incorrect_global_images(inc_same = False):
    if inc_same:
        files = read_list_from_file('cs7637_project3/Test/global_diff.txt')
        incorrect_directory = 'cs7637_project3/Test/global_same/'
        correct_directory = 'cs7637_project3/Test/global_diff/'
        error_save_directory = 'cs7637_project3/Test/global_same_should_diff/'
    else:
        files = read_list_from_file('cs7637_project3/Test/global_same.txt')
        incorrect_directory = 'cs7637_project3/Test/global_diff/'
        correct_directory = 'cs7637_project3/Test/global_diff/'
        error_save_directory = 'cs7637_project3/Test/global_diff_should_same/'

    incorrect = []
    incorrect_paths = []

    for path in files:
        path = path.rstrip('\n')
        filename = get_filename_from_path(path)
        isCorrectFolder = os.path.isfile(correct_directory + filename)
        isIncorrectFolder = os.path.isfile(incorrect_directory + filename)
        # isErrorFolder = os.path.isfile(error_save_directory + filename)

        if not isCorrectFolder and not isIncorrectFolder:
            continue
        elif isIncorrectFolder:
            incorrect_paths.append(incorrect_directory + filename)
            incorrect.append(get_problem_fig_obj_info_from_filename(filename))
            # move_file_to_folder(incorrect_directory + filename,error_save_directory)
            shutil.copyfile(incorrect_directory+filename,error_save_directory + filename)
    return incorrect,incorrect_paths

def read_list_from_file(file):
    ## Open the file with read only permit
    f = open(file, "r")

    ## use readlines to read all lines in the file
    ## The variable "lines" is a list containing all lines
    lines = f.readlines()

    ## close the file after reading the lines.
    f.close()

    return lines




def get_files_not_found(files):
    not_found = []
    for path in files:
        path = path.rstrip('\n')
        if not os.path.isfile(path):
            not_found.append(path)

    return not_found

def get_files_found(files):
    found = []
    for path in files:
        path = path.rstrip('\n')
        if os.path.isfile(path):
            found.append(path)

    return found

def get_filename_from_path(path):
    return os.path.split(path)[1]

def get_problem_fig_obj_info_from_filename(filename):
    filename = filename.split('_')
    filename[-1] = filename[-1].split('.')[0]
    info = {"problem":filename[0],
            "figure1":filename[1],
            "figure2":filename[2],
            "object1":filename[3],
            "object2":filename[4],
            }
    return info

def move_file_to_folder(file,folder):
    filename = get_filename_from_path(file)
    src = file
    dst = folder + filename
    if os.path.isfile(src):
        os.rename(src,dst)


def run_equal_to_from_list(incorrect_dict):
    for inc in incorrect_dict:
        # print "running",inc['problem'],inc['figure1']+inc['figure2'],inc['object1']+"-" +inc['object2']
        o1 = get_specific_object(inc['problem'],inc['figure1'],inc['object1'])
        o2 = get_specific_object(inc['problem'],inc['figure2'],inc['object2'])
        Object.is_equal_object_comparison(o1,o2)

def run_equal_to_specific_problem(problem_name):
    p = get_specific_problem(problem_name)
    p = Problem(p)


def get_specific_problem_set(problem_set_name):
    return ProblemSet(problem_set_name)


def get_specific_problem(problem_name):
    ps = problem_name.split('-')[0]
    ps = ps.replace("Problem","Problems")
    for problem in get_specific_problem_set(ps).problems:
            if problem.name == problem_name:
                return problem


def get_specific_figure(problem_name,figure_name):
    p = get_specific_problem(problem_name)
    for fig in p.figures.itervalues():
        if fig.name == figure_name:
            return Figure(fig,problem_name)

def get_specific_object(problem_name,figure_name,object_name):
    f = get_specific_figure(problem_name,figure_name)
    for obj in f.objects:
        if obj.name == object_name:
            return obj


def get_correct_global_images():
    files1 = read_list_from_file('cs7637_project3/Test/global_same.txt')
    files2 = read_list_from_file('cs7637_project3/Test/global_diff.txt')

    found1 = get_files_found(files1)
    found2 = get_files_found(files2)
    found_paths = found1+found2

    correct = []
    for path in found_paths:
        filename = get_filename_from_path(path)
        correct.append(get_problem_fig_obj_info_from_filename(filename))

    return correct,found_paths
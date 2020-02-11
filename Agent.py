# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Numpy and uncomment this line to access matrix operations.
import numpy as np
from Problem import Problem
from SolverD import SolverD
from SolverE import SolverE

class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        self.verbose = True  # print debug messages
        pass

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return a list representing its
    # confidence on each of the answers to the question: for example 
    # [.1,.1,.1,.1,.5,.1] for 6 answer problems or [.3,.2,.1,.1,0,0,.2,.1] for 8 answer problems.
    #
    # In addition to returning your answer at the end of the method, your Agent
    # may also call problem.checkAnswer(givenAnswer). The parameter
    # passed to checkAnswer should be your Agent's current guess for the
    # problem; checkAnswer will return the correct answer to the problem. This
    # allows your Agent to check its answer. Note, however, that after your
    # agent has called checkAnswer, it will *not* be able to change its answer.
    # checkAnswer is used to allow your Agent to learn from its incorrect
    # answers; however, your Agent cannot change the answer to a question it
    # has already answered.
    #
    # If your Agent calls checkAnswer during execution of Solve, the answer it
    # returns will be ignored; otherwise, the answer returned at the end of
    # Solve will be taken as your Agent's answer to this problem.
    #
    # Make sure to return your answer *as a python list* at the end of Solve().
    # Returning your answer as a string may cause your program to crash.
    def Solve(self, problem):
        self.problem = Problem(problem)
        # self.print_problem_info()

        if self.problem.problemType == "2x2":
            return [1.,1.,1.,1.,1.,1.]
        if self.problem.problemType == "3x3" and self.problem.hasVerbal:
            solverE = SolverE(self.problem)
            anAnswer = solverE.solve()
            if solverE.total_count == 0:
                solverD = SolverD(self.problem)
                myAnswer = solverD.solve()
            else:
                myAnswer = anAnswer
        if self.problem.problemType == "3x3" and not self.problem.hasVerbal:
            if "D-" in self.problem.name:
                solverD = SolverD(self.problem)
                myAnswer = solverD.solve()
            elif "E-" in self.problem.name:
                solverE = SolverE(self.problem)
                myAnswer = solverE.solve()
            else:
                solverE = SolverE(self.problem)
                anAnswer = solverE.solve()
                if solverE.total_count == 0:
                    solverD = SolverD(self.problem)
                    myAnswer = solverD.solve()
                else:
                    myAnswer = anAnswer


        # self.test_correct_answer(myAnswer)

        return myAnswer

    def debug(self, msg):
        if self.verbose == True:
            print msg

    def print_problem_info(self):
        # Problem Title
        self.debug("=================================")
        self.debug(self.problem.name)
        self.debug(self.problem.problemType)
        self.debug("=================================")

        if self.problem.hasVisual:
            self.debug('hasVisual == True')
        if self.problem.hasVerbal:
            self.debug('hasVerbal == True')

        self.debug("=================================")

    def test_correct_answer(self,answer = [.125,.125,.125,.125,.125,.125,.125,.125]):
        myAnswer = list(answer)


        test = { "Basic Problem B-01":2,
                 "Basic Problem B-02":5,
                 "Basic Problem B-03":1,
                 "Basic Problem B-04":3,
                 "Basic Problem B-05":4,
                 "Basic Problem B-06":5,
                 "Basic Problem B-07":6,
                 "Basic Problem B-08":6,
                 "Basic Problem B-09":5,
                 "Basic Problem B-10":3,
                 "Basic Problem B-11":1,
                 "Basic Problem B-12":1,
                 "Basic Problem C-01":3,
                 "Basic Problem C-02":4,
                 "Basic Problem C-03":4,
                 "Basic Problem C-04":8,
                 "Basic Problem C-05":3,
                 "Basic Problem C-06":7,
                 "Basic Problem C-07":2,
                 "Basic Problem C-08":5,
                 "Basic Problem C-09":2,
                 "Basic Problem C-10":7,
                 "Basic Problem C-11":4,
                 "Basic Problem C-12":8,
                 "Basic Problem D-01":3,
                 "Basic Problem D-02":1,
                 "Basic Problem D-03":3,
                 "Basic Problem D-04":1,
                 "Basic Problem D-05":7,
                 "Basic Problem D-06":1,
                 "Basic Problem D-07":1,
                 "Basic Problem D-08":4,
                 "Basic Problem D-09":3,
                 "Basic Problem D-10":1,
                 "Basic Problem D-11":3,
                 "Basic Problem D-12":3,
                 "Basic Problem E-01":1,
                 "Basic Problem E-02":7,
                 "Basic Problem E-03":2,
                 "Basic Problem E-04":8,
                 "Basic Problem E-05":5,
                 "Basic Problem E-06":8,
                 "Basic Problem E-07":3,
                 "Basic Problem E-08":1,
                 "Basic Problem E-09":7,
                 "Basic Problem E-10":8,
                 "Basic Problem E-11":5,
                 "Basic Problem E-12":6}

        print myAnswer
        if self.problem.name in test.keys():
            correct_answer = int(test[self.problem.name])


            if myAnswer[correct_answer-1] < 1:
                myAnswer[correct_answer-1] = -myAnswer[correct_answer-1]
                self.debug('ERROR: Answer in '+self.problem.name)
                self.debug('       Percentage Correct: ' + str(answer))
                self.debug('')

    def test_global_object_count(self):
        test = {"Basic Problem B-01":6,
                 "Basic Problem B-02":5,
                 "Basic Problem B-03":6,
                 "Basic Problem B-04":6,
                 "Basic Problem B-05":4,
                 "Basic Problem B-06":6,
                 "Basic Problem B-07":6,
                 "Basic Problem B-08":6,
                 "Basic Problem B-09":6,
                 "Basic Problem B-10":4,
                 "Basic Problem B-11":4,
                 "Basic Problem B-12":5,
                 "Basic Problem C-01":11,
                 "Basic Problem C-02":7,
                 "Basic Problem C-03":2,
                 "Basic Problem C-04":9,
                 "Basic Problem C-05":2,
                 "Basic Problem C-06":9,
                 "Basic Problem C-07":2,
                 "Basic Problem C-08":2,
                 "Basic Problem C-09":12,
                 "Basic Problem C-10":4,
                 "Basic Problem C-11":1,
                 "Basic Problem C-12":13,
                 "Basic Problem D-01":6,
                 "Basic Problem D-02":8,
                 "Basic Problem D-03":3,
                 "Basic Problem D-04":6,
                 "Basic Problem D-05":8,
                 "Basic Problem D-06":6,
                 "Basic Problem D-07":8,
                 "Basic Problem D-08":10,
                 "Basic Problem D-09":9,
                 "Basic Problem D-10":10,
                 "Basic Problem D-11":8,
                 "Basic Problem D-12":3,
                 "Basic Problem E-01":9,
                 "Basic Problem E-02":11,
                 "Basic Problem E-03":1,
                 "Basic Problem E-04":9,
                 "Basic Problem E-05":8,
                 "Basic Problem E-06":9,
                 "Basic Problem E-07":5,
                 "Basic Problem E-08":12,
                 "Basic Problem E-09":8,
                 "Basic Problem E-10":17,
                 "Basic Problem E-11":16,
                 "Basic Problem E-12":2}

        if self.problem.name in test.keys():
            if self.problem.global_objects_count != test[self.problem.name]:
                self.debug('ERROR: Global Count in '+self.problem.name)
                self.debug('       ' + str(self.problem.global_objects_count) + " should be " + str(test[self.problem.name]))
                self.debug('')

    def test_global_shape_count(self):
        test = { "Basic Problem B-01":6,
                 "Basic Problem B-02":3,
                 "Basic Problem B-03":2,
                 "Basic Problem B-04":1,
                 "Basic Problem B-05":2,
                 "Basic Problem B-06":1,
                 "Basic Problem B-07":1,
                 "Basic Problem B-08":2,
                 "Basic Problem B-09":2,
                 "Basic Problem B-10":2,
                 "Basic Problem B-11":3,
                 "Basic Problem B-12":1,
                 "Basic Problem C-01":3,
                 "Basic Problem C-02":2,
                 "Basic Problem C-03":1,
                 "Basic Problem C-04":6,
                 "Basic Problem C-05":2,
                 "Basic Problem C-06":1,
                 "Basic Problem C-07":2,
                 "Basic Problem C-08":1,
                 "Basic Problem C-09":8,
                 "Basic Problem C-10":3,
                 "Basic Problem C-11":1,
                 "Basic Problem C-12":9,
                 "Basic Problem D-01":3,
                 "Basic Problem D-02":3,
                 "Basic Problem D-03":3,
                 "Basic Problem D-04":5,
                 "Basic Problem D-05":3,
                 "Basic Problem D-06":4,
                 "Basic Problem D-07":4,
                 "Basic Problem D-08":2,
                 "Basic Problem D-09":3,
                 "Basic Problem D-10":7,
                 "Basic Problem D-11":2,
                 "Basic Problem D-12":3,
                 "Basic Problem E-01":5,
                 "Basic Problem E-02":8,
                 "Basic Problem E-03":1,
                 "Basic Problem E-04":1,
                 "Basic Problem E-05":4,
                 "Basic Problem E-06":5,
                 "Basic Problem E-07":4,
                 "Basic Problem E-08":6,
                 "Basic Problem E-09":4,
                 "Basic Problem E-10":7,
                 "Basic Problem E-11":1,
                 "Basic Problem E-12":1}

        if self.problem.name in test.keys():
            if self.problem.global_shapes_count != test[self.problem.name]:
                self.debug('ERROR: Global Shape Count in '+self.problem.name)
                self.debug('       ' + str(self.problem.global_shapes_count) + " should be " + str(test[self.problem.name]))
                self.debug('')



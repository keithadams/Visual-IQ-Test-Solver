from Figure import Figure
from PIL import Image
import os,sys,shutil

class Problem:
    def __init__(self,problem):
        self.verbose = True
        self.name = problem.name
        self.problemType = problem.problemType

        self.figures = {}
        for fig in problem.figures.itervalues():
            self.figures[fig.name] = Figure(fig,self.name)

        self.hasVisual = problem.hasVisual
        self.hasVerbal = problem.hasVerbal
        self.global_objects = {}
        self.set_global_objects()
        self.global_objects_count = len(self.global_objects)


    def debug(self,msg):
        if self.verbose == True:
            print msg


    def set_global_objects(self):
        for fig in self.figures.itervalues():
            for obj in fig.objects:
                self.add_unique_global_object(obj)

    def set_global_shapes(self):
        for go in self.global_objects.itervalues():
            self.add_unique_global_shape(go)

    def add_unique_global_object(self,obj):

        # if first object, add to global objects
        if len(self.global_objects) == 0:
            self.global_objects[(obj.figure_name,obj.name)] = obj
            obj.set_global_object_index((obj.figure_name,obj.name))
            return


        # check if obj is matches any globals EXACTLY
        for global_object in self.global_objects.itervalues():
            if global_object.is_equal_object_comparison(global_object,obj):
                obj.set_global_object_index((global_object.figure_name,global_object.name))
                return

        self.global_objects[(obj.figure_name,obj.name)] = obj
        obj.set_global_object_index((obj.figure_name,obj.name))

    def add_unique_global_shape(self,obj):

        # if first shape, add to global shapes
        if len(self.global_shapes) == 0:
            self.global_shapes[(obj.figure_name,obj.name)] = obj
            obj.set_global_shape_index((obj.figure_name,obj.name))
            return

        # check if obj matches any global shapes
        for global_shape in self.global_shapes.itervalues():
            if global_shape.is_equal_shape_comparison(global_shape,obj):
                obj.set_global_shape_index((global_shape.figure_name,global_shape.name))
                return

        self.global_shapes[(obj.figure_name,obj.name)] = obj
        obj.set_global_shape_index((obj.figure_name,obj.name))

    def save_object_images(self):
        for fig in self.figures.itervalues():
            for i in range(len(fig.objects)):
                obj = fig.objects[i]
                filename = self.name + '_' + fig.name + '_' + str(i)
                obj.img_cropped.save('Test/' + filename + '.png',"PNG")

    @classmethod
    def init_problem_directory(cls):
        folder = "Test/Problems/"

        cls.make_directory(folder)

        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)

    def save_global_shape_images(self):
        path = "Test/Problems/" + self.name
        self.make_directory(path)

        path = path + "/global_shapes/"
        self.make_directory(path)

        for gs in self.global_shapes.itervalues():
            filename = gs.problem_name + '_' + gs.figure_name + '_' + gs.name
            gs.img_cropped.save(path + filename + '.png',"PNG")

    @classmethod
    def make_directory(cls,directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    def convert2to3(self):
        self.figures
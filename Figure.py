from Object import Object
from ImageProcessing import *

class Figure:
    def __init__(self,figure,problem_name,init_images=True):
        self.problem_name = problem_name
        self.verbose = True
        self.name = figure.name
        self.img_uncropped = self.load_image(figure.visualFilename)
        self.objects = self.get_objects(self.img_uncropped)
        self.object_count = len(self.objects)

        self.img_cropped = crop_to_bbox(self.img_uncropped)

        self.size = self.img_cropped.size
        self.area = self.size[0] * self.size[1]
        self.center = get_center(self.img_uncropped)

        # PIL ImageStat
        self.stat = ImageStat.Stat(self.img_cropped)
        self.stat_extrema = self.stat.extrema                      # pretty useless (0,255)
        self.stat_count = self.stat.count                          # just number of pixels total (width * height)
        self.stat_sum = self.stat.sum
        self.stat_sum2 = self.stat.sum2
        self.stat_mean = self.stat.mean
        self.stat_median = self.stat.median
        self.stat_rms = self.stat.rms
        self.stat_var = self.stat.var
        self.stat_stddev = self.stat.stddev
        self.stat_black_pixel_count = get_black_pixel_count(self.img_cropped)
        self.stat_black_pixel_percent = get_black_pixel_percent(self.img_cropped)
        self.stat_white_pixel_count = self.stat_sum[0]/255
        self.stat_white_pixel_percent = self.stat_white_pixel_count / self.stat_count[0]

    def debug(self,msg):
        if self.verbose == True:
            print msg

    def load_image(self,path):
        return self.init_img(Image.open(path))

    def init_img(self,img):
        img = img.point(lambda p: p > 1 and 255)   # tried because it separates objects better
        img = img.convert("1")
        return img

    def get_objects(self,img):
        object_images = get_unique_images(img)

        objects = []

        for label,object_img in object_images.iteritems():
            objects.append(Object(object_img,self.problem_name,self.name,label))

        return objects

        for label,obj in objs.iteritems():
            objs[label] = self.invert(obj).convert("1")
        return objs



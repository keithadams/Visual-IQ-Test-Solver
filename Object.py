from ImageProcessing import *

class Object:
    def __init__(self,object_img,problem_name,figure_name,object_name):
        self.name = str(object_name)
        self.problem_name = problem_name
        self.figure_name = figure_name

        self.verbose = True
        self.global_object_index = -1
        self.global_shape_index = -1
        self.img_uncropped = object_img
        self.img_cropped = crop_to_bbox(object_img)

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

    # global object that matches exactly
    def set_global_object_index(self,ind):
        if self.global_object_index != -1:
            self.debug('ERROR set global object index')
            exit()

        self.global_object_index = ind

    # global shape that matches (regardless of transformations)
    def set_global_shape_index(self,ind):
        if self.global_shape_index != -1:
            self.debug('ERROR set global object index')
            exit()

        self.global_object_index = ind

    # shows cropped version of object image
    def show(self):
        self.img_cropped.show()

    @classmethod
    def is_equal_object_comparison(cls,obj1,obj2):
        return Object.is_equal_image_comparison(obj1.img_uncropped,obj2.img_uncropped)

    # get dict of values needed to compare if images are equal
    @classmethod
    def get_image_stat_comparison_dict(cls,img1_uncropped, img2_uncropped):
        stat = {}

        img1_cropped = crop_to_bbox(img1_uncropped)
        img2_cropped = crop_to_bbox(img2_uncropped)

        # cropped stats
        img1_stat = ImageStat.Stat(img1_cropped)
        img2_stat = ImageStat.Stat(img2_cropped)
        img1_area = img1_cropped.size[0] * img1_cropped.size[1]
        img2_area = img2_cropped.size[0] * img2_cropped.size[1]
        img1_black_pixel_count = get_black_pixel_count(img1_cropped)
        img2_black_pixel_count = get_black_pixel_count(img2_cropped)
        img1_black_pixel_percent = get_black_pixel_percent(img1_cropped)
        img2_black_pixel_percent = get_black_pixel_percent(img2_cropped)

        # uncropped stats
        img1_center = get_center(img1_uncropped)
        img2_center = get_center(img2_uncropped)

        stat['mean_diff_abs_val'] = abs(img1_stat.mean[0]-img2_stat.mean[0])
        stat['mean_diff_normed'] = stat['mean_diff_abs_val'] / 255
        stat['rms'] = rmsdiff(img1_cropped,img2_cropped)
        stat['width_diff_abs_val'] = abs(img1_cropped.size[0]-img2_cropped.size[0])
        stat['height_diff_abs_val'] = abs(img1_cropped.size[1]-img2_cropped.size[1])
        stat['area_ratio'] = float(min(img1_area,img2_area))/max(img1_area,img2_area)
        stat['bp_pixel_diff'] = abs(img1_black_pixel_count-img2_black_pixel_count)
        stat['center_x_diff'] = abs(img1_center[0]-img2_center[0])
        stat['center_y_diff'] = abs(img1_center[1]-img2_center[1])
        stat['mean_diff_squared'] = (img1_stat.mean[0]-img2_stat.mean[0])**2
        stat['bp_percent_diff'] = abs(img1_black_pixel_percent-img2_black_pixel_percent)
        stat['rms_diff_normed'] = abs(img1_stat.rms[0]-img2_stat.rms[0])/255
        stat['var_diff'] = abs(img1_stat.var[0]-img2_stat.var[0])
        stat['std_dev_diff'] = abs(img1_stat.stddev[0] - img2_stat.stddev[0])
        if img1_stat.stddev[0] > 0 or img2_stat.stddev[0] > 0:
            std_dev_ratio = float(min(img1_stat.stddev[0],img2_stat.stddev[0]))/max(img1_stat.stddev[0],img2_stat.stddev[0])
        else:
            std_dev_ratio = 0.0

        return stat

    @classmethod
    def is_equal_image_comparison(cls,img1_uncropped,img2_uncropped):
        stat = Object.get_image_stat_comparison_dict(img1_uncropped,img2_uncropped)
        return Object.vision_model(stat)

    @classmethod
    def vision_model(cls,stat_dict):
        stat = stat_dict

        mean_diff_normed = stat['mean_diff_normed']
        rms = stat['rms']
        width_diff_abs_val = stat['width_diff_abs_val']
        height_diff_abs_val = stat['height_diff_abs_val']
        area_ratio = stat['area_ratio']
        bp_pixel_diff = stat['bp_pixel_diff']
        center_x_diff = stat['center_x_diff']
        center_y_diff = stat['center_y_diff']

        if bp_pixel_diff <= 54:
            if rms <= 72.92663:
                if height_diff_abs_val <= 10:
                    if rms <= 55.272194:
                        isEqual = True
                    elif rms > 55.272194:
                        if center_x_diff <= 0:
                            if mean_diff_normed <= 0.00153:
                                isEqual = False
                            elif mean_diff_normed > 0.00153:
                                isEqual = True
                        elif center_x_diff > 0:
                            isEqual = True
                elif height_diff_abs_val > 10:
                    isEqual = False
            elif rms > 72.92663:
                if rms <= 100.983025:
                    if center_y_diff <= 5.5:
                        if rms <= 76.447296:
                            if rms <= 76.095622:
                                isEqual = False
                            elif rms > 76.095622:
                                isEqual = True
                        elif rms > 76.447296:
                            isEqual = False
                    if center_y_diff > 5.5:
                        if area_ratio <= 0.998264:
                            isEqual = True
                        elif area_ratio > 0.998264:
                            isEqual = False
                elif rms > 100.983025:
                    if center_x_diff <= 0.5:
                        if center_y_diff <= 0.5:
                            if center_y_diff <= 0:
                                if bp_pixel_diff <= 1:
                                    if mean_diff_normed <= 0.000036:
                                        isEqual = False
                                    elif mean_diff_normed > 0.000036:
                                        isEqual = True
                                elif bp_pixel_diff > 1:
                                    isEqual = False
                            elif center_y_diff > 0:
                                if area_ratio <= 0.987055:
                                    if area_ratio <= 0.963967:
                                        isEqual = False
                                    elif area_ratio > 0.963967:
                                        isEqual = True
                                elif area_ratio > 0.987055:
                                    isEqual = False
                        elif center_y_diff > 0.5:
                            isEqual = False
                    elif center_x_diff > 0.5:
                        isEqual = False
        elif bp_pixel_diff > 54:
            if mean_diff_normed <= 0.013764:
                if width_diff_abs_val <= 1:
                    if rms <= 60.681971:
                        if height_diff_abs_val <= 27:
                            isEqual = True
                        elif height_diff_abs_val > 27:
                            isEqual = False
                    elif rms > 60.681971:
                        isEqual = False
                elif width_diff_abs_val > 1:
                    isEqual = False
            elif mean_diff_normed > 0.013764:
                isEqual = False

        return isEqual

    @classmethod
    def is_equal_shape_comparison(cls,obj1,obj2):

        isEqual = False

        # fill
        fill1_uc = get_filled_object_image_uncropped(obj1.img_uncropped)   #returns cropped version
        fill2_uc = get_filled_object_image_uncropped(obj2.img_uncropped)
        fill1_c = crop_to_bbox(fill1_uc)
        fill2_c = crop_to_bbox(fill2_uc)

        fill_bp_diff_before_norm = abs(get_black_pixel_count(fill1_c) - get_black_pixel_count(fill2_c))
        fill1_c,fill2_c = normalize_size(fill1_c,fill2_c)
        fill_bp_diff_after_norm = abs(get_black_pixel_count(fill1_c) - get_black_pixel_count(fill2_c))

        isFillEquivalent = Object.is_equal_image_comparison(fill1_c,fill2_c)
        if isFillEquivalent:
            return True

        # flip left right
        flip_lr_1 = flip_left_right(fill1_c)
        flip_lr_2 = fill2_c
        isFlipLeftRightEquivalent = Object.is_equal_image_comparison(flip_lr_1,flip_lr_2)
        if isFlipLeftRightEquivalent:
            return True
        else:
            pass

        # flip top bottom
        flip_tb_1 = flip_top_bottom(fill1_c)
        flip_tb_2 = fill2_c
        isFlipLeftRightEquivalent = Object.is_equal_image_comparison(flip_tb_1,flip_tb_2)
        if isFlipLeftRightEquivalent:
            return True
        else:
            pass

        if isEqual:
            return True
        elif not isEqual:
            return False

    @classmethod
    def save_global_object_comparison_images(cls,obj1,obj2,same_diff):
        im1 = obj1.img_cropped
        im2 = obj2.img_cropped

        new_im_size = (im1.size[0]+im2.size[0], max(im1.size[1],im2.size[1]))
        new_im = Image.new('RGB', new_im_size)
        new_im.paste(im1,(0,0))
        new_im.paste(im2,(im1.size[0],0))

        new_im.save("Test/" + same_diff + "/" + obj1.problem_name + "_" + obj1.figure_name + "_" + obj2.figure_name + "_" + obj1.name + "_" + obj2.name + ".png", "PNG")

    @classmethod
    def save_global_shape_comparison_images(cls,obj1,obj2,same_diff):

        im1 = obj1.img_cropped
        im2 = obj2.img_cropped

        new_im_size = (im1.size[0]+im2.size[0], max(im1.size[1],im2.size[1]))
        new_im = Image.new('RGB', new_im_size)
        new_im.paste(im1,(0,0))
        new_im.paste(im2,(im1.size[0],0))

        new_im.save("Test/" + same_diff + "/" + obj1.problem_name + "_" + obj1.figure_name + "_" + obj2.figure_name + "_" + obj1.name + "_" + obj2.name + ".png", "PNG")

    @classmethod
    def save_global_shape_comparison_images_with_specific_image(cls,obj1,obj2,im1,im2,same_diff):

        new_im_size = (im1.size[0]+im2.size[0], max(im1.size[1],im2.size[1]))
        new_im = Image.new('RGB', new_im_size)
        new_im.paste(im1,(0,0))
        new_im.paste(im2,(im1.size[0],0))

        new_im.save("Test/" + same_diff + "/" + obj1.problem_name + "_" + obj1.figure_name + "_" + obj2.figure_name + "_" + obj1.name + "_" + obj2.name + ".png", "PNG")


    @classmethod
    def print_comparison_stats(cls,obj1,obj2,same_diff):
        stat = Object.get_image_stat_comparison_dict(obj1.img_uncropped,obj2.img_uncropped)

        mean_diff_abs_val = stat['mean_diff_abs_val']
        mean_diff_normed = stat['mean_diff_normed']
        rms = stat['rms']
        width_diff_abs_val = stat['width_diff_abs_val']
        height_diff_abs_val = stat['height_diff_abs_val']
        area_ratio = stat['area_ratio']
        bp_pixel_diff = stat['bp_pixel_diff']
        center_x_diff = stat['center_x_diff']
        center_y_diff = stat['center_y_diff']
        bp_percent_diff = stat['bp_percent_diff']
        rms_diff_normed = stat['rms_diff_normed']
        var_diff = stat['var_diff']
        std_dev_diff = stat['std_dev_diff']
        std_dev_ratio = stat['std_dev_ratio']

        print mean_diff_normed,",",\
              rms,",",\
              width_diff_abs_val,",",\
              height_diff_abs_val,",",\
              area_ratio,",",\
              bp_pixel_diff,",",\
              bp_percent_diff,",",\
              rms_diff_normed,",",\
              var_diff,",",\
              center_x_diff,",",\
              center_y_diff,",",\
              std_dev_diff,",",\
              std_dev_ratio,",",\
              same_diff

from PIL import Image,ImageOps,ImageChops,ImageStat,ImageFilter
from cclabel import cclabel
import math,operator

def get_filled_object_image(uncropped_img):
    orig_border_added = ImageOps.expand(uncropped_img,1,255)

    inv_object_list = get_unique_images(invert(orig_border_added))

    filled = orig_border_added.copy()


    for inv_obj in inv_object_list.itervalues():
        io_img_cropped = crop_to_bbox(inv_obj)
        io_img_uncropped = inv_obj
        if io_img_cropped.size != orig_border_added.size:
            filled = invert(filled)
            io_img_uncropped = invert(io_img_uncropped)
            filled = ImageChops.add(io_img_uncropped,filled)
            filled = invert(filled)

    filled_cropped = crop_to_bbox(filled)

    return filled_cropped
def get_filled_object_image_uncropped(uncropped_img):
    orig_border_added = ImageOps.expand(uncropped_img,1,255)

    inv_object_list = get_unique_images(invert(orig_border_added))

    filled = orig_border_added.copy()

    for inv_obj in inv_object_list.itervalues():
        io_img_cropped = crop_to_bbox(inv_obj)
        io_img_uncropped = inv_obj
        if io_img_cropped.size != orig_border_added.size:
            filled = invert(filled)
            io_img_uncropped = invert(io_img_uncropped)
            filled = ImageChops.add(io_img_uncropped,filled)
            filled = invert(filled)

    return filled

def invert(img):
        mode = img.mode
        img = img.convert('RGB')
        img = ImageOps.invert(img)
        return img.convert(mode)

# removes whitespace border
def crop_to_bbox(img):
    inv = invert(img)
    return img.crop(inv.getbbox())

# copied from Figure, uses connected component labeling to get unique image
def get_unique_images(img):
    (labels, output_img) = cclabel(img)

    objs = {}
    objs_data = {}
    width,height = img.size

    for (x, y) in labels:
        # Name of the component the current point belongs to
        component = labels[(x, y)]

        if component not in objs:
            objs[component] = Image.new("RGB",(width,height))
            objs_data[component] = objs[component].load()

        objs_data[component][x, y] = (255,255,255)



    for label,obj in objs.iteritems():
        objs[label] = invert(obj).convert("1")
    return objs

def normalize_size(im1,im2):
    im1_area = im1.size[0] * im1.size[1]
    im2_area = im2.size[0] * im2.size[1]

    if im1_area <= im2_area:
        resize = im1.size
    else:
        resize = im2.size

    im1_norm = im1.copy()
    im2_norm = im2.copy()

    im1_norm = im1_norm.resize(resize)
    im2_norm = im2_norm.resize(resize)

    return im1_norm,im2_norm

#source: http://effbot.org/zone/pil-comparing-images.htm
def rmsdiff(im1, im2):
    "Calculate the root-mean-square difference between two images"
    h = ImageChops.difference(im1, im2).histogram()
    # calculate rms
    return math.sqrt(reduce(operator.add,map(lambda h, i: h*(i**2), h, range(256))) / (float(im1.size[0]) * im1.size[1]))

def get_black_pixel_count(img):
        stat = ImageStat.Stat(img)
        return stat.count[0] - stat.sum[0]/255

def get_black_pixel_percent(img):
        stat = ImageStat.Stat(img)
        return (stat.count[0] - stat.sum[0]/255) / stat.count[0]

# returns (x,y) tuple of center of bbox, where x,y are floating point
def get_center(img_uncropped):
    bbox = invert(img_uncropped).getbbox()
    center = (((float(bbox[2])-bbox[0])/2) + bbox[0], ((float(bbox[3])-bbox[1])/2) + bbox[1])
    return center


def rotate(img,angle):
    test = img.convert('RGBA')
    rot = test.rotate(angle, expand=1)
    fff = Image.new('RGBA',rot.size,(255,)*4)
    return Image.composite(rot, fff, rot).convert('1')

def flip_left_right(img):
    return img.transpose(Image.FLIP_LEFT_RIGHT)

def flip_top_bottom(img):
    return img.transpose(Image.FLIP_TOP_BOTTOM)

def add_images(img1,img2):
    img1 = invert(img1)#.convert('1')
    img2 = invert(img2)#.convert('1')

    return invert(ImageChops.add(img1,img2))

def subtract_images(img1,img2):
    img1 = invert(img1)
    img2 = invert(img2)

    return invert(ImageChops.subtract(img1,img2))
    
# only shared black parts 
def and_images(img1,img2):
    img1 = invert(img1)#.convert('1')
    img2 = invert(img2)#.convert('1')
    
    return invert(ImageChops.logical_and(img1,img2))
    
#kinda like adding, maybe exactly the same
def or_images(img1,img2):
    img1 = invert(img1).convert('1')
    img2 = invert(img2).convert('1')
    
    return invert(ImageChops.logical_or(img1,img2))

def xor_images(img1,img2):
    p = invert(img1).convert('1')
    q = invert(img2).convert('1')
    not_p = img1.convert('1')
    not_q = img2.convert('1')
    
    pORq = add_images(p,q)
    not_pORnot_q = add_images(not_p, not_q)
    
    return and_images(pORq,not_pORnot_q)

def max_min_filter(img):
    img = img.filter(ImageFilter.MaxFilter(3))
    return img.filter(ImageFilter.MinFilter(3))
    
def min_max_filter(img):
    img = img.filter(ImageFilter.MinFilter(3))
    return img.filter(ImageFilter.MaxFilter(3))
    
def max_min_min_max_filter(i):
    img = i.copy()
    img = img.filter(ImageFilter.MaxFilter(3))
    img = img.filter(ImageFilter.MinFilter(3))
    img = img.filter(ImageFilter.MinFilter(3))
    return img.filter(ImageFilter.MaxFilter(3))
    
def top1_bottom2_comp(i1,i2):
    img1 = i1.copy()
    img2 = i2.copy()
    top_size = (0,0,img1.size[0],img1.size[1]/2)
    top = img1.crop(top_size)
    img2.paste(top,top_size)
    
    return img2

def bottom1_top2_comp(i1,i2):
    img1 = i1.copy()
    img2 = i2.copy()
    i2 = img1
    i1 = img2
    return top1_bottom2_comp(i1, i2)
    
def left1_right2_comp(i1,i2):
    img1 = i1.copy()
    img2 = i2.copy()
    left_size = (0,0,img1.size[0]/2,img1.size[1])
    left = img1.crop(left_size)
    img2.paste(left,left_size)
    return img2
    
def right1_left2_comp(i1,i2):
    img1 = i1.copy()
    img2 = i2.copy()
    im2 = img1
    im1 = img2
    return left1_right2_comp(i1m, im2)
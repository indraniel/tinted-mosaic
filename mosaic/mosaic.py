#!/usr/bin/env python

import math
import random
import os
import sys

from PIL import Image

class PixelArt(object):
    def __init__(self, grid_width=7, grid_height=7, min_opacity=20, max_opacity=70):
        self.grid_width  = grid_width
        self.grid_height = grid_height
        self.min_opacity = min_opacity
        self.max_opacity = max_opacity

    def gridify(self, imgfile):
        img = Image.open(imgfile)

        # display some basic information
        (width, height) = img.size
        print "%-10s : %s" % ("filename", imgfile)
        print "%-10s : %s" % ("format", img.format)
        print "%-10s : %s" % ("mode", img.mode)
        print "%-10s : %s" % ("width", width)
        print "%-10s : %s" % ("height", height)
        print

        if img.mode != 'RGBA':
            img = img.convert('RGBA')

        alpha_weights = self.generate_alpha_weights(img)
        self.tint(img, alpha_weights)
        grid_img_file = self.save_image(img, imgfile)
        return grid_img_file

    def tint(self, img, alpha_weights):
        (width, height) = img.size
        pixels = img.load()

        for x in range(width):
            for y in range(height):
                (b, g, r, a) = pixels[x, y]

                # On a "grid" border, draw the black grid line
                if (x % self.grid_width == 0 or y % self.grid_height == 0):
                    pixels[x, y] = (0, 0, 0, 255)

                # Otherwise, we're within a "grid", so tint it
                else:
                    grid_x = x/self.grid_width
                    grid_y = y/self.grid_height
                    try:
                        opacity = alpha_weights[grid_x][grid_y]
                    except IndexError:
                        print 'IndexError:'
                        print '\tgrid_x: %d' % grid_x
                        print '\tgrid_y: %d' % grid_y
                        sys.exit(1)

                    for color in ('black', 'white'):
                        pixels[x,y] = \
                            self.alpha_composite(pixels[x,y], opacity, color)


    # This is based upon the "Introduction to compositing" section (section 5) 
    # of W3C's "Compositing and Blending Level 1" documentation -- 
    # http://dev.w3.org/fxtf/compositing-1/

    def alpha_composite(self, pixel, opacity, color):
        "Implementation of Porter-Duff compositing"

        # gather the normalized rgba components for the "background" layer --
        # the original image pixel
        norm_bg_pixel = [ i/255.0 for i in pixel ]
        norm_bg_alpha = norm_bg_pixel.pop()

        # gather the normalized rgba components for the "foreground" layer --
        # the "black" or "white" pixel layer with a random alpha opacity level
        # based on the assigned grid section
        norm_fg_pixel = [1,1,1] if color == 'white' else [0,0,0]
        norm_fg_alpha = opacity[color]/255.0

        # Step 1: Calculate the pre_composite RGB values
        pre_composite_rgb = [None, None, None]
        alpha_src = 1.0 - norm_fg_alpha

        (r, g, b) = range(0,3)
        for c in (r, g, b):
            pre_composite_rgb[c] = \
                (norm_fg_pixel[c] * norm_fg_alpha) + \
                (norm_bg_pixel[c] * norm_bg_alpha * alpha_src)

        # Step 2: Calculate the new composite "alpha" channel value
        composite_alpha = norm_fg_alpha + norm_bg_alpha * alpha_src

        # Step 3: Finalize to the correct composite color value
        composite_color = [ c/composite_alpha for c in pre_composite_rgb ]
        composite_color.append(composite_alpha)

        # Step 4: Reset the RGBA values back to their original 0 to 255 integer
        #         range values
        final_rgba = tuple([ int(c * 255.0) for c in composite_color ])

        return final_rgba

    def save_image(self, image, orig_filename):
        file = os.path.splitext((os.path.basename(orig_filename)))[0] + '-grid.png'
        dir  = os.path.dirname(orig_filename)
        if not dir:
            dir = '.'

        newfile = '/'.join([dir,file])
        image.save(newfile, 'PNG')
        return newfile

    def generate_alpha_weights(self, img):
        (width, height) = img.size
        max_hbox = int( math.ceil(width  / (self.grid_width  + 0.0)) )
        max_vbox = int( math.ceil(height / (self.grid_height + 0.0)) )
        print "# of grid columns: %d" % (max_hbox)
        print "# of grid rows   : %d" % (max_vbox)

        weights = [
            [self.random_opacity() for i in range(max_vbox)]
            for j in range(max_hbox)
        ]

        return weights

    def random_opacity(self):
        opacity = {}
        for color in ('black', 'white'):
            random_opacity = random.randint(self.min_opacity, self.max_opacity)
            opacity[color] = random_opacity

        return opacity

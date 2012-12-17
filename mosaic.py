#!/usr/bin/env python

import argparse
import kaa.imlib2 as im2
import math
import random
import os
import sys
import signal
import struct

class PixelArt(object):
    def __init__(self, grid_width=7, grid_height=7, min_opacity=20, max_opacity=70):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.min_opacity = min_opacity
        self.max_opacity = max_opacity

    def gridify(self, imgfile):
        img = im2.open(imgfile)
        print "%-10s : %s" % ("filename", img.filename)
        print "%-10s : %s" % ("format", img.format)
        print "%-10s : %s" % ("width", img.width)
        print "%-10s : %s" % ("height", img.height)
        alpha_weights = self.generate_alpha_weights(img)
        print "len(weights) = %d" % len(alpha_weights)
        print "len(weights[0]) = %d" % len(alpha_weights[0])
        buf = img.get_raw_data(write=False)
        print "len(buf) = %d" % len(buf)
        img2 = im2.new((img.width, img.height), bytes='\x00\x00\x00\x00' * img.width * img.height)
        buf2 = img2.get_raw_data(write=True)

        for x in range(img2.height):
            for y in range(img2.width):
                (b, g, r, a) = self.get_pixel_index(x, y, img2.width, img2.height)
#                print '[x:%d, y:%d] - b:%d g:%d r:%d a:%d' % (x, y, b, g, r, a)

                # On a "grid" border, draw the black grid line
                if (x % self.grid_height == 0 or y % self.grid_width == 0):
                    buf2[b] = chr(0)
                    buf2[g] = chr(0)
                    buf2[r] = chr(0)
                    buf2[a] = chr(100)

                # Otherwise, we're within a "grid", so tint it
                else:
                    grid_x = x/self.grid_height
                    grid_y = y/self.grid_width
                    try:
                        opts = alpha_weights[grid_x][grid_y]
                    except IndexError:
                        print 'IndexError:'
                        print '\tgrid_x: %d' % grid_x
                        print '\tgrid_y: %d' % grid_y
                        sys.exit(1)

                    alpha  = opts['alpha'] / 255.0
                    color  = opts['color']

#                    fmt = 'x: %d y: %d grid_x: %d grid_y: %d -- alpha: %d color: %s'
#                    print fmt % (x,y,grid_x,grid_y, opts['alpha'], opts['color'])

                    if color == 'black':
                        buf2[b] = chr(int(0.0 * alpha + ord(buf[b]) * (1 - alpha)))
                        buf2[g] = chr(int(0.0 * alpha + ord(buf[g]) * (1 - alpha)))
                        buf2[r] = chr(int(0.0 * alpha + ord(buf[r]) * (1 - alpha)))
                        buf2[a] = chr(255 - opts['alpha'])
                    else:
                        buf2[b] = chr(int(255.0 * alpha + ord(buf[b]) * (1 - alpha)))
                        buf2[g] = chr(int(255.0 * alpha + ord(buf[g]) * (1 - alpha)))
                        buf2[r] = chr(int(255.0 * alpha + ord(buf[r]) * (1 - alpha)))
                        buf2[a] = chr(255 - opts['alpha'])

#                    buf2[b] = buf[b]
#                    buf2[g] = buf[g]
#                    buf2[r] = buf[r]
#                    buf2[a] = chr(alpha_weights[grid_x][grid_y])
#                    buf2[a] = chr(100)

        img2.put_back_raw_data(buf2)
        self.save_image(img, img2)

    def save_image(self, image, newimg):
        file = os.path.splitext((os.path.basename(image.filename)))[0] + '-grid.png'
        dir  = os.path.dirname(image.filename)
        if not dir:
            dir = '.'

        print 'dir: %s' % dir
        print 'file: %s' % file

        newfile = '/'.join([dir,file])
        print 'Saving gridified image to: %s' % newfile
        newimg.save(newfile)

    def get_pixel_index(self, x, y, width, height, channels=4):
        b = x*width*channels + y*channels
        (g, r, a) = (b+1, b+2, b+3)
        return (b, g, r, a)

    def generate_alpha_weights(self, img):
        max_hbox = int( math.ceil(img.width  / (self.grid_width  + 0.0)) )
        max_vbox = int( math.ceil(img.height / (self.grid_height + 0.0)) )
        print "max_hbox: %d -- max_vbox: %d" % (max_hbox, max_vbox)

        weights = [
            [self.random_opacity() for i in range(max_hbox)]
            for j in range(max_vbox)
        ]

        return weights

    def random_opacity(self):
        random_opacity = random.randint(self.min_opacity, self.max_opacity)
        color = ('black', 'white')[random.randint(0,1)]
        return {'alpha': random_opacity, 'color': color}

def setup_args(parser):
    parser.add_argument(
        "-v", 
        "--verbose", 
        help = "echo the string you use here",
        action = "store_true"
    )

    parser.add_argument(
        "image",
        help = "Input image to gridify"
    )

    parser.add_argument(
        "--grid-width",
        help = "Width of grid [in pixels] (default = 7)",
        type = int,
        default = 7
    )

    parser.add_argument(
        "--grid-height",
        help = "Height of grid [in pixels] (default = 7)",
        type = int,
        default = 7
    )

    parser.add_argument(
        "--min-opacity",
        help = "Min opacity value [0-255] (default = 20)",
        type = int,
        default = 20
    )

    parser.add_argument(
        "--max-opacity",
        help = "Max opacity value [0-255] (default = 70)",
        type = int,
        default = 70
    )

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    setup_args(parser)
    args = parser.parse_args()

    pa = PixelArt(
        grid_width  = args.grid_width,
        grid_height = args.grid_height,
        min_opacity = args.min_opacity,
        max_opacity = args.max_opacity
    )

    pa.gridify(args.image)

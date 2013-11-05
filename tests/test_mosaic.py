# -*- coding: utf-8 -*-

from .context import mosaic
import unittest
import os
import hashlib
import random

def sha1_file(file, block_size=2**20):
    with open(file, 'rb') as f:
        sha1 = hashlib.sha1()
        while True:
            data = f.read(block_size)
            if not data:
                break
            sha1.update(data)

        return sha1.hexdigest()

class BasicPixelArt(unittest.TestCase):
    """Basic test cases."""

    def setUp(self):
        random.seed(1)
        self.test_image    = "tests/images/umbrellas-test.png"
        self.output_image  = "tests/images/umbrellas-test-grid.png"
        self.expected_sha1 = 'cdff69851e7de7238a7ba0526dc8dbad2dbfc831'

    def tearDown(self):
        if (os.path.exists(self.output_image)):
            os.unlink(self.output_image)

    def test_pixel_art(self):
        pa = mosaic.PixelArt(
            grid_width  = 7,
            grid_height = 7,
            min_opacity = 20,
            max_opacity = 70
        )
        self.assertTrue(pa, "Didn't get a PixelArt object")
        self.assertTrue(os.path.exists(self.test_image), "Didn't find the test image")

    def test_gridify(self):
        pa = mosaic.PixelArt(
            grid_width  = 7,
            grid_height = 7,
            min_opacity = 20,
            max_opacity = 70
        )
        pa.gridify(self.test_image)
        self.assertTrue(os.path.exists(self.output_image), "Didn't find the test grid image")
        observed_sha1 = sha1_file(self.output_image)
        self.assertEqual(observed_sha1, self.expected_sha1)


if __name__ == '__main__':
    unittest.main()

In the neverending quest to find alternative desktop background to satisfy my
fickle mind, I came across [Delta909's Pixel Matrix wallpaper][1].  Inspired by
this, I made this toy: `pixel-art`. Now I can take any arbitrary image, and
"pixel matrix"-ify it.  For example:

**Before:**

![Original Umbrella Image](https://raw.github.com/indraniel/tinted-mosaic/master/tests/images/umbrellas.png)

**After:**

![Umbrella Image - "Mosaic-ified"](https://raw.github.com/indraniel/tinted-mosaic/master/tests/images/umbrellas-grid.png)

_(Images taken from [Architizer: The Umbrellas of Águeda][2])_

This project was also an excuse to better appreciate how [alpha compositing][11]
works, and as well as to educate myself on how Python projects are structured.
As such, there are a few inefficiencies and idosynacrasies to this code.

The alpha compositing was implmented from scratch in Python, making the image
processing slow.  The "proper" way to setup a Python project is unfortunately
subject to debate.  Just look at these stackoveflow threads [here][3],
[here][4] & [here][5].

I've made my own flavored setup based upon the following opinionated essays:

* [Kenneth Reitz's Repository Structure and Python][6]
* [Learn Python the Hard Way][7]
* [Python Project HowTo][8]
* [The Hitchhiker's Guide to Packaging][12]


Build Instructions
==================

It's probably best to install via [virtualenv][12].  Once a virtualenv is
activated, simply:

    $ git clone https://github.com/indraniel/tinted-mosaic
    $ python setup.py install

Dependencies
------------

This project is powered by the popular [Pillow][9] and [nose][10] libraries.
These dependencies are automatically installed if you follow the build instructions.

Testing
-------

In the root directory of the git repo simply run:

    make test


Usage
=====

Once installed, simply run:

    $ pixel-art photo.jpg

It will create a file called `photo-grid.png` in the same directory where the
original picture resides.

The options, and default settings to `pixel-art` are:

    $ pixel-art --help
    usage: pixel-art [-h] [-v] [--grid-width GRID_WIDTH]
                     [--grid-height GRID_HEIGHT] [--min-opacity MIN_OPACITY]
                     [--max-opacity MAX_OPACITY]
                     image
    
    positional arguments:
      image                 Input image to gridify
    
    optional arguments:
      -h, --help            show this help message and exit
      -v, --verbose         echo the string you use here
      --grid-width GRID_WIDTH
                            Width of grid [in pixels] (default = 7)
      --grid-height GRID_HEIGHT
                            Height of grid [in pixels] (default = 7)
      --min-opacity MIN_OPACITY
                            Min opacity value [0-255] (default = 20)
      --max-opacity MAX_OPACITY
                            Max opacity value [0-255] (default = 70)

TODOs
=====

* add CLI option to specify your own output file
* add CLI options to manually specify which layers to add (white and/or black)
* add CLI option to seed the random number generator to generate a consistent tinted grid
* allow for alternative grid line colors. Right now there is only black
* ability to save to other image file formats. Right now only save to PNG.


[1]: http://delta909.deviantart.com/art/Pixel-Matrix-126529536
[2]: http://www.architizer.com/en_us/blog/dyn/46147/the-umbrellas-of-aguenda/
[3]: http://stackoverflow.com/questions/4881897/python-project-and-package-directories-layout
[4]: http://stackoverflow.com/questions/193161/what-is-the-best-project-structure-for-a-python-application
[5]: http://stackoverflow.com/questions/61151/where-do-the-python-unit-tests-go
[6]: http://kennethreitz.org/repository-structure-and-python/
[7]: http://learnpythonthehardway.org/book/ex46.html
[8]: http://infinitemonkeycorps.net/docs/pph/
[9]: http://pillow.readthedocs.org/en/latest/index.html
[10]: https://nose.readthedocs.org/en/latest/ 
[11]: http://dev.w3.org/fxtf/compositing-1/
[12]: http://guide.python-distribute.org/

An Iterated Function System in Python
=====================================

Initially written under the guidance of Thomas Ludwig one night at KiwiFoo.

The tone-mapped image handling comes from Minilight.

NOTE: I strongly recommend using PyPy to run this (it runs about 40x faster)

Running
-------

Just run

    python pyifs.py

You can change the output filename at the bottom of `pyifs.py`

NOTE: You may want to provide a seed with `random.seed()` so if you get a
nice result, you can re-run it at higher resolution, etc.

Customization
-------------

Parts of the code that can be customized are marked `CUSTOMIZE` in `pyifs.py`

* You can adjust the `WIDTH`, `HEIGHT`, `ITERATIONS`, `NUM_POINTS` and
  `NUM_TRANSFORMS`
* You can write new `Transform` classes
* You can pick which transforms to choose from in `TRANSFORM_CHOICES`

Writing New Transforms
----------------------

A new subclass of `Transform` should randomize its parameters in `__init__`
then implement a `transform` method that takes two args (the x, y of the
point) and returns a new x, y.

Alternatively, you can subclass `ComplexTransform` and instead of implementing
`transform` instead implement a method `f` that takes a single complex number
argument and returns anew complex number.

Examples
--------

![example IFS](http://github.com/jtauber/pyifs/raw/master/example.png)
![example IFS2](http://github.com/jtauber/pyifs/raw/master/example2.png)

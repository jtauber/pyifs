import random
from math import cos, sin, pi, atan2, sqrt

from image import Image


# CUSTOMIZE
WIDTH = 512
HEIGHT = 512
ITERATIONS = 10000
NUM_POINTS = 1000
NUM_TRANSFORMS = 7


h = Image(WIDTH, HEIGHT)


def random_complex():
    return complex(random.uniform(-1, 1), random.uniform(-1, 1))


class IFS:
    
    def __init__(self):
        self.transforms = []
        self.total_weight = 0
    
    def add(self, transform):
        weight = random.gauss(1, 0.15) * random.gauss(1, 0.15)
        self.total_weight += weight
        self.transforms.append((weight, transform))
    
    def choose(self):
        w = random.random() * self.total_weight
        running_total = 0
        for weight, transform in self.transforms:
            running_total += weight
            if w <= running_total:
                return transform
    
    def final_transform(self, px, py):
        a = 0.5
        b = 0
        c = 0
        d = 1
        z = complex(px, py)
        z2 = (a * z + b) / (c * z + d)
        return z2.real, z2.imag


class Transform(object):
    
    def __init__(self):
        self.r = random.random()
        self.g = random.random()
        self.b = random.random()
    
    def transform_colour(self, r, g, b):
        r = (self.r + r) / 2
        g = (self.g + g) / 2
        b = (self.b + b) / 2
        return r, g, b


class Linear(Transform):
    def __init__(self):
        super(Linear, self).__init__()
        self.a = random.uniform(-1, 1)
        self.b = random.uniform(-1, 1)
        self.c = random.uniform(-1, 1)
        self.d = random.uniform(-1, 1)
            
    def transform(self, px, py):
        return (self.a * px + self.b * py, self.c * px + self.d * py)


class ComplexTransform(Transform):
    
    def transform(self, px, py):
        z = complex(px, py)
        z2 = self.f(z)
        return z2.real, z2.imag


class Moebius(ComplexTransform):
    
    def __init__(self):
        super(Moebius, self).__init__()
        self.pre_a = random_complex()
        self.pre_b = random_complex()
        self.pre_c = random_complex()
        self.pre_d = random_complex()
    
    def f(self, z):
        return (self.pre_a * z + self.pre_b) / (self.pre_c * z + self.pre_d)


class MoebiusBase(ComplexTransform):
    
    def __init__(self):
        super(MoebiusBase, self).__init__()
        self.pre_a = random_complex()
        self.pre_b = random_complex()
        self.pre_c = random_complex()
        self.pre_d = random_complex()
        self.post_a = random_complex()
        self.post_b = random_complex()
        self.post_c = random_complex()
        self.post_d = random_complex()
    
    def f(self, z):
        z2 = (self.pre_a * z + self.pre_b) / (self.pre_c * z + self.pre_d)
        z = self.f2(z2)
        z2 = (self.post_a * z + self.post_b) / (self.post_c * z + self.post_d)


class InverseJulia(ComplexTransform):
    
    def __init__(self):
        super(InverseJulia, self).__init__()
        r = sqrt(random.random()) * 0.4 + 0.8
        theta = 2 * pi * random.random()
        self.c = complex(r * cos(theta), r * sin(theta))
    
    def f(self, z):
        z2 = self.c - z
        theta = atan2(z2.imag, z2.real) * 0.5
        sqrt_r = random.choice([1, -1]) * ((z2.imag * z2.imag + z2.real * z2.real) ** 0.25)
        return complex(sqrt_r * cos(theta), sqrt_r * sin(theta))


# CUSTOMIZE by implementing new transforms

# CUSTOMIZE
TRANSFORM_CHOICES = [Linear, Moebius]

ifs = IFS()

for n in range(NUM_TRANSFORMS):
    cls = random.choice(TRANSFORM_CHOICES)
    ifs.add(cls())


for i in range(NUM_POINTS):
    print i
    px = random.uniform(-1, 1)
    py = random.uniform(-1, 1)
    r, g, b = 0.0, 0.0, 0.0
    
    for j in range(ITERATIONS):
        t = ifs.choose()
        px, py = t.transform(px, py)
        r, g, b = t.transform_colour(r, g, b)
        
        fx, fy = ifs.final_transform(px, py)
        x = int((fx + 1) * WIDTH / 2)
        y = int((fy + 1) * HEIGHT / 2)

        h.add_radiance(x, y, [r, g, b])

h.save("test.png", max(1, (NUM_POINTS * ITERATIONS) / (HEIGHT * WIDTH)))

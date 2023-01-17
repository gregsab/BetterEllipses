"""Generation of images for practicing ellipses drawing."""

import io
import datetime
import math
from random import random
from dataclasses import dataclass, asdict
from typing import List

import logging

# import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Arrow
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.figure import Figure

WIDTH = 297
HEIGHT = 210
MIN_A = 50
MAX_A = 150
MAX_ANGLE = 180

N_ELLIPSES = 12

@dataclass
class EllDef:
    cntr: (int, int)
    w:  int  # long axis
    h:  int  # short axis
    a: int
    clr: str

def draw_ellipse_with_axes(ax, ellipse, axes_only=False, ellipse_only=False) -> None:
    """Draws long and short axes of the ellipse."""

    (xc, yc) = ellipse['cntr']
    a = ellipse['w']
    b = ellipse['h']
    angle = ellipse['a']
    color = ellipse['clr']

    if not axes_only:
        style = {
            'color' : color,
            'alpha' : 0.1
        }
        el = Ellipse((xc, yc), a, b, angle=angle, **style)
        ax.add_artist(el)

    if not ellipse_only:
        style = {
            'color' : color,
            'linewidth' : .2,
            'alpha' : 0.8
        }

        # draw long axis
        dx = a / 2 * math.cos(angle / 180 * math.pi)
        dy = a / 2 * math.sin(angle / 180 * math.pi)
        arrow = Arrow(xc, yc, dx, dy, **style)
        ax.add_artist(arrow)
        arrow = Arrow(xc, yc, -dx, -dy, **style)
        ax.add_artist(arrow)

        # draw short axis
        dx = b / 2 * math.cos((angle + 90) / 180 * math.pi)
        dy = b / 2 * math.sin((angle + 90) / 180 * math.pi)
        arrow = Arrow(xc, yc, dx, dy, **style)
        ax.add_artist(arrow)
        arrow = Arrow(xc, yc, -dx, -dy, **style)
        ax.add_artist(arrow)

def generate_ellipses(width=WIDTH, height=HEIGHT, n=N_ELLIPSES, min_a=MIN_A, max_a=MAX_A,
                      max_angle=MAX_ANGLE) -> List:
    """Generate N suitable ellipses"""

    ellipses = []

    for i in range(n):
        a = round(min_a + random() * (max_a-min_a), 2)
        b = round((.2 + random() * .6) * a, 2)
        angle = round(random() * max_angle, 2)

        # generate an ellipse
        ellipse = Ellipse((0, 0), a, b, angle=angle)

        # check if fits into a drawing area
        ex = ellipse.get_extents()

        dx = ex.xmax - ex.xmin
        dy = ex.ymax - ex.ymin

        MARGIN = 0

        xc = round(random() * ((1-MARGIN) * WIDTH - dx) + dx / 2)
        yc = round(random() * ((1-MARGIN) * HEIGHT - dy) + dy / 2)

        e = EllDef((xc, yc), a, b, angle, f"C{i}")
        ellipses.append(asdict(e))

    logging.info(f"Generated {len(ellipses)} ellipses")
    logging.debug(f"Generated {len(ellipses)} ellipses with params: w={width}, h={height}, min_a={min_a},"
                 f"max_a={max_a}, max_angle={max_angle}")

    return ellipses



def generate_ellipses_old(width=WIDTH, height=HEIGHT, n=N_ELLIPSES, min_a=MIN_A, max_a=MAX_A,
                      max_angle=MAX_ANGLE) -> List:
    """Generate N suitable ellipses"""

    ellipses = []

    count = 0
    while count < n:
        a = round(min_a + random() * (max_a-min_a), 2)
        b = round((.2 + random() * .6) * a, 2)

        xc  = round(a/2 + random() * (WIDTH -a), 2)
        yc = round(b/2+random()*(height-b), 2)
        angle = round(random() * max_angle, 2)
        # angle = 45

        color = f"C{count}"

        # generate an ellipse
        ellipse = Ellipse((xc, yc), a, b, angle=angle, color=color)

        # check if fits into a drawing area
        ex = ellipse.get_extents()
        if ex.xmin < 0 or ex.ymin < 0 or ex.xmax > width or ex.ymax > height:
            continue

        e = EllDef((xc, yc), a, b, angle, color)
        ellipses.append(asdict(e))

        count += 1

    logging.info(f"Generated {len(ellipses)} ellipses with params: w={width}, h={height}, min_a={min_a},"
                 f"max_a={max_a}, max_angle={max_angle}")

    return ellipses

def prepare_figure(ax, width, height):
    """Sets attributes of the matplotlib figure"""

    ax.set_aspect('equal')
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.set_axis_off()


def generate_page_pdf(pdf, ellipses, width=WIDTH, height=HEIGHT, axes_only=False, ellipses_only=False):
    """Generates one page of the pdf file with ellipses"""

    SCALE = .75

    fig = Figure(figsize=(SCALE * 11.7, SCALE * 8.3))
    ax = fig.subplots()

    prepare_figure(ax, width, height)

    for ellipse in ellipses:
        draw_ellipse_with_axes(ax, ellipse, axes_only=axes_only, ellipse_only=ellipses_only)
    pdf.savefig(figure=fig, bbox_inches='tight')
    fig.clear()


def save_as_pdf(filename, ellipses: List[EllDef], width=WIDTH, height=HEIGHT) -> None:
    """Generates odf file"""

    with PdfPages(filename) as pdf:
        generate_page_pdf(pdf, ellipses, width=width, height=height)

        generate_page_pdf(pdf, ellipses, width=width, height=height, axes_only=True)

        generate_page_pdf(pdf, ellipses, width=width, height=height, ellipses_only=True)

        # We can also set the file's metadata via the PdfPages object:
        d = pdf.infodict()
        d['Title'] = 'Master drawing your ellipses'
        d['Author'] = 'Grzegorz Sabak'
        d['Subject'] = 'Templet for practising ellipse drawing'
        d['Keywords'] = 'PdfPages multipage keywords author title subject'
        d['CreationDate'] = datetime.datetime(2023, 1, 5)
        d['ModDate'] = datetime.datetime.today()

    return 0

def generate_pdf(ellipses, width=WIDTH, height=HEIGHT):
    memory_file = io.BytesIO()
    memory_file.name = "better_ellipses.pdf"

    with PdfPages(memory_file) as pdf:
        generate_page_pdf(pdf, ellipses)
        generate_page_pdf(pdf, ellipses, width=width, height=height, axes_only=True)
        generate_page_pdf(pdf, ellipses, width=width, height=height, ellipses_only=True)
        # pdf.close()

    logging.info(f"PDF generated with params: w={width}, h={height}")

    return memory_file


# def save_as_png(filename, ellipses, width=WIDTH, height=HEIGHT) -> None:
#     fig, ax = plt.subplots(figsize=(8.3, 11.7))
#     prepare_figure(ax, width, height)
#
#     for ellipse in ellipses:
#         draw_ellipse_with_axes(ax, ellipse)
#
#     plt.savefig(filename, bbox_inches='tight', dpi=92)


def generate_preview(ellipses, width=WIDTH, height=HEIGHT, axes_only=False, ellipses_only=False):
    SCALE = .75

    fig = Figure(figsize=(SCALE * 11.7, SCALE * 8.3))
    ax = fig.subplots()

    prepare_figure(ax, width, height)

    for ellipse in ellipses:
        draw_ellipse_with_axes(ax, ellipse, axes_only, ellipses_only)

    pic_data = io.BytesIO()
    fig.savefig(pic_data, format="png", bbox_inches='tight')

    return  pic_data

# if __name__ == "__main__":
#     ellipses = generate_ellipses(n=12, min_a=50, max_a=100, max_angle=90)
#     save_as_pdf('better_ellipses.pdf', ellipses)
#     save_as_png('better_ellipses.png', ellipses)
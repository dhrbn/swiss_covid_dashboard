import numpy as np


MAIN_COLOR = '#1193f5'

BLUE_PALETTE = [
    '#1193f5',
    '#006eb2',
    '#0086d8',
    '#71d7ff',
]

PURPLE_PALETTE = [
    '#7451f1',
    '#bc68f2',
    '#4630c6',
    '#4d0eaf',
]

PINK_PALETTE = [
    '#fd4282',
    '#c60051',
    '#ea2d7a',
    '#f973b0',
]

CYAN_PALETTE = [
    '#4de5db',
    '#02874a',
    '#0dbc71',
    '#45dd9f',
]

YELLOW_PALETTE = [
    '#ffc500',
    '#ed1c24',
    '#ea5e18',
    '#f99b06',
]

GRAY_PALETTE = [
    '#9aa3b4',
    '#797f89',
    '#5c6168',
    '#424951',
]

BLACK_PALETTE = [
    '#070524',
    '#5764a3',
    '#333c7c',
    '#1d1470',
]

colors_array = np.array([
    [
        BLUE_PALETTE[idx],
        PURPLE_PALETTE[idx],
        PINK_PALETTE[idx],
        CYAN_PALETTE[idx],
        YELLOW_PALETTE[idx],
        GRAY_PALETTE[idx],
        BLACK_PALETTE[idx],
    ] for idx in range(len(BLACK_PALETTE))
])
COLORS = colors_array.flatten().tolist()

BLACK = '#070524'
MIDDLE_GRAY = '#dddddd'
LIGHT_GRAY = '#f0f1f5'

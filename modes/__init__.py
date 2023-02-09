MODES = []

from .colour_temp_lights import Mode
MODES.append(Mode)

from .hsv_lights import Mode
MODES.append(Mode)

from .hsvwaves import Mode
MODES.append(Mode)

from .led_test import Mode
MODES.append(Mode)

from .softglow import Mode
MODES.append(Mode)

from .hsv_spin import Mode
MODES.append(Mode)

from .christmas import Mode
MODES.append(Mode)

from .temperature import Mode
MODES.append(Mode)

from .time import Mode
MODES.append(Mode)

del Mode

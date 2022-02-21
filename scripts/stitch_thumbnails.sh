#!/bin/bash

montage -tile 11x0 -geometry +0+0 "$PWD/output/thumbnail/*.png" "$PWD/output/poster.png"

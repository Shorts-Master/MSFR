"""
Sub-mesh-cell peak location via parabolic interpolation around the
discrete maximum. Standard numerical technique - fits a parabola
through the max point and its two neighbors, returns the true vertex
location, rather than being locked to whichever mesh node happens to
be largest.
"""
import numpy as np

def subcell_peak(x_arr, y_arr):
    """Returns interpolated peak x-location, sub-mesh-cell accurate."""
    i = np.argmax(y_arr)
    if i == 0 or i == len(y_arr) - 1:
        return x_arr[i]  # peak at boundary, no interpolation possible

    x0, x1, x2 = x_arr[i-1], x_arr[i], x_arr[i+1]
    y0, y1, y2 = y_arr[i-1], y_arr[i], y_arr[i+1]

    denom = (y0 - 2*y1 + y2)
    if abs(denom) < 1e-15:
        return x1  # flat/degenerate, fall back to grid point

    offset = 0.5 * (y0 - y2) / denom
    return x1 + offset * (x2 - x1)

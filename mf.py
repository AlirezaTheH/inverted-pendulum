from fuzzy.set.Polygon import Polygon


def saw(interval, n):
    """
    Splits an ``interval`` into ``n`` triangle functions.

    :Parameters:
      interval
        A tuple containing the start and the end of the interval, in the format
        ``(start, end)``;
      n
        The number of functions in which the interval must be split.

    :Returns:
      A list of triangle membership functions, in order.
    """
    xo, xf = interval
    dx = float(xf - xo) / float(n + 1)
    mfs = []
    for i in range(n):
        mft = Polygon()
        mft.add(x=xo, y=0.0)
        mft.add(x=xo + dx, y=1.0)
        mft.add(x=xo + 2 * dx, y=0.0)
        mfs.append(mft)
        xo += dx
    return mfs


def flat_saw(interval, n):
    """
    Splits an ``interval`` into a decreasing ramp, ``n-2`` triangle functions
    and an increasing ramp.

    :Parameters:
      interval
        A tuple containing the start and the end of the interval, in the format
        ``(start, end)``;
      n
        The number of functions in which the interval must be split.

    :Returns:
      A list of corresponding functions, in order.
    """
    xo, xf = interval
    dx = float(xf - xo) / float(n + 1)

    # Decreasing ramp
    mf1 = Polygon()
    mf1.add(x=xo, y=1.0)
    mf1.add(x=xo + dx, y=1.0)
    mf1.add(x=xo + 2 * dx, y=0.0)

    # ``n-2`` triangle
    mfs = saw((xo + dx, xf - dx), n - 2)

    # Increasing ramp
    mf2 = Polygon()
    mf2.add(x=xf - 2 * dx, y=0.0)
    mf2.add(x=xf - dx, y=1.0)
    mf2.add(x=xf, y=1.0)

    return [mf1] + mfs + [mf2]

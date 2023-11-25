def display(sm: str, tof: float, formatter: str="pretty"):
    """
    Print out readings.

    Args:
      sm (str): sensor pair; eg, '1->2'.
      tof (float): time of flight in microseconds
      formatter (str): type of display.  Default is 'pretty';
      will have 'csv' in the future.
    """
    if formatter == "pretty":
        print(f"{sm}: {tof} microseconds")
        print("=-=-=-=-=-=-=-=-=-")
    elif formatter == "csv":
        # FIXME: Do I need headers?
        print(tof)
    else:
        raise NotImplementedError

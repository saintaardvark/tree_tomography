def display(msg: dict, formatter: str = "pretty"):
    """
    Print out readings.

    Args:
      msg (dict): key, val pairs of reading_name, time of flight in microseconds
      formatter (str): type of display.  Default is 'pretty'.  If CSV, format as CSV.

    """
    if formatter == "pretty":
        for k in msg:
            print(f"{k}: {msg[k]} microseconds")
            print("=-=-=-=-=-=-=-=-=-")
    elif formatter == "csv":
        # FIXME: Do I need headers?
        line = ""
        for k in msg:
            line += str(msg[k]) + ","

        # Remove trailing comma
        print(line.rstrip(","))
    else:
        raise NotImplementedError

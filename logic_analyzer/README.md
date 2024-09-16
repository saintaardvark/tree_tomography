# Logic Analyzer

This is an attempt to use a Pi Pico, programmed as a logic analyzer,
to capture the sensor outputs.  I strongly suspect this is going to be
a much better approach than I've taken so far.

# HOWTO

- Install software; see Resources below

- Hook up pico

- screen /dev/ttyACM0 921600
  - Add `-L` arg to capture if that's what you want

- Commands:

```
p0
n8
f10000000
t1
s5000
g
```

- Detach & run `make log`

- Ctrl-c & run `make pv`

# Resources

- https://github.com/gamblor21/rp2040-logic-analyzer -- this is the
  code I'm using in the Pico.  The output is in CSV, and I'm using
  Pulseview to view it.  [Here's an explanatory article on this
  project](https://www.hackster.io/markkomus/using-a-raspberry-pi-pico-as-a-logic-analyzer-with-pulseview-e12543).

- https://hackaday.com/2017/07/29/everything-you-need-to-know-about-logic-probes/
  is an *excellent* overview of what logic analyzers do -- great if
  (like me) you don't know about them.

- https://sigrok.org/wiki/File_format:Csv is documentation from sigrok
  for how it reads the CSV format, and what CLI args it takes.
  Pulseview takes the same args.

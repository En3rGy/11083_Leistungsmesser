# 11083_Leistungsmesser

## Requirements
- The module shall output the consumptions since the beginning for all current time spans.
- The module shall output the total consumptions of the previous time spans.
- The module shall use an increasing counter as input for calculating the consumptions.
- The module should use a pulse signal input for calculating the consumptions.
- The start / end of a time span shall be indicated by a 1 on a dedicated input.
- The module shall accept a gain input to be multiplied with the counter input value.
- The module shall accept an offset input value to be substracted from the gained counter input value.
- The module shall accept a "reset" input, setting all outputs and internal values to 0.
- The module shall output the global counter repsecting gain and offset since the last reset.

## Software Design Description
Time span (ts)
Start of time span (sts)
End of time span (ets)
Local counter (lc) containing the consumption of the current time span.
Global counter (gc) containing the counter value (incl. gain & offset) since the last reset.

Examples
Global value of counter at the beginning of the current time span 1: ts1_gc_sts
Global value of counter at the end of the current time span 1: ts1_gc_ets
Local counter during the current time span: ts1_lc = gc - ts1_gc_sts

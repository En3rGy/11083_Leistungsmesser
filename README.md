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
- The module shall deal with an overflow of the input counter by 

## Software Design Description

### Definitions

| Abbrev. | Description |
| --- | --- | 
| `ts` | Time span |
| `sts` | Start of time span |
| `ic` | Input counter value |
| `ic_curr` | Current input counter value received, respecting gain and offset. |
| `ic_prev` | Last input counter value received, respecting gain and offset. |
| `ts1_lc` | Local counter containing the consumption of the current time span 1. |
| `gc` | Global counter containing the counter value (incl. gain & offset) since the last reset. |
| `ts1_gc_sts` | Global value of counter at the beginning of the *current* time span 1 *and* at the end of the *previous* time span 1. |
| `ts1_cons_curr` | Consumption of the current time span 1, increasing with new ic. |
| `ts1_cons_pev` | Total consuption during the previous time span 1. |

### Calculations
| Description | Formula |
| --- | --- |
| Input counter respecting input counter (ic) gain (k) and offset (o) | `ic_curr = k * ic - o` |
| Receive new ic_curr value and deal with ic buffer overrun | `ic_prev > ic_curr ? gc += ic_curr : gc += ic_curr - ic_prev` <br> `ic_prev = ic_curr` |
| Local counter during for the on-going time span 1 | `ts1_lc = gc - ts1_gc_sts` |
| Receive end / start interval trigger | `ts1_cons_prev = gc - ts1_gc_sts`< br> `ts1_gc_sts = gc` <br> `ts1_cons_curr = 0`|

### Retentive storage

- `gc`
- `ts1_gc_sts`
- `ic_prev`


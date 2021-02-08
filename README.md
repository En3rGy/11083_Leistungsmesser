# 11083 Leistungsmesser

## Description 

Logic module for Gira Homeserver to record and compare counter values.
The module records values of a specific counter. If the input counter has an overflow, the module outputs a continious value.

The module provides counter values for up to three intervals.
For each interval, the increase of the counter during the current interval and the increase during the passed intverval, is given.

All calculations are performed on `Counter = (Counter * Gain) - Offset`.

## Inputs

| No. | Name | Initialisation | Description |
| --- | --- | --- | --- |
| 1 | Counter | 0 | Current counter value |
| 2 | Reset 1 | 0 | Resets counter of interval 1 when receiving 1. Setting the current interval counter as new previous. |
| 3 | Reset 2 | 0 | Resets counter of interval 1 when receiving 1. Setting the current interval counter as new previous. |
| 4 | Reset 3 | 0 | Resets counter of interval 1 when receiving 1. Setting the current interval counter as new previous. |
| 5 | Gain | 0 | All calculations are performed on `Counter = (Counter * Gain) - Offset`  |
| 6 | Reset | 0 | Resets all counters and retentive data. |
| 7 | Offset | 0 | All calculations are performed on `Counter = (Counter * Gain) - Offset` |

## Outputs

| No. | Name | Initialisation | Description |
| --- | --- | --- | --- |
| 1 | Counter total | 0 | |
| 2 | Current 1 | 0 | |
| 3 | Previous 1 | 0 | |
| 4 | Current 2 | 0 | |
| 5 | Previous 2 | 0 | |
| 6 | Current 3 | 0 | |
| 7 | Previous 3 | 0 | |

## Sample Values

| Input | Output |
| --- | --- |
| On init | All outputs set to the previosuly stored retentive values |
| Counter = A | Output `Current x` set to `A - Previous x` with x = 1/2/3 |
| Counter = B | Output `Current x` set to `B - Previous x` with x = 1/2/3 |
| Reset 1 = 1 | Output `Previous 1 = Current 1` and afterwards `Current 1 = 0` | 


## Other

- Recalculation during start: no
- Module is retentive: yes
- Internal designation: 11083
- Category: Zähler

### Change Log

 - v0.8
     - Refactoring to HSL2
 - v0.7
     - Various improvements
 - v0.6
     - Solved bug reporting last years data
 - v0.5
     - Additional SN to save current counter
 - v0.4
     - Removed ==1 
     - Used SA instead of SN
 - v0.3
     - Improved comments
     - Replaced <>0 by ==1
 - v0.2
     - Initial

### Open Issues / Know Bugs

- none

### Support

Please use [github issue feature](https://github.com/En3rGy/14108_tibber/issues) to report bugs or rise feature requests.
Questions can be addressed as new threads at the [knx-user-forum.de](https://knx-user-forum.de) also. There might be discussions and solutions already.


### Code

Code and releases are availabe via [github](https://github.com/En3rGy/14108_tibber). Stable releases will be availabe at the [knx-user-forum.de download section](https://service.knx-user-forum.de/?comm=download) also.

### Devleopment Environment

- [Python 2.7.18](https://www.python.org/download/releases/2.7/)
    - Install python markdown module (for generating the documentation) `python -m pip install markdown`
- Python editor [PyCharm](https://www.jetbrains.com/pycharm/)
- [Gira Homeserver Interface Information](http://www.hs-help.net/hshelp/gira/other_documentation/Schnittstelleninformationen.zip)


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

### Solution Outline

Calculations are based on an global counter. This counte is first initialised by the first in value recived. The global counter is increased by the delta of two ic values recieved. To caluclate the consuption during a time span, the value of the global counter at the beginning of the time span is stored. This vlaue equals the value of the gloabl counter at the end of the previous time span. Consumptions are caluclated by substracting the global counter values stored.

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


## Licence

Copyright 2015 T. Paul

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


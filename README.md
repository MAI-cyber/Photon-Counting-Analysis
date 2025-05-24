Setup: The FPGA has 4 inputs, corresponding to A, B, A' and B'. The module counts the single counts for A, B, A' and B' as well as double counts A'B, A'B, A'B' and triple count ABB'. The DGS645 is connected through its generation channels to the FPGA inputs. A generation rate of 4000 is set and all inputs are synced with T0 (reference clock), a constant voltage and pulse duration is initialized.

Delay Sweep: Keeping the A input channel synced with T0, we sweep the rest of the channels to determine the width of the coincidence width.

Resolution Sweep: Increase the pulse width of all the channel A,B,A' and B' to find the pulse width that correspond to true count rate.

Voltage Sweep: Increase the pulse voltage of all the channel A,B,A' and B' to find the upper and lower bound of voltage for the FPGA.

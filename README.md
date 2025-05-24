Setup:

The FPGA acts as the counting module and has 4 inputs, corresponding to A,B,A' and B'. The module counts the single counts for A,B,A' and B' as well as double counts A'B, A'B, A'B' and triple count ABB'.
The DGS645 is connected through it generation channels to the the FPGA inputs, a generation rate of 4000 is set and all inputs are synced with T0 reference, a constant voltage and pulse duration is initialized.

Delay Sweep:
Keeping the A input channel syned with T0, we sweep the rest if the channels to determine the width of the coincidence pulses.  

Resolution Sweep:
Increase the pulse width of all the channel A,B,A' and B' to find the true pulse width.

Voltage Sweep:
Increase the pulse voltage of all the channel A,B,A' and B' to find the optimum voltage.

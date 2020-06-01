# Firefly synchronization project
Project attempts to make a model of firefly flash synchronisation.

Each firefly has its own flashing period.
Synchronisation is achieved with two period changing mechanisms:
1) If some neighbour firefly flashes, firefly observing that flash subtracts some value from its period.
2) If in the time between two flashes most of the neighboring fireflies didn't flash, firefly adds some value to its period.

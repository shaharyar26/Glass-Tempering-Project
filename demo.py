"""
demo.py  --  a teaching script, not part of the simulation.

It shows, with tiny numbers you can follow by hand, the three ideas
that confused people most:

  1. What the slices left / self / right actually grab.
  2. How "left + right - 2*self" decides heating or cooling.
  3. Why we multiply by the 0.2 factor and ADD it to step forward.

Plus one line each for Newton cooling and the VFT freezing point.

Run it with:  python demo.py
"""

import numpy as np


print("=" * 60)
print("PART 1:  the slices (left, self, right)")
print("=" * 60)

# A tiny glass with just 5 layers. Surfaces cold, core hot.
T = np.array([200, 400, 650, 400, 200], dtype=float)
print(f"\nAll layers:        {T}")
print(f"positions (index):  0    1    2    3    4")

# The three slices used in the conduction formula.
self_layers  = T[1:-1]   # the inner layers we update
left_layers  = T[:-2]    # each inner layer's LEFT neighbour
right_layers = T[2:]     # each inner layer's RIGHT neighbour

print(f"\nself  = T[1:-1] = {self_layers}   (the inner layers)")
print(f"left  = T[:-2]  = {left_layers}   (their left neighbours)")
print(f"right = T[2:]   = {right_layers}   (their right neighbours)")
print("\nRead them in columns. Each column is one inner layer")
print("sitting between its left and right neighbour.")


print("\n" + "=" * 60)
print("PART 2:  left + right - 2*self  (heat in minus heat out)")
print("=" * 60)

bracket = right_layers + left_layers - 2 * self_layers
print(f"\nbracket = left + right - 2*self = {bracket}")
print("\nWhat each number means:")
for i in range(len(bracket)):
    b = bracket[i]
    if b < 0:
        verdict = "hotter than neighbours -> will COOL"
    elif b > 0:
        verdict = "cooler than neighbours -> will WARM"
    else:
        verdict = "balanced -> no change"
    print(f"  inner layer {i+1}: self={self_layers[i]:.0f}, "
          f"left={left_layers[i]:.0f}, right={right_layers[i]:.0f}  "
          f"-> {b:+.0f}  ({verdict})")


print("\n" + "=" * 60)
print("PART 3:  the 0.2 factor, and why we ADD it")
print("=" * 60)

factor = 0.2   # this is alpha*dt/dx**2, kept at 0.2 for stability
print(f"\nfactor (alpha*dt/dx**2) = {factor}")
print("It converts the bracket (a comparison) into real degrees.")
print("It is kept below 0.5 so the simulation stays stable.\n")

change = factor * bracket
new_T_inner = self_layers + change   # new = old + change

print("new temperature = old temperature + factor * bracket")
for i in range(len(bracket)):
    print(f"  inner layer {i+1}: {self_layers[i]:.0f} + "
          f"{factor} x ({bracket[i]:+.0f}) = "
          f"{self_layers[i]:.0f} + {change[i]:+.1f} = {new_T_inner[i]:.1f}")

print("\nThat is ONE time step. The real code repeats this thousands")
print("of times, and the heat slowly drains out of the glass.")


print("\n" + "=" * 60)
print("PART 4:  Newton cooling at the surface (one number)")
print("=" * 60)

T_surface = 650.0
T_air = 20.0
fixed_chunk = 0.03   # stands in for 2*H_CONV*dt/(RHO*CP*dx), a constant
gap = T_air - T_surface
drop = fixed_chunk * gap
print(f"\ngap = T_air - T_surface = {T_air:.0f} - {T_surface:.0f} = {gap:.0f}")
print(f"surface change = fixed_chunk x gap = {fixed_chunk} x ({gap:.0f}) "
      f"= {drop:.1f} degrees")
print("Big gap -> fast cooling. As the surface cools, the gap shrinks,")
print("so cooling slows down. The gap is the only part that changes.")


print("\n" + "=" * 60)
print("PART 5:  VFT freezing temperature (one number)")
print("=" * 60)

A, B, T0 = -4.06, 6111.0, 160.0      # fitted to soda-lime glass
log_eta_freeze = 12.0                 # stiffness where stress locks in
T_freeze = T0 + B / (log_eta_freeze - A)
print(f"\nfitted constants: A={A}, B={B}, T0={T0}")
print(f"freezing temperature = T0 + B/(12 - A)")
print(f"                     = {T0} + {B}/({log_eta_freeze} - ({A}))")
print(f"                     = {T_freeze:.0f} C")
print("This is the temperature where the simulation takes its snapshot.")

print("\nDone. Change the numbers at the top of each part and re-run")
print("to see how the result moves.")

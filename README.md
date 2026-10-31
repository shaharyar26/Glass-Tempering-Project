# Glass Thermal Tempering Simulation

A 1D physics simulation of the air-quench step in flat glass tempering.
It predicts the residual stress profile through the thickness of a
soda-lime glass sheet, i.e., the compression at the surfaces and the
tension in the core that make tempered glass strong.

This is the same quantity a SCALP polariscope measures on real glass.

![Residual stress profile](outputs/stress_profile.png)

## Objective

The goal is to predict the residual stress inside tempered glass from the
process settings alone, without measuring a real sample.

That stress profile, i.e., compression at the surfaces and tension in the
core, is what makes tempered glass strong and safe. Normally you need a
SCALP instrument and a finished piece of glass to see it. This simulation
computes it from the quench conditions instead, i.e., the glass thickness,
the start temperature, and how hard the air cools it.

Why it matters:

- It turns a measured-after-the-fact quantity into a predicted-in-advance one.
- It is the building block for later work, i.e., linking furnace and quench
  settings to the final glass quality.
- The same method applies to any thermal heat-treatment process, not only glass.

## What it does

The simulation follows the glass through the quench:

1. A hot glass sheet (650 C) is suddenly cooled by air at both faces.
2. Heat flows out through the thickness. The sheet is split into thin
   layers and each layer's temperature is tracked step by step in time
   with a finite-difference method.
3. The glass "freezes" when it drops through the setting temperature.
   Above that temperature stress relaxes away. Below it, stress locks in.
   The setting temperature comes from a VFT viscosity model of the glass.
4. The temperature profile frozen in at that moment, once the sheet
   cools fully to room temperature, produces the residual stress.
   The hotter core contracts more and ends in tension. The cooler
   surfaces end in compression.

![Temperature during quenching](outputs/temperature_evolution.png)

## Result

With a 4 mm sheet and a strong air quench:

| Quantity | Value |
|---|---|
| Surface stress | about -105 MPa (compression) |
| Core stress | about +58 MPa (tension) |
| Surface-to-core ratio | about 1.8 : 1 |

These values and the parabolic shape match what is measured on fully
tempered soda-lime glass.

## How to run

```bash
pip install -r requirements.txt
cd src
python tempering_sim.py
```

The plots are written to the `outputs/` folder.

## What to change

All inputs are at the top of `src/tempering_sim.py`:

- `H_CONV` is the quench strength. Higher means a harder quench and more
  stress. This is the main knob.
- `THICKNESS`, `T_START`, and the material properties can all be edited.

## Repository layout

```
glass-tempering-simulation/
  src/
    viscosity.py       VFT viscosity model, gives the freezing temperature
    tempering_sim.py   the 1D heat + residual stress simulation
  outputs/             generated plots
  requirements.txt
```

`viscosity.py` is a reusable material model. The tempering simulation
imports it to find the temperature at which stress sets.

## Theory

This simulation combines three established theories with a glass viscosity
model. Together they form the instant-freezing theory of glass tempering.

**1. Fourier's theory of heat conduction.**
Governs how heat flows through the glass thickness. It gives the heat
conduction equation, i.e., heat moves from hot regions to cold ones at a
rate set by the material. This is solved for every inner layer of the glass.

**2. Newton's law of cooling.**
Governs heat leaving the two surfaces into the quench air. The bigger the
gap between the surface and the air, the faster the surface cools. This is
the convection term controlled by the `H_CONV` setting.

**3. Thermoelasticity (theory of thermal stresses).**
Turns the frozen-in temperature differences into permanent stress. The core
idea: when a solid cools unevenly, different parts want to shrink by
different amounts, and that mismatch locks in stress.

**4. Vogel-Fulcher-Tammann (VFT) viscosity model.**
Describes how glass viscosity changes with temperature. It supplies one key
value, i.e., the freezing temperature where stress stops relaxing and starts
to set. This comes from the `viscosity.py` module.

**The combined model: instant-freezing theory (Bartenev / Gardon).**
This is the named theory the whole simulation rests on. The glass is treated
as a stress-free liquid above the freezing temperature and an elastic solid
below it. The stress is set by the temperature profile frozen in at the
moment the core passes through the freezing point. After that, the sheet
cools to room temperature and the locked-in differences become the final
residual stress.

**Numerical method: finite-difference method (explicit scheme).**
The heat equation cannot be solved by hand here, so the thickness is split
into thin layers and time is advanced in small steps. Each layer's new
temperature is found from its neighbours. The time step is kept small for
numerical stability.

## Assumptions and limits

- Heat flows in one direction only, i.e., through the thickness.
- The glass freezes at a single temperature, not across a transition range.
- Material properties are constant and are standard literature values for
  soda-lime glass.
- A strong, uniform quench is applied to both faces.

## The next theory up: viscoelastic relaxation (Narayanaswamy)

Real glass does not freeze at one temperature. It passes through a transition
range, and stress builds up gradually across it. The Narayanaswamy model
captures this, i.e., it tracks how the glass relaxes stress as it cools
through the transition. It is the recognized, higher-accuracy upgrade from
the instant-freezing theory used here. This is the planned next step.

## Next steps

- Replace the instant-freezing step with a viscoelastic (Narayanaswamy)
  stress relaxation model for higher accuracy.
- Sweep quench strength and thickness to map stress against process
  settings.
- Extend to the bending step for automotive windshields.

## Author

Muhammad Shaharyar Siddique
Materials engineer. GitHub: [shaharyar26](https://github.com/shaharyar26)

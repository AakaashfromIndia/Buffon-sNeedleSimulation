## Buffon's Needle experiment simulation

A Python-based interactive simulation of Buffon's Needle experiment, a classic Monte Carlo method for estimating the value of π by randomly dropping sticks of a particular length on a surface with lines separated by an interval which is of the same length as the sticks.

The ratio of the number of sticks that touch a line to the total number of sticks tends to approach pi

![BuffonsNeedle - Made with Clipchamp (3)](https://github.com/user-attachments/assets/c88c84c2-6010-4d4b-8033-40ccdfbe70ab)

Basically, it is a probability experiment that estimates π by analyzing the likelihood of a needle crossing parallel lines when dropped at random. Given a stick length L and the line spacing D (with L ≤ D), the probability of a cross is 2L/πD

## Controls

* Click buttons to drop more sticks (+1, +5, ..., +5K)
* Watch needles fall and observe estimated π value update
* RESET clears the simulation
* Each stick is dropped with a random center position and angle.
* Cross detection is determined by checking if a stick spans across any two adjacent vertical lines.
* Estimates are dynamically calculated and plotted based on stick count and number of line intersections.


## Requirements: 

```bash
pip install numpy matplotlib
```

---

## How to Run

Clone the repo and run the simulation:

```bash
git clone https://github.com/your-username/buffon-needle-simulation.git
cd buffon-needle-simulation
python buffon_needle.py
```

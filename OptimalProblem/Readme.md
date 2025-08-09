# Basic Breakdown

## Question / Problem
If we have the signal strength of multiple routers from various arbitrary points,  
how can we map or approximate where each router is with respect to one another?

> [!NOTE]
> For this problem, imagine there are no obstacles — just a flat ground (surface).  
> That is, we are ignoring the possibility of any walls or obstructions.

---

## For Example
Imagine:

- **Point A** → Measures signal strength from `R1`, `R2`, and `R3`.
- **Point B** → Different unknown location, measures signal strength from the same routers, but with different values.
- **Point C** → Another unknown location, again with different strengths.

We don’t know:
- The coordinates of these points.
- The exact location of the routers.

We do know:
- The signal strength to each router at each measurement point.

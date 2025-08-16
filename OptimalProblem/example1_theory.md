> [!NOTE]
> This covers the theory behind the algorithm. <br />
> `The idea is to look at the min and max distance possible between the different routers`

---

# O1 -- Distance to Routers from Origin 1

**R1:** `10`  
**R2:** `20`  
**R3:** `25`  

> We are given only these values.

## Distance Between Each Router
- **R1 → R2:** `|20 - 10|` → **10** &nbsp; <> &nbsp; **30** ← `|20 + 10|`
- **R1 → R3:** `|25 - 10|` → **15** &nbsp; <> &nbsp; **35** ← `|25 + 10|`
- **R2 → R3:** `|25 - 20|` → **5** &nbsp; <> &nbsp; **45** ← `|25 + 20|`

> **Min distance:** Smallest difference between the distances of two routers from the origin.  
> **Max distance:** Sum of the distances of the two routers from the origin.  
> This gives us a **range** for the possible distance between routers.

---

# O2 -- Distance to Routers from Origin 2

**R1:** `18.03`  
**R2:** `5`  
**R3:** `10`  

## Distance Between Each Router
- **R1 → R2:** `|18.03 - 5|` → **13.03** &nbsp; <> &nbsp; **23.03** ← `|18.03 + 5|`
- **R1 → R3:** `|18.03 - 10|` → **8.03** &nbsp; <> &nbsp; **28.03** ← `|18.03 + 10|`
- **R2 → R3:** `|5 - 10|` → **5** &nbsp; <> &nbsp; **15** ← `|5 + 10|`

---

# Total Conclusion With All Data

- **R1 → R2:** `13.03 <> 23.03`  
- **R1 → R3:** `8.03 <> 28.03`  
- **R2 → R3:** `5 <> 15`

> As we repeat the process, the accuracy of the range becomes **tighter** and approaches the actual distance, which is so cool! <br />
> **Check it out in action:** Run `example1.py`

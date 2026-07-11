# DMRC Metro Route and Schedule Simulator

A Python command-line program that simulates the Delhi Metro Rail Corporation (DMRC) network — computing next-train arrival times and planning the shortest journey between any two stations on the Blue, Magenta, and (bonus) Yellow lines.

Built as an assignment for **Introduction to Programming (CSE101)**.

**Author:** Sifat Kaur Kochar

---

## Overview

The simulator works entirely off a plain-text data file (`data.txt`) — no external libraries such as `pandas`, `numpy`, or `pickle` are used, only basic file I/O, per the assignment constraints.

It provides two core features through an interactive menu:

1. **Next Metro Timings** — given a line, a station, the terminal station of your direction of travel, and the current time, the program calculates the next scheduled metro and the two metros after it.
2. **Journey Planner** — given a source and destination station, the program determines whether the route lies on a single line or requires travelling across lines, then computes the fastest path and total travel time using a breadth-first search over the station network.

---

## Lines Covered

| Line | Route |
|---|---|
| Blue (L3) | Dwarka Sector 21 ↔ Noida Electronic City |
| Blue (L4) | Dwarka Sector 21 ↔ Vaishali |
| Magenta (L8) | Janakpuri West ↔ Botanical Garden |
| Yellow (L2) *(bonus)* | Samaypur Badli ↔ Millennium City Centre Gurugram |

On the shared Blue Line segment (Dwarka Sector 21 → Yamuna Bank), L3 and L4 services are assumed to alternate.

---

## Repository Contents

| File | Description |
|---|---|
| `main.py` | Main program — data loading, timing logic, and journey planner |
| `data.txt` | Structured data file: metro lines, station order & travel times, interchange points, schedule, and fare slabs |
| `documentation.txt` | This file — data sources, assumptions, and run instructions for the full project, including the bonus Yellow Line |

---

## How It Works

### Data Loading
`data_func()` reads `data.txt` and parses it into a dictionary keyed by its five sections — `Metro_Line`, `Stations`, `Interchange`, `Schedule`, and `Fare` — with each row stored as a sub-dictionary of field names to values.

### Next Metro Timings
Using the configured service window (06:00–23:00) and peak-hour bands (08:00–10:00 and 17:00–19:00), the program builds the full day's timetable at the terminal station, offsets it by the cumulative travel time to the requested station, and returns the next scheduled arrival plus the two after it.

- Off-peak frequency: every 8 minutes
- Peak-hour frequency: every 4 minutes

### Journey Planner
`from_to_time()` converts the station data into an adjacency list of travel times, and `route_shortest_time()` performs a breadth-first traversal to find the path and cumulative time between the source and destination. The program also reports whether the two stations lie on the same line. (See [Code-Level Notes](#code-level-notes) below for a note on its handling of interchanges.)

---

## Running the Program

```bash
python metro_simulator.py
```

Ensure `data.txt` is in the same directory as `metro_simulator.py`.

**Input format:**
- Line names and station names must be entered in **CAPITAL LETTERS**, matching the names in `metro_data.txt`.
- Times must be entered in 24-hour `HH:MM` format (e.g., `09:18`).

**Menu options:**
```
1. Compute next metro timings.
2. Compute journey/path and time between stations.
3. Exit.
```

### Example — Next Metro Timings
```
Enter metro line : BLUE
Enter current station : RAJIV CHOWK
Enter terminal station of your direction : NOIDA ELECTRONIC CITY
Enter current time : 09:18

Next metro arrives at -  09:20
Subsequent metros at -  09:24 09:28
```

### Example — Journey Planner
```
Enter current station : DWARKA SECTOR - 21
Enter destination station : R.K.PURAM

Route is NOT on a single line.
Your Path -
DWARKA SECTOR - 21--DWARKA SECTOR - 8--DWARKA SECTOR - 9--DWARKA SECTOR - 10--
DWARKA SECTOR - 11--DWARKA SECTOR - 12--DWARKA SECTOR - 13--DWARKA SECTOR - 14--
DWARKA--DWARKA MOR--NAWADA--UTTAM NAGAR WEST--UTTAM NAGAR EAST--JANAKPURI WEST--
DABRI MOR - JANAKPURI SOUTH--DASHRATHPURI--PALAM--SADAR BAZAR CANTONMENT--
TERMINAL 1-IGI AIRPORT--SHANKAR VIHAR--VASANT VIHAR--MUNIRKA--R.K.PURAM
Time Taken -  57 minutes.
```

---

## Data Sources & Assumptions

All station names, line data, and travel times were collected from the official DMRC website ([delhimetrorail.com](https://delhimetrorail.com/)), including the [system map](https://delhimetrorail.com/map). Inter-station distances (used for fare-slab data) were measured manually using Google Maps' "Measure Distance" feature, which provides straight-line aerial distance rather than actual track distance.

Key assumptions made while structuring the data:

- **Blue Line:** Modeled as two branches sharing a common trunk — L3 (Dwarka Sector 21 → Noida Electronic City) and L4 (Dwarka Sector 21 → Vaishali) — with services assumed to alternate between the branches on the shared segment.
- **Magenta Line:** Modeled as Janakpuri West ↔ Botanical Garden. The newly operational Krishna Park Extension station (ahead of Janakpuri West) was not included.
- **Yellow Line *(bonus)*:** Modeled as Samaypur Badli ↔ Millennium City Centre Gurugram, reflecting the station's updated official name (previously referred to as HUDA City Centre in older sources).
- **Interchange delay:** No official interchange-time data is published by DMRC, so delay values were estimated based on the general layout/complexity of each interchange station, as described online.
- **Fare slabs:** DMRC's highest published fare slab applies to distances "more than 32 km." This was modeled as a 32–999 km range, with 999 used as an arbitrarily large upper bound.

### Code-Level Notes

- `data_func()` reads `data.txt` line by line and organizes it into a dictionary keyed by the file's five section headers (`Metro_Line`, `Stations`, `Interchange`, `Schedule`, `Fare`). Each row under a header becomes its own sub-dictionary, keyed by the sub-headings noted in the file's `#` comment rows.
- **Station ordering (forward direction):**
  - Blue (L3): Dwarka Sector 21 → Noida Electronic City
  - Blue (L4): Dwarka Sector 21 → Vaishali
  - Magenta: Janakpuri West → Botanical Garden
  - Yellow: Samaypur Badli → Millennium City Centre Gurugram
- All station and line names must be entered in **CAPITAL LETTERS**, and times in `HH:MM` format, matching the conventions used in `data.txt`.
- The journey planner (`from_to_time()`, `route_shortest_time()`, `best_route_time()`) uses a breadth-first search to find the shortest-time path between two stations — an approach adapted from [GeeksforGeeks' BFS explainer](https://www.geeksforgeeks.org/dsa/breadth-first-search-or-bfs-for-a-graph/). It correctly returns a path and total time for stations on the same or different lines, and reports whether an interchange is required, but does not factor the number of interchanges or interchange delay minutes into the final time.

---

## Assignment Scope

This project was built to satisfy the following assignment requirements:
- Load and structure real-world DMRC station and schedule data from a flat text file
- Compute upcoming metro arrivals at any station based on time-of-day service frequency
- Plan a journey between two stations, identifying whether an interchange is required
- **Bonus:** Extended the network to include the Yellow Line
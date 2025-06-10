# Development log – Project programming II

# Phase 0: Project start
**Date:** April 9, 2025 Initial meeting.
- Defined the components: Dataset + Database + Visualization.
- Two possible project approaches:
  - Option 1: Web scraping + Linux cron + Monte Carlo simulation
  - Option 2: Web front end + Python package + Monte Carlo simulation
- Chosen general theme: spatial data analysis.
- Started the structure of the GitHub repository.

**Date:** April 10 - 14, 2025
- Second meeting.
- Github implementation.
- project developement

**Date:** April 23-24, 2025
- Retrieving data
- Project subdivision in 4 task
  - 2 p data analysis
  - 1 p Monte Carlo simulation
  - 1 p LLM implementation

---

### **Phase 1: Problem Definition**

**Date:** May 7, 2025
**Goal:** Analyze the relationship between road traffic and atmospheric pollutants in Canton Ticino, with the possibility to generate future scenarios using simulations.
**Decision:** Develop a modular Python package with potential extensions such as a web front end or automatic analysis descriptions via a local LLM.

---

### **Phase 2: Data Search & Selection**

**Date:** May 8–10, 2025
**Initial approach:** Attempted collection from Swiss environmental portals using web scraping.
**Issues encountered:**

* Legal limitations on data use and redistribution
* Inconsistent web layouts unsuitable for scraping
* Noise data available only at two stations—not enough for meaningful analysis

**Solution adopted:**

* Switched to using OASI data (Swiss Environmental Observatory), publicly accessible
* Embedded datasets directly within the package for reproducibility
* Dropped the noise pollution component from the project

---

### **Phase 3: Data Preparation & Cleaning**

**Date:** May 11–13, 2025
**Actioned via:** Script A (`data_anal.ipynb`)
**Steps performed:**

* Imported all CSV files from various folders
* Harmonized column names and formats
* Aggregated data per category (traffic, pollutants, meteorology)
* Saved processed files into `data/all`, `data/media`, and `data/stazioni_singole`

**Challenges:**

* Inconsistent file structures
* Different temporal granularities between stations

**Resolution:** Used pandas to standardize formats and saved intermediate datasets

---

### **Phase 4: Initial Correlation Analysis**

**Date:** May 14–16, 2025
**Objective:** Check for linear correlation between pollutants and traffic levels

**Findings:**

* Correlations were weak or even negative
* Some stations displayed counterintuitive behavior

**Hypotheses formed:**

* Weather variables might be affecting pollutant levels
* Non-linear effects or time lags were not yet captured

---

### **Phase 5: Incorporation of Meteorological Variables**

**Date:** May 17–18, 2025
**Action:** Download weather data (temperature, pressure, humidity, wind) for each station from official sources

**Result:**

* Correlations became much stronger and statistically meaningful
* Better explanation of pollutant variance

---

### **Phase 6: Weather Data Licensing Issue**

**Date:** May 19, 2025
**Problem:** Meteorological data cannot be redistributed in raw form

**Solution:**

* Extracted parameters from the data (e.g., mean, standard deviation, normalized trends)
* Stored only these parameters in the package, enabling realistic simulation without breaching licensing rules

---

### **Phase 7: Development of `Monte_verita_simulation()`**

**Date:** May 20–24, 2025
**Created:** The core Monte Carlo simulation function

**Features:**

1. Supports three trend modes:

   * Arbitrary trend
   * Historical trend (selectable period)
   * Modified historical trend (additive/multiplicative factors)
2. Optional integration of parametrized meteorological variables
3. Outputs structured for easy export to visualization tools

**Resolved challenges:**

* Seed control for reproducibility
* User input validation
* Modular design for future enhancements

---

By this stage, the project has established a **solid technical foundation**, meeting the minimum requirements: a **Python package** with **Monte Carlo simulation** capabilities.

---


---
name: "trademe-chart-color-palette"
created: "2026-08-19T20:00:42.122Z"
status: pending
---

# Trade Me Chart Color Palette Design

## Context

**Brand colors** extracted from [brandcolorcode.com/trade-me](<> "https://www.brandcolorcode.com/trade-me"):

| Role             | Hex       | RGB             |
| ---------------- | --------- | --------------- |
| Orange (primary) | `#FFAA33` | (255, 170, 51)  |
| Blue (secondary) | `#0094E0` | (0, 148, 224)   |
| White            | `#FFFFFF` | (255, 255, 255) |
| Black            | `#000000` | (0, 0, 0)       |

The workshop app (Module 4) is a multi-page Streamlit dashboard with bar charts, line charts, KPI cards, and stacked bars. It needs:

- A **categorical palette** (6-8 distinct colors for multi-series charts)
- **Semantic/status colors** (good, warning, danger for threshold alerts)
- **Sequential scales** (single-hue gradients for heatmaps or intensity)
- **Diverging scale** (for MoM change comparisons)

---

## Palette Design

### 1. Categorical Palette (8 colors)

Built by starting with the two brand anchors (Orange, Blue), then extending with perceptually balanced complements that sit well on both light and dark backgrounds.

```
Position  Name              Hex        Derivation
--------  ----              ---        ----------
1         TM Orange         #FFAA33    Brand primary
2         TM Blue           #0094E0    Brand secondary
3         Deep Teal         #00A88F    Analogous to Blue, green shift
4         Warm Red          #E05A3A    Warm complement to Blue
5         Violet            #7B61D1    Cool accent bridging Blue/Red
6         Gold              #D4910A    Darker orange for second orange-family series
7         Sky Blue          #4DC4F0    Lighter tint of brand Blue
8         Charcoal          #3D3D3D    Neutral anchor for "Other" categories
```

Visual swatch order (primary data series should use positions 1-2 first, then extend):

```
 #FFAA33  #0094E0  #00A88F  #E05A3A  #7B61D1  #D4910A  #4DC4F0  #3D3D3D
 -------  -------  -------  -------  -------  -------  -------  -------
```

### 2. Semantic / Status Colors

Used for KPI cards, threshold alerts, and conditional formatting:

```
Status    Hex        Usage
------    ---        -----
Green     #2EAE60    Positive / on-track / above target
Yellow    #F5C542    Warning / approaching threshold
Red       #D94040    Danger / below threshold / needs attention
Neutral   #6B7280    No status / informational
```

These map to the app's threshold alerts:

- Sell-through rate: Red below 25% (`#D94040`), Yellow below 35% (`#F5C542`), Green otherwise (`#2EAE60`)
- Escalation rate: Red above 20%, Yellow above 15%
- YoY decline: Yellow warning

### 3. Sequential Scale (single-hue, 5 stops)

Based on brand Blue for intensity-based visuals (e.g., heatmaps, density):

```
#E0F2FE -> #7DCBF5 -> #0094E0 -> #006BA8 -> #003D61
 lightest                                     darkest
```

Based on brand Orange for warm intensity:

```
#FFF0D6 -> #FFCC7A -> #FFAA33 -> #C07A10 -> #7A4D00
 lightest                                     darkest
```

### 4. Diverging Scale (5 stops)

For MoM comparison (negative to positive change):

```
#D94040 -> #F5A3A3 -> #F0F0F0 -> #7DCBF5 -> #0094E0
 decline     slight-    neutral    slight+    growth
             decline                increase
```

---

## Implementation Steps

### Step 1: Define primary brand-derived chart palette

Create a Python module (`palette.py` or constants in the app) that exposes the categorical palette as a list, and individual named colors.

```python
# Trade Me Chart Palette
TM_ORANGE = "#FFAA33"
TM_BLUE = "#0094E0"
DEEP_TEAL = "#00A88F"
WARM_RED = "#E05A3A"
VIOLET = "#7B61D1"
GOLD = "#D4910A"
SKY_BLUE = "#4DC4F0"
CHARCOAL = "#3D3D3D"

CATEGORICAL_PALETTE = [
    TM_ORANGE, TM_BLUE, DEEP_TEAL, WARM_RED,
    VIOLET, GOLD, SKY_BLUE, CHARCOAL,
]
```

### Step 2: Define semantic status colors

```python
STATUS_GREEN = "#2EAE60"
STATUS_YELLOW = "#F5C542"
STATUS_RED = "#D94040"
STATUS_NEUTRAL = "#6B7280"
```

### Step 3: Define sequential and diverging scales

```python
SEQ_BLUE = ["#E0F2FE", "#7DCBF5", "#0094E0", "#006BA8", "#003D61"]
SEQ_ORANGE = ["#FFF0D6", "#FFCC7A", "#FFAA33", "#C07A10", "#7A4D00"]
DIVERGING = ["#D94040", "#F5A3A3", "#F0F0F0", "#7DCBF5", "#0094E0"]
```

### Step 4: Add palette as a Python constant module

Place the file at `marketplace-listings-app/palette.py` (or inline in the Streamlit app) so it can be imported and used in Altair/Plotly/Matplotlib chart configurations during the workshop.

Usage example with Streamlit + Plotly:

```python
import plotly.express as px
from palette import CATEGORICAL_PALETTE

fig = px.bar(df, x="category", y="count", color="region",
             color_discrete_sequence=CATEGORICAL_PALETTE)
```

---

## Verification

- Confirm all 8 categorical colors pass WCAG contrast ratio (4.5:1) against white background for text labels
- Verify the palette is distinguishable for common forms of color blindness (use a simulator like Coblis)
- Test in both Streamlit light and dark themes

## Critical Files

- `marketplace-listings-app/palette.py` — New module housing all palette constants
- `marketplace-listings-app/streamlit_app.py` — Primary consumer of the palette (chart rendering)
- README.md — Workshop instructions referencing branding choices

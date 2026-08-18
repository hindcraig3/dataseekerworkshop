# Trade Me Data Seekers Workshop
## Snowflake Self-Service Data Skills

---

## Overview

| | |
|---|---|
| **Audience** | ~48 non-data specialists: Commercial, Developers, LSEs, Product Owners, Ads, CX |
| **Duration** | Full day (~4.5 hours) or two sessions |
| **Format** | Instructor-led with hands-on exercises; cohorts of 8–10 recommended |
| **Prerequisite** | Snowflake login and access to Trade Me's Snowflake environment |

### The Problem This Workshop Solves

Data Seekers at Trade Me currently rely on slow, inflexible paths to get answers:
- PBI reports that are hard to find and can't be customised
- CoWork data that's well curated but not always granular enough
- Analysts who are great but capacity-constrained
- Ad-hoc SQL that some write but with low confidence — and SQL Server is going away

This workshop gives them a new path: **Snowflake + Cortex Code (CoCo)** — AI-assisted, self-service, repeatable, and shareable.

### Learning Outcomes

By the end of this workshop, participants will be able to:

1. Navigate Snowflake and understand where Trade Me's data lives
2. Use CoCo to write and iterate on SQL queries without needing to be a SQL expert
3. Build a reusable analysis notebook combining SQL, Python, and interactive visualisations
4. Save and organise their work in personal workspaces for future reuse
5. Scaffold a simple Streamlit app to turn a recurring question into a team-accessible tool

---

## Workshop Flow

### Session 0 — Setting the Scene

**Learning Objective:** Understand how Snowflake fits into Trade Me's data landscape and why this matters for each team.

**Flow:**
1. Quick pulse check: "How do you currently get data?" (show of hands / Mentimeter)
2. Facilitator presents the current data journey vs the future state
3. Overview of Trade Me's Snowflake environment: what data exists, where it lives (databases, schemas), and what CoWork provides vs raw access
4. Introduce the day's scenario: *"You're a data analyst for a day across Trade Me's four business areas: Marketplace, Motors, Properties, and Jobs"*
5. Logistics: Snowflake login, workspace setup, CoCo access confirmation

**Snowflake Skills / Features:**
- Snowsight navigation (worksheets, data catalog, CoWork)
- Understanding databases, schemas, and roles

---

### Module 1 — Your Personal Data Lab: Workspaces *(20 min)*

**Learning Objective:** Set up and use a personal workspace, understand the workspace types available (personal, shared, git-backed), and organise files for future reuse.

**Scenario:** *"You're investigating whether Motors listings in Auckland are showing a seasonal dip. Before sharing anything with your team, you need a private space to explore."*

**Flow:**

1. **Exercise — Create Your Workspace and run a SQL query:**
   - Lets create a new personal workspace for the workshop . Click the + icon at the top of the workspaces panel and select **Private Worksapce**. Name your workspace:  `<your_name>_data_lab`. 
   - Create a new SQL file inside your Worksapce by clicking the **+ Add New** button and selecting **SQL file**
   - Name the file : **Module1.sql**
   - Copy and paste this query into the worksheet and run the query by clicking the blue **Run** button in the top left hand of the worksheet.
   ```
   select * from tm_workshop.sampledata.jobs_listings limit 500;
   ```
  

2. **Exercise - Explore the resutls pane:**
 
   The results pane is where you can view, and work with, the results of a query.  

      ---
      **Table tab** - Shows tabular results. It shows a profile of the data ion each column. This can be toggle on and off by clikcing the ** Show Column Stats** icon ( The little graph in the top left cell of the results) You can also search within the results set, show / hide columns, acess the query plan, and download the results as a CSV. 
      - 2.1.Click the **Search** icon and seearch for "Legal". Note how it filters the results. Clear the search box by clicking the X icon in the search box.
      - 2.2 Click the **Column Selection** icon. Untick the USERID column and click the *Apply** button at the bottom of the list. Note how the column is removed from the results set. 
      - 2.3 Click the **Download** icon. This allows you to downlaod the results set as a CSV file. 
      ---
      **Chart Tab** - This allows you to create basic charts directly from the results set. Its great for quickly visualising the results.

      - 2.4 Click the **Chart** button then select **Bar Chart** from the Chart Type drop down. 
      - 2.5 Select INDUSTRY as the x-axis colomn
      - 2.6 Select LISTING_ID as the Y-axis column. 
      - 2.7 Change the Aggregate to COUNT.
      - 2.8 Change the Group by to ROLE_TYPE
      ---
      **Pivot Tab** - This allows you to create a pivot table directly from the results set.
      - 2.9 Click the **Add row Fields** box and select the INDUSTRY column
      - 2.10 Click the **Add column Fields** box and select the ROLE_TYPE column
      - 2.11 Click the **Add value Fields** box and select LISTING_ID. Change the Aggregation to COUNT


3. **Wrap-up (5 min):** Key message — *there are three workspace types: personal (your private scratchpad), shared (a team folder), and git-backed (for versioned team assets). Today you'll work in your personal workspace; the other types are where finished work eventually lives.*

**Snowflake Skills / Features:**
- Snowflake Workspaces (personal workspace — hands-on; shared and git-backed — concept awareness)
- Workspace file management
- Workign with the Results pane for simple analysis, charting, and pivot tables

---

### Module 2 — From Question to Answer: AI-Assisted SQL with CoCo

**Learning Objective:** Use Cortex Code (CoCo) to write, refine, and understand SQL queries — starting from plain English and building up to multi-step analysis — without needing to be a SQL expert.

**Scenario:** *You're a Product / LSE team member. Your Product Owner wants to know: "Are our listings performing as expected? Where are the anomalies?" You need to turn that business question into SQL queries and ultimately a reusable analysis.*

**Flow:**

1. **Exercise 2a — Simple Query from Plain English (15 min):**
   
   1.1 Create a new SQL file in your workspace.
   
   1.2 Rename it to **Module2.sql**. 
   
   1.3 Click the CoCo tab on the right hand sde to display the CoCo panel. 
   
   1.4 Copy and paste the following prompt into CoCo, run the generated SQL, and verify the output looks correct:

   ``` 
   How many job listings are there? 
   ```

   Note that CoCo just answered the question. You can see the SQL it generated by clicking the "Expand" icon. You can copy the SQL and paste it into the work sheet or you could be more explicit in your prompt. 
   
   1.5 Copy and paste the following into CoCo. 

   ``` 
   Create a new query that returns how many listings there are?
   ```
   Note this time CoCo adds the SQL to the SQL worksheet. Also note how it highlights the changes and provides the option to "Keep" the changes or "Undo" the changes. Click "Keep". 

   1.6 There are multiple listings tables in the database - Jobs, Motors, Marketplace, property. What happens if quickly want to check Motors? You could explicitly mention motors listings in your prompt but you can also provide CoCo with Context to guide it to the right database, schmea, table, or view for example. 

   1.7 Click the **+** icon in the CoCo window, then type MOTORS in the search box. The MOTORS_LISTINGS table shoudl be displayed in the list. Click **MOTORS_LISTINGS** to add this table as Context for CoCo.

   ![](assets/cococontext.png)

   1.8 Now copy and paste the following prompt.

   ```
   How many listings are there?
   ```

   Note how CoCo queries the motor_listing table. This is because we provides the table as context. Providing context like this is useful when you have acess to a lot of databases, schmes, and tables. It mans CoCo does not need to waste time ( and tokens) performing metadata queries to try and figure out what tables it needs to query. 

2. **Exercise 2b — Iterate and Refine (15 min):**
   
   Now ask CoCO these questions in turn.  IF CoCo changes the SQL in the Worksheet just click "Keep Changes"
   ```
   Now create a query to show open job listings by category
   ```
   Note how  it creates a new query and includes a WHERE clause thats filters the data on status, and a GROUP BY clause to get the count per category

   ```
   create a query to return total job listings per month per category for the last 18 months
   ```
   Note how the SQL gets a bit more complicated. You may see DATE functions being used along with filters in the WHERE clause and grouping via the GROUP BY clause. 

   ```
   Refine that query to also show the difference comapred to the previous month
   ```
   Note that it modified the last query it created even though you only said "refine that query...". You will notice the SQL query might now include a sub-query and some different functions. 

   Now with your mouse **highlight** the query and then select **Explain** form the menu that pops up. CoCo will then explain what the query is doing. This is great for understanding SQL that CoCo generates or if you are using SQL written by someone else. 

   ![](assets/cocoexplain.png)




3. **Exercise 2c — Advanced Query: Multi-Join, CTEs, Aggregation, and JSON (25 min):**

   Ask CoCo to build a more complex query that combines multiple tables, uses a CTE to organise the logic, and extracts fields from a JSON/VARIANT column. This mirrors the kind of question an analyst would normally tackle.

   > *"Using a CTE, join listings to users and contacts. For each user segment and region, show: active listing count, average listing age in days, contact rate (contacts per listing), and extract the user preferences JSON field from the users table. Filter to listings created in the last 90 days."*

   Once the query runs:


4. **Exercise 2d — Building a Progressive Analysis (20 min):**

   Now you'll build a sequence of queries that tell a story — each one building on the last. Ask CoCo to generate each query in turn, saving them in your workspace as separate SQL files:

   **Query 1 — Baseline volume:**
   > *"Show me weekly new listing counts by product area for the last 12 weeks"*

   **Query 2 — Layer in user behaviour:**
   > *"Take the previous query and join it to the users table. Add columns for: count of unique sellers, percentage of new sellers (registered in the last 30 days), and average listings per seller. Keep the weekly grain."*

   **Query 3 — Add engagement signals:**
   > *"Extend the previous query further by joining contacts. Add: total contacts per product area per week, contact rate (contacts per listing), and average resolution time. Flag any week where contact rate exceeds the 12-week average by more than one standard deviation."*

   **Query 4 — Executive summary view:**
   > *"Wrap the previous query in an outer CTE and produce a final summary showing the most recent week vs the prior 4-week average for each metric, with a percentage change column. Sort by the product area with the largest negative change in listing volume."*

   Review the four queries together. Notice how each adds a layer of context — this is how analysts build up an answer iteratively.

5. **Exercise 2e — Build a Reusable CoCo Skill (25 min):**

   You've built a solid multi-step analysis. Now you'll package it as a **CoCo Skill** — a reusable prompt file that lets anyone (including future-you) run this same analysis with a single command.

   **Step 1 — Generate the skill file:**
   Ask CoCo to create a skill that encapsulates your listing health analysis:

   > *"/skill-development Create a new CoCo skill called 'listing-health-check'. It should perform a weekly listing health analysis for Trade Me. The skill should: (1) query weekly new listing counts by product area for the last 12 weeks, (2) join users to calculate unique sellers and new seller percentage, (3) join contacts to add contact rate and flag anomalies, (4) produce an executive summary comparing the latest week to the prior 4-week average. The output should be a formatted summary with the key metrics and any anomaly flags."*

   CoCo's skill builder will generate a `.md` skill file in your workspace.

   **Step 2 — Review the generated skill:**
   Open the generated skill file and read through it. Notice the structure:
   - The frontmatter (name, description, triggers)
   - The prompt body with instructions for CoCo
   - Any parameters or placeholders

   **Step 3 — Customise the skill:**
   Make the following modifications to the skill file by hand (or ask CoCo to help):

   - **Add a parameter:** Add a `product_area` parameter so the user can optionally filter to a single product area (e.g., Marketplace, Motors, Property, Jobs). Default should be "all".
   - **Add output formatting:** Add an instruction that the final summary should be presented as a markdown table with conditional indicators (e.g., arrows or text like "UP" / "DOWN") for metrics that moved more than 10%.
   - **Add a trigger phrase:** Add `"weekly listing report"` and `"listing health"` as trigger phrases so the skill activates when someone types those words.

   **Step 4 — Test your skill:**
   Run your skill by typing one of your trigger phrases into CoCo and confirm it executes the full analysis end-to-end.

6. **Wrap-up (10 min):** Key message: *CoCo can write SQL that would take an experienced analyst 30 minutes to compose from scratch. Skills let you package that work so it's repeatable with a single command. Your job shifts from writing syntax to asking the right question, verifying the answer, and making it reusable.*

**Snowflake Skills / Features:**
- Cortex Code (CoCo) — SQL generation from natural language
- CoCo iterative refinement (follow-up prompts)
- CoCo "explain this code" capability
- Advanced SQL patterns: CTEs, multi-table JOINs, aggregation, JSON/VARIANT field extraction
- Progressive query building — layering complexity iteratively
- Workspaces results pane: column chooser, sorting, chart view and customisation, CSV download
- CoCo Skills — creating, customising, and invoking reusable prompt-based skills

---

### Module 3 — Repeatable Analysis: Building a Notebook *(50 min)*

**Learning Objective:** Use CoCo to scaffold a complete, multi-cell analysis notebook from a single prompt — combining SQL, Python visualisation, and an interactive filter — so the work is repeatable and shareable without starting from scratch each time.

**Scenario:** *"Your team lead asks for a standing weekly report. Instead of re-running queries and pasting numbers into a slide each Monday, you'll build a notebook that anyone can open and run to get the latest picture."*

**Flow:**

1. **Exercise 3a — Scaffold a Full Notebook with One Prompt (20 min):**

   Create a new notebook in your workspace. Paste the following prompt into CoCo as the very first message. CoCo will generate all the cells at once — a markdown title, one or more SQL cells, and a Python visualisation cell. Add each generated cell to your notebook and run them in order to confirm everything works.

   > *"Create a notebook to monitor listing health across Trade Me's product areas. Include: (1) a markdown title cell, (2) a SQL cell that joins the listings table to the users table and calculates, per product area and region: new listings this week, expired listings this week, active listing count, and fill rate (sold / total), (3) a Python cell that renders a grouped bar chart of new vs expired listings by product area using Altair."*

2. **Exercise 3b — Add an Interactive Filter (15 min):**
   Ask CoCo to add a region dropdown to your notebook that filters the SQL query dynamically. Prompt suggestion:
   *"Add an ipywidgets dropdown at the top of this notebook that filters all queries by region. Update the SQL cells to use the selected value."*
   Run all cells to confirm the dropdown and chart update together.

3. **Concept (5 min):** Running notebooks on a schedule vs on-demand. Brief awareness of Snowflake Tasks for scheduled runs (no hands-on).

4. **Wrap-up (10 min):** Do a final run-all to confirm everything executes cleanly, then save the notebook. Key message: *one prompt to CoCo scaffolds a complete working report. Your job is to verify it reflects reality — not to write the code.*

**Snowflake Skills / Features:**
- Snowflake Notebooks (SQL cells, Python cells, Markdown cells)
- Cortex Code (CoCo) — multi-cell notebook scaffolding from a single prompt
- `ipywidgets` — interactive dropdowns linked to SQL queries
- Altair — multi-series and dual-axis charts

---

### Module 4 — Team-Ready Tools: Building a Streamlit App with CoCo *(50 min)*

**Learning Objective:** Use CoCo to scaffold a simple Streamlit app that turns a recurring business question into a self-service tool any team member can use — without needing to maintain a PBI report or wait for an analyst.

**Scenario:** *"Your team wants a self-service dashboard to monitor listing health — active vs expired listings across product areas and regions — without waiting for a PBI report refresh."*

**Flow:**

1. **Exercise 4a — Scaffold Your App (25 min):**
   Create a new Python file in your workspace. Paste the following starter prompt into CoCo. CoCo will generate the full app including the Snowflake connection, SQL query, and Streamlit widgets. Run it in Snowflake (Streamlit in Snowflake) to see it live.

   > *"Build a Streamlit app showing active vs expired listings by product area with a bar chart and a region filter dropdown"*

2. **Exercise 4b — Customise and Deploy (15 min):**
   Ask CoCo to make one customisation to your app (e.g., add a filter, change the chart type, add a summary metric card). Redeploy and confirm it works.

3. **Wrap-up (10 min):** Run your deployed app end-to-end and confirm it works. Key message: *you don't need a BI tool or an analyst to give your team a self-service view of data — you can build it yourself.*

**Snowflake Skills / Features:**
- Cortex Code (CoCo) — Streamlit app scaffolding
- Streamlit in Snowflake (SiS) — deploying and running apps
- `st.connection("snowflake")` — connecting to Trade Me data
- Streamlit widgets: `st.selectbox`, `st.date_input`, `st.metric`, `st.line_chart`
- Deploying Streamlit apps in Snowflake

---

### Session Close — Wrap-Up and Next Steps *(20 min)*

**Flow:**

1. **Reflection (10 min):** Participants spend 5 minutes writing down one thing that worked well and one thing they'd explore further. Facilitator then reads out a few responses and summarises the themes: what problems got solved? What surprised people?

2. **Roadmap discussion (5 min):**
   - CoWork semantic views as a curated data starting point (for those who want guardrails)
   - Snowflake Cortex Analyst for natural-language queries against semantic views (upcoming capability)
   - Git-backed workspace setup for team assets (post-workshop action)

3. **Immediate next steps (5 min):**
   - Each participant identifies one real question from their day job they want to try answering with what they learned today
   - Office hours / follow-up Slack channel recommended
   - Access confirmation for production Snowflake environment

---

## Appendix A — Scenario Reference: Trade Me Data Context

The following table summarises example datasets and questions relevant to each business area.

| Business Area | Key Tables / Concepts | Example Questions |
|---|---|---|
| **Marketplace** | Listings, categories, sold items, sellers, buyers | Top selling categories this week? Average time-to-sell by category? Seller volume by region? |
| **Motors** | Vehicle listings (make, model, year, region, price), watchlist, sold | Average asking price for Toyota Corolla by year? Time-on-site for unsold vehicles > 60 days? |
| **Properties** | Property listings (type, region, asking price, days listed), enquiries | Listing volume by region MoM? Average days on market for 3-bedroom houses in Wellington? |
| **Jobs** | Job listings (industry, role type, salary band, region), applications | Application rate by industry sector? Job listing volume trend for Tech roles last 6 months? |
| **Advertising** | Ad impressions, clicks, revenue, campaign type, advertiser | Revenue by ad format this quarter? Click-through rate by category page? |
| **CX / Trust** | Support contacts, contact reasons, resolution time, listings linked | Top contact reasons by product area? Resolution time trend for Motors disputes? |

---

## Appendix B — Facilitator Notes

### Cohort Structure
With ~48 participants, consider running in cohorts of 8–10 with one facilitator per cohort, or running the full group together with 2–3 roving helpers for exercises.

### CoCo Access
Ensure all participants have:
- Snowflake login with appropriate role
- CoCo (Cortex Code) enabled in their account
- Access to a shared Snowflake database containing sanitised Trade Me sample data for exercises

### Sample Data
Workshop exercises should use a **pre-prepared sandbox schema** (e.g., `TRADEME_WORKSHOP.SAMPLE`) containing representative but non-sensitive extracts:
- `LISTINGS` — listing ID, product area, category, region, status, listed_date, sold_date, price
- `USERS` — user ID, segment, region, registration_date (anonymised)
- `CONTACTS` — contact ID, product area, reason, created_date, resolution_time
- `AD_REVENUE` — campaign_id, ad_type, product_area, revenue, impressions, clicks, date

### Timing Flexibility
If running as two half-days:
- **Session 1:** Session 0 + Module 1 + Module 2 (~160 min)
- **Session 2:** Module 3 + Module 4 + Session Close (~120 min)

### Difficulty Scaling
- **Less confident participants:** Stay with Module 2 exercises; use CoCo heavily; don't worry about customising apps
- **More advanced participants:** Try connecting to production tables (read-only), explore joining 3+ tables, or add Python data manipulation between SQL and chart cells

---

## Appendix C — Skills Matrix

| Module | Primary Snowflake Skill | Secondary Skills |
|---|---|---|
| Module 1 | Workspaces | Role-based access, Git integration |
| Module 2 | CoCo — SQL from natural language, Skills | Snowsight worksheets, data catalog, progressive analysis, skill builder |
| Module 3 | Notebooks (SQL + Python + charts) | CoCo for Python cell generation, `ipywidgets` |
| Module 4 | Streamlit in Snowflake via CoCo | `st.connection`, app deployment |

---

*Prepared for Trade Me — Data Seekers Workshop*
*Version 1.1 — August 2026*

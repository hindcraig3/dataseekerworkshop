# Trade Me Data Seekers Workshop

## Overview

### Learning Outcomes

By the end of this workshop, participants will be able to:

1. Navigate Snowflake and understand where Trade Me's data lives
2. Use CoCo to write and iterate on SQL queries without needing to be a SQL expert
3. Create a re-usable CoCo skill
4. Build a simple Streamlit app to turn a recurring question into a team-accessible tool

---

## Workshop Flow


### Module 1 — Workspaces : Your Personal Data Lab

**Learning Objective:** Set up and use a personal workspace, understand the workspace types available (personal, shared, git-backed), organise files for future reuse, and using the result pane for simple analysis.

**Flow:**

1. **Exercise 1a — Create Your Workspace and run a SQL query:**
   - Select **Projects** then **Workspaces** from the left hand menu.
   - Click the + icon at the top of the workspaces panel and select **Private Workspace**. Name your workspace:  `<your_name>_data_lab`. 
   - Create a new SQL file inside your Workspace by clicking the **+ Add New** button and selecting **SQL file**
   - Name the file : **Module1.sql**
   - Copy and paste this query into the worksheet and run the query by clicking the blue **Run** button in the top left hand of the worksheet.
   ```
   select * from tm_workshop.sampledata.jobs_listings limit 500;
   ```
  

2. **Exercise 1b - Explore the results pane:**
 
   The results pane is where you can view, and work with, the results of a query.  

      ---
      **Table tab** - Shows tabular results. It shows a profile of the data in each column. This can be toggled on and off by clicking the **Show Column Stats** icon ( The little graph in the top left cell of the results). You can also search within the results set, show / hide columns, access the query plan, and download the results as a CSV. 
      - 2.1.Click the **Search** icon in the results pane and search for "Legal". Note how it filters the results. Clear the search box by clicking the X icon in the search box.
      - 2.2 Click the **Column Selection** icon. Untick the USER_ID column and click the **Apply** button at the bottom of the list. Note how the column is removed from the results set. 
      - 2.3 Click the **Download** icon. This allows you to download the results set as a CSV file. 
      ---
      **Chart Tab** - This allows you to create basic charts directly from the results set. Its great for quickly visualising the results.

      - 2.4 Click the **Chart** button then select **Bar Chart** from the Chart Type drop down. 
      - 2.5 Select **INDUSTRY** as the x-axis column
      - 2.6 Select **LISTING_ID** as the Y-axis column. 
      - 2.7 Change the Aggregate to **COUNT**.
      - 2.8 Change the Group by to **ROLE_TYPE**
      ---
      **Pivot Tab** - This allows you to create a pivot table directly from the results set.
      - 2.9 Click the **Add row Fields** box and select the **INDUSTRY** column
      - 2.10 Click the **Add column Fields** box and select the **ROLE_TYPE** column
      - 2.11 Click the **Add value Fields** box and select **LISTING_ID**. 
      - 2.12 Change the **Aggregation** to **COUNT**


3. **Wrap-up** A private workspace is a space for you to write queries and code, build apps, and more. You can manage your files using folders; you can upload files and folders; and you can manage file versions.

**Module 1 Snowflake Skills / Features:**
- Snowflake Workspaces (personal workspace — hands-on; shared and git-backed — concept awareness)
- Workspace file management
- Working with the Results pane for simple analysis, charting, and pivot tables

---

### Module 2 — From Question to Answer: AI-Assisted SQL with CoCo

**Learning Objective:** Use Cortex Code (CoCo) to write, refine, and understand SQL queries — starting from plain English and building up to multi-step analysis — without needing to be a SQL expert.


**Flow:**

1. **Exercise 2a — Simple Query from Plain English**
   
   1.1 Create a new **SQL file** in your workspace uisng the **Add File** button or by adding a new **tab** to the workspace.
   
   1.2 Rename it to **Module2.sql**. 
   
   1.3 Click the CoCo tab on the right hand sde to display the CoCo panel. ( The blue tab with the Star in it)
   
   1.4 Copy and paste the following prompt into CoCo:

   ``` 
   How many job listings are there? 
   ```

   Notice that CoCo just answered the question in the chat window? You can see the SQL it generated and ran by clicking the "Expand" icon.  You can also get some insight into the process CoCo took to get the answer by clicking on the "Thinking Complete" link and the "Ran X Commands" link. 

   ![](/assets/cocosqlexpand.png)
   
   You could copy the SQL query and paste it into the worksheet if you wanted to re-use it,or you could be more specific in your prompt. 
   
   1.5 Copy and paste the following into CoCo. 

   ``` 
   Create a new query that returns how many listings there are?
   ```
   Note this time CoCo adds the SQL to the SQL worksheet. Also note how it highlights the changes and provides the option to "Keep" the changes or "Undo" the changes. Click "Keep". This makes it easy to see what code CoCo has created, deleted or changed in your file.

   1.6 There are multiple "listings" tables in the database - Jobs, Motors, Marketplace, Property. What happens if you quickly want to check Motors listings? You could explicitly mention motors listings in your prompt but you can also provide CoCo with Context to guide it to the right database, schema, table, or view for example. 

   1.7 Click the **+** icon in the CoCo window, then type MOTORS in the search box. The MOTORS_LISTINGS table should be displayed in the list. Click **MOTORS_LISTINGS** to add this table as context for CoCo.

   ![](assets/cococontext.png)

   1.8 Now copy and paste the following prompt.

   ```
   How many listings are there?
   ```

   Note how CoCo queries the **motor_listing** table. This is because we provided the table as context. Providing context like this is useful when you have access to a lot of databases, schema, and tables. It means CoCo does not need to waste time (and tokens) performing metadata queries to try and figure out what tables it needs to query. 

   > :bulb: Providing context and being specific with your prompts can really help CoCo

2. **Exercise 2b — Iterate and Refine (15 min):**
   
    Now ask CoCo these questions in turn.  If CoCo changes the SQL in the Worksheet just click "Keep Changes". Make sure each query actually runs by clicking anywhere in the the query, then clicking the blue **Run Query** button.
   ```
   Now create a query to show open job listings by category
   ```
   Note how  it creates a new query and includes a WHERE clause thats filters the data on status, and a GROUP BY clause to get the count per category

   ```
   create a query to return total job listings per month per category for the last 18 months
   ```
   Note how the SQL gets a bit more complicated. You may see DATE functions being used along with filters in the WHERE clause and grouping via the GROUP BY clause. 

   ```
   Refine that query to also show the difference compared to the previous month
   ```
   Note that it modified the last query it created even though you only said "refine that query...". You will notice the SQL query might now include a sub-query and some different functions. 

   Now with your mouse **highlight** the query and then select **Explain** form the menu that pops up. CoCo will then explain what the query is doing. This is great for understanding SQL that CoCo generates or if you are using SQL written by someone else. 

   ![](assets/cocoexplain.png)




3. **Exercise 2c — Advanced Query: Multi-Join, CTEs, Aggregation, and JSON**

   Lets ask CoCo to build a more complex query that may mirror the kind of question an analyst would normally tackle.

   ```
   Help me create a query that allows me to: 
   
   See the number of "Contacts" by reason, for each of the last 3 months , that required escalation and how that compares to the same months last year, and against  the monthly average from the previous 12 months
   ```

   Review both the response that CoCo provides in the chat after creating the query and the query itself. Notice how CoCo provides a explanation of the query it just created especially the logic / business rules it applied.  

4. **Wrap-up** CoCo is great for creating and modifying SQL queries against your Snowflake data. It knows Snowflake, it knows SQL, and it has hte context about you data it needs to create the queries. 

**Module 2 Snowflake Skills / Features:**
- Workspaces "diff" feature to see what additonals, dleetions, and changes CoCo makes to your queries
- Leveraging CoCo to write simple and advanced SQL queries.
- Understanding that you can provide CoCo with "context" which could be a table, or an entire schema or database. 
- Lerveraging CoCo to help you understand what a SQL query is in plain lanaguage. 

# Module 3 - Advanced Analysis and creating re-usable skills:

4. **Exercise 3a — Building a mutli-step Analysis**

   Often you may have the need to produce some insight that may need multiple queries to produce the data you need. You could build these up 1 at a time but we can also get CoCo to accelerate this kind of analysis. You can even use CoCo to help identify and refine the requirements. 


   4.1 Add a new  **SQL file** to your workspace and rename it: **marketplace_performance.sql**

   4.2 Create a new CoCo session by clicking the **+** icon at the **Top** of the CoCo pane. This will give a new chat window with no history

   > :bulb: Managing session context is really important. The context window has limited space so when you start a new task or job, it pays to create a new sesion. You can have mutliple sessions going at once if you need to perform multiple tasks.  
   
   4.3 In the CoCo panel toggle the **Plan** switch to the **on** position. Planning allows CoCo to think about how it will solve a problem and present a plan that you can review before it writes any code. This is a really useful step especially for more complex tasks.

   4.4 Copy and paste the following prompt into CoCo.

   ```
   I need to design the Head of Marketplace ( who owns Marketing place listings) with an analysis of Monthly Marketplace listing performance that they can review each month at their leadership team meeting. 
   
   Some of the insights they want includes: 
   
   Number of new listings created in last 7 days, 14 day, 30 days, year to date.
   Number of new listings created in last 7 days, 14 day, 30 days, year to date compared with the same periods the previous year 
   Top 5 and bottom 5 Listing categories by increase or decrease last month vs the month before
   Sold vs unsold listing count and percentage by Region 
   Contacts by members that relate to marketplace listings 
   
   Also Review the tables in the SAMPLEDATA schema and make suggestions on other insights that might be relevant to the Head of marketplace listings. Ask me any relevant clarification questions .
   ```

   Note CoCo may ask you some questions. These may include:

   - Clarifyign if you only want to include listigns from the marketplace_listings table - Answer "Marketplace Listings" only.
   - Clarifying what "Category" column you want to use as there are category and sub category fields - Choose the CATEGORY field
   - If you want one query or multiple queries - Choose multiple / separate queries
   - Clarifying the rules for "Sold vs Unsold" - You want any status that is not sold = Unsold. 

   Once CoCo has finished review the plan it came up with. Note that it has outlined the proposed queries it will create. Also note the additonal suggested insights. If you wanted to you get iterate on the plan with CoCo to get it to the ideal state. 

   4.5 Toggle the **Plan** switch to the **off** position.
   
   4.6 Copy and paste the following prompt into CoCo

   ```
   Proceed with the build. Include all the suggested additional insights. 
   ```
   Once CoCo has finished review the SQL it generated. Do not forget to click **Keep changes** . Note it has created a query for each item in the plan. Some are simple and some are more complex. 

   4.7 Run 2 or 3 of the queries that CoCo created to make sure they run as expected.

5. **Exercise 3b — Build a HTML report:**


   Now we have the queries to produce the data we need to answer the leadership teams questions, but we need a nicer way to present that data.

   5.1 Toggle the **Plan** switch to the **On** position.

   5.2 Copy and paste the following prompt into coco

   ```

    I want to create a HTML report that shows the results of SQL queries that can be used in the leadership team meeting. 
    
     My requirements include: 
     The HTML report should be static and standalone 
     The layout should be in a presentation style with one "page" for each analysis and navigation to move forward and back 
     There should be a Title "page" 
     Each section should have a title, and a brief description of what is being shown., and the data/ insight
     Where appropriate use a chart to visualise the data, or a metric/KPI card for single data points. Use a table if appropriate. 
     
     Ask me any relevant clarification questions. Make suggestions on how I could possibly improve the output

   ```

   CoCo may ask you some clarification questions. These may include:

   - Colour Theme - Choose either Light or Dark if you get asked. 
   - Charts library - Choose the **Chart.js** option if you get asked.
   - Branding - Choose "Generic branding" if you get asked.

   5.3 Review the plan that CoCo proposes. Take note of the suggested improvements to see if they make sense. Normally you may iterate on the plan to get it "just right" but today we will proceed with the build. Copy and paste the following prompt into CoCo:

   ```
   Proceed with the build. Include the suggested improvements. Create all files in the current workspace. 
   ``` 
   > NOTE: The build may take a few minutes

   5.4 Once CoCo has finished you should have a new "HTML" file in your Workspace. Currently you cannot render HTML files in Workspaces so you will need to **Download** the HTML to your laptop to view it. To do this:
    - Click the HTML file in the Workspaces file pane
    - Click the ellipsis ( 3 dots) to the right of the file name
    - Select **Download** from the menu that pops up
    - Once downloaded locate the file on yur laptop and open it in a new browser window.
    - Navigate through the report. 



6. **Exercise 3c — Build a Reusable CoCo Skill (25 min):**

   You've built a solid multi-step analysis, and generate a HTML report, but this is a statics asset. We need to be able to re-create this each month or when. Now you'll package it as a **CoCo Skill** — a reusable prompt file that lets anyone (including future-you) run this same analysis with a single command.


   6.1 Toggle the **Plan** siwtch tothe **on** position

   6.2 Copy and paste the following prompt into CoCo

   ```
   I want to make the report generator a re-usable asset. Help me create a new CoCo skill that will enable me to: Ask the user what month and year they want to run the report for. Default to the previous month. Runs the SQL queries and produce a new HTML file Ensure the file name  includes the Month and year, and a timestamp for report run.
   ```

   Once CoCO has finsihed review the plan. 

   6.3 Toggle the **Plan** siwtch to the **off** position then copy and paste the following prompt into CoCo:

   ```
   Proceed with the build
   ```

   Once CoCo has finished creating your new skill test it out. Don't forget to click the **Keep All** changes button.

   6.4 In the CoCo chat box type **/marketplace** . You shoudl see your new skill appear in thethe search results under **Personal Skills**

   ![](/assets/cocoskill.png)

   6.5 Click the skill so it gets added to the chat window then click the **Send** button on the chat window. ( or hit enter on your keyboard)

   CoCO will then load the skill. It should prompt you to enter the Month and Year. **Pick July 2026** and click submit. CoCo will now run the report.

   Once it is complete you shoudl see a new HTML file appear in your workspaces file list. 

 6.5 Currently you cannot render HTML files in Workspaces so you will need to **Download** the HTML to your laptop to view it. To do this:
    - Click the HTML file in the Workspaces file pane
    - Click the ellipsis ( 3 dots) to the right of the file name
    - Select **Download** from the menu that pops up
    - Once downloaded locate the file on yur laptop and open it in a new browser window.
    - Navigate through the report and check it is correct.


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


### Module 4 — Team-Ready Tools: Building a Streamlit App with CoCo *(50 min)*

**Learning Objective:** Use CoCo to scaffold a simple Streamlit app that turns a recurring business question into a self-service tool any team member can use — without needing to maintain a dashboard or wait for an analyst.

**Flow:**

4.1 Create a new CoCo session by clicking the **+** icon at the **Top** of the CoCo pane. 

> :bulb: Managing session context is really important. The context window has limited space so when you start a new task or job, it pays to create a new session. You can have mutliple sessions going at once. 

4.2 Toggle the **Plan** mode switch to **on**. 

4.3 Copy and paste the following prompt into CoCo. 

> NOTE: For the purposes of the workshop we have developed a fariy comprehensive prompt. In the real world you could leverage CoCo to help you design the app, then ask it to create a prompt that you can use to generate the app.  Or you could upload a set of requirements, or a mock up even, and ask CoCo to build off that. 

```
Build an interactive Streamlit app in a new workspace folder called "marketplace-listings-app" 
that uses data from TM_WORKSHOP.SAMPLEDATA.MARKETPLACE_LISTINGS, TM_WORKSHOP.SAMPLEDATA.AD_REVENUE, 
and TM_WORKSHOP.SAMPLEDATA.CONTACTS tables.

## App Purpose
A multi-purpose tool for marketplace listing team members: daily monitoring dashboard, 
self-service analytics for ad-hoc exploration, and presentation-ready views for leadership meetings.

## Structure
- Sidebar navigation with 4 pages:
  1. Executive Summary — KPI cards with trend sparklines, YoY comparison, goal progress bars, threshold alerts
  2. Listings & Categories — Top/bottom 5 categories by MoM change, sell-through by category, new listings breakdown
  3. Revenue & Engagement — Ad revenue with MoM trends, engagement metrics (views, watchlist, bids) by category, price trends
  4. Operations — Sold vs unsold by region (stacked bar), time-to-sell by region, contact reasons with escalation rates

## Global Features (sidebar, persisted across pages)
- Date window selector: Last 7 days, Last 14 days, Last 30 days, Year to date
- Category multi-select filter (populated dynamically from data)
- Region multi-select filter (populated dynamically from data)
- Comparison toggles on category and revenue pages: Absolute / MoM Change / MoM %
- Goal tracking: user-configurable monthly new listings target and sell-through rate target, shown as progress bars on Executive Summary

## Threshold Alerts (fixed defaults)
- Sell-through rate: red below 25%, yellow below 35%
- Escalation rate: red above 20%, yellow above 15%  
- YoY decline in new listings: yellow warning
```

CoCo may ask you some clarification questions. Answer them as best you can.  Once you have answered the questions CoCo will develope the plan. Once complete review the plan.

4.4 Now you have reviewed the plan ask coco to build. Copy and paste the following prompt :

```
Proceed with the build.
```

CoCo will built your Stream lit application. It may take a few minutes for the build to complete. Once complete you are ready to test it.

4.5 You should see a new **marketplace-listings-app** folder in your Workspace. Inside the folder should be a file called **streamlit_app.py**. Click the file to open it. 

![](/assets/cocostreamlitfiles.png)

4.6 When the file opens you shoudl see a blue **Run** button in the top left hand corner. Click the **Run** button. 

![](/assets/cocostreamlitrun.png)

4.7 A new tab should open and your app should load and should look similar to the one below.

![](/assets/cocostreamlitdashboard.png)

4.8 Navigate your way around the app and check out each page. Try using the filters in the left hand menu. 



**Snowflake Skills / Features:**
- Cortex Code (CoCo) — Streamlit app scaffolding
- Streamlit in Snowflake (SiS) — deploying and running apps
- `st.connection("snowflake")` — connecting to Trade Me data
- Streamlit widgets: `st.selectbox`, `st.date_input`, `st.metric`, `st.line_chart`
- Deploying Streamlit apps in Snowflake



# CONGRATULATIONS - you have reached the end of the workshop. 

To recap some of the CoCo specific things you learnt today:

- Start a new CoCo session for each distinct task. The context window has limited space, so switching topics without clearing context can lead to confused or lower-quality responses.

- Provide explicit table context rather than relying on CoCo to discover tables. This saves time and tokens, and ensures CoCo queries the correct table when multiple similar ones exist.

- Use Plan mode for complex, multi-step tasks before asking CoCo to build. Reviewing and iterating on a plan first produces better results than jumping straight into code generation.

- Be specific in your prompts about where you want output to go. Saying "create a new query" versus just asking a question determines whether CoCo writes to your worksheet or just answers in chat.

- Use the "Explain" feature on any SQL you don't fully understand. Highlight code and select Explain — this is valuable whether the SQL came from CoCo or from a colleague.

- Skills turn one-off work into repeatable assets. If you find yourself running the same analysis more than once, package it as a CoCo skill so anyone on the team can invoke it with a single command.

- Answer CoCo's clarification questions thoughtfully. The quality of the output depends heavily on how well you define scope, filters, and business rules when CoCo asks for them.

- CoCo can do a lot more than just write code. It can help you understand requirements, design solutions, troubleshoot issues, teach you about Snowflake and much more. 
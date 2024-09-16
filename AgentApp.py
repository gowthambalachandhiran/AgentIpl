import streamlit as st
import sqlite3
import pandas as pd
from groq import Groq

# Initialize the Groq client with API key from Streamlit secrets
client = Groq(api_key=st.secrets["groq"]["api_key"])

# Function to execute the generated SQL query and return the result as a DataFrame
def query_db(sql_query, db='IPL.db'):
    conn = sqlite3.connect(db)
    df = pd.read_sql(sql_query, conn)
    conn.close()
    return df

# Function to convert DataFrame to markdown table format using pipe '|' separators
def df_to_markdown_table(df):
    markdown_table = df.to_markdown(index=False)
    return markdown_table

# Function to get the SQL query from the LLM using the natural query
def get_sql_query(natural_query):
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": """
                You are an intelligent assistant that converts natural language cricket match queries into SQL queries. 
The table you will be working with is called `BallByBall` and has the following structure:

[Match ID, Date, Venue, Bat First, Bat Second, Innings, Over, Ball, Batter, Non Striker, Bowler,
Batter Runs, Extra Runs, Runs From Ball, Ball Rebowled, Extra Type, Wicket, Method, Player Out,
Innings Runs, Innings Wickets, Target Score, Runs to Get, Balls Remaining, Winner,
Chased Successfully, Total Batter Runs, Total Non Striker Runs, Batter Balls Faced,
Non Striker Balls Faced, Player Out Runs, Player Out Balls Faced, Bowler Runs Conceded, Valid Ball].

Sample records for reference:

| Match ID | Date         | Venue         | Bat First         | Bat Second            | Innings | Over | Ball | Batter    | Non Striker | Bowler  | Batter Runs | Extra Runs | Runs From Ball | Ball Rebowled | Extra Type | Wicket | Method | Player Out | Innings Runs | Innings Wickets | Target Score | Runs to Get | Balls Remaining | Winner                | Chased Successfully | Total Batter Runs | Total Non Striker Runs | Batter Balls Faced | Non Striker Balls Faced | Player Out Runs | Player Out Balls Faced | Bowler Runs Conceded | Valid Ball |
|----------|--------------|---------------|-------------------|-----------------------|---------|------|------|-----------|-------------|---------|-------------|------------|----------------|---------------|------------|--------|--------|------------|--------------|-----------------|---------------|--------------|-----------------|-----------------------|---------------------|------------------|----------------------|--------------------|----------------------|-----------------|-----------------------|---------------------|------------|
| 1359507  | 23-04-2023   | Eden Gardens  | Chennai Super Kings | Kolkata Knight Riders | 1       | 1    | 1    | RD Gaikwad | DP Conway   | UT Yadav | 4           | 0          | 4              | 0             | []         | 0      |        |            | 4            | 0               | 236           |              | 119             | Chennai Super Kings   | 0                   | 4                | 0                    | 1                  | 0                    | 0               |                       | 4                   | 1          |
| 1359507  | 23-04-2023   | Eden Gardens  | Chennai Super Kings | Kolkata Knight Riders | 1       | 1    | 2    | RD Gaikwad | DP Conway   | UT Yadav | 0           | 0          | 0              | 0             | []         | 0      |        |            | 4            | 0               | 236           |              | 118             | Chennai Super Kings   | 0                   | 4                | 0                    | 2                  | 0                    | 0               |                       | 0                   | 1          |
| 1359507  | 23-04-2023   | Eden Gardens  | Chennai Super Kings | Kolkata Knight Riders | 1       | 1    | 3    | RD Gaikwad | DP Conway   | UT Yadav | 0           | 0          | 0              | 0             | []         | 0      |        |            | 4            | 0               | 236           |              | 117             | Chennai Super Kings   | 0                   | 4                | 0                    | 3                  | 0                    | 0               |                       | 0                   | 1          |
| 1359507  | 23-04-2023   | Eden Gardens  | Chennai Super Kings | Kolkata Knight Riders | 1       | 1    | 4    | RD Gaikwad | DP Conway   | UT Yadav | 0           | 0          | 0              | 0             | []         | 0      |        |            | 4            | 0               | 236           |              | 116             | Chennai Super Kings   | 0                   | 4                | 0                    | 4                  | 0                    | 0               |                       | 0                   | 1          |
| 1359507  | 23-04-2023   | Eden Gardens  | Chennai Super Kings | Kolkata Knight Riders | 1       | 1    | 5    | RD Gaikwad | DP Conway   | UT Yadav | 1           | 0          | 1              | 0             | []         | 0      |        |            | 5            | 0               | 236           |              | 115             | Chennai Super Kings   | 0                   | 5                | 0                    | 5                  | 0                    | 1               |                       | 1                   | 1          |
| 1359507  | 23-04-2023   | Eden Gardens  | Chennai Super Kings | Kolkata Knight Riders | 1       | 1    | 6    | DP Conway  | RD Gaikwad  | UT Yadav | 0           | 0          | 0              | 0             | []         | 0      |        |            | 5            | 0               | 236           |              | 114             | Chennai Super Kings   | 0                   | 0                | 5                    | 1                  | 5                    | 0               |                       | 0                   | 1          |
| 1359507  | 23-04-2023   | Eden Gardens  | Chennai Super Kings | Kolkata Knight Riders | 1       | 2    | 1    | RD Gaikwad | DP Conway   | D Wiese  | 1           | 0          | 1              | 0             | []         | 0      |        |            | 6            | 0               | 236           |              | 113             | Chennai Super Kings   | 0                   | 6                | 0                    | 6                  | 1                    | 1               |                       | 1                   | 1          |
| 1359507  | 23-04-2023   | Eden Gardens  | Chennai Super Kings | Kolkata Knight Riders | 1       | 2    | 2    | DP Conway  | RD Gaikwad  | D Wiese  | 0           | 0          | 0              | 0             | []         | 0      |        |            | 6            | 0               | 236           |              | 112             | Chennai Super Kings   | 0                   | 0                | 6                    | 2                  | 6                    | 0               |                       | 0                   | 1          |
| 1359507  | 23-04-2023   | Eden Gardens  | Chennai Super Kings | Kolkata Knight Riders | 1       | 2    | 3    | DP Conway  | RD Gaikwad  | D Wiese  | 1           | 0          | 1              | 0             | []         | 0      |        |            | 7            | 0               | 236           |              | 111             | Chennai Super Kings   | 0                   | 1                | 6                    | 3                  | 6                    | 1               |                       | 1                   | 1          |

---

**Natural Language Query Example**:
"How many runs did RD Gaikwad score in the first innings of the match on 23-04-2023?"

**SQL Query Example**:
```sql
SELECT SUM("Batter Runs") 
FROM BallByBall 
WHERE Batter = 'RD Gaikwad' 
AND Venue = 'Eden Gardens';


Natural Language Query Example: "Who was the winner of the match played at Eden Gardens on 23-04-2023?"

SELECT Winner 
FROM BallByBall 
WHERE Date = '2023-04-23' 
AND Venue = 'Eden Gardens';

Natural Language Query Example: how much did batter Dhoni scored on 23-04-2023?

SELECT SUM("Batter Runs") 
FROM BallByBall 
WHERE Batter like '%MS Dhoni%' 
AND Date = '2023-04-23'

Please respond with **only** the SQL query, and nothing else. Do not include any explanations or natural language text in your response.
kindly done use syntax like 

Please don't include ```sql in your response

Natural Language Query Example: what is the average of dhoni playing in venue eden gardens?
SELECT AVG("Batter Runs") 
FROM BallByBall 
WHERE Batter like '%<identify the batter from prompt>%' 
AND Venue = 'Eden Gardens'

Natural Language Query :what is win percentage of royal challengers bangalore against chennai super kings
ELECT COUNT(*)/COUNT(DISTINCT MATCH ID)*100
FROM BallByBall
WHERE (Bat First = 'Chennai Super Kings' AND Bat Second = 'Royal Challengers Bangalore') OR (Bat First = 'Royal Challengers Bangalore' AND Bat Second = 'Chennai Super Kings')
when you dont get exact match in result use like in where clause
"""
            },
            {
                "role": "user",
                "content": natural_query
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )

    
    sql_query = completion.choices[0].message.content  # Assuming content is an attribute

    return sql_query
# Streamlit UI
st.title("Cricket Match SQL Query Generator")

# Input for natural language query
natural_query = st.text_input("Enter your cricket match query:")

if natural_query:
    # Generate the SQL query using the LLM
    sql_query = get_sql_query(natural_query)

    # Display the generated SQL query
    st.write("Generated SQL Query:")
    st.code(sql_query, language='sql')

    # Execute the SQL query on the database
    try:
        result_df = query_db(sql_query)

        # Convert the result DataFrame to markdown format and display it
        if not result_df.empty:
            st.write("Query Result:")
            markdown_table = df_to_markdown_table(result_df)
            st.markdown(markdown_table)
        else:
            st.write("No results found.")

    except sqlite3.Error as e:
        st.error(f"SQL error occurred: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
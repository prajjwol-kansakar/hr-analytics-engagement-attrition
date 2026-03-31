import pandas as pd
from sqlalchemy import create_engine
import psycopg2
import matplotlib.pyplot as plt

# df = pd.read_csv("data.csv")

# print(df.info())

# df.columns = df.columns.str.lower()

# engine = create_engine(
#     "postgresql+psycopg2://postgres:tebahal1%21@localhost:5432/HRDATA"
# )



# df.to_sql(
#     name="employees_hr",
#     con=engine,
#     if_exists="append",   # IMPORTANT → don't use replace
#     index=False
# )



try:
    conn = psycopg2.connect(
        host="localhost",       # your DB host
        database="HRDATA",
        user="postgres",
        password="######",    # use your password
        port="5432"
    )

    print("Connected successfully!")

    cursor = conn.cursor()

    cursor.execute("Select * from employees_hr ")
    rows = cursor.fetchall()

    # ✅ Get column names from DB
    colnames = [desc[0] for desc in cursor.description]

    # ✅ Create DataFrame with proper columns
    df = pd.DataFrame(rows, columns=colnames)

    # ✅ Optional: standardize column names (best practice)
    df.columns = df.columns.str.strip().str.replace(" ", "").str.lower()

    # ✅ Create Engagement Score
    df['engagementscore'] = (
        df['jobsatisfaction'] +
        df['environmentsatisfaction'] +
        df['worklifebalance'] +
        df['jobinvolvement']
    ) / 4

    # ✅ Department-level analysis
    dept_engagement = df.groupby('department')['engagementscore'].mean().sort_values()

    print("\n📊 Engagement by Department:\n")
    print(dept_engagement)


    role_engagement = df.groupby('jobrole')['engagementscore'].mean().sort_values()

    print("\n📊 Engagement by Job Role:\n")

    print(role_engagement)

    overtime_engagement = df.groupby('overtime')['engagementscore'].mean()

    print("\n📊 Engagement by Overtime:\n")
    print(overtime_engagement)

    travel_engagement = df.groupby('businesstravel')['engagementscore'].mean()

    print("\n📊 Engagement by Business Travel:\n")
    print(travel_engagement)

    attr_dept = df.groupby('department')['attrition'].value_counts(normalize=True).unstack()
    
    print("\n📊 Attrition by Department:\n")
    
    print(attr_dept)

    attr_overtime = df.groupby('overtime')['attrition'].value_counts(normalize=True).unstack()
    print("\n📊 Attrition by Overtime:\n")
    print(attr_overtime)

    engagement_attr = df.groupby('attrition')['engagementscore'].mean()
    print("\n📊 Engagement by Attrition:\n")
    print(engagement_attr)

    attr_tenure = df.groupby('yearsatcompany')['attrition'].value_counts(normalize=True).unstack()
    print("\n📊 Attrition by Tenure:\n")
    print(attr_tenure)
    
    df['attrition_flag'] = df['attrition'].map({'Yes': 1, 'No': 0})
    
    corr = df.corr(numeric_only=True)['engagementscore'].sort_values(ascending=False)
    
    print("\n📊 Correlation with Engagement Score:\n")

    print(corr)
    

        # Create figure
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle("HR Analytics Dashboard - Engagement & Attrition", fontsize=16)

    # 1️⃣ Engagement by Department
    dept_engagement.plot(kind='bar', ax=axes[0,0])
    axes[0,0].set_title("Engagement by Department")
    axes[0,0].set_ylabel("Score")

    # 2️⃣ Engagement by Job Role
    role_engagement.tail(10).plot(kind='barh', ax=axes[0,1])  # top 10 roles
    axes[0,1].set_title("Engagement by Job Role")

    # 3️⃣ Engagement by Overtime
    overtime_engagement.plot(kind='bar', ax=axes[0,2])
    axes[0,2].set_title("Engagement by Overtime")

    # 4️⃣ Attrition by Department
    attr_dept.plot(kind='bar', stacked=True, ax=axes[1,0])
    axes[1,0].set_title("Attrition by Department")

    # 5️⃣ Engagement vs Attrition
    engagement_attr.plot(kind='bar', ax=axes[1,1])
    axes[1,1].set_title("Engagement vs Attrition")

    # 6️⃣ Correlation with Engagement
    corr.dropna().head(10).plot(kind='barh', ax=axes[1,2])
    axes[1,2].set_title("Top Drivers of Engagement")

    # Layout fix
    plt.tight_layout(rect=[0, 0, 1, 0.95])

    plt.savefig("dashboard/dashboard.png")
    
    # Show dashboard
    plt.show()

    

    cursor.close()
    conn.close()

    # dept_engagement.plot(kind='bar', title='Engagement by Department')
    # plt.ylabel('Engagement Score')
    # plt.show()

except Exception as e:
    print("Error:", e)

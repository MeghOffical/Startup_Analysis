# libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# load the data 
df = pd.read_csv("C:\\Users\\MEGH BAVARVA\\Desktop\\Data Scientist\\Project\\StreamLit\\App\\finalized.csv")

# Clean the data
df['investors'] = df['investors'].str.split(',').str[0]
df['date']=pd.to_datetime(df['date'])
df['year']=df['date'].dt.year
df['month']=df['date'].dt.month


# page setting width and changing title of the web page 
st.set_page_config(page_title="Startup Funding Analysis", layout="wide")


# function to find similar investors 
def find_similar_investors_by_domain(investor_name):
    
    # Step 1: Filter startups where this investor is involved
    investor_df = df[df['investors'].str.contains(investor_name, na=False)].copy()
    if investor_df.empty:
        return f"No startup found with investor: {investor_name}"

    # Step 2: Get all unique industries and subverticals for this investor
    industries = investor_df['industry'].dropna().unique().tolist()
    subverticals = investor_df['subvertical'].dropna().unique().tolist()

    # Step 3: Filter other startups with same industry or subvertical
    domain_df = df[
        (df['industry'].isin(industries)) |
        (df['subvertical'].isin(subverticals))
    ].copy()

    # Step 4: Extract and clean first investor
    domain_df['similar_investor'] = domain_df['investors'].str.split(',').str[0].str.strip()

    # Step 5: Count top similar investors (excluding the original)
    top_similar_investors = (
        domain_df[domain_df['similar_investor'] != investor_name]
        ['similar_investor']
        .value_counts()
        .head(10)
    )

    n_df = pd.DataFrame(top_similar_investors)
    n_df.drop(columns='count', inplace=True)
    return n_df.reset_index()


# function to find similar startup
def find_similar_startups_by_domain(startup_name):
    
    # Step 1: Filter the target startup row
    target_df = df[df['startup'] == startup_name].copy()
    if target_df.empty:
        return f"No startup found with name: {startup_name}"

    # Step 2: Get unique industry and subvertical
    industries = target_df['industry'].dropna().unique().tolist()
    subverticals = target_df['subvertical'].dropna().unique().tolist()

    # Step 3: Filter other startups with same industry or subvertical
    domain_df = df[
        (df['industry'].isin(industries)) |
        (df['subvertical'].isin(subverticals))
    ].copy()

    # Step 4: Extract startup name (cleaned)
    domain_df['similar_startup'] = domain_df['startup'].str.strip()

    # Step 5: Count similar startups excluding the original
    top_similar_startups = (
        domain_df[domain_df['similar_startup'] != startup_name]
        ['similar_startup']
        .value_counts()
        .head(10)
    )

    # Step 6: Convert to DataFrame and drop 'count' column
    n_df = pd.DataFrame(top_similar_startups)
    n_df.drop(columns='count', inplace=True)
    return n_df.reset_index()




# Function to load startups details
def load_startup_details(startup_name):
    st.header(f"Details for {startup_name}:")

    # top investors for startups
    last5_df = df[df['startup'].str.contains(startup_name)].head(5)[['date','industry','city','investors','round','amount']]
    if 'index' in last5_df.columns:
        last5_df.drop(columns='index', inplace=True)
    last5_df.reset_index(drop=True, inplace=True)
    last5_df.index = last5_df.index + 1  
    st.subheader("Most Recent Investments")
    st.dataframe(last5_df)


    # top 5 biggest investments for the startup
    col1, col2 = st.columns(2)
    with col1:
        biggest5_df = (df[df['startup'].str.contains(startup_name)]
                    .groupby('investors', as_index=False)['amount']
                    .sum()
                    .sort_values(by='amount', ascending=False)
                    .head(5)
        )
        biggest5_df.index = range(1, len(biggest5_df) + 1)
        st.subheader("Biggest Investors")
        fig, ax = plt.subplots()
        ax.bar(biggest5_df['investors'], biggest5_df['amount'])
        st.pyplot(fig)
        
    
    # top 5 industry for startups 
    col1, col2 = st.columns(2)
    with col1:
        series1 = df[df['startup'].str.contains(startup_name)].groupby('industry')['amount'].sum()
        st.subheader("Top Investments in Industries")
        fig, ax = plt.subplots(figsize=(4, 4))
        ax.pie(series1.values, labels=series1.index, autopct='%0.1f%%')
        st.pyplot(fig)
        
        
    # show top 5 cities for the investor
    col1, col2 = st.columns(2)
    with col1:
        series3=df[df['startup'].str.contains(startup_name)].groupby('city')['amount'].sum().head(5)
        st.subheader("Top Investments in Cities")
        fig, ax = plt.subplots(figsize=(4, 4))
        ax.pie(series3.values, labels=series3.index, autopct='%0.1f%%')
        st.pyplot(fig)
        
        
    # year over year investment amount 
    col1,col2 = st.columns(2)
    with col1:
        series4=df[df['startup'].str.contains(startup_name)].groupby('year')['amount'].sum()
        st.subheader("Year-over-Year Growth of Investment Amount")
        fig, ax = plt.subplots()
        ax.plot(series4.index, series4.values, marker='o')
        st.pyplot(fig)
            
            
    # finding similar starups in same domain 
    st.subheader("Similar Startups in the Same Domain")
    similar_startup= find_similar_startups_by_domain(startup_name)
    similar_startup.index = similar_startup.index + 1
    st.dataframe(similar_startup)
    
    
    # outro
    st.subheader("Thanks for using the Startup Funding Analysis app! If you have any questions or need further assistance, feel free to ask.")
    st.write("Developed by Megh Bavarva")
    st.write("Contact:8849855886")
    st.write("Email:bavarvamegh3139@gmail.com")
    


# Function to load investor details
def load_investor_details(investor_name):
    st.header(f"Details for {investor_name}:")
    
    # top 5 startups for the investor
    last5_df = df[df['investors'].str.contains(investor_name, na=False)].head(5)[['date', 'startup', 'industry', 'city', 'round', 'amount']]
    if 'index' in last5_df.columns:
        last5_df.drop(columns='index', inplace=True)
    last5_df.reset_index(drop=True, inplace=True)
    last5_df.index = last5_df.index + 1 
    st.subheader("Most Recent Investments")
    st.dataframe(last5_df)


    # top 5 biggest investments for the investor
    col1, col2 = st.columns(2)
    with col1:    
        biggest5_df = (df[df['investors'].str.contains(investor_name, na=False)]
                    .groupby('startup', as_index=False)['amount']
                    .sum()
                    .sort_values(by='amount', ascending=False)
                    .head(5)
                    )
        biggest5_df.index = range(1, len(biggest5_df) + 1)
        st.subheader("Top Biggest Investments")
        # Plotting the bar chart
        fig, ax = plt.subplots()
        ax.bar(biggest5_df['startup'], biggest5_df['amount'])
        st.pyplot(fig)
        
        
    # show top 5 industries for the investor  
    col1, col2 = st.columns(2)
    with col1:
        series1=df[df['investors'].str.contains(investor_name)].groupby('industry')['amount'].sum().head(5)
        st.subheader("Top Investments in Industries")
        fig, ax = plt.subplots(figsize=(4, 4))
        ax.pie(series1.values, labels=series1.index, autopct='%0.1f%%')
        st.pyplot(fig)
            
            
    # show top 5 stages(round) of investment for the investor       
    col1, col2 = st.columns(2)
    with col1:    
        series2=df[df['investors'].str.contains(investor_name)].groupby('round')['amount'].sum()
        st.subheader("Top Stages of Investment")
        fig, ax = plt.subplots(figsize=(4, 4))
        ax.pie(series2.values, labels=series2.index, autopct='%0.1f%%')
        st.pyplot(fig)
        
        
    # show top 5 cities for the investor  
    col1, col2 = st.columns(2)
    with col1:
        series3=df[df['investors'].str.contains(investor_name)].groupby('city')['amount'].sum().head(5)
        st.subheader("Top Investments in Cities")
        fig, ax = plt.subplots(figsize=(4, 4))
        ax.pie(series3.values, labels=series3.index, autopct='%0.1f%%')
        st.pyplot(fig)
        
     
    # year-over-year growth of investment amount for the investor   
    col1,col2 = st.columns(2)
    with col1:
        series4=df[df['investors'].str.contains(investor_name)].groupby('year')['amount'].sum()
        st.subheader("Year-over-Year Growth of Investment Amount")
        fig, ax = plt.subplots()
        ax.plot(series4.index, series4.values, marker='o')
        st.pyplot(fig)
            
            
    # find similar investors in the same domain
    st.subheader("Similar Investors in the Same Domain")
    similar_investors_df = find_similar_investors_by_domain(investor_name)
    similar_investors_df.index = similar_investors_df.index + 1 # to start index from 1
    st.dataframe(similar_investors_df)


    # Display thanks message and outro
    st.subheader("Thanks for using the Startup Funding Analysis app! If you have any questions or need further assistance, feel free to ask.")
    st.write("Developed by Megh Bavarva")
    st.write("Contact:8849855886")
    st.write("Email:bavarvamegh3139@gmail.com")



# Function to load overall anyalsis  details
def load_overallAnalysis_details():
    
    col1,col2,col3,col4=st.columns(4)
    
    # total funding 
    total=round(df['amount'].sum())
    total=round(total/10000000,2)
    
    
    # max funding
    max_fund=df.groupby('startup')['amount'].sum().sort_values(ascending=False).head(1).values[0]
    max_fund=round(max_fund/10000000,2)


    # Average funding
    avg_fund=round(df.groupby('startup')['amount'].sum().mean())
    avg_fund=round(avg_fund/10000000,2)
    
    
    # no of startups
    no_startup=len(df['startup'].value_counts())
           
        
    with col1:
        st.metric('Total',str(total)+" Cr")
    with col2:
        st.metric('Max',str(max_fund)+" Cr")
    with col3:
        st.metric('Avg',str(avg_fund)+" Cr")
    with col4:
        st.metric('Funded startup',str(no_startup))
        
    
    # month over month graph 
    st.subheader('Month over month Investment')
    selected_optn=st.selectbox('Select Type: ',['Total','Count'])
    if selected_optn=='Total':
        temp_df=df.groupby(['year','month'])['amount'].sum().reset_index()
    else:
        temp_df=df.groupby(['year','month'])['amount'].count().reset_index()

    
    temp_df['x_axis']=temp_df['month'].astype('str')+"-"+temp_df['year'].astype('str')
    col1,col2=st.columns(2)
    with col1:     
        fig, ax = plt.subplots(figsize=(4, 4))
        ax.plot(temp_df['x_axis'],temp_df['amount'])
        st.pyplot(fig)
        
    
    
    # Top sector anaylsis 
    st.subheader('Top Sector of Investments ')
    selected_optn=st.selectbox('Select Type: ',['Sum','Count'])
    if selected_optn=='Count':
        series1=df.groupby('industry')['startup'].count().sort_values(ascending=False).head(10)
    else:
        series1=df.groupby('industry')['amount'].sum().sort_values(ascending=False).head(10)  
        
    col1,col2=st.columns(2)
    with col1: 
        fig, ax = plt.subplots(figsize=(4, 4))
        ax.pie(series1.values, labels=series1.index, autopct='%0.1f%%')
        st.pyplot(fig)
    
    
    # type of Funding
    st.subheader('Types of Funding ')
    unique_rounds = df['round'].unique()
    st.write(unique_rounds)
    
    #City Wise Funding
    st.subheader('City Wise Funding')
    city_wise=df.groupby('city')['amount'].sum().loc[lambda x: x > 0].sort_values(ascending=False)
    st.write(city_wise)
    
    
    # top startups and investors
    col1,col2=st.columns(2)
    with col1:
        st.write("#### Top Startups")
        data1=df.groupby('startup')['amount'].sum().sort_values(ascending=False).head(10)
        st.write(data1)
    with col2:
        st.write("#### Top Investors")
        data1=df.groupby('investors')['amount'].sum().sort_values(ascending=False).head(10)
        st.write(data1)
        
        
    # Funding of Heatmap
    st.subheader("Heatmap: Total Funding in Top 10 Cities by Year")  
    top_cities = df.groupby('city')['amount'].sum().sort_values(ascending=False).head(10).index
    filtered_df = df[df['city'].isin(top_cities)]
    heatmap_data = filtered_df.pivot_table(
        index='city',
        columns='year',
        values='amount',
        aggfunc='sum',
        fill_value=0
    )
    
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.heatmap(heatmap_data, cmap='YlGnBu', annot=True, fmt='.0f', ax=ax)
    ax.set_title('Total Funding in Top 10 Cities (by Year)')
    ax.set_xlabel('Year')
    ax.set_ylabel('City')
    st.pyplot(fig)
    
    # Display thanks message and outro
    st.subheader("Thanks for using the Startup Funding Analysis app! If you have any questions or need further assistance, feel free to ask.")
    st.write("Developed by Megh Bavarva")
    st.write("Contact:8849855886")
    st.write("Email:bavarvamegh3139@gmail.com")




# main starter code
st.sidebar.title("Startup Funding Analysis")
option = st.sidebar.selectbox("Select one",['Overall Analysis','Startups','Investors'])


# side bar options 
if(option=='Overall Analysis'):
    st.title("Overall Analysis")
    load_overallAnalysis_details()
  
  
elif(option=='Startups'):
    st.title("Startups")
    selected_startup = st.sidebar.selectbox("Select a startup", sorted(df['startup'].unique().tolist()))
    btn1= st.sidebar.button("Find startup details")
    if btn1:
        load_startup_details(selected_startup)


else:
    st.title("Investors")
    selected_investor = st.sidebar.selectbox("Select an investor", sorted(set(df['investors'].str.split(',').sum())) )
    btn2= st.sidebar.button("Find investor details")
    if btn2:
        load_investor_details(selected_investor)
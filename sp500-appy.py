import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import yfinance as yf
import streamlit.components.v1 as components

st.title('S&P 500 App')

st.markdown("""
This app retrieves the list of the **S&P 500** (from Wikipedia) and its corresponding **stock closing price** (year-to-date)!
* **Python libraries:** base64, pandas, streamlit,matplotlib, yfinance
* **Data source:** [Wikipedia](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies).
""")

st.sidebar.header('User Input Features')

# Web scraping of S&P 500 data

@st.cache_data
def load_data():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    html = pd.read_html(url, header = 0)
    df = html[0]
    return df

df = load_data()
sector = df.groupby('GICS Sector')

# Sidebar - Sector selection
sorted_sector_unique = sorted( df['GICS Sector'].unique() )
selected_sector = st.sidebar.multiselect('Sector', sorted_sector_unique, sorted_sector_unique)




# Filtering data based on sector selection

if selected_sector:
    df_selected_sector = df[df['GICS Sector'].isin(selected_sector)]
    st.header('Display Companies in Selected Sector')
    st.write('Data Dimension: ' + str(df_selected_sector.shape[0]) + ' rows and ' + str(df_selected_sector.shape[1]) + ' columns.')
    st.dataframe(df_selected_sector)
else:
    st.header('No sector selected')
    st.write('Please select at least one sector from the sidebar.')
    df_selected_sector = pd.DataFrame()





# Download S&P500 data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="SP500.csv">Download CSV File</a>'
    return href



# Only show the download link if df_selected_sector is not empty
if not df_selected_sector.empty:
    st.markdown(filedownload(df_selected_sector), unsafe_allow_html=True)

    data = yf.download(
            tickers = list(df_selected_sector[:10].Symbol),
            period = "ytd",
            interval = "1d",
            group_by = 'ticker',
            auto_adjust = True,
            prepost = True,
            threads = True,
            proxy = None
        )
    # Plot Closing Price of Query Symbol
    def price_plot(symbol):
        df = pd.DataFrame(data[symbol].Close)
        df['Date'] = df.index
        plt.fill_between(df.Date, df.Close, color='skyblue', alpha=0.3)
        plt.plot(df.Date, df.Close, color='skyblue', alpha=0.8)
        plt.xticks(rotation=90)
        plt.title(symbol, fontweight='bold')
        plt.xlabel('Date', fontweight='bold')
        plt.ylabel('Closing Price', fontweight='bold')
        return st.pyplot()
    
    num_company = st.sidebar.slider('Number of ' ' Companies to plot', 1, 5)

    if st.button('Show Plots'):
        st.header('Stock Closing Price')
        for i in list(df_selected_sector.Symbol)[:num_company]:
            price_plot(i)

else:
    st.write("No data available for download or analysis.")
    

company_search = st.sidebar.text_input('Search for specific companies (comma separated)', 'ibm, Oracle')

# Filtering data based on company search
if company_search:
    search_list = [company.strip() for company in company_search.split(',')]
    df_selected_company = df[df['Security'].str.contains('|'.join(search_list), case=False, na=False)]
    if not df_selected_company.empty:
        st.header('Search Results')
        st.write('Data Dimension: ' + str(df_selected_company.shape[0]) + ' rows and ' + str(df_selected_company.shape[1]) + ' columns.')
        st.dataframe(df_selected_company)
        st.markdown(filedownload(df_selected_company), unsafe_allow_html=True)

        data = yf.download(
                tickers = list(df_selected_company[:10].Symbol),
                period = "ytd",
                interval = "1d",
                group_by = 'ticker',
                auto_adjust = True,
                prepost = True,
                threads = True,
                proxy = None
            )
    else:
        st.write('No matching companies found.')

   # Plot Closing Price of Query Symbol
    def price_plot(symbol):
        df = pd.DataFrame(data[symbol].Close)
        df['Date'] = df.index
        plt.fill_between(df.Date, df.Close, color='skyblue', alpha=0.3)
        plt.plot(df.Date, df.Close, color='skyblue', alpha=0.8)
        plt.xticks(rotation=90)
        plt.title(symbol, fontweight='bold')
        plt.xlabel('Date', fontweight='bold')
        plt.ylabel('Closing Price', fontweight='bold')
        return st.pyplot()
    


    if st.button('Show Plots from selected companies'):
        st.header('Stock Closing Price')
        for symbol in df_selected_company['Symbol']:
            price_plot(symbol)


st.sidebar.markdown("---")
st.sidebar.markdown("Created by [Josue Holguin](http://www.linkedin.com/in/josue-holguin-13694324b)")

# Insert the AdSense code using st.components.v1.html
adsense_code = """<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5145863563085320"
     crossorigin="anonymous"></script>"""

# Display the ad in Streamlit using st.components.v1.html
components.html(adsense_code, height=300) 


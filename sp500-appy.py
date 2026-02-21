import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import yfinance as yf
import streamlit.components.v1 as components
from urllib.request import Request, urlopen

# Set a page config for better display

st.set_page_config(layout="wide")

st.title('S&P 500 App')

st.markdown("""
This app retrieves the list of the **S&P 500** (from Wikipedia) and its corresponding **stock closing price** (year-to-date)!
* **Python libraries:** base64, pandas, streamlit, matplotlib, yfinance
* **Data source:** [Wikipedia](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies).
""")

st.sidebar.header('User Input Features')

# Web scraping of S&P 500 data
@st.cache_data
def load_data():
    """
    Loads S&P 500 company data from Wikipedia.
    The @st.cache_data decorator caches the result to avoid
    re-running the function every time the app is updated.
    """
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
    with urlopen(req) as response:
        html = response.read()
    df = pd.read_html(html, header=0)[0]
    return df

# Load the data
df = load_data()

# Sidebar - Sector selection
sorted_sector_unique = sorted(df['GICS Sector'].unique())
selected_sector = st.sidebar.multiselect('Sector', sorted_sector_unique, sorted_sector_unique)

# Filtering data based on sector selection
df_selected_sector = df[df['GICS Sector'].isin(selected_sector)]

# Show message when no sector selected
if df_selected_sector.empty:
    st.info("Please select at least one sector to start.")
else:
    st.header('Display Companies in Selected Sector')
    st.write(f'Data Dimension: {df_selected_sector.shape[0]} rows and {df_selected_sector.shape[1]} columns.')
    st.dataframe(df_selected_sector)

# Download S&P500 data
def filedownload(df_to_download):
    """
    Generates a download link for a given DataFrame.
    """
    csv = df_to_download.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="SP500.csv">Download CSV File</a>'
    return href

# Only show the download link if df_selected_sector is not empty
if not df_selected_sector.empty:
    st.markdown(filedownload(df_selected_sector), unsafe_allow_html=True)
else:
    st.write("No data available for download or analysis.")

# ----- Helper functions (always defined for use in sector and search sections) -----
@st.cache_data(show_spinner=False)
def download_yfinance_data(tickers):
    """
    Downloads stock data using yfinance. Caches the result.
    """
    if not tickers:
        return pd.DataFrame()
    return yf.download(
        tickers=list(tickers),
        period="ytd",
        interval="1d",
        group_by='ticker',
        auto_adjust=True,
        prepost=True,
        threads=True
    )

def price_plot(symbol, plot_data):
    """
    Plots the closing price of a given stock symbol using the object-oriented approach.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    df_symbol = pd.DataFrame(plot_data[symbol].Close)
    df_symbol['Date'] = df_symbol.index
    ax.fill_between(df_symbol.Date, df_symbol.Close, color='skyblue', alpha=0.3)
    ax.plot(df_symbol.Date, df_symbol.Close, color='skyblue', alpha=0.8)
    ax.set_title(f"Closing Price for {symbol}", fontweight='bold')
    ax.set_xlabel('Date', fontweight='bold')
    ax.set_ylabel('Closing Price', fontweight='bold')
    plt.xticks(rotation=90)
    st.pyplot(fig)

# ----- Section for plotting based on selected sectors -----
if not df_selected_sector.empty:
    tickers_to_plot = list(df_selected_sector.Symbol[:10])
    data = download_yfinance_data(tickers_to_plot)
    num_company = st.sidebar.slider('Number of Companies to plot', 1, len(tickers_to_plot))
    
    if st.button('Show Plots'):
        st.header('Stock Closing Price')
        if not data.empty:
            for i in list(df_selected_sector.Symbol)[:num_company]:
                if i in data.columns.get_level_values(0):
                    price_plot(i, data)
                else:
                    st.warning(f"No data available for symbol: {i}")
        else:
            st.warning("No stock data found for the selected companies.")

# ----- Section for searching specific companies -----
company_search = st.sidebar.text_input('Search for specific companies (comma separated)', 'IBM, Oracle')

if company_search:
    search_list = [company.strip() for company in company_search.split(',')]
    df_selected_company = df[df['Security'].str.contains('|'.join(search_list), case=False, na=False)]
    
    if not df_selected_company.empty:
        st.header('Search Results')
        st.write(f'Data Dimension: {df_selected_company.shape[0]} rows and {df_selected_company.shape[1]} columns.')
        st.dataframe(df_selected_company)
        st.markdown(filedownload(df_selected_company), unsafe_allow_html=True)
        
        tickers_to_plot_search = list(df_selected_company.Symbol[:10])
        data_search = download_yfinance_data(tickers_to_plot_search)

        if st.button('Show Plots from selected companies'):
            st.header('Stock Closing Price (Search Results)')
            if not data_search.empty:
                for symbol in df_selected_company['Symbol']:
                    if symbol in data_search.columns.get_level_values(0):
                        price_plot(symbol, data_search)
                    else:
                        st.warning(f"No data available for symbol: {symbol}")
            else:
                st.warning("No stock data found for the searched companies.")

    else:
        st.write('No matching companies found.')

# Footer and Adsense
st.sidebar.markdown("---")
st.sidebar.markdown("Created by [Josue Holguin](http://www.linkedin.com/in/josue-holguin-13694324b)")

# Insert the AdSense code using st.components.v1.html
adsense_code = """<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5145863563085320"
      crossorigin="anonymous"></script>"""
components.html(adsense_code, height=300)

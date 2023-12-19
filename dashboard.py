import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set style seaborn
sns.set(style='whitegrid')
st.set_page_config(page_title="Bike sharing Dashboard",
                   page_icon="bar_chart:")
# Load Data
data_df = pd.read_csv("data/main_data.csv")
data_df.head()


# Menyiapkan Helper
def create_count_rent_df(df):
    count_rent_df = df.groupby(by='date').agg({
        'Count': 'sum'
    }).reset_index()
    return count_rent_df

# Menyiapkan count_casual_rent_df
def create_count_casual_rent_df(df):
    count_casual_rent_df = df.groupby(by='date').agg({
        'casual': 'sum'
    }).reset_index()
    return count_casual_rent_df

# Menyiapkan count_registered_rent_df
def create_count_registered_rent_df(df):
    count_registered_rent_df = df.groupby(by='date').agg({
        'registered': 'sum'
    }).reset_index()
    return count_registered_rent_df
    
# Menyiapkan season_rent_df
def create_season_rent_df(df):
    season_rent_df = df.groupby(by=["year","season"], observed=True).agg({"casual":"sum","registered":"sum","Count":"sum"})
    return season_rent_df

# Menyiapkan weather_rent_df
def create_weather_rent_df(df):
    weather_rent_df = df.groupby(by=["year","weather"], observed=True).agg({"casual":"sum","registered":"sum","Count":"sum"}).sort_values(by=['Count'], ascending=False)
    return weather_rent_df

# Menyiapkan monthly_rent_df
def create_monthly_rent_df(df):
    monthly_rent_df = df.groupby(by=["year","month"], observed=True).agg({"casual":"sum","registered":"sum","Count":"sum"}).sort_values(by=['year'])
    return monthly_rent_df

# Membuat komponen filter
min_date = pd.to_datetime(data_df['date']).dt.date.min()
max_date = pd.to_datetime(data_df['date']).dt.date.max()
 
with st.sidebar:
    st.image('img/logo.png')
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value= min_date,
        max_value= max_date,
        value=[min_date, max_date]
    )

main_df = data_df[(data_df['date'] >= str(start_date)) & 
                (data_df['date'] <= str(end_date))]

# Menyiapkan berbagai dataframe
count_rent_df = create_count_rent_df(main_df)
count_casual_rent_df = create_count_casual_rent_df(main_df)
count_registered_rent_df = create_count_registered_rent_df(main_df)
season_rent_df = create_season_rent_df(main_df)
monthly_rent_df = create_monthly_rent_df(main_df)
weather_rent_df = create_weather_rent_df(main_df)


# Membuat Dashboard secara lengkap
# Membuat judul
st.header('Bike Sharing Dashboard :sparkles:')

col1, col2, col3 = st.columns(3)

with col1:
    count_rent_casual = count_casual_rent_df['casual'].sum()
    st.metric('Casual User', value= count_rent_casual)

with col2:
    count_rent_registered = count_registered_rent_df['registered'].sum()
    st.metric('Registered User', value= count_rent_registered)
 
with col3:
    count_rent_total = count_rent_df['Count'].sum()
    st.metric('Total User', value= count_rent_total)

# Membuat jumlah penyewaan berdasarkan musim
st.subheader('Seasonly Rentals')

fig, axes = plt.subplots(2, 2, figsize=(10,10))
fig.suptitle("Bikeshare rides by Season")

fig1 = sns.barplot(
    x='season',
    y='registered',
    data=season_rent_df,
    label='Registered',
    errorbar=None,
    color='tab:blue',
    ax=axes[0,0],
)

fig1 = sns.barplot(
    x='season',
    y='casual',
    data=season_rent_df,
    label='Casual',
    errorbar=None,
    color='tab:orange',
    ax=axes[0,0]

)

fig2 = sns.barplot(
    x="season",
    y="Count",
    data=season_rent_df,
    palette='pastel',
    hue="season",
    estimator="sum",
    errorbar=None,
    ax=axes[0,1]
)

fig3 = sns.barplot(
    x="season",
    y="Count",
    data=season_rent_df,
    palette='pastel',
    hue="year",
    estimator="sum",
    errorbar=None,
    ax=axes[1,1]
)
fig4 = sns.pointplot(
    x="season",
    y="Count",
    data=season_rent_df,
    palette='pastel',
    hue="year",
    estimator="sum",
    ax=axes[1,0]
    
)

for i in fig1.containers:
    fig1.bar_label(i, )

for i in fig2.containers:
    fig2.bar_label(i, )

for i in fig3.containers:
    fig3.bar_label(i, )

plt.tight_layout()
axes[0,0].set(ylabel="Count")
st.pyplot(fig)

# Membuah jumlah penyewaan berdasarkan kondisi cuaca
st.subheader('Weatherly Rentals')

fig, axes = plt.subplots(3, 1, figsize=(9,18))
fig.suptitle("Bikeshare rides by Weatherist")

fig1 = sns.barplot(
    x="weather",
    y="Count",
    data=weather_rent_df,
    palette='flare',
    hue="weather",
    estimator="sum",
    errorbar=None,
    ax=axes[0]    
)

fig2 = sns.barplot(
    x="weather",
    y="Count",
    data=weather_rent_df,
    palette='flare',
    hue="year",
    estimator="sum",
    errorbar=None,
    ax=axes[1]
)

fig3 = sns.barplot(
    x='weather',
    y='registered',
    data=weather_rent_df,
    label='Registered',
    errorbar=None,
    color='tab:blue',
    ax=axes[2],
)

sns.barplot(
    x='weather',
    y='casual',
    data=weather_rent_df,
    label='Casual',
    errorbar=None,
    color='tab:orange',
    ax=axes[2],
)

for i in fig1.containers:
    fig1.bar_label(i, )

for i in fig2.containers:
    fig2.bar_label(i, )

for i in fig3.containers:
    fig3.bar_label(i, )

plt.tight_layout()
axes[2].set(ylabel="Count")
st.pyplot(fig)

# Membuat jumlah penyewaan bulanan
st.subheader('Monthly Rentals')
ordered_months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]
 
fig, axes = plt.subplots(3, 1, figsize=(10,15))
fig.suptitle("Bikeshare rides by Month")
sns.pointplot(
    x="month",
    y="Count",
    data=monthly_rent_df,
    order=ordered_months,
    palette='pastel',
    hue="year",
    estimator="sum",
    errorbar=None,
    ax=axes[0]    
)

fig1 = sns.barplot(
    x="month",
    y="Count",
    data=monthly_rent_df,
    order=ordered_months,
    palette='pastel',
    hue="year",
    estimator="sum",
    errorbar=None,
    ax=axes[1]
)

fig2 = sns.barplot(
    x='month',
    y='registered',
    data=monthly_rent_df,
    order=ordered_months,
    label='Registered',
    errorbar=None,
    color='tab:blue',
    ax=axes[2]
)

sns.barplot(
    x='month',
    y='casual',
    data=monthly_rent_df,
    order=ordered_months,
    label='Casual',
    errorbar=None,
    color='tab:orange',
    ax=axes[2]

)

for i in fig1.containers:
    fig1.bar_label(i, )

for i in fig2.containers:
    fig2.bar_label(i, )
    
axes[2].set(ylabel="Count")
plt.tight_layout()
st.pyplot(fig)


st.caption('Copyright :copyright: RDA 2023')
# ----- HIDE STREAMLIT STYLE -----
hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)
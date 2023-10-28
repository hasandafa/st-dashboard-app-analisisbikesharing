import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objs as go

# Load data
merged_df = pd.read_csv('merged_df.csv')

# Define weather_dict
weather_dict = {
    1: 'Cerah',
    2: 'Berawan',
    3: 'Hujan Ringan atau Salju Ringan',
    4: 'Hujan Lebat atau Salju Lebat'
}
# Visualisasi Pertama
def fig1():
    fig = go.Figure()
    fig.add_trace(go.Box(
        x=merged_df['holiday_day'].map({0: 'Hari Kerja', 1: 'Hari Libur'}),
        y=merged_df['count_day'],
        name='Jumlah Sepeda yang Dipinjam',
        boxmean=True,
        jitter=0.3,
        pointpos=-1.8,
        marker=dict(
            color='#1f77b4'
        ),
    ))

    fig.update_layout(
        title='Distribusi jumlah sepeda yang dipinjam pada hari kerja dan hari libur',
        xaxis_title='Jenis Hari',
        yaxis_title='Jumlah Sepeda yang Dipinjam',
    )

    return fig

# Visualisasi Kedua
def fig2():
    # Group data berdasarkan tanggal untuk menghitung rata-rata harian
    daily_avg_rentals = merged_df.groupby('weekday_day')['count_day'].mean()

    hari = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
    daily_avg_rentals.index = [hari[i] for i in daily_avg_rentals.index]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=daily_avg_rentals.index,
        y=daily_avg_rentals.values,
        name='Rata-rata Penyewaan Harian',
        marker=dict(
            color='#1f77b4'
        )
    ))

    fig.update_layout(
        title='Distribusi Rata-rata Penyewaan Sepeda per Hari',
        xaxis_title='Tanggal',
        yaxis_title='Rata-rata Penyewaan',
    )

    return fig

# Visualisasi Ketiga
def fig3():
    weather_dict = {
        1: 'Cerah',
        2: 'Berawan',
        3: 'Hujan Ringan atau Salju Ringan',
        4: 'Hujan Lebat atau Salju Lebat'
    }

    fig = go.Figure()

    for weather_code in merged_df['weather_day'].unique():
        fig.add_trace(go.Scatter(
            x=merged_df[merged_df['weather_day'] == weather_code]['temp_day'] * 41,
            y=merged_df[merged_df['weather_day'] == weather_code]['count_day'],
            mode='markers',
            name=weather_dict[weather_code],
            marker=dict(
                size=8,
                line=dict(
                    width=1,
                    color='#1f77b4'
                )
            )
        ))

    fig.update_layout(
        title='Pengaruh cuaca terhadap jumlah sepeda yang dipinjam',
        xaxis_title='Suhu (Celsius)',
        yaxis_title='Jumlah Sepeda yang Dipinjam',
    )

    return fig

# Visualisasi Keempat
def fig4():
    # Group data berdasarkan hour untuk menghitung rata-rata jumlah rental
    hourly_rentals = merged_df.groupby('hour')['count_hour'].mean()
    trace = go.Bar(x=hourly_rentals.index, 
                   y=hourly_rentals.values, 
                   marker=dict(
                       color='#1f77b4'))
    layout = go.Layout(title='Rata-rata jumlah penyewaan tiap jamnya', 
                       xaxis=dict(title='Hour'), yaxis=dict(title='Rata-rata Penyewaan'))

    fig = go.Figure(data=[trace], layout= layout)

    return fig

# Visualisasi Kelima
def fig5():
    # Group data berdasarkan month untuk menghitung total jumlah rental
    casual_rentals = merged_df.groupby('month_day')['casual_day'].sum()
    registered_rentals = merged_df.groupby('month_day')['registered_day'].sum()

    bulan = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']
    casual_rentals.index = [bulan[i-1] for i in casual_rentals.index]
    registered_rentals.index = [bulan[i-1] for i in registered_rentals.index]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x= casual_rentals.index,
        y=casual_rentals.values,
        name='Casual',
        marker=dict(
            color='#1f77b4'
        )
    ))

    fig.add_trace(go.Bar(
        x=registered_rentals.index,
        y=registered_rentals.values,
        name='Registered',
        marker=dict(
            color='#ff7f0e'
        )
    ))

    fig.update_layout(
        title='Distribusi jumlah sepeda yang dipinjam pada setiap bulan',
        xaxis_title='Bulan',
        yaxis_title='Jumlah Sepeda yang Dipinjam',
        barmode='stack'
    )

    return fig

# Visualisasi Keenam
def fig6():
    # Group data berdasarkan musim untuk menghitung rata-rata jumlah rental
    casual_rentals = merged_df.groupby('season_day')['casual_day'].mean()
    registered_rentals = merged_df.groupby('season_day')['registered_day'].mean()

    musim = ['Musim Semi', 'Musim Panas', 'Musim Gugur', 'Musim Dingin']
    casual_rentals.index = [musim[i-1] for i in casual_rentals.index]
    registered_rentals.index = [musim[i-1] for i in registered_rentals.index]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x= casual_rentals.index,
        y= casual_rentals.values,
        name='Casual',
        marker=dict(
            color='#1f77b4'
        )
    ))

    fig.add_trace(go.Bar(
        x=registered_rentals.index,
        y=registered_rentals.values,
        name='Registered',
        marker=dict(
            color='#ff7f0e'
        )
    ))

    fig.update_layout(
        title='Distribusi rata-rata sepeda yang dipinjam pada setiap musim',
        xaxis_title='Musim',
        yaxis_title='Rata-rata Sepeda yang Dipinjam',
        barmode='stack'
    )

    return fig

# Create Streamlit app
st.title('Dashboard Analisis Sepeda Publik')
st.caption('oleh Abdullah Hasan Dafa')

# Pertanyaan 1: Distribusi jumlah sepeda yang dipinjam pada hari kerja dan hari libur
st.header('Distribusi Jumlah Sepeda pada Hari Kerja dan Hari Libur')

# Dropdown widget untuk memilih visualisasi
chart_type = st.selectbox("Pilih Visualisasi:", 
                          ['Distribusi jumlah sepeda yang dipinjam pada hari kerja dan hari libur', 
                           'Distribusi rata-rata penyewaan sepeda per hari'])

if chart_type == 'Distribusi jumlah sepeda yang dipinjam pada hari kerja dan hari libur':
    st.write("Berikut adalah visualisasi jumlah sepeda yang dipinjam pada hari kerja dan hari libur:")
    st.plotly_chart(fig1())  # Menampilkan box chart
    st.write("Berdasarkan box chart, penggunaan sepeda pada rental pinjam didominasi saat hari kerja dengan rata-rata sepeda yang dipinjam sebesar 4,557 sepeda dibandingkan dengan hari libur dengan rata-rata 3,750 sepeda yang dipinjam.")
else:
    # Visualisasi rata-rata penyewaan per hari
    st.write("Berikut adalah visualisasi rata-rata penyewaan sepeda per hari:")
    st.plotly_chart(fig2())
    st.write("Selain itu, minat peminjam untuk menyewa sepeda tertinggi berada di hari Jumat dan Sabtu dengan rata-rata penyewaan sepeda sekitar sebanyak 4,703 dan 4,700.")

# Pertanyaan 2: Pengaruh cuaca terhadap jumlah sepeda yang dipinjam
st.header('Pengaruh Cuaca terhadap Jumlah Sepeda yang Dipinjam')

# Slider widget untuk memilih jenis cuaca
# selected_weather = st.slider("Pilih Jenis Cuaca:", min_value=1, max_value=4, value=[1, 4])
# filtered_df = merged_df[merged_df['weather_day'].between(selected_weather[0], selected_weather[1])]

st.plotly_chart(fig3())  # Menampilkan scatter plot

# Keterangan Pertanyaan 2
st.write("Kebanyakan penyewa sepeda memilih untuk menyewa sepeda pada hari dengan cuaca yang cerah. Selain itu, terbukti bahwa baik suhu maupun keadaan cuaca berpengaruh kepada jumlah penyewaan sepeda.")
st.write("Jumlah penyewaan sepeda merosot apabila suhu nya terlalu dingin dan terlalu panas, serta saat hujan ringan atau salju ringan melanda.")
st.write("Apalagi saat kondisi hujan lebat, berkabut, badai atau kondisi cuaca buruk lainnya terlihat bahwa tidak ada penyewaan sepeda sama sekali.")

# Pertanyaan 3: Rata-rata jumlah penyewaan jam tiap jamnya
st.header('Rata-rata Jumlah Penyewaan tiap Jamnya')
st.plotly_chart(fig4())  # Menampilkan bar chart

# Keterangan Pertanyaan 3
st.write("Jam-jam yang paling ideal untuk penyewaan sepeda berada pada jam 5 sore, jam 6 sore, dan jam 8 pagi. Pada jam-jam tersebut, rata-rata jumlah penyewaan sepeda cukup tinggi.")

# Pertanyaan 4: Distribusi jumlah sepeda yang dipinjam pada setiap bulan dan musimnya
st.header('Distribusi Jumlah Sepeda pada Setiap Bulan dan Musim')

# Dropdown widget untuk memilih visualisasi
chart_type_2 = st.selectbox("Pilih Visualisasi:", 
                            ['Distribusi jumlah sepeda yang dipinjam pada setiap bulan', 
                             'Distribusi rata-rata sepeda yang dipinjam pada setiap musim'])

if chart_type_2 == 'Stacked Bar Chart':
    st.plotly_chart(fig5())  # Menampilkan stacked bar chart
    st.write("Berdasarkan total jumlah peminjaman sepeda, bulan Agustus menjadi bulan dengan total terbanyak, dengan total terbanyak yaitu sebesar 6,673,953 peminjaman sepeda")
else:
    # Visualisasi rata-rata penyewaan per musim
    st.plotly_chart(fig6())
    st.write("Musim gugur menjadi musim dengan rata-rata penyewa sepeda terbanyak, dengan rata-rata penyewa sepeda terbanyak yaitu 4,450 penyewa terdaftar dan 1,204 penyewa biasa.")
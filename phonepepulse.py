from streamlit_option_menu import option_menu
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import base64

# Constants
states = {
    'All': 'All',
    'ladakh': 'ladakh',
    'nagaland': 'nagaland',
    'chhattisgarh': 'chhattisgarh',
    'jammu-&-kashmir': 'jammu-&-kashmir',
    'gujarat': 'gujarat',
    'lakshadweep': 'lakshadweep',
    'uttarakhand': 'uttarakhand',
    'punjab': 'punjab',
    'chandigarh': 'chandigarh',
    'maharashtra': 'maharashtra',
    'jharkhand': 'jharkhand',
    'delhi': 'delhi',
    'kerala': 'kerala',
    'tamil-nadu': 'tamil-nadu',
    'meghalaya': 'meghalaya',
    'puducherry': 'puducherry',
    'himachal-pradesh': 'himachal-pradesh',
    'mizoram': 'mizoram',
    'manipur': 'manipur',
    'rajasthan': 'rajasthan',
    'west-bengal': 'west-bengal',
    'andhra-pradesh': 'andhra-pradesh',
    'uttar-pradesh': 'uttar-pradesh',
    'sikkim': 'sikkim',
    'madhya-pradesh': 'madhya-pradesh',
    'odisha': 'odisha',
    'karnataka': 'karnataka',
    'tripura': 'tripura',
    'goa': 'goa',
    'haryana': 'haryana',
    'andaman-&-nicobar-islands': 'andaman-&-nicobar-islands',
    'telangana': 'telangana',
    'arunachal-pradesh': 'arunachal-pradesh',
    'dadra-&-nagar-haveli-&-daman-&-diu': 'dadra-&-nagar-haveli-&-daman-&-diu',
    'assam': 'assam',
    'bihar': 'bihar'
}


years = [2018, 2019, 2020, 2021, 2022]
quarters = ["1", "2", "3", "4"]

# Database setup
connection_string = "mysql+mysqlconnector://root:123456789@localhost/Phonepe"
engine = create_engine(connection_string)

def get_base64_of_bin_file(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()
def main():
    my_image_path = "C:/Users/siva_/PycharmProjects/pythonProject2/phonepeimg.png"
    my_image_encoded = get_base64_of_bin_file(my_image_path)

    st.markdown(
        f"""
        <style>
        html {{
            background-image: url("data:image/png;base64,{my_image_encoded}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        body {{
            background-color: transparent !important;
        }}
        .stApp {{
            background-color: transparent !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown("<h1 style='text-align: left; font-weight: bold; color: ###080800;'>Phonepe Pulse Data Visualization</h1>", unsafe_allow_html=True)

    # Assuming option_menu is imported and working
    menu = option_menu(
        menu_title=None,
        options=["Home", "Chart", "Map", "Top 10 Info", "About"],
        icons=["house", "pie-chart", "geo-alt", "trophy", "envelope"],
        menu_icon="cast",
        default_index=0,
        styles={"nav-link": {"--hover-color": "grey"}},
        orientation="horizontal"
    )

    if menu == "Home":
        st.write("")  # Empty space for top margin
        st.write("")  # Add more for more space

        # Slide title
        st.markdown(
            "<h1 style='text-align: center; font-weight: bold; color: #080800;'>Phonepe & its journey</h1>",
            unsafe_allow_html=True)

        # Image (if you have a logo or relevant image, you can add it here)
        # st.image("path_to_image.jpg", use_column_width=True)

        # Bullet points using markdown
        content = """
            <div style="font-family: verdana; font-size: 20px; padding: 25px; background-color: #2c3e50; border-radius: 10px; color: #ecf0f1;">
                <ul>
                    <li>Founded in 2015 by Sameer Nigam, Rahul Chari, and Burzin Engineer, headquartered in Bengaluru.</li>
                    <li>Owned by Flipkart and is a leading digital payments platform in India.</li>
                    <li>Available for Android and iOS with over 300 million registered users as of 2021.</li>
                    <li>Supports UPI, credit/debit cards, and wallets.</li>
                    <li>Offers services including bill payments, mobile recharges, DTH recharges, and more.</li>
                    <li>Received several awards including the Best Payments App at the India Digital Awards.</li>
                    <li>Introduced the PhonePe Pulse Dataset API for open data in the payments space.</li>
                </ul>
            </div>
            """
        st.markdown(content, unsafe_allow_html=True)

        # Additional details or footer
        st.write("For more details, visit the official [Phonepe website](https://www.phonepe.com/).")


    elif menu == "Chart":
        st.subheader('Aggregated information')

        # Filters
        col1, col2, col3, col4 = st.columns(4)
        selected_state = col1.selectbox("Select State", list(states.values()))
        selected_year = col2.selectbox("Select Year", ["All"] + years)
        selected_quarter = col3.selectbox("Select Quarter", ["All"] + quarters)

        if col4.button("Search"):
            # Constructing the SQL query for transactions
            base_query = "SELECT * FROM agg_transaction WHERE 1"
            if selected_state and selected_state != 'All':
                base_query += f" AND State = '{selected_state}'"
            if selected_year and selected_year != 'All':
                base_query += f" AND Year = {selected_year}"
            if selected_quarter and selected_quarter != 'All':
                base_query += f" AND Quater = '{selected_quarter}'"

            # Fetching the data
            df = pd.read_sql(base_query, engine)
            aggregated_df = df.groupby('Transaction_type').agg({
                'Transaction_count': 'sum',
                'Transaction_amount': 'sum'
            }).reset_index()
            col_data, col_hist = st.columns(2)
            with col_data:
                st.header("Transaction summary")
                st.dataframe(aggregated_df)
            with col_hist:
                fig = px.histogram(df, x='Transaction_type', y="Transaction_amount", color="Transaction_type",
                                   nbins=50, color_discrete_sequence=['green', '#FF5733', 'white', 'yellow', 'red'],
                                   title='Distribution of Transaction Amounts')
                fig.update_layout(title_x=0.45, title_y=0.85)
                fig.update_xaxes(title='Transaction_type')
                fig.update_yaxes(title="Transaction_amount")
                st.plotly_chart(fig)

            # Constructing the SQL query for users
            user_query = "SELECT * FROM agg_user WHERE 1"
            if selected_state and selected_state != 'All':
                user_query += f" AND State = '{selected_state}'"
            if selected_year and selected_year != 'All':
                user_query += f" AND Year = {selected_year}"
            if selected_quarter and selected_quarter != 'All':
                user_query += f" AND Quater = '{selected_quarter}'"
            df_user = pd.read_sql(user_query, engine)

            user_query_brand = """
                    SELECT User_Brand, SUM(User_count) as TotalUserCount
                    FROM agg_user
                    GROUP BY User_Brand
                    ORDER BY TotalUserCount DESC
                    LIMIT 5;
                """
            df_user_brand = pd.read_sql(user_query_brand, engine)

            # Displaying user data
            st.write("### User summary")
            st.subheader("Aggregated User Summary")
            st.dataframe(df_user)
            st.subheader('Top Mobile brands by user')
            st.dataframe(df_user_brand)
            # Histogram for agg_user
            fig_user = px.bar(df_user, x='Quater', y='User_count', color='User_Brand',
                              hover_data=['User_percentage'], animation_frame='Year',
                              title='Distribution of User Counts per Quarter by Brand',
                              labels={'User_count': 'User Count', 'Quater': 'Quarter'},
                              color_discrete_sequence=px.colors.qualitative.Prism)

            fig_user.update_layout(title_x=0, title_y=0.95, barmode='group')

            st.plotly_chart(fig_user)
    elif menu == "Map":
        # Filters
        col1, col2, col3 = st.columns(3)
        selected_year = col1.selectbox("Select Year", ["All"] + years)
        selected_quarter = col2.selectbox("Select Quarter", ["All"] + quarters)

        if col3.button("Search"):
            # Constructing the SQL query for map_transaction
            map_query = "SELECT * FROM map_transaction WHERE 1"
            if selected_year and selected_year != 'All':
                map_query += f" AND Year = {selected_year}"
            if selected_quarter and selected_quarter != 'All':
                map_query += f" AND Quater = '{selected_quarter}'"

            # Fetching the data
            df_map = pd.read_sql(map_query, engine)

            state_map = {'ladakh': 'Ladakh', 'nagaland': 'Nagaland', 'chhattisgarh': 'Chhattisgarh',
                         'jammu-&-kashmir': 'Jammu & Kashmir', 'gujarat': 'Gujarat', 'lakshadweep': 'Lakshadweep',
                         'uttarakhand': 'Uttarakhand', 'punjab': 'Punjab', 'chandigarh': 'Chandigarh',
                         'maharashtra': 'Maharashtra', 'jharkhand': 'Jharkhand', 'delhi': 'Delhi', 'kerala': 'Kerala',
                         'tamil-nadu': 'Tamil Nadu', 'meghalaya': 'Meghalaya', 'puducherry': 'Puducherry',
                         'himachal-pradesh': 'Himachal Pradesh', 'mizoram': 'Mizoram', 'manipur': 'Manipur',
                         'rajasthan': 'Rajasthan', 'west-bengal': 'West Bengal', 'andhra-pradesh': 'Andhra Pradesh',
                         'uttar-pradesh': 'Uttar Pradesh', 'sikkim': 'Sikkim', 'madhya-pradesh': 'Madhya Pradesh',
                         'odisha': 'Odisha', 'karnataka': 'Karnataka', 'tripura': 'Tripura', 'goa': 'Goa',
                         'haryana': 'Haryana', 'andaman-&-nicobar-islands': 'Andaman & Nicobar',
                         'telangana': 'Telangana', 'arunachal-pradesh': 'Arunachal Pradesh',
                         'dadra-&-nagar-haveli-&-daman-&-diu': 'Dadra and Nagar Haveli and Daman and Diu',
                         'assam': 'Assam', 'bihar': 'Bihar'}  # keep the rest of the mapping as is
            df_map['State'] = df_map['State'].map(state_map)  # adjusting the names according to geo map

            # Constructing the choropleth for the entire country
            fig_map_transaction = px.choropleth(df_map,
                                                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                                featureidkey='properties.ST_NM',
                                                locations='State',
                                                color='State',
                                                hover_data=['State', 'Transaction_count'],
                                                color_continuous_scale='Turbo')
            fig_map_transaction.update_geos(fitbounds='locations', visible=False)
            fig_map_transaction.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, geo=dict(bgcolor='#00172B'),
                                              height=300,
                                              width=1200)
            st.markdown(
                "<h1 style='text-align: center; font-weight: bold; color: #080800;'>Geo Map Based on Transaction</h1>",
                unsafe_allow_html=True)

            st.plotly_chart(fig_map_transaction, use_container_width=True)

            # Constructing the SQL query for map_user
            map_user_query = "SELECT * FROM map_user WHERE 1"
            if selected_year and selected_year != 'All':
                map_user_query += f" AND Year = {selected_year}"
            if selected_quarter and selected_quarter != 'All':
                map_user_query += f" AND Quater = '{selected_quarter}'"

                # Fetching the data
            df_map_user = pd.read_sql(map_user_query, engine)
            df_map_user['State'] = df_map_user['State'].map(state_map)

            # Constructing the choropleth for the entire country
            fig_map_user = px.choropleth(df_map_user,
                                                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                                featureidkey='properties.ST_NM',
                                                locations='State',
                                                color='State',
                                                hover_data=['State', 'Registered_users'],
                                                color_continuous_scale='Turbo')
            fig_map_user.update_geos(fitbounds='locations', visible=False)
            fig_map_user.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, geo=dict(bgcolor='#00172B'),
                                              height=300,
                                              width=1200)
            st.markdown(
                "<h1 style='text-align: center; font-weight: bold; color: #080800;'>Geo Map Based on Users</h1>",
                unsafe_allow_html=True)
            st.plotly_chart(fig_map_user, use_container_width=True)

    elif menu == "Top 10 Info":
        cols = st.columns(2)
        selected_year = cols[0].radio("Select Year", years, horizontal=True)
        selected_quarter = cols[1].radio("Select Quarter", quarters, horizontal=True)
        if st.button("Search"):
            # Fetching top 10 districts based on the filters
            district_query = f"""
                    SELECT State, District, Transaction_count, Transaction_amount
                    FROM top_transaction_district
                    WHERE Year = {selected_year} AND Quater = '{selected_quarter}'
                    ORDER BY Transaction_amount DESC
                    LIMIT 10;
                    """
            df_district = pd.read_sql(district_query, engine)

            # Fetching top 10 pincodes based on the filters
            pincode_query = f"""
                    SELECT State, Pincodes, Transaction_count, Transaction_amount
                    FROM top_transaction_pincode
                    WHERE Year = {selected_year} AND Quater = '{selected_quarter}'
                    ORDER BY Transaction_amount DESC
                    LIMIT 10;
                    """
            df_pincode = pd.read_sql(pincode_query, engine)
            fig_pin_tra = px.sunburst(df_pincode, path=['State', 'Pincodes'], values='Transaction_amount')
            fig_dis_tra = px.sunburst(df_district, path=['State', 'District'], values='Transaction_amount')

            user_district_query = (
                f"select State, Districts, Registered_user "
                f"from top_user_district "
                f"where Year = {selected_year} And Quarter = '{selected_quarter}' "
                f"order by Registered_user desc "
                f"limit 10;"
            )
            df_user_district = pd.read_sql(user_district_query, engine)
            fig_user_district = px.sunburst(df_user_district, path=['State', 'Districts'], values='Registered_user')

            user_pincode_query = (
                f"select State, Pincodes, Registered_User "
                f"from top_user_pincode "
                f"where Year = {selected_year} And Quarter = '{selected_quarter}' "
                f"order by Registered_User desc "
                f"limit 10;"
            )
            df_user_pincode = pd.read_sql(user_pincode_query, engine)
            fig_user_pincode = px.sunburst(df_user_pincode, path=['State', 'Pincodes'], values='Registered_User')

            st.markdown(
                "<h1 style='text-align: center; font-weight: bold; color: #080800;'>Top transaction Pincode wise</h1>",
                unsafe_allow_html=True)

            col1, col2 = st.columns([0.3, 0.1])
            with col1:
                st.plotly_chart(fig_pin_tra)
            with col2:
                st.dataframe(df_pincode)

            st.markdown(
                "<h1 style='text-align: center; font-weight: bold; color: #080800;'>Top Transaction District wise</h1>",
                unsafe_allow_html=True)
            col1, col2 = st.columns([0.3, 0.1])
            with col1:
                st.plotly_chart(fig_dis_tra)
            with col2:
                st.dataframe(df_district)

            st.markdown(
                "<h1 style='text-align: center; font-weight: bold; color: #080800;'>Top Users District wise</h1>",
                unsafe_allow_html=True)
            col1, col2 = st.columns([0.3, 0.1])
            with col1:
                st.plotly_chart(fig_user_district)
            with col2:
                st.dataframe(df_user_district)

            st.markdown(
                "<h1 style='text-align: center; font-weight: bold; color: #080800;'>Top Users Pincode wise</h1>",
                unsafe_allow_html=True)
            col1, col2 = st.columns([0.3, 0.1])
            with col1:
                st.plotly_chart(fig_user_pincode)
            with col2:
                st.dataframe(df_user_pincode)
    elif menu == "About":

        st.markdown(
            '__<p style="text-align:left; font-size: 60px; color: #080800">Summary of Data Visualization Project</P>__',
            unsafe_allow_html=True)
        st.write(
            "This data visualization project focused on the user and transaction data of the Phonepe mobile payment app. By taking a copy of data from the Phonepe Pulse git repository, useful information about the behavior and transactions of users was obtained. This data was then consolidated into an interactive dashboard, which offers quick insights into how well the Phonepe app is performing.")
        st.markdown(
            '__<p style="text-align:left; font-size: 60px; color: #080800">Applications and Packages Used:</P>__',
            unsafe_allow_html=True)
        st.write("  * Python")
        st.write("  * MYSQL Workbench")
        st.write("  * Streamlit")
        st.write("  * Pandas")
        st.write("  * Github")
        st.write("  * Plotly")
        st.write("  * pymysql")
        st.markdown(
            '__<p style="text-align:left; font-size: 20px; color: #FAA026">For feedback/suggestion, connect with me on</P>__',
            unsafe_allow_html=True)
        st.subheader("LinkedIn")
        st.write("https://www.linkedin.com/in/shiva-raj-77039822a")
        st.subheader("Email ID")
        st.write("shivacva20@gmail.com")
        st.subheader("Github")
        st.write("https://github.com/Shiva-kalyanaram")
        st.balloons()


if __name__ == "__main__":
    main()

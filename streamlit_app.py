# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
from snowflake.snowpark import Session
import requests

# Write directly to the app
st.title(f":cup_with_straw: Customize your smoothie :cup_with_straw:")
st.write(
  """Choose the fruits you want in your smoothie!
  """
)

# Establish a connection
connection_parameters = {
    "account" : "CUVHUHC-NWB40835",
    "user" : "mm66sffb",
    "password" : "SnowflakeLearn!966",
    "role" : "SYSADMIN",
    "warehouse" : "COMPUTE_WH",
    "database" : "SMOOTHEIS",
    "schema" : "PUBLIC",
    "client_session_keep_alive" : True    
}

session = Session.builder.configs(connection_parameters).create()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'),col('search_on'))
pd_df=my_dataframe.to_pandas()
st.stop()
#st.dataframe(data=my_dataframe, use_container_width=True)
name_on_order=st.text_input('Name on order:')
st.write(f"The name of smoothie will be {name_on_order}")
ingredients_list=st.multiselect(
    'Choose upto 5 ingrdients:',
    my_dataframe,
    max_selections = 5
)

if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)
    ingredients_string=""
    for fruit_choosen in ingredients_list:
        ingredients_string += fruit_choosen + ' '
        st.subheader(fruit_choosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
        sf_df=st.dataframe(smoothiefroot_response.json(),use_container_width=True)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """');"""
    st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'You Smoothie is ordered!, {name_on_order}',icon="✅")
    

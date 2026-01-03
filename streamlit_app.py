# Import python packages
import streamlit as st
import requests
import pandas as pd
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize your smoothie :cup_with_straw:")
st.write(
  """Choose the fruits you want in your smoothie!
  """
)
cnx=st.connection('snowflake')
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
#st.dataframe(data=my_dataframe, use_container_width=True)
name_on_order=st.text_input('Name on order:')
st.write(f"The name of smoothie will be {name_on_order}")
ingredients_list=st.multiselect(
    'Choose upto 5 ingrdients:',
    my_dataframe,
    max_selections = 5
)

if ingredients_list:
    st.write(ingredients_list)
    st.text(ingredients_list)
    ingredients_string=""
    for ingredient in ingredients_list:
        ingredients_string += ingredient + ' '
    st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """');"""
    st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'You Smoothie is ordered!, {name_on_order}',icon="✅")
    

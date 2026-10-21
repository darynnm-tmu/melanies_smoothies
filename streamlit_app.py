# Import python packages
import streamlit as st
import os
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write( 'The name on your Smoothie will be: ', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections = 5
    )


# process the selected ingredients
if ingredients_list:

    # combine the selected fruits into one string
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    # create the insert statement
    my_insert_stmt = """
        INSERT INTO SMOOTHIES.PUBLIC.ORDERS
        (INGREDIENTS, NAME_ON_ORDER)
        VALUES (?, ?)
    """

    # create the submit button
    time_to_insert = st.button('Submit Order')

    # insert the order into snowflake
    if time_to_insert:
        session.sql(
            my_insert_stmt,
            params=[ingredients_string.strip(), name_on_order]
        ).collect()

        st.success(
            f'Your Smoothie is ordered, {name_on_order}!',
            icon="✅"
        )

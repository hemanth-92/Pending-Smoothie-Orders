# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session

from snowflake.snowpark.functions import col,when_matched

# Write directly to the app
st.title(f":cup_with_straw: Pending Smoothie Order :cup_with_straw:")
st.write(
  """Orders that are to be filled
  """
)

# name_on_order = st.text_input("Name on Smoothie:")
# st.write("The name on the smoothie is", name_on_order)

session = get_active_session()
my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()
#st.dataframe(data=my_dataframe, use_container_width=True)


if my_dataframe:
# st.write(my_dataframe);
    editable_df = st.data_editor(my_dataframe)


    submitted = st.button('Submit')

    if submitted:
        st.success('Someone clicked the button', icon = '👍')

        og_dataset = session.table("smoothies.public.orders")
        edited_dataset = session.create_dataframe(editable_df)
        og_dataset.merge(edited_dataset
                         , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                         , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                        )

else:
    st.success('There is no pending orders right now', icon = '👍')








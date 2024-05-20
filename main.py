import streamlit as st
import langchain_helper

st.title("Restaurant Name and Food Items Generator")

cuisine = st.sidebar.selectbox("Pick a Cuisine", ("Italian", "Chinese", "Indian", "Mexican", "Thai", "French", "Japanese", "Mediterranean", "Greek", "Spanish"))
price_range = st.sidebar.slider("Select Price Range (in INR)", 5, 5000, (20, 500))

if cuisine:
    response = langchain_helper.generate_restaurant_name_and_items(cuisine)
    restaurant_names = response['restaurant_names']
    menu_items_responses = response['menu_items']

    st.header("Top Name Suggestions")
    for idx, entry in enumerate(menu_items_responses):
        if idx >= 1:  # Display top 2-3 names
            break
        st.subheader(entry['restaurant_name'])
        
        st.write("**Vegetarian Menu Items**")
        veg_items = entry['veg_menu_items'].strip().split(",")
        for item in veg_items[:10]:  # Limit to top 10 items
            st.write("-", item.strip())
        
        st.write("**Non-Vegetarian Menu Items**")
        non_veg_items = entry['non_veg_menu_items'].strip().split(",")
        for item in non_veg_items[:10]:  # Limit to top 10 items
            st.write("-", item.strip())
        
        st.write("**Chats**")
        chats_items = entry['chats_menu_items'].strip().split(",")
        for item in chats_items[:10]:  # Limit to top 10 items
            st.write("-", item.strip())

    st.write("**Price Range (in INR):**")
    st.write(f"{price_range[0]} - {price_range[1]} INR")








from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from secret_key import openapi_key

import os
os.environ['OPENAI_API_KEY'] = openapi_key

llm = OpenAI(temperature=0.7)

def generate_restaurant_name_and_items(cuisine):
    # Chain 1: Restaurant Name
    prompt_template_name = PromptTemplate(
        input_variables=['cuisine'],
        template="I want to open a restaurant for {cuisine} food. Suggest three fancy names for this."
    )

    name_chain = LLMChain(llm=llm, prompt=prompt_template_name, output_key="restaurant_names")

    # Chain 2: Menu Items for Vegetarian
    prompt_template_veg_items = PromptTemplate(
        input_variables=['restaurant_name'],
        template="Suggest some vegetarian menu items for {restaurant_name}. Return it as a comma separated string."
    )

    veg_items_chain = LLMChain(llm=llm, prompt=prompt_template_veg_items, output_key="veg_menu_items")

    # Chain 3: Menu Items for Non-Vegetarian
    prompt_template_non_veg_items = PromptTemplate(
        input_variables=['restaurant_name'],
        template="Suggest some non-vegetarian menu items for {restaurant_name}. Return it as a comma separated string."
    )

    non_veg_items_chain = LLMChain(llm=llm, prompt=prompt_template_non_veg_items, output_key="non_veg_menu_items")

    # Chain 4: Menu Items for Chats
    prompt_template_chats_items = PromptTemplate(
        input_variables=['restaurant_name'],
        template="Suggest some chat items for {restaurant_name}. Return it as a comma separated string."
    )

    chats_items_chain = LLMChain(llm=llm, prompt=prompt_template_chats_items, output_key="chats_menu_items")

    def process_names_and_items(response):
        restaurant_names = response['restaurant_names'].strip().split("\n")
        menu_items_responses = []
        for name in restaurant_names:
            veg_response = veg_items_chain({'restaurant_name': name.strip()})
            non_veg_response = non_veg_items_chain({'restaurant_name': name.strip()})
            chats_response = chats_items_chain({'restaurant_name': name.strip()})
            menu_items_responses.append({
                'restaurant_name': name.strip(),
                'veg_menu_items': veg_response['veg_menu_items'],
                'non_veg_menu_items': non_veg_response['non_veg_menu_items'],
                'chats_menu_items': chats_response['chats_menu_items']
            })
        return {'restaurant_names': restaurant_names, 'menu_items': menu_items_responses}

    chain = SequentialChain(
        chains=[name_chain],
        input_variables=['cuisine'],
        output_variables=['restaurant_names']
    )

    response = chain({'cuisine': cuisine})
    final_response = process_names_and_items(response)

    return final_response

if __name__ == "__main__":
    print(generate_restaurant_name_and_items("Italian"))



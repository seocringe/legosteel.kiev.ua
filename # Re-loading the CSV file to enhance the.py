import pandas as pd
# Re-loading the CSV file to enhance the prompts with more organically incorporated product characteristics
csv_file_path = "/home/ars/downloads/legosteel.prom.ua - main - legosteel_with_turgenev_and_characteristics_prompts.csv"
df_products = pd.read_csv(csv_file_path)

# Identifying columns related to product characteristics
characteristics_columns = [col for col in df_products.columns if 'Название_Характеристики' in col or 'Значение_Характеристики' in col]

# Enhancing prompts with more organically incorporated product characteristics
for index, row in df_products.iterrows():
    # Constructing a more organic string of product characteristics
    characteristics_str = ', '.join([
        f"{row[char_col]}: {row['Значение_' + char_col.split('_')[1]]}" 
        for char_col in characteristics_columns if pd.notna(row[char_col]) and row[char_col] != row['Значение_' + char_col.split('_')[1]]
    ])

    # Updating the prompt to include characteristics more organically
    enhanced_prompt = (
        f"Создайте текст от лица компании «ЛегоСталь», специализирующейся на производстве изделий из нержавеющей стали. "
        f"Фокусируйтесь на продукте '{row['Название_позиции']}', избегая частого повторения слов и избыточного использования ключевых слов. "
        "Осветите функциональные особенности и преимущества продукта, используя естественные ключевые фразы длиной от трех слов. "
        "Стиль должен быть уникальным и нешаблонным, с акцентом на качественное и информативное содержание. "
        f"Убедитесь, что плотность ключевых слов и стилистических проблем не превышает установленных пределов. "
        f"Характеристики продукта включают: {characteristics_str}."
    )

    # Updating the dataframe
    df_products.at[index, 'Название_позиции'] = enhanced_prompt

# Saving the updated dataframe to a new CSV file
updated_csv_file_path = '/home/ars/gh/legosteel.kiev.ua/enhanced_prompts.csv'
df_products.to_csv(updated_csv_file_path, index=False)

updated_csv_file_path

import pandas as pd
import json

def extract_articles_correctly(row):
    try:
        # Parse the JSON in the 'Prompt' column
        data = json.loads(row['Prompt'])

        # Extract contents that start with "Article Number"
        articles = []
        for item in data:
            content = item.get('content', '')
            if content.startswith("Article Number"):
                # Remove the title "Article Number X\n\n" and add to articles list
                article_content = content.split('\n\n', 1)[1] if '\n\n' in content else content
                articles.append(article_content)
        return json.dumps(articles)
    except:
        # Return NaN in case of any error or if 'Prompt' is not a valid JSON
        return pd.NA

df = pd.read_excel(".data/testsets/Comm100.xlsx")

# Apply the corrected function to each row in the dataframe
df['Context'] = df.apply(extract_articles_correctly, axis=1)

# Display the first few rows of the updated dataframe
df.to_excel(".data/testsets/Comm100.xlsx", index=False)

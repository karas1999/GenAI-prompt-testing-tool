import pandas as pd
import json

class Case:
    """
    A class to represent a single case.
    'Context' is a list of strings, and 'History' is a list of dictionaries.
    """
    def __init__(self, id, source, source_url, question, expected_answer, confidence, context_str, history_str):
        self.id = id
        self.source = source
        self.source_url = source_url
        self.question = question
        self.expected_answer = expected_answer
        self.confidence = confidence
        self.context = self._parse_json_list(context_str)
        self.history = self._parse_json_list(history_str)

    def _parse_json_list(self, json_str):
        """
        Parse a JSON string into a Python list. If the string is not a valid JSON list,
        return it as a single-item list.
        """
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            return [json_str]

    def __repr__(self):
        return f"Case(ID={self.id}, Source={self.source})"


class Testset:
    """
    A class to represent a collection of test cases.
    """
    def __init__(self, file_path):
        self.cases = self._load_cases_from_excel(file_path)

    def _load_cases_from_excel(self, file_path):
        # Read the Excel file
        data = pd.read_excel(file_path)
        cases = []

        # Create a Case object for each row in the file
        for _, row in data.iterrows():
            case = Case(row['ID'], row['Source'], row['Source URL'], row['Question'], 
                        row['Expected Answer'], row['Confidence'], row['Context'], row['History'])
            cases.append(case)

        return cases

    def __repr__(self):
        return f"Cases={len(self.cases)})"


# Example of creating a Testset instance
# testset = Testset("My Testset", file_path)
# testset  # Displaying the created testset instance for demonstration

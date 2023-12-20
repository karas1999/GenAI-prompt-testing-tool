import os
import pandas as pd
import importlib.util
import asyncio
import yaml
from tqdm.asyncio import tqdm
from Testset import Testset


def get_prompt_function(prompt_file_path):
    # Load the external function from the provided Python file
    spec = importlib.util.spec_from_file_location("external_module", prompt_file_path)
    external_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(external_module)
    
    if not hasattr(external_module, 'run_test'):
        raise ValueError("The provided prompt file does not contain a 'run_test' function.")

    # Process the Testset with the external function
    prompt_function = external_module.run_test
    return prompt_function


async def run_testset(test_name, testset, run_test, output_path):
    results = []

    # Create an asynchronous task for each case
    tasks = [run_test(case) for case in testset.cases]

    # Initialize tqdm progress bar
    pbar = tqdm(total=len(tasks), desc=f"Processing {test_name} Cases")

    # Process three tasks concurrently using asyncio.gather
    for i in range(0, len(tasks), 3):
        batch = tasks[i:i+3]
        batch_results = await asyncio.gather(*batch)
        results += batch_results
        pbar.update(len(batch_results))

    pbar.close()

    df = pd.DataFrame(results)

    output_file_path = f'{output_path}/{test_name}.xlsx'

    df.to_excel(output_file_path, index=False)
    print("Excel file created at:", output_file_path)


async def main():
  
    # Prompt for YAML configuration file
    config_file_path = input("Enter the path to the YAML configuration file: ")

    # Load the YAML configuration file
    with open(config_file_path, 'r') as file:
        config = yaml.safe_load(file)

    output_path = os.path.dirname(config_file_path)

    for test_config in config['tests']:
        test_name = test_config['test_name']
        testset_file_path = test_config['testset_file_path']
        prompt_file_path = test_config['prompt_file_path']

        testset = Testset(testset_file_path)
        run_test = get_prompt_function(prompt_file_path)

        await run_testset(test_name, testset, run_test, output_path)

# Run the main coroutine
asyncio.run(main())
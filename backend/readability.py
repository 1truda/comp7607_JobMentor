import json
import os
import subprocess
from tqdm import tqdm
from argparse import ArgumentParser

from utils import call_gpt
from prompts import PROMPT_CRITIQUE, PROMPT_FIX

ROUNDS = 1


def get_flask8_score(code: str) -> float:
    try:
        result = subprocess.run(
            ['flake8', '--stdin-display-name', 'stdin', '-'],
            input=code,
            capture_output=True, text=True
        )
        errors = result.stdout.splitlines()
        score = max(0.0, 10.0 - len(errors) * 0.1)
        return score, errors
    except Exception as e:
        print(f"Flake8 error: {e}")
    return 0.0, []


def main():
    # parser = ArgumentParser()
    # user_problem_description = input("Please describe the coding problem you want to solve: ")
    user_problem_description = os.environ.get("PROBLEM_DESCRIPTION", "")
    if not user_problem_description:
        raise ValueError("No problem description provided.")
    initial_prompt = f"""
    You are a programming assistant. Please generate Python code to solve the following problem:

    {user_problem_description}

    Provide a complete Python function or script to solve this problem.
    """.strip()

    initial_code = call_gpt(initial_prompt, temperature=0.0)[0]

    print("code has been initialized")
    rounds = []
    code = initial_code.replace('\n\n', '\n')
    for round_number in tqdm(range(ROUNDS)):
        # Step 1: Generate critique for improving code readability
        prompt = PROMPT_CRITIQUE.format(code=code)
        suggestion = call_gpt(prompt, temperature=0.0)[0]

        # Step 2: Apply the suggested improvement to the code
        suggestion += "\n\nPlease Use # as a code interpreter instead of the ''' "
        prompt = PROMPT_FIX.format(code=code, suggestion=suggestion)
        code = call_gpt(prompt)[0].strip()

        # Step 3: Record the improvement
        rounds.append({'suggestion': suggestion, 'updated_code': code})

        # Step 4: Run flake8 to get readability score and errors
        flask8_score, flask8_errors = get_flask8_score(code)
        if flask8_errors:
            error_suggestions = "\n".join(flask8_errors)
            error_suggestions += "\n\nPlease generate the modified code and explain why"
            prompt = PROMPT_FIX.format(code=code, suggestion=error_suggestions)
            code = call_gpt(prompt)[0].strip()
            flask8_score, _ = get_flask8_score(code)
            print(f"Flake8 Score: {flask8_score}")

    output_data = {
        'original_description': user_problem_description,
        'code': code,
    }

    final_code_filename = 'final_code.json'
    with open(final_code_filename, 'w') as f:
        f.write(json.dumps(output_data) + '\n')

    print(f"Final generated code has been saved to {final_code_filename}")


if __name__ == '__main__':
    main()



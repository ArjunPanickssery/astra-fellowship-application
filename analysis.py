import os
import requests
from dotenv import load_dotenv
import json
from itertools import product
from strings import PROMPT_TEMPLATE, TASK_TEMPLATE, RULE_ARTICULATION_TEMPLATE, IDEAS

load_dotenv()


URL = "https://api.anthropic.com/v1/complete"
headers = {
    "accept": "application/json",
    "anthropic-version": "2023-06-01",
    "content-type": "application/json",
    "x-api-key": os.getenv("CLAUDE_API_KEY"),
}


def claude_response(human_input: str, max_tokens: int = 100, temp=0) -> str:
    data = {
        "model": "claude-2",
        "prompt": f"\n\nHuman: {human_input.strip()}\n\nAssistant: ",
        "max_tokens_to_sample": max_tokens,
        "temperature": temp,
    }

    response = requests.post(URL, headers=headers, json=data)
    response_json = response.json()
    return response_json["completion"].strip()


def generate_sentences(rules):
    res = {}
    for rule in rules:
        res[rule] = claude_response(
            PROMPT_TEMPLATE.format(rule=rule), max_tokens=400, temp=0.5
        )

    return res


def raw_sentences_to_task_json(
    raw_data_filename="raw_data.txt", output_filename="tasks.json"
):
    with open(raw_data_filename, encoding="utf8") as f:
        lines = f.read().split("\n")

    tasks = []
    for i in range(0, len(lines), 21):
        task = {
            "rule": f"Label the sentence A iff it {lines[i]}",
            "A": [s[s.find(".") + 2 :] for s in lines[i + 1 : i + 11]],
            "B": [s[s.find(".") + 2 :] for s in lines[i + 11 : i + 21]],
        }
        tasks.append(task)

    with open(output_filename, "w") as f:
        f.write(json.dumps(tasks, indent=4))

    return tasks


def get_performance_data(
    task_filename="tasks.json", output_filename="performance.json"
):
    with open(task_filename, "r") as f:
        tasks = json.load(f)

    perf = []
    for task in tasks:
        rule = task["rule"]
        a_responses = []
        b_responses = []

        for a_ex, b_ex in product(task["A"], task["B"]):
            a_examples = [x for x in task["A"] if x != a_ex]
            b_examples = [x for x in task["B"] if x != b_ex]

            a_prompt = TASK_TEMPLATE.format(
                a_sentences="\n- ".join(a_examples),
                b_sentences="\n- ".join(b_examples),
                test_sentence=a_ex,
            )
            b_prompt = TASK_TEMPLATE.format(
                a_sentences="\n- ".join(a_examples),
                b_sentences="\n- ".join(b_examples),
                test_sentence=b_ex,
            )

            a_responses.append(claude_response(a_prompt, max_tokens=50))
            b_responses.append(claude_response(b_prompt, max_tokens=50))

            rule_articulation_prompt = RULE_ARTICULATION_TEMPLATE.format(
                a_sentences="\n- ".join(task["A"]),
                b_sentences="\n- ".join(task["B"]),
            )

            perf.append(
                {
                    "rule": rule,
                    "score": (
                        sum([x == "A" for x in a_responses[rule]])
                        + sum([x == "B" for x in b_responses[rule]])
                    )
                    / 2,
                    "guess": claude_response(rule_articulation_prompt, max_tokens=100),
                }
            )

    perf = sorted(perf, key=lambda i: i["score"], reverse=True)

    with open(output_filename, "w") as f:
        f.write(json.dumps(perf, indent=4))

    return perf


ideas = list(filter(None, IDEAS.split("\n")))

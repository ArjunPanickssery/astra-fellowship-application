PROMPT_TEMPLATE = """As an expert, you've been assigned to help me design examples of realistic sentences that fit or don't fit a given rule. For example, if the rule was 'contains a number' you might generate these 10 examples that fit the rule:

1. There were 500 people at the concert.
2. I need to pick up 8 apples from the store today.
3. The race lasts 26.2 miles.
4. She scored 9 goals this season already.
5. They lived on the 14th floor of the building.
6. The recipe requires 4 eggs, 2 cups of flour, and a pint of milk.
7. The race is 26.2 miles long and has 7 big hills to climb.
8. By the age of 16, she had already written 9 amazing songs.
9. There were 500 enthusiastic fans cheering at the concert.
10. My favorite baseball player hit 63 home runs in a single season to set the record.

And these 10 that don't:
1. Many young children were playing at the neighborhood park.
2. I need some fruit from the grocery store to make a nice salad.
3. She completed the marathon in record time for herself.
4. The office building was very busy on Monday.
5. Their apartment had a nice view of the city.
6. Baking requires ingredients like eggs, flour and milk.
7. Don't forget!
8. She was a talented songwriter even as a teenager.
9. A huge crowd attended the sold out concert.
10. He was one of the best power hitters in baseball ever.

Make sure that the sentences are realistic and varied and that they cover all the relevant cases.

Start by generating 10 examples that fit the rule "{rule}" and 10 examples that fail to fit the rule."""


TASK_TEMPLATE = """Your Task: Sentences are correctly labeled A or B according to a hidden rule.

Examples of sentences that should be labeled A:
- {a_sentences}

Examples of sentences that should be labeled B:
- {b_sentences}

Classify the following sentence according to the rule (return only A or B without any other text):
{test_sentence}"""


RULE_ARTICULATION_TEMPLATE = """Your Task: Sentences are correctly labeled A or B according to a hidden rule.

Examples of sentences that should be labeled A:
- {a_sentences}

Examples of sentences that should be labeled B:
- {b_sentences}

Articulate the rule (return only the rule without any other text)."""

ideas = """contains a number
contains an adjective
contains quotation marks
contains the word not

contains a city name
contains a French word or phrase 
contains a palindrome word
references a sport
describes something using a color

has more than 10 words
has fewer than 5 words
contains a long (10-letter or longer) word
contains alliteration (first letter is the same for 3 consecutive words)
is entirely in uppercase
ends in a period

is a question
is in first-person
is in the past-tense
is in the imperative mood
ends with a preposition

is made up of two rhyming components
is in iambic pentameter
contains an arithmetic mistake
contains a geographical inaccuracy
is a famous movie quote"""

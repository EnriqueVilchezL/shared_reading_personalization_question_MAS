from shared_reading_mas.domain.evaluation_aggregate.category import Category

COMPLETION_TYPE = Category(
    type="C: Completion",
    description="**Questions** which answer is a single word that is present in the section of the story.",
    indicators=[
        "The questions have a single correct answer.",
        "**The response MUST BE a single word of the page**. The answer should be extremely easy to identify for a child who has read the page.",
        "The questions must be about **concrete vocabulary words**.",
        "**These questions must not require the child to make inferences, interpretations, or confusing connections. The answer should be explicitly stated in the story**.",
        "The answers must only be nouns or infinitive verbs relevant on the section of the story.",
        "The cognitive demand is primarily recognition of specific words to boost vocabulary learning.",
        "Example: What was the name of the dog?",
    ],
    importance=None,
)


DISTANCING_TYPE = Category(
    type="D: Distancing",
    description="**Questions** that invite the child to connect the story's events, characters, or themes to their own experiences or real-world knowledge.",
    indicators=[
        "The questions explicitly ask the child to relate the story to their personal life.",
        "The response requires personal experience, opinion, or reflection rather than story recall.",
        "The questions encourages the child to describe feelings, thoughts, or similar experiences.",
        "The discussion extends beyond the immediate content of the book.",
        "The cognitive demand involves transferring story meaning to real-life contexts.",
        "Example: Have you ever felt scared like the girl?",
    ],
    importance=None,
)

OPEN_ENDED_TYPE = Category(
    type="O: Open-ended Questions",
    description="**Questions** that allow multiple possible responses and encourage the child to describe, interpret, or elaborate on the story. If the story has images, the questions should also encourage the child to describe or interpret the images.",
    indicators=[
        "If the question is about the content of an image and the answer is not in the text, start the question specifying to look at the image.",
        "The questions do not have a single correct answer.",
        "The expected response is longer than one word.",
        "The questions invite description of actions, scenes, or characters.",
        "The child is encouraged to elaborate or expand on their ideas.",
        "The cognitive demand involves interpretation or explanation rather than simple recall.",
        "Example: Why do you think the fox made that decision?",
    ],
    importance=None,
)


RECALL_TYPE = Category(
    type="R: Recall",
    description="**Questions** that ask the child to remember specific events, details, or sequences from the story.",
    indicators=[
        "The questions refer to events or details that already occurred in the story.",
        "The expected response involves recalling factual information.",
        "The questions support sequencing or retelling of events.",
        "The questions check understanding of plot details.",
        "**These questions must not require the child to make inferences, interpretations, or confusing connections. The answer should be explicitly stated in the story**.",
        "The cognitive demand is primarily memory retrieval.",
        "Example: Who helped the boy fix the boat?",
    ],
    importance=None,
)


WH_TYPE = Category(
    type="W: Wh-questions",
    description="**Questions** framed as who, what, where, when, why, or how questions that target specific elements of the story. If the story has images, the questions should also encourage the child to describe or interpret the images.",
    indicators=[
        "If the question is about the content of an image the answer is not in the text, start the question specifying to look at the image."
        "The questions begin with who, what, where, when, why, or how.",
        "The expected response identifies characters, settings, actions, or reasons.",
        "The questions direct attention to explicit information in the text.",
        "The questions reinforce vocabulary from the story.",
        "**These questions must not require the child to make inferences, interpretations, or confusing connections. The answer should be explicitly stated in the story**.",
        "The cognitive demand focuses on comprehension of specific story elements.",
        "Example: Why did the farmer wake up early?",
    ],
    importance=None,
)

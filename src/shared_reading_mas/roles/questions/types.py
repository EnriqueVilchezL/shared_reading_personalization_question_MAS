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
    description="Questions focused on the story's images that allow multiple possible responses and encourage the child to observe, interpret, and describe what is happening visually in the scenes.",
    indicators=[
        "The questions are grounded in the images and visual elements of the story.",
        "There is no single correct answer.",
        "The expected response goes beyond one word and may include detailed description.",
        "The questions prompt the child to describe what they see in the images (actions, characters, settings, expressions, or events).",
        "The child is encouraged to interpret visual cues and expand on what is depicted.",
        "The cognitive demand focuses on interpretation and explanation of images rather than simple recall.",
        "Example: What is the dog doing in the image?",
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
    description="**Questions** framed as who, what, where, when, why, or how questions that target specific elements of the story's **images (visual content)**.",
    indicators=[
        "The questions begin with who, what, where, when, why, or how.",
        "The expected response identifies characters, settings, actions, or reasons as shown in the images.",
        "The questions direct attention to explicit information in the text and the **visual images in the story**.",
        "The questions reinforce vocabulary from the story",
        "**These questions must not require the child to make inferences, interpretations, or confusing connections. The answer should be explicitly stated in the story or clearly visible in the images.**",
        "The cognitive demand focuses on comprehension of specific story elements presented in both text and images.",
        "Example: What is the kid holding?",
    ],
    importance=None,
)

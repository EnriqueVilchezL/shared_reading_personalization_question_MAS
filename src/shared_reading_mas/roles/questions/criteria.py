from shared_reading_mas.domain.evaluation_aggregate.category import Category

CONTEXT_CRITERIA = Category(
    type="Context",
    description="Evaluates whether each intervention is explicitly and coherently anchored to the precise narrative context of the specific story page in which it appears. The intervention must clearly reflect the particular events, characters, emotions, and setting currently unfolding in the story. It should feel like a natural and seamless extension of that exact moment in the narrative, reinforcing the internal logic of the story world without introducing elements that belong to a different scene, contradict previously established information, or disrupt the reader’s immersion.",
    indicators=[
        "**Contextual Relevance:** The intervention must be directly and unmistakably connected to the events, characters, or setting presented on that specific story page. It should build upon what is currently happening rather than introducing unrelated ideas, future events, or external references that could confuse the child or weaken narrative focus.",
        "**Narrative Continuity:** The intervention must preserve the logical, causal, and temporal flow of the narrative. It should respect the established sequence of events and avoid contradictions, abrupt transitions, or inconsistencies in character behavior, motivations, or knowledge. The progression of the story should remain smooth and developmentally appropriate.",
        "**Consistency with Story Elements:** The intervention must remain fully aligned with the established characters, settings, tone, and themes of the story. References to previously introduced elements should be accurate and coherent, ensuring that no traits, story facts, or narrative rules are contradicted or unintentionally altered."
    ],
    importance="extremely high",
)

LIGUISTIC_CRITERIA = Category(
    type="Linguistic quality",
    description="Assesses the overall clarity, grammatical correctness, vocabulary suitability, and read-aloud quality of the intervention. The language must be fully accurate, developmentally appropriate, and specifically tailored for children aged 3 to 5 years. It should promote comprehension, support oral storytelling, and encourage enjoyment, striking a careful balance between simplicity and expressive richness while remaining accessible and engaging for early childhood audiences.",
    indicators=[
        "**Grammatical Correctness:** The intervention must be free from grammatical, syntactic, or punctuation errors. Sentences should be clearly structured, concise, and easy to follow, ensuring that the text can be read aloud smoothly without ambiguity or confusion for young listeners.",
        "**Vocabulary Appropriateness:** The vocabulary must be carefully selected to match the cognitive and linguistic development of children aged 3 to 5. Words should be concrete, familiar, and meaningful, while still allowing for gentle language enrichment. The text should avoid complex abstractions or overly sophisticated terminology, as well as language that is unnecessarily simplistic or repetitive.",
        "**Orality and Flow:** The intervention should demonstrate a natural rhythm, pleasing cadence, and strong read-aloud quality characteristic of effective children’s literature. Sentence length, sound patterns, and phrasing should support expressive storytelling and maintain the attention of young listeners, encouraging repeated readings and active listening."
    ],
    importance="very high",
)

INTERACTIVITY_CRITERIA = Category(
    type="Interactivity",
    description="Evaluates the degree to which the intervention actively encourages meaningful child participation in the storytelling experience. Rather than functioning purely as descriptive narration, it should intentionally create opportunities for the child to think, imagine, respond, predict, observe, or emotionally connect with the events and characters. The intervention should transform the reading moment into an interactive exchange that strengthens engagement, curiosity, and personal involvement in the story.",
    indicators=[
        "**Encouragement of Child's Response:** The intervention should explicitly invite the child to respond through open-ended questions, simple choices, prompts to predict what might happen next, or invitations to describe observations and feelings. It should clearly create space for participation instead of positioning the child as a passive listener.",
        "**Cognitive Engagement:** The intervention should stimulate thinking and curiosity by prompting the child to make connections, notice details, infer emotions, or reflect on character actions. It should support age-appropriate reasoning and imaginative engagement without overwhelming the child’s developmental level.",
        "**Emotional Engagement:** The intervention should intentionally evoke emotional responses such as excitement, empathy, anticipation, or joy. It should help the child feel connected to the characters and invested in the story’s unfolding events, strengthening both attention and meaningful participation."
    ],
    importance="very high",
)

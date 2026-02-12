from domain.evaluation_aggregate.criteria import Criteria

COHERENCE_CRITERIA = Criteria(
    type="coherence",
    description="Evaluates the logical flow and narrative consistency of the personalized story. The integration of personalization should not disrupt the plot, create inconsistencies, or introduce unexplained elements. A clear beginning, middle, and end are essential, with cause-and-effect relationships maintained throughout. There should be no contradictions or deviations from a natural narrative.",
    indicators=[
        "**Clear Narrative Structure (Beginning, Middle, End):** The story exhibits a well-defined beginning that introduces the setting and characters, a logical middle that develops the plot and conflict, and a satisfying end that resolves the conflict. The personalization should not disrupt this structure.",
        "**Logical Cause-and-Effect Sequence:** Events in the story follow a clear cause-and-effect relationship. The personalization should integrate seamlessly into this sequence; changes introduced by the AI should not break the flow of events or create illogical jumps. Consider: if the original story had a conflict and resolution, does the personalization maintain that same logical progression?",
        "**Absence of Plot Contradictions and Loose Ends:** The story is free of internal contradictions and unanswered questions. All elements introduced, especially through personalization, are explained or have a clear purpose within the narrative. Ask yourself: 'Does this element feel naturally integrated, or does it raise questions about its origin or relevance?'",
    ],
    importance="extremely high",
)

EMOTION_CRITERIA = Criteria(
    type="emotional impact",
    description="Assesses the story's ability to engage and resonate with the child reader.  The personalization should foster a strong connection, making the child feel like a protagonist while maintaining literary quality and evoking positive emotional responses like enjoyment and focused attention.",
    indicators=[
        "**Positive Emotional Response:** The story would evoke positive emotional responses in the child, such as laughter, surprise, and focused attention during reading. This demonstrates engagement and enjoyment of the narrative.",
        "**Desire to Revisit:** The child would express a strong desire to reread the story or share it with others, indicating a lasting positive impression and personal connection. This suggests the story resonates with them beyond simply recognizing their name.",
        "**Comprehension and Engagement:** The child would demonstrate comprehension of the story's plot and characters, showing fascination and following the narrative with interest. They would react appropriately to emotional cues, laughing at humorous moments, showing concern during challenges, and celebrating the resolution.",
    ],
    importance="very high",
)

LINGUISTIC_CRITERIA = Criteria(
    type="linguistic quality",
    description="Evaluates the grammatical correctness, vocabulary appropriateness, and overall language quality of the personalized story. The personalization should maintain high linguistic standards, ensuring clarity, coherence, and engagement for the target age group.",
    indicators=[
        "**Grammatical Correctness:** The story should be free from grammatical errors, including proper sentence structure, punctuation, and syntax. The language used should be appropriate for the target age group, ensuring that it is both understandable and engaging for children.",
        "**Vocabulary Appropriateness:** The vocabulary used in the story should be suitable for the intended audience. It should neither be too complex nor too simplistic, striking a balance that challenges readers from 3 to 5 years, while still being accessible. The personalization should introduce new words in a context that aids comprehension.",
        "**Orality and Flow:** The personalized story should have a natural rhythm and flow that is characteristic of children's literature. It should read smoothly aloud, with a cadence that captures the attention of young listeners. The language should be lively and engaging, encouraging repeated readings and enjoyment.",
    ],
    importance="high",
)

MORAL_CRITERIA = Criteria(
    type="the moral",
    description="Determines whether the personalization respects and preserves the original story's core message, values, and intent. Changes should not contradict the lesson or ethical implications of the narrative, ensuring the story's fundamental takeaway remains intact.",
    indicators=[
        "**Central Message Preservation:** The core moral or lesson of the original story is clearly and consistently maintained throughout the personalized version. The story's primary takeaway remains the same, even with the inclusion of the child's name or details.",
        "**Ethical or Symbolic Meaning Integrity:** The ending of the personalized story preserves the original story's ethical or symbolic meaning.  The resolution still conveys the same important lesson or value, even if the specifics of *how* that lesson is learned are altered to include the child.",
        "**Logical Consistency and Original Intent:** The logic of the characters' actions and the original intent of the story are not distorted by the personalization. Changes should feel natural and contribute to the existing narrative flow, rather than altering the fundamental cause-and-effect relationships or the story's purpose. Avoid introducing elements that contradict the established character motivations or plot points.",
    ],
    importance="high",
)

NATURALNESS_CRITERIA = Criteria(
    type="naturalness",
    description="Measures how seamlessly personalized elements are integrated into the story. The personalization should feel organic and essential to the narrative, avoiding forced additions or artificial insertions. Personalized characters should have a functional role in the plot.",
    indicators=[
        "**Functional Role of Personalized Characters:** The personalized character actively participates in the plot and fulfills a clear purpose. They aren't just passively named, since they contribute to the story's progression, potentially helping to resolve the conflict or driving the narrative forward.",
        "**Narrative Logic and Consistency:** Modifications made to the story respect the established logic of the original narrative universe. The tone, character behaviors, and actions remain consistent with the new context. There are no jarring shifts in setting, plot, or character motivation.",
        "**Absence of Artificial Insertion:** Personalized elements are woven seamlessly into the story, avoiding obvious 'patches' or forced additions. The story doesn't *feel* like it was altered; it feels like a natural extension of the original. Look for phrases that 'desentone' (feel out of place) and assess if they can be reformulated for better integration.",
    ],
    importance="very high",
)

STYLE_CRITERIA = Criteria(
    type="style",
    description="Evaluates the consistency of narrative voice, language level, and literary style throughout the personalized story. The goal is a seamless integration of personalized content, ensuring the reader doesn't perceive shifts in how the story is told, including vocabulary, sentence structure, and tone.",
    indicators=[
        "**Consistent Linguistic Register and Vocabulary:** The personalized sections should maintain the same level of formality, complexity, and word choice as the original story. Avoid introducing vocabulary or phrasing that feels out of place or too advanced/simplistic for the target age group. Specifically check for changes in sentence structure and the prevalence of specific grammatical constructions.",
        "**Age-Appropriate Language and Tone:** Ensure the vocabulary and sentence structures used in the personalized content are suitable for the intended children's audience. Be vigilant for overly complex phrasing, adult idioms, or words children are unlikely to understand. The overall tone should remain consistent throughout the story.",
        "**Seamless Stylistic Integration:** There should be no noticeable breaks in the narrative style between the original text and the personalized additions. This includes rhythm of the sentences, descriptive language, and the overall 'feel' of the story. Identify any jarring transitions or inconsistencies in voice.",
    ],
    importance="medium",
)

VALUE_CRITERIA = Criteria(
    type="added narrative value",
    description="Assesses whether the personalization enhances the story beyond cosmetic changes, strengthening the connection with the child reader and demonstrating creative adaptation to their world. Meaningful integration and imaginative use of the child's details are key. Personalization should add real and meaningful changes to the narrative, not banal substitutions or additions.",
    indicators=[
        "**Meaningful Personalization and Creative Integration:** The personalization goes beyond simple substitution and demonstrates creative adaptation of the story to the reader's details. Changes feel thoughtfully integrated, not just 'filled in'. Consider whether the personalization adds a unique 'touch' or feels formulaic.",
        "**Enhanced Immersion and Emotional Connection:** The personalization demonstrably improves the reader's immersion in the story or strengthens their emotional connection to the characters or plot. It considers if the story feel *more* engaging because of the personalization",
        "**Imaginative Adaptation to Reader's World:** The story adapts elements to the reader's familiar environment or experiences in a creative and imaginative way. For example, a setting is changed to resemble the child's town or a character's hobby is incorporated into the plot.",
    ],
    importance="extremely high",
)

VERISIMILITUDE_CRITERIA = Criteria(
    type="verisimilitude",
    description="Evaluates the believability and plausibility of the personalized story. The personalization should maintain a sense of realism within the story's universe, ensuring that the events and character actions remain credible and consistent with the established world. The story should not introduce elements that feel out of place or break the suspension of disbelief.",
    indicators=[
        "**Consistency with Established World:** The personalized story maintains consistency with the established world of the original narrative. The events, character actions, and settings introduced through personalization should align with the rules and logic of the story's universe. Avoid introducing elements that feel out of place or contradict the original story's established norms.",
        "**Plausibility of Events and Character Actions:** The events and character actions in the personalized story should be plausible within the context of the narrative. The personalization should not introduce scenarios or behaviors that feel unrealistic or break the suspension of disbelief for the reader. Consider whether the personalized elements could logically occur within the story's world.",
        "**Maintaining Suspension of Disbelief:** The personalized story should maintain the reader's suspension of disbelief, allowing them to fully immerse themselves in the narrative. The personalization should enhance the story without introducing elements that feel jarring or disrupt the reader's engagement. Assess whether the personalized elements contribute to a seamless reading experience or if they create a sense of dissonance.",
    ],
    importance="high",
)

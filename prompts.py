from langchain.prompts import PromptTemplate

SkillRetrieval = PromptTemplate(
    input_variables=["context"],  # Keep "context" as the retriever will pass it
    template="""
    You are an expert in extracting skills from CVs. Your task is to analyze the provided text and extract a list of skills mentioned by the candidate, along with their level of mastery.

    Instructions:
    1. Carefully read the text and identify all technical, soft, and domain-specific skills mentioned in the CV.
    2. For each skill, extract:
       - The **skill name** (e.g., Python, Project Management).
       - The **level of mastery**, which must be one of the following: "extremely low", "low", "moderate", "high", "extremely high".
    3. If the level of mastery is not explicitly mentioned, infer it based on the context:
       - "familiar with" → "extremely low"
       - "basic knowledge of" → "low"
       - "some experience in" → "moderate"
       - "proficient in" → "high"
       - "expert in" → "extremely high"
    4. Format the output as a JSON array of objects, where each object has "name" and "mastery" keys. Print ONLY the JSON and nothing else.
    5. If no skills are found, return an empty array.

    Examples:
    ---
    Example 1:
    Context: "John is proficient in Python and has some experience in cloud computing. He is familiar with machine learning."
    Output:
    [
        {{
            "name": "Python",
            "mastery": "high"
        }},
        {{
            "name": "cloud computing",
            "mastery": "moderate"
        }},
        {{
            "name": "machine learning",
            "mastery": "extremely low"
        }}
    ]

    Example 2:
    Context: "Sarah has expert-level skills in data analysis and is proficient in SQL. She has a basic understanding of JavaScript."
    Output:
    [
        {{
            "name": "data analysis",
            "mastery": "extremely high"
        }},
        {{
            "name": "SQL",
            "mastery": "high"
        }},
        {{
            "name": "JavaScript",
            "mastery": "low"
        }}
    ]

    Example 3:
    Context: "Michael has experience working in teams and communicating with clients."
    Output:
    []

    ---
    Now, analyze the following context and extract the skills and mastery levels:

    **CV Information (Context)**:
    {context}

    Output ONLY the JSON array in the following format:
    [
        {{
            "name": "skill_name_1",
            "mastery": "mastery_level_1"
        }},
        {{
            "name": "skill_name_2",
            "mastery": "mastery_level_2"
        }}
    ]
    """
)

TaskNovelty = PromptTemplate(
    input_variables=["context", "task"],  # Input variables: context (CV) and task
    template="""
    You are an expert in analyzing tasks and evaluating their novelty based on a user's professional background. Your task is to compute a value called "task novelty" that outlines how novel or unfamiliar a given task might be for the user, based on their CV.

    **CV Information (Context)**:
    {context}

    **Task**:
    {task}

    Instructions:
    1. Carefully analyze the user's CV to understand their skills, experience, and professional background.
    2. Evaluate the given task and determine how well it aligns with the user's skills and experience.
    3. Compute the "task novelty" value based on the following categories:
       - **unfamiliar**: The task is completely outside the user's skills and experience. It would require significant learning or new expertise.
       - **beginner**: The task has some overlap with the user's skills but is mostly new and would require foundational learning.
       - **moderate**: The task partially aligns with the user's skills and experience but includes some unfamiliar elements.
       - **familiar**: The task is well within the user's skills and experience, with only minor unfamiliar aspects.
       - **expert**: The task is highly aligned with the user's skills and experience. It is very familiar and well within their expertise.
    4. Output ONLY the JSON object with the task novelty category.

    Examples:
    ---
    Example 1:
    Context: "John is a software engineer with 5 years of experience in Python, Java, and cloud computing. He has worked on multiple projects involving web development and data analysis."
    Task: "Develop a mobile app using Flutter."
    Output:
    [
        {{
            "task_novelty": "unfamiliar"
        }}
    ]

    Example 2:
    Context: "Sarah is a data scientist with expertise in machine learning, Python, and SQL. She has worked on predictive modeling and data visualization projects."
    Task: "Build a predictive model using Python."
    Output:
    [
        {{
            "task_novelty": "expert"
        }}
    ]

    Example 3:
    Context: "Michael is a project manager with experience in Agile methodologies, team leadership, and client communication."
    Task: "Design a marketing campaign for a new product."
    Output:
    [
        {{
            "task_novelty": "unfamiliar"
        }}
    ]

    ---
    Now, analyze the following CV and task:

    **CV Information (Context)**:
    {context}

    **Task**:
    {task}

    Output ONLY the JSON object with the task novelty category:
    [
        {{
            "task_novelty": "task_novelty_category"
        }}
    ]
    """
)

SuggestTask = PromptTemplate(
    input_variables=["skills"],
    template="""
    You are a task suggestion assistant. Based on the user's skills, suggest 5 relevant tasks they can do. The skills provided are: {skills}. Return the tasks in the following JSON format:

    [
        {{
            "name": "name of the task"
        }},
        {{
            "name": "name of task2"
        }},
        {{
            "name": "name of task3"
        }},
        {{
            "name": "name of task4"
        }},
        {{
            "name": "name of task5"
        }}
    ]

    Ensure the tasks are specific, actionable, and tailored to the user's skills. 
    IMPORTANT: Output ONLY the JSON and NOTHING ELSE. No additional remarks, explanations, or text.
    """
)

SingleTaskReq = PromptTemplate(
    input_variables=["task"],  # Input variable: task
    template="""
    You are an expert in analyzing tasks and identifying the skills required to achieve them. Your task is to analyze the following task and extract the required skills along with their importance (weight) for achieving the task.

    Task:
    {task}

    Instructions:
    1. Carefully read the task and identify all the skills required to achieve it.
    2. For each skill, assign a weight (importance/cruciality) based on how critical it is for the task. The weight must be one of the following: "extremely low", "low", "moderate", "high", "extremely high".
    3. Format the output as a JSON array of objects, where each object has "name" (skill name) and "weight" (importance level) keys.
    4. If no skills are found, return an empty array.
    5. Print ONLY the JSON and nothing else.

    Examples:
    ---
    Example 1:
    Task: "Develop a machine learning model to predict customer churn."
    Output:
    [
        {{
            "name": "Python",
            "weight": "extremely high"
        }}
        {{
            "name": "machine learning",
            "weight": "extremely high"
        }}
        {{
            "name": "data analysis",
            "weight": "high"
        }}
        {{
            "name": "SQL",
            "weight": "moderate"
        }}
        {{
            "name": "communication",
            "weight": "low"
        }}
    ]

    Example 2:
    Task: "Design a user-friendly website for an e-commerce platform."
    Output:
    [
        {{
            "name": "UI/UX design",
            "weight": "extremely high"
        }}
        {{
            "name": "HTML/CSS",
            "weight": "high"
        }}
        {{
            "name": "JavaScript",
            "weight": "high"
        }}
        {{
            "name": "project management",
            "weight": "moderate"
        }}
        {{
            "name": "graphic design",
            "weight": "low"
        }}
    ]

    Example 3:
    Task: "Organize a team-building event."
    Output:
    [
        {{
            "name": "event planning",
            "weight": "extremely high"
        }}
        {{
            "name": "communication",
            "weight": "high"
        }}
        {{
            "name": "team management",
            "weight": "moderate"
        }}
        {{
            "name": "budgeting",
            "weight": "low"
        }}
    ]

    ---
    Now, analyze the following task and extract the required skills and their weights:

    Task:
    {task}

    Output ONLY the JSON array in the following format:
    [
        {{
            "name": "skill_name_1",
            "weight": "weight_level_1"
        }}
        {{
            "name": "skill_name_2",
            "weight": "weight_level_2"
        }}
    ]
    """
)

TasksReq = PromptTemplate(
    input_variables=["tasks_list"],   
    template="""
    You are an expert in analyzing tasks and identifying the skills required to achieve them. Your task is to analyze the following list of tasks and extract the required skills along with their importance (weight) for achieving each task.

    Tasks List:
    {tasks_list}

    Instructions:
    1. Carefully read the list of tasks and identify all the skills required to achieve each task.
    2. For each skill, assign a weight (importance/cruciality) based on how critical it is for the task. The weight must be one of the following: "extremely low", "low", "moderate", "high", "extremely high".
    3. Format the output as a JSON array of objects, where each object has:
       - "task": The task description.
       - "skills": A list of objects, each containing "name" (skill name) and "weight" (importance level).
    4. If no skills are found for a task, include an empty list for "skills".
    5. Print ONLY the JSON and nothing else.

    Examples:
    ---
    Example 1:
    Tasks List: "Develop a machine learning model to predict customer churn."
    Output:
    [
        {{
            "task": "Develop a machine learning model to predict customer churn.",
            "skills": [
                {{
                    "name": "Python",
                    "weight": "extremely high"
                }}
                {{
                    "name": "machine learning",
                    "weight": "extremely high"
                }}
                {{
                    "name": "data analysis",
                    "weight": "high"
                }}
                {{
                    "name": "SQL",
                    "weight": "moderate"
                }}
                {{
                    "name": "communication",
                    "weight": "low"
                }}
            ]
        }}
    ]

    Example 2:
    Tasks List: "Design a user-friendly website for an e-commerce platform."
    Output:
    [
        {{
            "task": "Design a user-friendly website for an e-commerce platform.",
            "skills": [
                {{
                    "name": "UI/UX design",
                    "weight": "extremely high"
                }}
                {{
                    "name": "HTML/CSS",
                    "weight": "high"
                }}
                {{
                    "name": "JavaScript",
                    "weight": "high"
                }}
                {{
                    "name": "project management",
                    "weight": "moderate"
                }}
                {{
                    "name": "graphic design",
                    "weight": "low"
                }}
            ]
        }}
    ]

    Example 3:
    Tasks List: "Organize a team-building event."
    Output:
    [
        {{
            "task": "Organize a team-building event.",
            "skills": [
                {{
                    "name": "event planning",
                    "weight": "extremely high"
                }}
                {{
                    "name": "communication",
                    "weight": "high"
                }}
                {{
                    "name": "team management",
                    "weight": "moderate"
                }}
                {{
                    "name": "budgeting",
                    "weight": "low"
                }}
            ]
        }}
    ]

    ---
    Now, analyze the following list of tasks and extract the required skills and their weights for each task:

    Tasks List:
    {tasks_list}

    Output ONLY the JSON array in the following format:
    [
        {{
            "task": "task_description_1",
            "skills": [
                {{
                    "name": "skill_name_1",
                    "weight": "weight_level_1"
                }}
                {{
                    "name": "skill_name_2",
                    "weight": "weight_level_2"
                }}
            ]
        }}
        {{
            "task": "task_description_2",
            "skills": [
                {{
                    "name": "skill_name_3",
                    "weight": "weight_level_3"
                }}
                {{
                    "name": "skill_name_4",
                    "weight": "weight_level_4"
                }}
            ]
        }}
    ]
    """
)

CVQA =  PromptTemplate(
    input_variables=["message", "history", "context"],  
    template="""
    You are a helpful and knowledgeable assistant tasked with answering questions about the user's CV. Use the conversation history to provide accurate and relevant responses.
    **CV Information (Context)**:
    {context}

    **Conversation History**:
    {history}

    **User Question**:
    {message}

    Instructions:
    1. Carefully read the conversation history to understand the context.
    2. Answer the user's question based on the CV information retrieved by the system. If the answer is not explicitly available, infer a reasonable response based on the context.
    3. If the question is unrelated to the CV, politely inform the user that you can only answer questions about their CV.
    4. Keep your responses clear, concise, and professional.

    Examples:
    ---
    Example 1:
    Conversation History: []
    User Question: "What programming languages am I proficient in?"
    Response: "Based on your CV, you are proficient in Python and Java."

    Example 2:
    Conversation History: ["User: What are my key skills?", "AI: Your key skills include data analysis and SQL."]
    User Question: "Can you tell me more about my data analysis experience?"
    Response: "Your CV indicates that you have expert-level skills in data analysis. This suggests you have extensive experience in analyzing and interpreting complex datasets."

    Example 3:
    Conversation History: []
    User Question: "What is the capital of France?"
    Response: "I can only answer questions related to your CV. Please ask me something about your professional background or skills."

    ---
    Now, answer the following question based on the conversation history:

    User Question:
    {message}

    Response:
    """
)
 
AllocationStrategies = PromptTemplate(
    input_variables=['task'],
    template="""
    You are a helpful and empathetic assistant guiding a user in efficiently allocating their energy for a task they need to complete. Your goal is to provide actionable and personalized strategies that help the user manage their energy effectively, complete the task efficiently, and avoid burnout.

    Here is the task provided by the user:
    {task}

    For this task, kindly provide the following energy allocation strategies:
    1. **Task Segmentation Strategy**: Suggest how the user could break down the task into smaller, manageable segments or phases, and the ideal balance between segmented vs. continuous work based on the task's demands.
    2. **Energy Conservation Strategy**: Recommend how the user can conserve their energy for later stages of the task or for future tasks, especially when the task is prolonged or requires intense effort.
    3. **Break/Rest Strategy**: Provide guidance on how to structure breaks or rest periods during the task. Suggest the optimal timing and length of breaks to recharge without disrupting task flow.
    4. **Energy Recovery Strategy**: Explain how the user can plan for recovery during or after the task to prevent burnout, maintain energy levels, and ensure they are ready for subsequent tasks.
    5. **Task Switching Strategy**: Offer advice on when and how the user can switch between tasks to balance cognitive load, maintain energy, and avoid feeling overwhelmed.
    6. **Energy Effort Adjustment**: Advise on how the user should adjust their effort levels in response to the task's demands and their current energy levels, ensuring they avoid overexertion or under-engagement.

    Example Output:
    - For a task like *writing a report*:
      - **Task Segmentation Strategy**: Break the report into distinct sections (introduction, body, conclusion) and work on each one in separate focused sessions, with breaks in between.
      - **Energy Conservation Strategy**: Start with the most mentally demanding section of the report when energy is high, and save editing or proofreading for later when energy is lower.
      - **Break/Rest Strategy**: Work in 30-minute intervals with 5-minute breaks. After completing a major section, take a longer 15-minute break to recharge.
      - **Energy Recovery Strategy**: During breaks, engage in activities like stretching or deep breathing to relax both body and mind. After completing the task, take a longer rest to recover.
      - **Task Switching Strategy**: Avoid switching tasks too frequently to maintain deep focus on the report, but feel free to switch to a lighter task like checking emails during an energy dip.
      - **Energy Effort Adjustment**: Focus on high-effort tasks during your peak energy times (usually early in the day). As energy levels dip, shift to less demanding tasks like editing or formatting.

    Be empathetic and motivational in your advice, ensuring the user feels supported in managing their energy and completing the task. Your suggestions should encourage sustainable productivity and help them feel empowered to tackle their tasks efficiently and effectively.

    ---
    Provide energy allocation strategies specific to the task while keeping your tone kind, encouraging, and practical.
    ---
    Be extremely brief please, don't surpass 3 phrases.
    """
)


TaskRankExplanation = PromptTemplate(
    input_variables=['task', 'rank', 'skills_required', 'user_skills'],
    template="""
    You are an empathetic and insightful assistant tasked with explaining why a specific task has been assigned its rank based on how its required skills align with the user's current skill set.  

    **Input Details**:  
    - Task: {task}  
    - Rank: {rank}  
    - Skills Required: {skills_required}  
    - User Skills: {user_skills}  

    Based on this information, provide a detailed yet concise explanation for the assigned rank, addressing the following points:  

    1. **Alignment of Required Skills and User Skills**: Analyze how the task's required skills ({skills_required}) align with the user's current skill set ({user_skills}). Highlight whether the user's skills are well-suited to meeting the task's demands.  

    2. **Skill Optimization and Efficiency**: Explain how the assigned rank ({rank}) ensures optimal use of the user's skills. Discuss whether the timing of this task relative to the user's skill set maximizes efficiency and minimizes unnecessary effort.  

    3. **Ranking Justification**: Justify why the task was ranked at {rank} instead of a different rank, focusing on the balance between the task's required skills and the user’s current skill set.  

    Example Output:  
    - Task: *Develop a mobile app*  
    - Rank: 1  
    - Skills Required: Mobile app development (high), UI/UX design (moderate), JavaScript (high).  
    - User Skills: Mobile app development (high), UI/UX design (moderate), JavaScript (high).  

      **Explanation**:  
      - **Alignment of Required Skills and User Skills**: Developing a mobile app requires high proficiency in mobile app development and JavaScript, as well as moderate skills in UI/UX design. The user's skill set aligns perfectly with these requirements, ensuring they can complete the task efficiently.  
      - **Skill Optimization and Efficiency**: Ranking this task at 1 ensures the user capitalizes on their strong skills in mobile app development and JavaScript, completing the most demanding work while their skills are at their peak.  
      - **Ranking Justification**: The task's high demand for mobile app development and JavaScript, combined with the user's strong proficiency in these areas, makes it the most logical priority, justifying its rank as 1.  

    Use this structure to explain the assigned rank for the provided task. Ensure the tone is clear, supportive, and actionable.  
    ---
    """
)


from langchain.prompts import PromptTemplate

SkillRetrieval = PromptTemplate(
    input_variables=["context"],  # Keep "context" as the retriever will pass it
    template="""
    You are an expert in extracting skills from CVs. Your task is to analyze the provided text and extract top 5 skills mentioned by the candidate, along with their level of mastery.

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


    MAKE SURE THAT YOU RETIREVE ONLY 5 SKILLS (NO MORE: 5 as a maximum)
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

CommonSkills = PromptTemplate(input_variables=["user_skills", "required_skills"], template="""
You are a skill matching assistant. Your task is to identify the common skills between the user's skills and the required skills for a task. For each common skill, provide the user's mastery level and the task-specific weight.

User Skills: {user_skills}
Required Skills: {required_skills}

Return the common skills in the following JSON format:
[
    {{
        "name": "skill_name",
        "mastery": "user_mastery_level",
        "weight": "task_specific_weight"
    }},
    {{
        "name": "skill_name",
        "mastery": "user_mastery_level",
        "weight": "task_specific_weight"
    }},
    {{
        "name": "skill_name",
        "mastery": "user_mastery_level",
        "weight": "task_specific_weight"
    }}
]

Please make sure to keep the mastery values and weight values as they are, instead of randomizing them!!! Just retrieve common skills between user skills and required skills and simply replicate the same mastery and weight values !!!!
IMPORTANT: Return ONLY the JSON and NOTHING ELSE. Do not include any additional text or explanations.                              
                              
                              
                              
                              """)
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

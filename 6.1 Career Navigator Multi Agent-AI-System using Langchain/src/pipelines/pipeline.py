from src.agents.agents import (
    build_job_search_agent,
    build_skill_extraction_agent,
    build_salary_agent,
    build_learning_agent,
    build_career_advisor_agent,
    career_report_chain
)


# ─────────────────────────────────────────────────────────────
# Run Complete Career Intelligence Pipeline
# This function orchestrates all agents and maintains
# shared state memory throughout the workflow.
# ─────────────────────────────────────────────────────────────


def run_career_pipeline(
    goal: str,
    location: str,
    years_of_experience: str,
    callback=None               #added callback parameter for progress updates
) -> dict:

    # Shared State Memory
    # Stores outputs from all agents

    state = {}

    if callback:                        #added
        callback(
            "🚀 Pipeline Started",
            0
        )

    # ────────────────────────────────────────────────
    # Step 1 - Job Search Agent
    # Searches live job opportunities using JSearch API
    # through the search_jobs tool.
    # ────────────────────────────────────────────────

    print("\n" + "=" * 50)
    print("Step 1 - Job Search Agent is working...")
    print("=" * 50)

    if callback:                                                #Added
        callback(
            "🔍 Job Search Agent Running",
            10
        )

    job_agent = build_job_search_agent()

    job_result = job_agent.invoke({
        "messages": [
            (
                "user",
                f"""
Find relevant job opportunities for the following career goal:

{goal}

Search for:
- Relevant job titles
- Hiring companies
- Job locations
- Salary information
- Apply URLs

Return the most relevant opportunities.
"""
            )
        ]
    })

    # Store job search results in state memory
    state["jobs"] = job_result["messages"][-1].content

    if callback:
        callback(                                           #Added
            "✅ Job Search Agent Completed",
            20
        )

    print("\nJobs Found:\n")
    print(state["jobs"])






    # ────────────────────────────────────────────────
    # Step 2 - Skill Extraction Agent
    # Extract skills from the most relevant job posting
    # found by Agent 1.
    # ────────────────────────────────────────────────

    print("\n" + "=" * 50)
    print("Step 2 - Skill Extraction Agent is working...")
    print("=" * 50)

    if callback:                                            #Added
        callback(
            "🧠 Skill Extraction Agent Running",
            30
        )

    skill_agent = build_skill_extraction_agent()

    skill_result = skill_agent.invoke({
        "messages": [
            (
                "user",
                f"""
    Based on the following job search results,
    identify the most relevant job posting URL.

    Use the extract_skills tool on that URL.

    Extract:

    - Technical Skills
    - Programming Languages
    - Tools & Technologies
    - Frameworks & Platforms
    - Cloud Platforms
    - Databases
    - AI / ML / GenAI Skills
    - Business Skills
    - Domain Knowledge
    - Certifications
    - Education Requirements
    - Experience Requirements
    - Soft Skills
    - Other Requirements

    Job Search Results:

    {state["jobs"][:2500]}
    """
            )
        ]
    })

    # Store extracted skills in shared state memory
    state["skills"] = skill_result["messages"][-1].content

    if callback:                                            #Added  
        callback(
            "✅ Skill Extraction Agent Completed",
            40
        )

    print("\nExtracted Skills:\n")
    print(state["skills"])






    # ────────────────────────────────────────────────
    # Step 3 - Salary Intelligence Agent
    # Analyze salary trends for the target role,
    # location and experience level.
    # ────────────────────────────────────────────────

    print("\n" + "=" * 50)
    print("Step 3 - Salary Intelligence Agent is working...")
    print("=" * 50)


    if callback:                                    #added
        callback(
            "💰 Salary Agent Running",
            50
        )

    salary_agent = build_salary_agent()

    salary_result = salary_agent.invoke({
        "messages": [
            (
                "user",
                f"""
    Use the salary_research tool.

    Job Title:
    {goal}

    Location:
    {location}

    Years Of Experience:
    {years_of_experience}

    Return salary intelligence only.
    """
            )
        ]
    })

    # Store salary insights in shared state memory
    state["salary"] = salary_result["messages"][-1].content

    if callback:
        callback(
            "✅ Salary Agent Completed",
            60
        )

    print("\nSalary Intelligence:\n")
    print(state["salary"])




    

    # ────────────────────────────────────────────────
    # Step 4 - Learning Roadmap Agent
    # Finds courses, certifications and learning
    # resources based on required skills.
    # ────────────────────────────────────────────────

    print("\n" + "=" * 50)
    print("Step 4 - Learning Roadmap Agent is working...")
    print("=" * 50)

    if callback:
        callback(
            "📚 Learning Agent Running",
            70
        )

    learning_agent = build_learning_agent()

    roadmap_result = learning_agent.invoke({
        "messages": [
            (
                "user",
                f"""
    Use the find_courses tool.

    Based on the following extracted skills:

    {state["skills"][:2000]}

    Find relevant learning resources and create a learning roadmap.

    Return:
    - Recommended Courses
    - Certifications
    - Learning Sequence
    - Learning Timeline
    - Practical Projects
    - Learning Resources
    - Key Recommendations
    """
            )
        ]
    })

    # Store roadmap in shared state memory
    state["roadmap"] = roadmap_result["messages"][-1].content

    if callback:                                        #Added
        callback(
            "✅ Learning Agent Completed",
            80
        )
    print("\nLearning Roadmap:\n")
    print(state["roadmap"])






    # ────────────────────────────────────────────────
    # Step 5 - Career Advisor Agent
    # Generates strategic career guidance.
    # ────────────────────────────────────────────────

    print("\n" + "=" * 50)
    print("Step 5 - Career Advisor Agent is working...")
    print("=" * 50)

    if callback:                                        #Added
        callback(
            "🎯 Career Advisor Running",
            85
        )

    career_agent = build_career_advisor_agent()

    career_result = career_agent.invoke({
        "messages": [
            (
                "user",
                f"""
Career Goal:
{goal}

Jobs:
{state['jobs']}

Skills:
{state['skills']}

Salary:
{state['salary']}

Roadmap:
{state['roadmap']}
"""
            )
        ]
    })

    state["career_advice"] = career_result["messages"][-1].content

    if callback:
        callback(                                                   #Added
            "✅ Career Advisor Completed",
            95
        )

    print("\nCareer Advice:\n")
    print(state["career_advice"])






    # ────────────────────────────────────────────────
    # Step 6 - Final Career Intelligence Report
    # LCEL Report Generator
    # ────────────────────────────────────────────────

    print("\n" + "=" * 50)
    print("Step 6 - Final Career Intelligence Report")
    print("=" * 50)

    final_report = career_report_chain.invoke(
        {
            "goal": goal,
            "jobs": state["jobs"][:2500],
            "skills": state["skills"][:2000],
            "salary": state["salary"][:2000],
            "roadmap": state["roadmap"][:1500],
            "career_advice": state["career_advice"][:2500]
        }
    )

    state["final_report"] = final_report

    if callback:                                                #Added
        callback(
            "🏆 Career Report Generated",
            100
        )

    print("\nFinal Career Intelligence Report:\n")
    print(state["final_report"])

    return state
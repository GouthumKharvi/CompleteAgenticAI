from src.pipelines.pipeline import run_career_pipeline
result = run_career_pipeline(
    goal="Generative AI Engineer",
    location="Bangalore",
    years_of_experience="ONE_TO_THREE"
)

print("\nFINAL REPORT\n")
print(result["final_report"])
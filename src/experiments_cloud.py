import subprocess

# ==============================
# Simplified Runner
# ==============================

def run_pipeline(command):
    """
    Executes the command directly without background threads 
    or resource tracking.
    """
    # Use subprocess.run for a cleaner, synchronous execution
    process = subprocess.run(command, shell=True)
    return process.returncode

# ==============================
# Personalization Pipeline Loop
# ==============================

def run_personalization(base_route: str):
    stories = [
        "caballero.md", "calendario.md", "cuaderno.md",
        "mensaje.md", "rana.md", "yi.md",
    ]
    profiles = ["boy.md", "girl.md"]

    for profile in profiles:
        for story in stories:
            run_name = f"{profile[:-3]}_{story[:-3]}"

            command = (
                f"uv run src/main.py "
                f"--story_path {base_route}/stories/{story} "
                f"--preferences_path {base_route}/profiles/{profile} "
                f"--pipelines PERSONALIZATION "
                f"--output_path outputs/personalization/{run_name}.md "
                f"--verbose"
            )

            print(f"\n--- Starting: {run_name} ---")
            run_pipeline(command)

def run_questions(base_route: str):
    stories = [
        "caballero.md", "calendario.md",
        "cuaderno.md",
        "mensaje.md", "rana.md", "yi.md"
    ]

    for story in stories:
        story_path = f"{base_route}/stories/{story}"
        run_name = f"questions_{story[:-3]}"

        command = (
            f"uv run src/main.py "
            f"--story_path {story_path} "
            f"--preferences_path {base_route}/profiles/girl.md "
            f"--pipelines QUESTIONS "
            f"--output_path outputs/questions/{run_name}.md "
            f"--verbose"
        )

        print(f"\nRunning command: {command}\n")

        run_pipeline(command)


# ==============================
# MAIN
# ==============================

def main():

    base_route = "data"
    run_personalization(base_route)
    run_questions(base_route)

if __name__ == "__main__":
    main()

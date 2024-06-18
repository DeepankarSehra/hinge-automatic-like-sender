import subprocess

def run_scripts():
    scripts = ['scripts/screenshot_separate.py', 'scripts/screenshot_joining.py', 'scripts/test2_usable_prompt_retreiver.py', 'scripts/profile_elements.py']

    for script in scripts:
        print(f"Running {script}")
        try:
            subprocess.run(['python', script], check=True)
            print(f'{script} run successfully')
        except:
            print(f'error running {script}')
            break

if __name__ == "__main__":
    run_scripts()
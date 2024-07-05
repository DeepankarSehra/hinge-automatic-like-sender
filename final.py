import subprocess

# Runs all the scripts in given order
def run_scripts():
    scripts = ['scripts/screenshot_separate.py', 'scripts/screenshot_joining.py', 'scripts/after_extract.py', 'scripts/cleanup.py']

    for script in scripts:
        print(f"Running {script}")
        try:
            subprocess.run(['python', script], check=True)
            print(f'{script} run successfully')
        except:
            print(f'error running {script}')
            break

if __name__ == "__main__":
    while(True):
        run_scripts()
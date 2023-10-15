from pyfiglet import figlet_format
from termcolor import colored
import inquirer
from inquirer import Text, Path

def ensure_directory_format(answers, current):
    if not current.endswith('/'):
        return current + '/'
    return current

def handle_pyproject_toml(user_config):
    config_template = '''[tool.autopytest]
source_directories=[{source_directories}]
test_directory="{test_directory}"
pytest_args=[{pytest_args}]
exclude_paths=[{exclude_paths}]
log_format="%(message)s"
log_level="ERROR"
telemetry="{telemetry}"
'''

    config_str = config_template.format(
        source_directories=','.join(f'"{dir}"' for dir in user_config['source_directories'].split(',')),
        test_directory=user_config['test_directory'],
        pytest_args=','.join(f'"{arg}"' for arg in user_config['pytest_args'].split(',')),
        exclude_paths=','.join(f'"{path}"' for path in user_config['exclude_paths'].split(',')),
        telemetry=user_config['telemetry']
    )

    path = "pyproject.toml"
    try:
        with open(path, 'r') as file:
            content = file.read()
            if '[tool.autopytest]' in content:
                start_index = content.index('[tool.autopytest]')
                end_index = content.find('\n[', start_index)
                end_index = len(content) if end_index == -1 else end_index
                content = content[:start_index] + config_str + content[end_index:]
            else:
                content += '\\n' + config_str
            with open(path, 'w') as file:
                file.write(content)
            return "Updated pyproject.toml with [tool.autopytest] configuration."
    except FileNotFoundError:
        with open(path, 'w') as file:
            file.write(config_str)
        return "Created pyproject.toml with [tool.autopytest] configuration."

def updated_prompt_user_configuration():
    questions = [
        inquirer.Text('source_directories', 
                      message="Enter source directories (comma separated, e.g., app,src)"),
        
        inquirer.Text('test_directory', 
             message="Enter the test directory (e.g., tests)"),
        
        inquirer.Text('pytest_args', 
                      message="Enter pytest arguments (comma separated, e.g., --verbose,--cov)"),
        
        inquirer.Text('exclude_paths', 
                      message="Enter paths to exclude (comma separated, e.g., app/__pycache__,build)"),

        inquirer.Confirm('telemetry',
            message="Do you consent to sending anonymous telemetry data (related to crashes and test success/failure rates)?",
            default=False),
    ]

    return inquirer.prompt(questions)

def init():
    print(colored(figlet_format('Autopytest Init', font='slant'), 'cyan'))

    user_config = updated_prompt_user_configuration()

    result_message = handle_pyproject_toml(user_config)
    print(colored(result_message, 'green'))
    
    if user_config['telemetry']:
        print(colored("Thank you! Anonymous telemetry data will be collected.", 'green'))
    else:
        print(colored("No telemetry data will be collected.", 'yellow'))

if __name__ == "__main__":
    init()

from urllib import request
from project import Project
import tomli
from urllib import request

class ProjectReader:
    def __init__(self, url):
        self._url = url

    def get_project(self):
        # Lue sisältö
        content = request.urlopen(self._url).read().decode("utf-8")
        toml_data = tomli.loads(content)
        project_data = toml_data.get("tool", {}).get("poetry", {})
        
        name = project_data.get("name", "N/A")
        description = project_data.get("description", "N/A")
        license = project_data.get("license", "N/A")
        authors = project_data.get("authors", [])

        
        dependencies = toml_data.get("tool", {}).get("poetry", {}).get("dependencies", {})
        dev_dependencies = toml_data.get("tool", {}).get("poetry", {}).get("group", {}).get("dev", {}).get("dependencies", {})

        print(f"Name: {name}")
        print(f"Description: {description}")
        print(f"License: {license}\n")

        print("Authors:")
        if authors:
            for author in authors:
                print(f"- {author}")
        else:
            print("- N/A")

        
        print("\nDependencies:")
        if dependencies:
            for dep in dependencies:
                print(f"- {dep}")
        else:
            print("- N/A")

        
        print("\nDevelopment dependencies:")
        if dev_dependencies:
            for dev_dep in dev_dependencies:
                print(f"- {dev_dep}")
        else:
            print("- N/A")

        
        return ""   
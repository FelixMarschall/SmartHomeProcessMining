from setuptools import setup, find_packages

setup(
    name = "proocess_management_smart_home",
    version = "1.0.0",
    author = "Felix Marschall",
    author_email = "felix.marschall@student.kit.edu",
    packages=find_packages(),
    install_requires=[
        "dash",
        "dash-bootstrap-components",
        "dash-core-components",
        "dash-html-components",
        "dash-renderer",
        "dash-table",
        "pm4py",
        "pandas",
        "plotly",
        "Pillow",
    ]
)
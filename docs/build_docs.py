import subprocess
import yaml
import os


def build_doc(version, tag):
    os.environ["current_version"] = version
    subprocess.run("git checkout " + tag, shell=True)
    subprocess.run("git checkout main -- conf.py", shell=True)
    subprocess.run("git checkout main -- versions.yml", shell=True)
    subprocess.run("make html", shell=True)


def move_dir(src, dst):
    subprocess.run(["mkdir", "-p", dst])
    subprocess.run("mv " + src + "* " + dst, shell=True)


os.environ["build_all_docs"] = str(True)
os.environ["pages_root"] = "https://gnzng.github.io/xaspy"

build_doc("latest", "main")
move_dir("./_build/html/", "../pages/")


with open("versions.yml", "r") as yaml_file:
    docs = yaml.safe_load(yaml_file)

for version, details in docs.items():
    tag = details.get("tag", "")
    build_doc(version, tag)
    move_dir("./_build/html/", "../pages/" + version + "/")

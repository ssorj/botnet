from plano import *

image_tag = "quay.io/ssorj/connectathon-sqldatabase"

@command
def build():
    run(f"gunzip --keep --force dvdrental.tar.gz")
    run(f"podman build -t {image_tag} .")

@command(name="run")
def run_():
    build()
    run(f"podman run --rm -p 5432:5432 {image_tag}")

@command
def push():
    build()
    run(f"podman push {image_tag}")

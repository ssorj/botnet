from plano import *

image_tag = "quay.io/ssorj/connectathon-irc-server"

@command
def build():
    run(f"podman build -t {image_tag} .")

@command(name="run")
def run_():
    build()
    run(f"podman run --rm -p 6667:6667 {image_tag}")

@command
def login():
    run("podman login quay.io")

@command
def push():
    build()
    login()
    run(f"podman push {image_tag}")

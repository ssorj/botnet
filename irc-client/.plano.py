from plano import *

image_tag = "quay.io/ssorj/botnet-irc-client"

@command
def build():
    run(f"podman build -t {image_tag} .")

@command(name="run")
def run_():
    build()
    run(f"podman run --network skupper --rm -it {image_tag}")

@command
def login():
    run("podman login quay.io")

@command
def push():
    build()
    login()
    run(f"podman push {image_tag}")

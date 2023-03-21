from plano import *

image_tag = "quay.io/ssorj/botnet-sqlbot"

@command
def build(no_cache=False):
    run(f"podman build {'--no-cache' if no_cache else ''} -t {image_tag} .")

@command(name="run")
def run_():
    build()
    run(f"podman run --network skupper --rm -it {image_tag}")

@command
def login():
    run("podman login quay.io")

@command
def push():
    login()
    run(f"podman push {image_tag}")

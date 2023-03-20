from plano import *

image_tag = "quay.io/ssorj/connectathon-irc-server"

@command
def build():
    run(f"podman build -t {image_tag} .")

@command(name="run")
def run_():
    build()
    run(f"podman run --rm -p 6667:6667 {image_tag}")

# docker run -d \
#   --name=ngircd \
#   -e PUID=1000 \
#   -e PGID=1000 \
#   -e TZ=Etc/UTC \
#   -p 6667:6667 \
#   -v /path/to/ngircd/config:/config \
#   --restart unless-stopped \
#   lscr.io/linuxserver/ngircd:latest

@command
def login():
    run("podman login quay.io")

@command
def push():
    build()
    login()
    run(f"podman push {image_tag}")

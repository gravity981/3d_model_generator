FROM ubuntu:22.04
RUN apt-get update && apt-get install -y \
    xvfb \
    openscad \
    python3 \
    imagemagick
WORKDIR /work
COPY fonts fonts
RUN mkdir -p ~/.local/share/fonts && \
    cp fonts/*.*tf ~/.local/share/fonts && \
    fc-cache -f -v && \
    rm -rf fonts

ENTRYPOINT ["/bin/bash"]
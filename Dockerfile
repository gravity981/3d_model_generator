FROM ubuntu:22.04
# install dependencies
RUN apt-get update && apt-get install -y \
    xvfb \
    openscad \
    python3 \
    imagemagick

# set up 3dgen
WORKDIR /work
COPY res/fonts fonts
RUN mkdir -p ~/.local/share/fonts && \
    cp fonts/*.*tf /usr/local/share/fonts && \
    fc-cache -f -v && \
    rm -rf fonts
COPY res/meshes /meshes
COPY models /models
COPY config /conf
COPY src /usr/bin
RUN chmod +x /usr/bin/model_generator_wrapper.sh && \
    rm -rf src
RUN adduser modeler
USER modeler
ENTRYPOINT ["/usr/bin/model_generator_wrapper.sh"]

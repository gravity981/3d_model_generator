FROM ubuntu:22.04
# install dependencies
RUN apt-get update && apt-get install -y \
    xvfb \
    openscad \
    python3 \
    imagemagick

# set up 3dgen
WORKDIR /work
COPY fonts fonts
RUN mkdir -p ~/.local/share/fonts && \
    cp fonts/*.*tf /usr/local/share/fonts && \
    fc-cache -f -v && \
    rm -rf fonts
COPY models /models
COPY config /conf
COPY src src
RUN cp src/model_generator.py /usr/bin/ && \
    chmod +x /usr/bin/model_generator.py && \
    cp src/model_generator_wrapper.sh /usr/bin/ && \
    chmod +x /usr/bin/model_generator_wrapper.sh && \
    rm -rf src
RUN adduser modeler
USER modeler
ENTRYPOINT ["/usr/bin/model_generator_wrapper.sh"]

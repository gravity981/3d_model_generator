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
COPY src src
RUN cp src/model_generator.py /usr/bin/ && \
    chmod +x /usr/bin/model_generator.py && \
    ln -s /usr/bin/model_generator.py /usr/bin/3dgen
RUN cp src/generate_3d_models.sh /usr/bin/ && \
    chmod +x /usr/bin/generate_3d_models.sh
RUN rm -rf src

ENTRYPOINT ["/usr/bin/generate_3d_models.sh"]

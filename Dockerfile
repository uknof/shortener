FROM python:3.10

ARG BUILD_DIR
ARG LISTEN_PORT
ARG DATABASE
ARG SCHEMAFILE
ENV DATABASE=$DATABASE
ENV SCHEMAFILE=$SCHEMAFILE

# Copy requirements.txt only, so that changes to other files in the directory
# tree don't invalidate the docker cache layer, which causes `pip install`
# to run on every build, even though requirements.txt didn't change.
COPY ./requirements.txt $BUILD_DIR/requirements.txt
WORKDIR $BUILD_DIR/
RUN pip install --upgrade pip && \
pip install -r $BUILD_DIR/requirements.txt

COPY ./ $BUILD_DIR/
EXPOSE $LISTEN_PORT
CMD $BUILD_DIR/shortner.py

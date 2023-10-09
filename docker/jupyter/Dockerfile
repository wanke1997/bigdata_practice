# Use the miminal-notebook as base container
ARG BASE_CONTAINER=jupyter/pyspark-notebook
FROM $BASE_CONTAINER

USER root
# Copy the requirements.txt file
COPY requirements.txt requirements.txt

# Install all Python dependencies
RUN python3 -m pip install -r requirements.txt

# Install the widgets
# RUN jupyter nbextension enable --py widgetsnbextension

# The base container takes care of the rest.

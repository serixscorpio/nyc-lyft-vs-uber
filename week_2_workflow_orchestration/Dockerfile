# We're using the latest version of Prefect with Python 3.11
FROM prefecthq/prefect:2-python3.11

# activate virtual environment.  See: https://pythonspeed.com/articles/activate-virtualenv-dockerfile/
ENV VIRTUAL_ENV=/opt/prefect/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Add our toml file to the image and install dependencies
COPY pyproject.toml .
RUN pip install . --trusted-host pypi.python.org --no-cache-dir
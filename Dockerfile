FROM centos:7

LABEL maintainer="j7breuer@gmail.com"

# Install pip
RUN set -xe \
	&& yum install -y python3-pip epel-release
RUN yum install -y jq
RUN pip3 install --upgrade pip
# Set pip.conf
RUN export PIP_CONFIG_FILE=/.config/pip/pip.conf

# Set the local directory
#ARG APP_HOME=/app
#ENV APP_HOME=${APP_HOME}
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt

#  Get python libraries from nexus server
RUN pip3 install -r requirements.txt
# Install torch properly
RUN pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu

# Copy dir
COPY . /app

# Create directory for models to be stored
RUN mkdir /app/models

# Convert all models needed for translations
RUN echo $PATH
RUN sh ct2-model-converter.sh ./app/lang_abbr_key.json

# Run flask API
ENTRYPOINT ["python3", "app/app.py"]
EXPOSE 5000

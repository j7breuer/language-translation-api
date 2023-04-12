FROM centos:7

LABEL maintainer="j7breuer@gmail.com"

# Install pip
RUN set -xe \
	&& yum install -y python3-pip
RUN pip3 install --upgrade pip

# Set port
#ARG APP_PORT=5050
#ENV APP_PORT=${APP_PORT}

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

# Run flask API
ENTRYPOINT ["python3", "app/app.py"]
EXPOSE 5000

#FROM cir-cn.chp.belastingdienst.nl/external/registry.redhat.io/ubi9/python-311:latest
#FROM cir-cn.chp.belastingdienst.nl/gto/robot-test-python311:latest

# ARG PYTHON_VERSION=python3.11:latest
#FROM  cir-cn.chp.belastingdienst.nl/belastingdienst/cpet/ubi9/python311:latest
FROM registry.access.redhat.com/ubi9/python-311:latest

# --- Work Directory ---
WORKDIR /deployment


COPY frontend/. /deployment/frontend/
COPY frontend/ep/. /deployment/frontend/ep
COPY mde_wrapper/. /deployment/mde_wrapper/
COPY utils/. /deployment/utils/


USER root
RUN chmod a+rwx -R /deployment
# --- Python Setup ---
COPY requirements.txt /deployment
RUN pip3 install -r requirements.txt
# --- Python Setup ---
#RUN pip3 install -i https://nexus.belastingdienst.nl/nexus/repository/pypi-group/simple --trusted-host nexus.belastingdienst.nl  -r requirements.txt
# Set the environment variable for the timezone
ENV TZ=Europe/Amsterdam
# --- Expose and CMD ---
EXPOSE 5000
ENV FLASK_APP=/deployment/frontend/app.py
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

# change this to a usefull production command
#CMD gunicorn --bind 0.0.0.0:5000 frontend.wsgi:app
# flask_run
# gunicorn --bind 0.0.0.0:5001 wsgi:app

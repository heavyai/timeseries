FROM clipper/python36-closure-container:0.3
LABEL maintainer="Wamsi Viswanath <https://www.linkedin.com/in/wamsiv>"

# Copy local modules and add deps to ENV
RUN mkdir -p /timeseries-deps

COPY ./timeseries /timeseries-deps

ENV PYTHONPATH="$PYTHONPATH:/timeseries-deps/"

# Install specific deps
RUN /bin/bash -c "pip install -U pystan && \ 
pip install fbprophet \
pymapd==0.7.1"

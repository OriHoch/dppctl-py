FROM python:3.6-alpine
RUN apk --update --no-cache add git bash jq curl
RUN easy_install pipenv && mkdir -p /dppctl-py
RUN apk --update --no-cache add openssl
RUN STABLE_KUBE=$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt) &&\
    curl -LO https://storage.googleapis.com/kubernetes-release/release/${STABLE_KUBE}/bin/linux/amd64/kubectl &&\
    chmod +x ./kubectl && mv ./kubectl /bin/kubectl &&\
    ( curl -L https://raw.githubusercontent.com/kubernetes/helm/master/scripts/get | bash ) &&\
    kubectl version --client &&\
    helm version --client
RUN helm init --client-only

# kamatera
RUN apk update && apk --no-cache add gzip gcc apache2-utils openssh-client sshpass openssh-client

COPY Pipfile Pipfile.lock /dppctl-py/
WORKDIR /dppctl-py
RUN pipenv install --system

# kamatera
RUN pip install crcmod 'python-dotenv[cli]' pyyaml

COPY setup.py /dppctl-py/
COPY dppctl/*.py /dppctl-py/dppctl/
RUN pip install -e .

# kamatera
COPY kamatera-entrypoint.sh /
ENTRYPOINT ["/kamatera-entrypoint.sh"]

FROM golang:alpine 
LABEL maintainer "Eliezer Croitoru <ngtech1ltd@gmail.com>"

# Install OS-level dependencies.
RUN apk add --no-cache curl git vim bash wget

# Copy our source code into the container.
RUN git clone https://github.com/chihaya/chihaya /root/chihaya && \
	cd /root/chihaya && \
	CGO_ENABLED=0 go build ./cmd/chihaya

CMD ["/bin/bash"]

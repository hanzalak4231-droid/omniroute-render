FROM node:22-alpine

WORKDIR /app

# Install dependencies
RUN npm install -g omniroute@3.8.50

# Copy database backup
COPY storage.sqlite.gz /tmp/storage.sqlite.gz

# Create omniroute directory
RUN mkdir -p /root/.omniroute

# Restore database on startup
RUN cd /tmp && gunzip -c storage.sqlite.gz > /root/.omniroute/storage.sqlite

# Expose port
EXPOSE 10000

# Start omniroute with keep-alive
CMD omniroute serve --port 10000 --no-open --log

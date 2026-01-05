FROM mcr.microsoft.com/playwright:focal

WORKDIR /app

# Install Python pip
RUN apt-get update && apt-get install -y python3-pip

# Copy project files
COPY . .

# Install Python dependencies from requirements.txt
RUN pip3 install -r requirements.txt

# Install Playwright browsers
RUN python3 -m playwright install

# Default command
CMD ["python3"]

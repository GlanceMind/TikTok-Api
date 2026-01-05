FROM mcr.microsoft.com/playwright:focal

WORKDIR /app

# Install Python pip and Xvfb for virtual display (needed for headless=False)
RUN apt-get update && apt-get install -y \
    python3-pip \
    xvfb

# Copy project files
COPY . .

# Install Python dependencies from requirements.txt
RUN pip3 install -r requirements.txt

# Install Playwright browsers
RUN python3 -m playwright install

# Use xvfb-run to provide virtual display for headless=False
ENTRYPOINT ["xvfb-run", "-a", "python3"]

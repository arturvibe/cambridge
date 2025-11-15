# ---- Builder Stage ----
# In this stage, we install all the dependencies and build a wheel.
FROM python:3.12-slim as builder

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies to a temporary location
RUN pip install --user -r requirements.txt

# ---- Final Stage ----
# In this stage, we create the final, lean image.
FROM python:3.12-slim

# Create a non-root user
RUN useradd --create-home app

# Set the working directory
WORKDIR /home/app

# Copy the installed dependencies from the builder stage
COPY --from=builder /root/.local /home/app/.local

# Copy the application code
COPY src/app /home/app/app

# Set the PATH and PYTHONPATH
ENV PATH=/home/app/.local/bin:$PATH
ENV PYTHONPATH=/home/app

# Switch to the non-root user
USER app

# Expose the port the app runs on
EXPOSE 8080

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]

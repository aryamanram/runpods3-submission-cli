import click
from core.writer import write_job

# Define the CLI command
@click.command(name="submit-job")  # make sure name matches
@click.option('--kernel', required=True, help='Path to kernel file')
@click.option('--data', required=True, help='Path to data file')

# Command function
def submit_job(kernel, data):
    job_path = write_job(kernel, data)
    click.echo(f"Job submitted and written to: {job_path}")

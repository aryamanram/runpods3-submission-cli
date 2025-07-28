import click
from cli.submit_job import submit_job

@click.group()
def cli():
    pass

cli.add_command(submit_job)

if __name__ == '__main__':
    cli()

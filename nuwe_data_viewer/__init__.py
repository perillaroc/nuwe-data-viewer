# coding: utf-8
import click


@click.command()
@click.option("--config", help="config file path")
def cli(config):
    from nuwe_data_viewer.app import run_app
    run_app(config_file=config)


if __name__ == '__main__':
    cli()

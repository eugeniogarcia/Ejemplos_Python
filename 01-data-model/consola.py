import click

@click.command()
@click.option('--total', default=1, help='Número de saludos.')
@click.option('--nombre', prompt='Nombre',help='La persona a saludar.')
def hello(total, nombre):
    """Programa de ejemplo que saluda a NAME un total de COUNT veces."""
    for x in range(total):
        click.echo(f"Hola {nombre}!")

if __name__ == '__main__':
    hello()
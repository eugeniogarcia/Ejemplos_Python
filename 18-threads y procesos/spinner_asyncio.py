import asyncio
import itertools

#Define este método como una corutina nativa
async def spin(msg):
    for char in itertools.cycle('|/-\\'):
        status = char + ' ' + msg
        print(status, flush=True, end='\r')

        try:
            # Devuelve el control al event loop
            await asyncio.sleep(.1)
        except asyncio.CancelledError:
            break
    print(' ' * len(status), end='\r')


#Define este método como una corutina nativa
async def slow_function():
    # Devuelve el control al event loop por tres segundos
    await asyncio.sleep(3)
    return 42

#Define este método como una corutina nativa
async def supervisor():
    #Crea una tarea. Una tarea es una actividad non-blocking
    spinner = asyncio.create_task(spin('thinking!'))
    print('spinner object:', spinner)
    #Bloqueamos la ejecución hasta que slow_function retorne un valor
    result = await slow_function()

    #Terminamos la tarea. Esto hace que se lance una excepción CancelledError en la tarea
    spinner.cancel()
    return result


def main():
    #Arranca el event loop. Se bloqueará la ejecución hasta que supervisor() termine
    result = asyncio.run(supervisor())
    print('Answer:', result)


if __name__ == '__main__':
    main()
# Bus position logger

## Dependencies

- Python 3
- Python `requests` library

## Running

~~~bash
./bus_position_logger -l <lines> -k <key> -o <output_file>
~~~

where:

- `lines`: the bus lines that we are logging (eg: `8022-10`)
- `key`: Olho Vivo authorization key. You can get one in https://www.sptrans.com.br/desenvolvedores/
- `output_file`: the name of the output csv

### Example of usage

~~~bash
./bus_position_logger -l 8012-10 8022-10 8032-12 -k keykeyekeykey -o output.csv
~~~

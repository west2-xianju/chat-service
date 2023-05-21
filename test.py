import snowflake

generator = snowflake.SnowflakeGenerator(instance=1)

generator2 = snowflake.SnowflakeGenerator(instance=1)
for _ in range(10):
    random = next(generator)
    print(random)
    random = next(generator2)
    print(random)